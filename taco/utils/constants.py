kSecretKey = 'booty call time'

# MySql
endpoint = 'fruitfam.ctzo20w7hrck.us-east-1.rds.amazonaws.com'
db_port = '3306'
db_username = 'a_creator'
db_passwd = 'timetojumpthehoopstoday'
db_prod_dbname = 'proddb'
db_devel_dbname = 'develdb'
kMysqlProdUrl = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username, db_passwd, endpoint, db_port, db_prod_dbname)
kMysqlDevelUrl = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username, db_passwd, endpoint, db_port, db_devel_dbname)

# Redis
kRedisDevelUrl = 'redis://h:p3ad39467fd791b69ab19cbae2f12f5ba46b0e8f82da4f40d67d746fc55247e30@ec2-107-21-109-207.compute-1.amazonaws.com:11709'
kRedisProdUrl = 'redis://h:p3c39e8cee22930ea016469a3de4a7ccd0f7a6bfd454475c055b19e15f181f6d1@ec2-107-22-239-248.compute-1.amazonaws.com:10269'
