from datetime import datetime
from flask import g, jsonify, request, send_from_directory
from taco import app, auth, db
# from taco.models.request_log import RequestLog
from taco.models.comment import Comment
from taco.models.user import User
from taco.models.group import Group
from taco.models.group_user import GroupUser
from taco.models.memory import Memory
from taco.media.upload_media import upload_image_memory_from_request, upload_video_memory_from_request
from taco.utils.common import is_prod, send_report_exception_email, serialize_image, send_email, create_branch_link
from taco.utils.emoji import Emoji
from taco.utils.upload_image import upload_image_from_bytes
import os
from sqlalchemy import desc, and_, not_
from sqlalchemy.orm import joinedload, load_only, Load
import sys
import traceback
import urllib, cStringIO, ast

@auth.verify_password
def verify_password(token, password):
  # first try to authenticate by token
  user = User.verify_auth_token(token)
  g.user = user
  if not user:
    return False
  return True

@app.route('/')
@auth.login_required
def index():
  test_endpoint.delay(4)
  return 'Hello World!'

@app.route('/email_log', methods=['GET', 'POST'])
def log_email():
  print 'here1'
  args1 = dict(request.args) if request.args != None else {}
  args2 = dict(request.json) if request.json != None else {}
  args3 = dict(request.form) if request.form != None else {}
  print 'here2'
  args = args1
  args.update(args2)
  args.update(args3)
  print 'here3'
  print args
  email = args['email']
  c = Comment(99, 99, str(email))
  db.session.add(c)
  db.session.commit()
  print c
  send_email('founders@strivesdk.com', 'New interest in taco', email+' is interested in  Aviato SDK')
  return 'Email logged'

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'bin'),
    'peach.ico', mimetype='image/vnd.microsoft.icon')

# Measure request times
@app.before_request
def before_request():
  g.last_request_start = datetime.utcnow()

@app.after_request
def log_request_stats(r):
  ms_taken = (datetime.utcnow() - g.last_request_start).total_seconds() * 1000
  url = request.url_rule
  if url == None:
    url = 'unknown'
  try:
    user = g.user
  except AttributeError, e:
    user = None
  ip = request.remote_addr
  env = os.environ.get('ENV', 'DEVEL')
  user_id = user.id if user != None else None
  #log_request.delay(url, user_id, ip, env, ms_taken)
  r.cache_control.max_age = 1209600
  return r

# Handle exceptions in prod
if False:#is_prod():
  @app.errorhandler(Exception)
  def all_exception_handler(error):
    print 'Reporting an exception!'
    args1 = dict(request.args) if request.args != None else {}
    args2 = dict(request.json) if request.json != None else {}
    args3 = dict(request.form) if request.form != None else {}
    args = args1
    args.update(args2)
    args.update(args3)
    etype, value, tb = sys.exc_info()
    traceback_lst = traceback.format_exception(etype, value, tb)
    traceback_str = '<br />'.join(map(lambda x: x.strip(), traceback_lst))
    error_message = error.message
    url = request.url_rule
    exception_str = '<div style="font-family: Courier New"><h3>%s</h3><p>%s</p></div>' % (error_message, traceback_str)
    send_report_exception_email(exception_str, g, url, args=args)
    raise error

##############
# Core Views #
##############


@app.route('/check/phone_number', methods=['POST'])
def check_phone_number():
  data = request.json
  phone_number = data["phoneNumber"] # "+1 325 523 2532"

  user = User.query.filter_by(phone_number=phone_number).first()
  token = ''
  available_group_user = GroupUser.query.filter_by(user_id=user.id).first()
  group_id = None
  if available_group_user != None:
    group_id = available_group_user.group_id
  if user != None:
    token = user.token

  return jsonify(
    hasAccount = user != None,
    token = token,
    groupId = group_id
  )

@app.route('/create/account', methods=['POST'])
def login():
  username = request.json['username']
  phone_number = request.json['phoneNumber']
  user, token = User.create_user(username, phone_number)
  if token == None:
    return "Invalid username or phone number!"
  return jsonify(
    userId=user.id,
    token=token
  )

@app.route('/add/phone_contacts', methods=['POST'])
@auth.login_required
def add_phone_contacts():
  data = request.json
  contacts = data["contacts"]
  country_code = data["countryCode"]

  return jsonify(
    chill = "ok"
  )

@app.route('/upload/photo', methods=['POST'])
@auth.login_required
def upload_photo():
  # using a hack to send an array object via form -> cast/uncast from string
  recipients_list_raw = request.form.get("recipients", "[]") # "(32,25,1)"
  recipients_list = ast.literal_eval(recipients_list_raw)
  
  groups = Group.query.filter(Group.id.in_(recipients_list)).all()
  # other_users = User.query.filter(User.id.in_(others)).all()
  # image_data = request.files.get('docfile', None)
  
  memory = upload_image_memory_from_request(request, g.user, groups)
  db.session.commit()
  
  return jsonify(
    awesome = "ok"
  )

@app.route('/upload/movie', methods=['POST'])
@auth.login_required
def upload_movie():
  recipients_list_raw = request.form.get("recipients", "[]") # "(32,25,1)"
  recipients_list = ast.literal_eval(recipients_list_raw)

  groups = Group.query.filter(Group.id.in_(recipients_list)).all()

  # grab movie here
  upload_video_memory_from_request(request, g.user, groups)
  db.session.commit()

  return jsonify(
    awesome = "ok"
  )

