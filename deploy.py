import argparse
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

def write_to_file(str, file_name):
  text_file = open(file_name, "w")
  text_file.write(str)
  text_file.close()

# Arg options
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prod', help='deploy in production!', action='store_true')
parsed_args = parser.parse_args()

# Check directory is clean
cmd = 'git status --porcelain'
number_of_uncommitted_files = len(run(cmd, True, True).split('\n')) - 1

if number_of_uncommitted_files != 0:
  print 'You have %d uncommitted files. Please commit and try again.' % number_of_uncommitted_files
  sys.exit()

if parsed_args.prod:
  o = None
  while o != 'y' or o != 'n':
    red = '\033[91m'
    bold = '\033[1m'
    message = 'Warning: You are deploying in production. Are you REALLY sure? (y/n)\n'
    end = '\033[0m'
    o = raw_input(red + bold + message + end)
    if o == 'n':
      print 'Saved ya from disaster! Try deploying in devel.'
      sys.exit()
    elif o == 'y':
      break
    else:
      print 'Didn\'t quite get that. Try typing \'y\' or \'n\''

if parsed_args.prod:
  run('heroku config:set ENV=prod --app fruitfam-prod')
  run('heroku config:set APP_CONFIG_FILE=../config/prod.py --app fruitfam-prod')
  run('git push prod master')
  run('heroku ps:scale celery=0 --app fruitfam-prod')
  run('heroku ps:scale celery=1 --app fruitfam-prod')
else:
  run('heroku config:set ENV=devel --app fruitfam-devel')
  run('heroku config:set APP_CONFIG_FILE=../config/devel.py --app fruitfam-devel')
  run('git push -f devel HEAD:master')
  run('heroku ps:scale celery=0 --app fruitfam-devel')
  run('heroku ps:scale celery=1 --app fruitfam-devel')