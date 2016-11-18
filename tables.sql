CREATE PROCEDURE `create_database_tables`()
BEGIN
	
	DROP TABLE IF EXISTS users;
	CREATE TABLE users (
		id INT NOT NULL AUTO_INCREMENT,
		name VARCHAR(100) NOT NULL,
		password VARCHAR(100) NOT NULL,
		PRIMARY KEY (id)
	);

	DROP TABLE IF EXISTS comments;
	CREATE TABLE comments (
		id INT NOT NULL AUTO_INCREMENT,
		comment VARCHAR(100) NOT NULL,
		user VARCHAR(100) NOT NULL,
		time VARCHAR(100) NOT NULL,
		PRIMARY KEY (id)
	);

END