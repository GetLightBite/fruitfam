import argparse
import os
import subprocess
import sys


def run(command, suppress_command_details=False, suppress_output=False, dry_run=False, shell=False):
  if dry_run:
    print '\033[92mRunning: \'%s\'\033[0m' % command
  else:
    if not suppress_command_details:
      print '\033[92mRunning: \'%s\'\033[0m' % command
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=shell)
    output = process.communicate()[0]
    # output = ''
    if not suppress_output:
      # for line in process.stdout:
      #   sys.stdout.write(line)
      #   output += line
      #   output += '\n'
      print output
    return output

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--prod', help='run with prod db!', action='store_true')
  parsed_args = parser.parse_args()
  # if parsed_args.prod:
  #   print 'Env is PROD'
  #   os.environ["ENV"] = "PROD"
  #   os.environ["APP_CONFIG_FILE"] = "../config/prod.py"
  # else:
  #   print 'Env is DEVEL'
  #   os.environ["ENV"] = "DEVEL"
  #   os.environ["APP_CONFIG_FILE"] = "../config/devel.py"
  run('celery -f -A fruitfam.tasks purge')
  run('celery -A fruitfam.tasks worker --loglevel=DEBUG -P gevent')