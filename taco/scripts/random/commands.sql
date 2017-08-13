CREATE TABLE users
(
  ID int NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  phone_number varchar(80) NOT NULL,
  token varchar(255),
  joined DATETIME,
  apns_token varchar(255),
  send_notifications tinyint(1) default 1,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID)
);

CREATE TABLE groups
(
  ID int NOT NULL AUTO_INCREMENT,
  admin_id integer(11),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID)
);
alter table groups add group_name varchar(255);

CREATE TABLE group_users
(
  ID int NOT NULL AUTO_INCREMENT,
  group_id integer(11),
  user_id integer(11),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID)
);

CREATE TABLE memories
(
  ID int NOT NULL AUTO_INCREMENT,
  user_id integer(11),
  url_icon varchar(255) NOT NULL,
  url_diary varchar(255) NOT NULL,
  url_fullscreen varchar(255) NOT NULL,
  width integer(11),
  height integer(11),
  url_original varchar(255) NOT NULL,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID)
);
alter table memories add group_id integer(11);
alter table memories add memory_type varchar(80);
alter table memories add url_small varchar(255);

CREATE TABLE comments
(
  ID int NOT NULL AUTO_INCREMENT,
  user_id integer(11),
  memory_id integer(11),
  message blob,
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

alter table users change fb_id fb_token varchar(255);
alter table users add fb_id varchar(255);
alter table users add gender varchar(80);

CREATE TABLE recipes
(
  ID int NOT NULL AUTO_INCREMENT,
  component_id integer(11),
  name varchar(255),
  yummly_recipe_id varchar(255),
  yield_amount varchar(127),
  number_of_servings varchar(127),
  img_url varchar(127),
  prep_time_seconds integer(11),
  ingredient_lines_json blob,
  calories integer(11),
  recipe_source_url varchar(255),
  directions_list blob,
  yummly_query varchar(127),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (yummly_recipe_id),
  PRIMARY KEY (ID)
);

CREATE TABLE recipe_unlocks
(
  ID int NOT NULL AUTO_INCREMENT,
  user_id integer(11),
  recipe_id integer(11),
  unlock_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (user_id, recipe_id),
  PRIMARY KEY (ID)
);

CREATE TABLE user_missions
(
  ID int NOT NULL AUTO_INCREMENT,
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  user_id integer(11),
  is_over tinyint(1) default 0,
  mission_id integer(11),
  booty integer(11),
  timeouts_reached integer(11) default 0,
  UNIQUE (user_id, mission_id),
  PRIMARY KEY (ID)
);
alter table users add apns_token varchar(255);
alter table users add send_notifications tinyint(1) default 1;

CREATE TABLE blocked_users
(
  ID int NOT NULL AUTO_INCREMENT,
  blocking_user_id integer(11),
  blocked_user_id integer(11),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (blocking_user_id, blocked_user_id),
  PRIMARY KEY (ID)
);

alter table food_items add component_id integer(11);

CREATE TABLE request_logs
(
ID int NOT NULL AUTO_INCREMENT,
user_id int(11),
url varchar(511) NOT NULL,
ip varchar(255),
env varchar(255),
request_time DATETIME DEFAULT CURRENT_TIMESTAMP,
ms_taken float,
PRIMARY KEY (ID)
);