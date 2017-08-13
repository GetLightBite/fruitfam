from fruitfam import celery, db
from fruitfam.models.food_item import FoodItem
from fruitfam.models.user import User
from fruitfam.tasks.utils import FruitFamTask
from fruitfam.utils.common import send_notification
from fruitfam.utils.emoji import Emoji

@celery.task(base=FruitFamTask)
def like_notification(user_id, food_item_id):
  user = db.session.query(User).filter_by(id=user_id).one()
  food_item = FoodItem.query.filter_by(id=food_item_id).one()
  if food_item.user_id != user.id or user_id == 1:
    message = "%s liked one of your photos! Take another, and get more love %s" % (user.real_name(), Emoji.love().decode('utf-8'))
    message = message.encode('utf-8')
    title = "You got a like!"
    send_notification(message, food_item.user_id, badge_increment=0, params={}, title=title)
