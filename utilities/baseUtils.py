import os
import importlib
import inspect
from utilities.logger import log
from nextcord.ext import commands

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

                try:
                    module = importlib.import_module(module_name)
                    found_cogs = False

                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Ensure it's a Cog, but not the base Cog class itself, and it's defined in the module
                        if issubclass(obj, commands.Cog) and obj is not commands.Cog and obj.__module__ == module_name:
                            found_cogs = True
                            cog_class = obj
                            class_name = name

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
                            log.info(f"Loaded: {class_name} from {module_name}")

                    if not found_cogs:
                        log.warning(f"No Cog classes found in {module_name}.")

                except Exception as e:
                    log.error(f"Failed to load {module_name}: {e}")