DEBUG = False

### MYSQL CONFIGS
endpoint = 'fruitfam.ctzo20w7hrck.us-east-1.rds.amazonaws.com'
db_port = '3306'
db_username = 'a_creator'
db_passwd = 'timetojumpthehoopstoday'
db_prod_dbname = 'proddb'
kMysqlProdUrl = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username, db_passwd, endpoint, db_port, db_prod_dbname)

SQLALCHEMY_DATABASE_URI = kMysqlProdUrl