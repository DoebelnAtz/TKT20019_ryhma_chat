#! /bin/bash
# This script will set up the testing environment.

# Set up the virtual environment
python -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Initialize the environment
./init_env.sh

# Set environment variables for the database connection
DB_NAME=deep_thought
DB_USER=marvin
DB_PORT=6543
DB_PASSWORD=42
DB_HOST=localhost
DB_URI="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
# Start the PostgreSQL database if not started
if ! [ "$(docker-compose ps -q db)" ]; then
  echo "Starting PostgreSQL database..."
  docker-compose up -d
fi

# Wait for the database to be ready
while ! [ "$(pg_isready -d $DB_NAME -h $DB_HOST -p $DB_PORT -U $DB_USER)" = "$DB_HOST:$DB_PORT - accepting connections" ]; do
  echo "$(pg_isready -d $DB_NAME -h $DB_HOST -p $DB_PORT -U $DB_USER)"
  echo "Not ready yet, waiting for the database to be ready..."
  sleep 3
done
echo "Database is ready"


# Reset and initialize the database if schema isn't initalized
if ! [ "$(psql $DB_URI -c 'SELECT COUNT(*) FROM pg_tables WHERE tablename = 'users';')" = "1" ]; then
  echo "Initializing database..."
  ./reset_db.sh
fi
echo "Database is initialized"

# Start flask
flask run

# Open the application in the default web browser
open http://127.0.0.1:5000

