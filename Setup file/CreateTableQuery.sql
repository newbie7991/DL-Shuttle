CREATE TABLE IF NOT EXISTS accounts (  
	user_id int(11) NOT NULL AUTO_INCREMENT,  
	username varchar(100) NOT NULL,      
	password varchar(100) NOT NULL,     
	email varchar(100) NOT NULL,     
	skill varchar(100) NULL,     
	gender varchar(100) NULL,     
	PRIMARY KEY (user_id)  
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS training_records (  
	training_id int(11) NOT NULL AUTO_INCREMENT,  
	user_id int(11) NOT NULL,      
	training_date date NOT NULL,     
	technique varchar(100) NOT NULL,     
	correct_pose int(50) NULL,     
	training_count int(50) NULL,     
	incorrect_pose int(50) NULL,     
	PRIMARY KEY (training_id),     
	FOREIGN KEY (user_id) REFERENCES accounts(user_id) 
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;	
