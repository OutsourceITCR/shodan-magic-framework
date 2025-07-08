import os
import sys
import shutil
from config import CLI_DIR
from utils.files import replace_word_in_file

SOURCE_FOLDER = os.path.join(CLI_DIR, "_data/templates/module")


def init(subparsers):
    parser_modules = subparsers.add_parser("modules", help="Manage modules")
    parser_modules.add_argument("action", help="Action to execute")
    parser_modules.add_argument("name", help="Name of the module")
    parser_modules.set_defaults(func=lambda args: handler(args.action, args.name))


def handler(action, name):
    if action == "create":
        create(name)


def create(name):
    if not os.path.isdir(SOURCE_FOLDER):
        print(f"Error: Source folder '{SOURCE_FOLDER}' not found.")
        sys.exit(1)

    destination = os.path.abspath(name)

    if os.path.isdir(destination):
        print(f"The module already exists in '{destination}'.")
        sys.exit(1)

    os.makedirs(destination, exist_ok=False)

    try:
        for item in os.listdir(SOURCE_FOLDER):
            src_path = os.path.join(SOURCE_FOLDER, item)
            dest_path = os.path.join(destination, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dest_path)

        print(f"Contents of '{SOURCE_FOLDER}' copied to '{destination}'.")
    except Exception as e:
        print(f"Error copying files: {e}")
        sys.exit(1)

    replace_word_in_file(os.path.join(destination, "alembic/env.py"), "module_name", name)
    replace_word_in_file(os.path.join(destination, "main.py"), "module_name", name)
    print("Module was configured")
    print("Remember to create the schema on script/docker/db/create_schemas.sql, you will need to restart the container")
    print("Remember to add the module to your migrations on maintenance/migrations.py if necessary")
