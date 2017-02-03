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

CREATE TABLE food_items
(
  ID int NOT NULL AUTO_INCREMENT,
  clarifai_tags blob,
  client_timestamp int(11),
  num_likes integer(11) DEFAULT 0,
  not_food tinyint(1) DEFAULT 0,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  img_url_tiny varchar(255),
  img_url_small varchar(255),
  img_url_large varchar(255),
  img_url_fullscreen varchar(255),
  img_url_recognition varchar(255),
  user_id integer(11),
  PRIMARY KEY (ID)
);

alter table users add last_log DATETIME;
alter table users add max_streak int(11);

alter table components add vitamins varchar(255);
alter table components add cals varchar(255);
alter table components add benefits varchar(255);
alter table components add glycemic_load integer(11);

alter table users add booty int(11) default 0;
alter table users add level int(11) default 1;

alter table food_items change img_url_fullscreen img_url_original varchar(255);
alter table food_items change img_url_large img_url_fullscreen varchar(255);
alter table food_items change img_url_small img_url_diary varchar(255);
alter table food_items change img_url_tiny img_url_icon varchar(255);

CREATE TABLE likes
(
  ID int NOT NULL AUTO_INCREMENT,
  user_id integer(11),
  food_item_id integer(11),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (user_id, food_item_id),
  PRIMARY KEY (ID)
);

CREATE TABLE comments
(
  ID int NOT NULL AUTO_INCREMENT,
  user_id integer(11),
  food_item_id integer(11),
  message blob,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID)
);