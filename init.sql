CREATE DATABASE sheduler_db;
CREATE USER sheduler_user WITH PASSWORD 'sheduler_password';
GRANT ALL PRIVILEGES ON DATABASE sheduler_db to sheduler_user;