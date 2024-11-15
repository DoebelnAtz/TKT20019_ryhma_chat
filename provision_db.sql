DO $do$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'marvin') THEN
          CREATE ROLE marvin;
        END IF;
        ALTER ROLE marvin WITH LOGIN PASSWORD '42' NOSUPERUSER CREATEDB NOCREATEROLE;
    END
$do$;

DROP DATABASE IF EXISTS deep_thought;
CREATE DATABASE deep_thought OWNER marvin;
GRANT ALL ON DATABASE deep_thought TO marvin;
