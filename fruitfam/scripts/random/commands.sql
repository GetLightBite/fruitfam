CREATE TABLE users
(
  ID int NOT NULL AUTO_INCREMENT,
  firstname varchar(255) NOT NULL,
  lastname varchar(255) NOT NULL,
  email varchar(255),
  token varchar(255),
  joined DATETIME,
  profile_photo varchar(255),
  utc_offset integer(11),
  streak integer(11) NOT NULL,
  fb_id varchar(255),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID)
);

CREATE TABLE components
(
  ID int NOT NULL AUTO_INCREMENT,
  name varchar(255),
  category_id int(11),
  health_info varchar(255),
  message varchar(255),
  PRIMARY KEY (ID)
);