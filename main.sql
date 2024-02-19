-- Créer la base de données
CREATE DATABASE IF NOT EXISTS store;

-- Utiliser la base de données
USE store;

-- Créer la table category
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Créer la table product
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT,
    quantity INT,
    id_category INT,
    FOREIGN KEY (id_category) REFERENCES category(id)
);
