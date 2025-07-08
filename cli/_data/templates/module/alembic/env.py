import os
import re
from sqlalchemy import engine_from_config, pool
from alembic import context

# Regex to extract timestamp from migration filenames (YYYYMMDDHHMMSS)
TIMESTAMP_REGEX = re.compile(r"(\d{14})")


def get_sorted_migrations(reverse=False):
    """Retrieve migration files and sort them by filename timestamp.

    - reverse=False -> Ascending order (for upgrades)
    - reverse=True  -> Descending order (for downgrades)
    """
    versions_dir = os.path.join(os.path.dirname(__file__), "versions")

    if not os.path.exists(versions_dir):
        return []

    migrations = [
        f for f in os.listdir(versions_dir)
        if f.endswith(".py") and TIMESTAMP_REGEX.search(f)
    ]

    # Sort migrations based on extracted timestamp
    migrations.sort(key=lambda f: TIMESTAMP_REGEX.search(f).group(), reverse=reverse)

    return migrations


def get_database_url():
    """Retrieve the database URL, handling the 'ENV' placeholder correctly."""
    url = context.config.get_main_option("sqlalchemy.url")

    if url == "ENV":
        url = f"{os.environ['DATABASE_URI']}?options=-c%20search_path%3Dmodule_name"

    return url


def run_migrations_offline():
    """Generate raw SQL migration scripts in timestamp order."""
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=None,  # Set your metadata if using autogenerate
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        if context.get_x_argument(as_dictionary=True).get("downgrade"):
            sorted_migrations = get_sorted_migrations(reverse=True)  # Reverse for downgrades
        else:
            sorted_migrations = get_sorted_migrations(reverse=False)  # Normal order for upgrades

        for migration in sorted_migrations:
            migration_path = os.path.join("versions", migration)
            context.run_migrations(script_location=migration_path)


def run_migrations_online():
    """Apply migrations in timestamp order using a database connection."""
    url = get_database_url()

    config_section = context.config.get_section(context.config.config_ini_section, {})
    config_section["sqlalchemy.url"] = url

    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=None,  # Set your metadata if using autogenerate
            version_table="alembic_version",
            include_schemas=True,
            transactional_ddl=True,
            render_as_batch=True,  # Important for SQLite compatibility
        )

        with context.begin_transaction():
            if context.get_x_argument(as_dictionary=True).get("downgrade"):
                sorted_migrations = get_sorted_migrations(reverse=True)  # Reverse for downgrades
            else:
                sorted_migrations = get_sorted_migrations(reverse=False)  # Normal order for upgrades

            for migration in sorted_migrations:
                migration_path = os.path.join("versions", migration)
                context.run_migrations(script_location=migration_path)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
