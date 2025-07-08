import os
import importlib.util
import sys


from config import services
root_path = os.path.join(os.getcwd())
if root_path not in sys.path:
    sys.path.insert(0, root_path)


def execute_seed(script_path):
    module_name = os.path.splitext(os.path.basename(script_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "ENVIRONMENTS") or not module.ENVIRONMENTS:
        print(f"{module_name}: Does not have ENVIRONMENTS set up")

    if hasattr(module, "seed"):
        module.seed()


for service in services:
    seeds_path = os.path.join(os.getcwd(), service + "/seeds")
    if os.path.exists(seeds_path):
        print(f"Running seed for {service}")
        for file in os.listdir(seeds_path):
            if file.endswith(".py"):
                file_path = os.path.join(seeds_path, file)
                execute_seed(file_path)
