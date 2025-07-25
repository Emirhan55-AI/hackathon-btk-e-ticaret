-- Initialize Aura Database
-- This script is run automatically when the postgres container starts

-- Create UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types and enums (will be added as needed)

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE aura_db TO aura_user;

-- Create schema for application
CREATE SCHEMA IF NOT EXISTS aura;
GRANT ALL ON SCHEMA aura TO aura_user;
