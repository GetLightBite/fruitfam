from fruitfam import celery, db
from fruitfam.models.food_item import FoodItem
from fruitfam.models.user import User
from fruitfam.models.user_mission import UserMission
from fruitfam.tasks.utils import FruitFamTask
from fruitfam.utils.common import send_notification, get_user_friends
from fruitfam.utils.emoji import Emoji
from sqlalchemy import func

@celery.task(base=FruitFamTask)
def simple_pokedex_reminder(user_id):
  user = db.session.query(User).filter_by(id=user_id).one()
  if user.level == 2:
    user_mission = UserMission.query.filter(
      UserMission.user_id == user_id
    ).filter(
      UserMission.is_over == False
    ).one()
    rules = user_mission.get_rules()
    
    images_with_id, num_matches, num_items = rules.get_progress()
    
    if num_matches < 3:
      message = '%d down, %d to go! Finish this challenge to learn how to lower blood pressure and improve skin quality! %s' % (num_matches, num_items - num_matches, Emoji.muscle())
      
      # Find any friend
      friends = get_user_friends(user)
      if len(friends) > 0:
        for friend in friends:
          gender = 'him' if friend.gender == 'male' else 'her'
          pass_reach = 'pass' if friend.level <= 2 else 'reach'
          message = '%s is at level %d. Log now to %s %s! %s' % (friend.real_name(), friend.level, pass_reach, gender, Emoji.trophy().decode('utf-8'))
          message = message.encode('utf-8')
          break
      
      # Find a friend also at level 2!
      if len(friends) > 0:
        for friend in friends:
          if friend.level == 2:
            gender = 'him' if friend.gender == 'male' else 'her'
            pass_reach = 'pass' if friend.level <= 2 else 'reach'
            message = '%s is at also at level %d! Log now to %s %s! %s' % (friend.real_name(), friend.level, pass_reach, gender, Emoji.trophy().decode('utf-8'))
            message = message.encode('utf-8')
            break
      
      title = 'Eat fruit now, prevent binge eating later ' + Emoji.wink()
      send_notification(message, user_id, badge_increment=0, params={}, title=title)