CREATE DATABASE lost_and_found_db;
USE lost_and_found_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role ENUM('user','admin')
);

CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    category VARCHAR(50),
    description TEXT,
    location VARCHAR(100),
    item_date DATE,
    status ENUM('Lost','Found','Returned'),
    posted_by INT,
    FOREIGN KEY (posted_by) REFERENCES users(user_id)
);
SHOW TABLES;


INSERT INTO users VALUES
(NULL, 'Test User', 'test@gmail.com', 'test123', 'user');
SELECT * FROM items;
SELECT * FROM users;



