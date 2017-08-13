DEBUG = True

### MYSQL CONFIGS
endpoint = 'fruitfam.ctzo20w7hrck.us-east-1.rds.amazonaws.com'
db_port = '3306'
db_username = 'a_creator'
db_passwd = 'timetojumpthehoopstoday'
db_devel_dbname = 'tacodevel'
kMysqlDevelUrl = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username, db_passwd, endpoint, db_port, db_devel_dbname)

SQLALCHEMY_DATABASE_URI = kMysqlDevelUrl
CELERY_BROKER_URL = "redis://h:p2a8198acce063239e9ad645c1a7c90d71ff62d0cb9e202e531931b19dfc7854d@ec2-34-198-189-86.compute-1.amazonaws.com:7159"