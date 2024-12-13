#!/bin/bash

# Script to install and configure PostgreSQL on Debian
# Configures PostgreSQL to listen on port 6543
# and sets up a user and database for the Flask app

# Exit immediately if a command exits with a non-zero status
set -e

# Variables (Please update these with your desired values)
PG_PORT=6543                  # PostgreSQL port to listen on

echo "Updating package lists..."
sudo apt update

echo "Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

# Modify postgresql.conf to change the listening port
PG_CONF="/etc/postgresql/$(ls /etc/postgresql)/main/postgresql.conf"
sudo sed -i "s/^#port = .*/port = $PG_PORT/" "$PG_CONF"

# Ensure PostgreSQL is listening on localhost
sudo sed -i "s/^#listen_addresses = .*/listen_addresses = 'localhost'/" "$PG_CONF"

# Configure PostgreSQL to accept local connections with password authentication
PG_HBA="/etc/postgresql/$(ls /etc/postgresql)/main/pg_hba.conf"
sudo sed -i "s/^local\s\+all\s\+all\s\+peer/local   all             all                                     md5/" "$PG_HBA"

echo "Restarting PostgreSQL service..."
sudo systemctl restart postgresql

while ! sudo -u postgres psql -c "SELECT 1" > /dev/null 2>&1; do
    echo "Waiting for PostgreSQL to start..."
    sleep 5
done

echo "Creating PostgreSQL user and database..."
# Switch to the postgres user to create user and database
sudo -u postgres psql -c "DO \$do\$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN CREATE ROLE $DB_USER; END IF; ALTER ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASSWORD' NOSUPERUSER CREATEDB NOCREATEROLE; END \$do\$;"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER"
sudo -u postgres psql -c "GRANT ALL ON DATABASE $DB_NAME TO $DB_USER;"

psql "postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${PG_PORT}/${DB_NAME}" -f schema.sql
echo "PostgreSQL installation and configuration complete."

echo "Connection details:"
echo "Host: localhost"
echo "Port: $PG_PORT"
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Password: $DB_PASSWORD"

