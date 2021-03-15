-- Set up MySQL database server

CREATE DATABASE IF NOT EXISTS tempo_db;
CREATE USER IF NOT EXISTS 'tempo_dev'@'localhost' IDENTIFIED BY 'Tempo_pwd_2001';
GRANT ALL PRIVILEGES ON `tempo_db`.* TO 'tempo_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'tempo_dev'@'localhost';
FLUSH PRIVILEGES;
