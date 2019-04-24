create database myflaskapp;

use myflaskapp;

create table users(
	id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45),
    email VARCHAR(45),
    username VARCHAR(45),
    password VARCHAR(45),
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from users;

SELECT User FROM mysql.user;
drop user 'oliverxu'@'localhost';
CREATE USER 'oliverxu'@'localhost';
grant all privileges
on myflaskapp.*
to 'oliverxu'@'localhost';
show grants for 'oliverxu'@'localhost';