#! /bin/bash
PORT=6543
PASSWORD=42
HOST=localhost
DB_NAME=deep_thought
DB_USER=marvin

# Clear database
echo "Dropping database..."

psql "postgresql://${DB_USER}:${PASSWORD}@${HOST}:${PORT}/${DB_NAME}" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Create database
echo "Creating database"
psql "postgresql://${DB_USER}:${PASSWORD}@${HOST}:${PORT}/${DB_NAME}" -f schema.sql