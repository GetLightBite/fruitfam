class Rule(object):
  """
  The rules of all single player missions are defined with the Rule object.
  All missions have a target booty. if the user reaches that booty, the mission
  is accomplished.
  """
  def __init__(self, user_mission):
    self.user_mission = user_mission
  
  def mission_name(self):
    """
    String of the mission name
    """
    pass
  
  def rules_text(self):
    """
    Returns a list of rules. Each clause is a different item in the list
    """
    pass
  
  def mission_id(self):
    """ Each mission gets an ID """
    pass
  
  def on_food_log(self):
    """
    Increments booty, sends notifications, any other work
    """
    pass
  
  def target_booty(self):
    """
    Mission is over when user hits the target
    """
    pass
  
  def mission_type(self):
    """
    Pokedex vs normal vs timed.
    """
    pass
  
  def booty_call(self):
    """
    Defines daily booty call for a user
    """
    pass