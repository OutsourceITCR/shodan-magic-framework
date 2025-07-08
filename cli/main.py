#!/usr/local/bin/python3

import argparse
import sys
from commands.testing.greet import init as init_greet_command
from commands.modules import init as init_modules_command
from commands.database import init as init_database_command


def main():
    parser = argparse.ArgumentParser(description="Welcome to MagiCli.")
    subparsers = parser.add_subparsers(dest="command")

    init_greet_command(subparsers)
    init_modules_command(subparsers)
    init_database_command(subparsers)

    # Parse arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Execute the appropriate command
    args.func(args)


if __name__ == "__main__":
    main()
