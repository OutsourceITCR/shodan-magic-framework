def init(subparsers):
    parser_greet = subparsers.add_parser("greet", help="Print a greeting message")
    parser_greet.add_argument("name", help="Name to greet")
    parser_greet.add_argument("--uppercase", "-u", action="store_true", help="Print the greeting in uppercase")
    parser_greet.set_defaults(func=lambda args: greet(args.name, args.uppercase))


def greet(name, uppercase=False):
    message = f"Hello, {name}!"
    if uppercase:
        message = message.upper()
    print(message)
