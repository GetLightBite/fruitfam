DEBUG = True

### MYSQL CONFIGS
endpoint = 'fruitfam.ctzo20w7hrck.us-east-1.rds.amazonaws.com'
db_port = '3306'
db_username = 'a_creator'
db_passwd = 'timetojumpthehoopstoday'
db_prod_dbname = 'proddb'
kMysqlProdUrl = 'mysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(db_username, db_passwd, endpoint, db_port, db_prod_dbname)

SQLALCHEMY_DATABASE_URI = kMysqlProdUrl
CELERY_BROKER_URL="redis://h:p43009ea5cf1ea7efa4356c301933d47ba0b88daae7a86598161db61be5273279@ec2-34-199-14-64.compute-1.amazonaws.com:8109"