@app.route('/create/comment', methods=['POST'])
@auth.login_required
def create_comment():
  data = request.json
  memory_id = data["memoryId"]
  message = data["message"]
  
  c = Comment(g.user.id, memory_id, message)
  db.session.add(c)
  db.session.commit()
  
  return jsonify(
    awesome = "ok"
  )

@app.route('/create/group', methods=['POST'])
@auth.login_required
def create_group():
  name = request.json['groupName']
  # create group
  group = Group(name, g.user)
  db.session.add(group)
  db.session.commit()
  contacts = {
    'name' : g.user.get_username(),
    'uid' : g.user.id,
    'is_taco_user': 1
  }
  invite_url = group.get_invite_link()
  return jsonify(
    groupName = name, # lol i know
    groupId = group.id,
    inviteMessage = "Join my Taco Group, link self-destructs in 24 hours: %s" % invite_url,
    contacts = [contacts]
  )

@app.route('/join/group', methods=['POST'])
@auth.login_required
def join_group():
  invite_id = request.json['inviteId']
  print invite_id
  
  group = Group.query.filter_by(id=invite_id).one()
  
  new_group_user = GroupUser(group, g.user)
  db.session.add(new_group_user)
  db.session.commit()
  
  return '', 200

@app.route('/update/group', methods=['POST'])
@auth.login_required
def update_group():
  data = request.json
  group_id = data["groupId"]
  members = data["members"]
  
  group = Group.query.filter(
    Group.id == int(group_id)
  ).options(
    joinedload(Group.group_users)
  ).first()
  
  if group == None:
    return 'No such group'
  
  if g.user.id != group.admin_id:
    return 'Unauthorized action'
  
  # Delete members not in new group
  all_group_users = []
  for group_user in group.group_users:
    all_group_users.append(group_user.id)
    if group_user.user_id not in members:
      db.session.delete(group_user)
  
  # Add new members in the group
  for member_id in members:
    if member_id not in all_group_users:
      member = User.query.filter_by(id=member_id).first()
      if member != None:
        new_group_user = GroupUser(group, member)
        db.session.add(new_group_user)
  
  db.session.commit()

  return jsonify(
    awesome = "ok"
  )

@app.route('/load/groups_list', methods=['GET'])
@auth.login_required
def load_groups_list():
  group_users = GroupUser.query.filter(
    GroupUser.user_id == g.user.id
  ).options(
    joinedload(GroupUser.group)
  ).all()
  groups = [
    {
      'name' : group_user.group.group_name,
      'uid' : group_user.group.id,
      'badged' : 0
    } for group_user in group_users
  ]
  return jsonify(
    groups=groups
  )

@app.route('/load/group_members', methods=['GET'])
@auth.login_required
def load_group_members():
  group_id = int(request.args['groupId'])
  
  group = Group.query.filter(
    Group.id == int(group_id)
  ).options(
    joinedload(
      Group.group_users
    ).joinedload(
      GroupUser.user
    )
  ).first()
  
  if group == None:
    return 'No such group'
  
  members = [
    {
      'name' : groupuser.user.get_username()
    } for groupuser in group
  ]
  
  return jsonify(
    members = members
  )

@app.route('/load/memories', methods=['GET'])
@auth.login_required
def load_memories():
  group_id = int(request.args['groupId'])
  
  memories = Memory.query.filter(
    Memory.group_id == group_id
  ).options(
    joinedload(Memory.user)
  ).limit(150)
  
  group = Group.query.filter_by(id=group_id).first()
  
  if group == None:
    return 'No such group'
  
  memories_json = []
  for memory in memories:
    if memory.memory_type == 'photo':
      memory_json = { # this definition is image specific, not sure about videos yet
        'uid' : memory.id, 
        'thumbnailUrl' : memory.url_icon,
        'fullscreenUrl' : memory.url_fullscreen,
        'smallUrl': memory.url_small, # small, original proportions
        'width': memory.width,
        'height': memory.height,
        'authorName': memory.user.get_username()
      }
      memories_json.append(memory_json)
    else:
      memory_json = { # this is for videos
        'uid' : memory.id, 
        'thumbnailUrl' : memory.url_icon,
        'videoUrl': memory.url_fullscreen, # original image
        'width': memory.width,
        'height': memory.height,
        'authorName': memory.user.get_username()
      }
      memories_json.append(memory_json)
  
  return jsonify(
    memories = memories_json,
    groupName = group.group_name
  )


@app.route('/load/comments', methods=['GET'])
@auth.login_required
def load_comments():
  memory_id = int(request.args['memoryId'])
  
  all_comments = Comment.query.filter(
    Comment.memory_id==memory_id
  ).options(
    joinedload(Comment.user)
  ).all()
  epoch = datetime.utcfromtimestamp(0)
  
  comments = []
  for comment in all_comments:
    comment = {
      'commentId': comment.id,
      'senderId' : comment.user_id,
      'senderName' : comment.user.get_username(),
      'epochTime' : (comment.created - epoch).total_seconds() * 1000,
      'ownComment': int(comment.user_id == g.user.id),
      'message': comment.get_message()
    }
    comments.append(comment)
  
  return jsonify(
    comments = comments
  )

@app.route("/upload/apns_token", methods=['POST'])
@auth.login_required
def upload_apns_token():
  apns_token = request.json['token']
  g.user.apns_token = apns_token
  db.session.add(g.user)
  db.session.commit()
  return '', 204
