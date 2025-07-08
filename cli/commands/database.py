import os

from sqlalchemy import create_engine, text


def init(subparsers):
    parser_database = subparsers.add_parser("database", help="Database commands")
    parser_database.add_argument("action", help="Database action")
    parser_database.add_argument("schema", help="Database schema to execute the action")
    parser_database.set_defaults(func=lambda args: handler(args.action, args.schema))


def handler(action, schema):
    if action == "reset":
        reset(schema)


def reset(schema):
    try:
        engine = create_engine(os.environ['DATABASE_URI'])

        with engine.begin() as connection:
            connection.execute(text(f"DROP SCHEMA {schema} CASCADE"))
            connection.execute(text(f"CREATE SCHEMA {schema}"))

        print(f"Schema {schema} reset successfully")

    except Exception as e:
        print(f"Error: {e}")
