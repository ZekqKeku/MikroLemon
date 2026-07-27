import os
import importlib
import inspect
from utilities.logger import log

class Loader:
    def __init__(self, payload: dict[str, any], folder="cogs"):

        self.payload = payload
        self.client = payload.get("client")
        self.folder = folder

        if not os.path.exists(self.folder):
            log.warning(f"Folder {self.folder} not found.")
            return

        for filename in os.listdir(self.folder):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"{self.folder}.{filename[:-3]}"
                class_name = "N/A"

                base_name = filename[:-3]
                pascal_case_name = "".join(word.capitalize() for word in base_name.split("_"))
                cog_class_name = f"{pascal_case_name}Cog"
                standard_class_name = pascal_case_name

                try:
                    module = importlib.import_module(module_name)

                    if hasattr(module, cog_class_name):
                        class_name = cog_class_name
                        cog_class = getattr(module, cog_class_name)
                    elif hasattr(module, standard_class_name):
                        class_name = standard_class_name
                        cog_class = getattr(module, standard_class_name)
                    else:
                        log.error(f"Failed to load: {module_name}: Class not found.")
                        continue

                    sig = inspect.signature(cog_class.__init__)
                    params = list(sig.parameters)[1:]

                    args = []
                    for p in params:
                        if p in self.payload:
                            args.append(self.payload[p])
                        else:
                            log.warning(f"Parameter '{p}' not found in payload for {class_name}")

                    cog_instance = cog_class(*args)
                    self.client.add_cog(cog_instance)
                    log.info(f"Loaded: {class_name}")

                except Exception as e:
                    log.error(f"Failed to load {module_name} ({class_name}): {e}")