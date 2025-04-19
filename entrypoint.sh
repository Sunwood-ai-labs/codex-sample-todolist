#!/usr/bin/env sh
# Auto-initialize the database if not present
set -e
# If the database file does not exist in /app, initialize it
if [ ! -f "/app/tasks.db" ]; then
  echo "Initializing database..."
  flask init-db
fi
# Execute the provided command (e.g., flask run)
exec "$@"