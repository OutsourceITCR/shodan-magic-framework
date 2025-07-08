#!/bin/bash
set -e

# Let PostgreSQL start as usual
echo "Starting PostgreSQL..."
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to become ready
until pg_isready -h localhost -U "$POSTGRES_USER"; do
    echo "Waiting for database to be ready..."
    sleep 1
done

# Run custom initialization logic
echo "Running initialization scripts..."
for script in /docker-entrypoint-initdb.d/*; do
    case "$script" in
        *.sh)
            echo "Executing $script"
            bash "$script"
            ;;
        *.sql)
            echo "Executing $script"
            psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$script"
            ;;
        *)
            echo "Skipping $script"
            ;;
    esac
done

echo "Initialization complete."

# Wait for PostgreSQL process to finish
wait