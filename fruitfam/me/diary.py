from fruitfam.models.food_item import FoodItem


def get_diary(user, requesting_user):
  food_items = FoodItem.query.options(
    load_only('id'),
    load_only('img_url_large'),
    load_only('img_url_recognition'),
  ).filter_by(
    user_id=user.id
  ).all()
  diary = []
  for food in food_items:
    diary_data = {
      'foodItemId': food.id,
      'thumbnailUrl': food.img_url_small()
    }