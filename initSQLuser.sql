CREATE USER 'mysql'@'localhost' IDENTIFIED BY 'romanelli';
GRANT ALL PRIVILEGES ON * . * TO 'mysql'@'localhost';
FLUSH PRIVILEGES;