SECRET_KEY = 'booty call time'

### MYSQL CONFIGS
endpoint = 'fruitfam.ctzo20w7hrck.us-east-1.rds.amazonaws.com'
db_port = '3306'
db_username = 'a_creator'
db_passwd = 'timetojumpthehoopstoday'
db_devel_dbname = 'develdb'
kMysqlDevelUrl = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username, db_passwd, endpoint, db_port, db_devel_dbname)

SQLALCHEMY_DATABASE_URI = kMysqlDevelUrl