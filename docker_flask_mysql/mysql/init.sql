-- Create the 'shop' database
CREATE DATABASE IF NOT EXISTS shop
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Use the 'shop' database
USE shop;

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE
);


INSERT INTO users (name, email) VALUES
('test01', 'test01@example.com'),
('test02', 'test02@example.com');