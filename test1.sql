CREATE DATABASE lost_and_found_db;
USE lost_and_found_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role ENUM('user','admin')
);

CREATE TABLE IF NOT EXISTS lost_items (
    lost_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    category VARCHAR(50),
    description TEXT,
    location VARCHAR(100),
    lost_date DATE,
    user_id INT,
    status ENUM('Open','Matched','Returned') DEFAULT 'Open',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
SHOW TABLES;
CREATE TABLE found_items (
    found_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    category VARCHAR(50),
    description TEXT,
    location VARCHAR(100),
    found_date DATE,
    reported_by INT,
    matched_lost_id INT NULL,
    FOREIGN KEY (reported_by) REFERENCES users(user_id),
    FOREIGN KEY (matched_lost_id) REFERENCES lost_items(lost_id)
);


INSERT INTO users VALUES
(NULL, 'Test User', 'test@gmail.com', 'test123', 'user');
SELECT * FROM lost_items;
select * from found_items;
SELECT * FROM users;

INSERT INTO users (name, email, password, role)
VALUES ('Admin', 'admin@college.com', 'admin123', 'admin');



