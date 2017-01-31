# set env variables
import argparse
import os

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--prod', help='deploy in production!', action='store_true')
  parsed_args = parser.parse_args()
  if parsed_args.prod:
    print 'Env is PROD'
    os.environ["ENV"] = "PROD"
    os.environ["APP_CONFIG_FILE"] = "../config/prod.py"
  else:
    print 'Env is DEVEL'
    os.environ["ENV"] = "DEVEL"
    os.environ["APP_CONFIG_FILE"] = "../config/devel.py"

from fruitfam import app
app.run(host='0.0.0.0', port=5000, use_reloader=False)