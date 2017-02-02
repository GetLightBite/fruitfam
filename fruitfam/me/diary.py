from fruitfam.models.food_item import FoodItem
from sqlalchemy import and_, or_, distinct, desc, not_, func
from sqlalchemy.orm import defer, joinedload, joinedload_all, sessionmaker, subqueryload, load_only, Load

def get_diary(user, requesting_user):
  food_items = FoodItem.query.options(
    load_only('id'),
    load_only('img_url_diary'),
    load_only('img_url_recognition'),
  ).filter_by(
    user_id=user.id
  ).order_by(
    desc(FoodItem.created)
  ).all()
  diary = []
  for food in food_items:
    diary_data = {
      'foodItemId': food.id,
      'thumbnailUrl': food.diary_img()
    }
    diary.append(diary_data)
  return diary