import os


def get_config():
    return {
        "DATABASE_URI": os.getenv("DATABASE_URI", ""),
        "DEBUG": os.getenv("DEBUG", "False") == "True",
    }
