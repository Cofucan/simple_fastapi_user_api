-- Create the database and tables
CREATE USER IF NOT EXISTS 'uche'@'localhost' IDENTIFIED BY 'hngpassword';
GRANT ALL PRIVILEGES ON *.* TO 'uche'@localhost;
DROP DATABASE IF EXISTS hngdb_stage_two;
CREATE DATABASE IF NOT EXISTS hngdb_stage_two;
USE hngdb_stage_two;
CREATE TABLE IF NOT EXISTS tracks (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    PRIMARY KEY (id)
);
INSERT INTO tracks (name) VALUES ("Backend"), ("Fullstack"), ("Frontend"), ("Mobile"), ("Design"), ("DevOps"), ("Video Editing");

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    track_id INT,
    gender VARCHAR(1),
    email VARCHAR(256),
    username VARCHAR(256),
    FOREIGN KEY(track_id) REFERENCES tracks(id),
    stage INT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id)
);
INSERT INTO users (name, gender, email, username, track_id, stage) VALUES ("John Doe", "M", "johndoe@me.com", "johndoe", 1, 0);
