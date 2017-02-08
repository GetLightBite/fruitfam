class Rule(object):
  """
  The rules of all single player missions are defined with the Rule object.
  All missions have a target booty. If the user reaches that booty, the mission
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
  
  def on_food_log(self, food_item):
    """
    Increments booty, sends notifications, any other work. Calls
    self.on_mission_end() if the target booty is reached.
    """
    pass
  
  def on_mission_end(self, food_item):
    """
    Increments users level, ends current mission, creates new one.
    """
    return self.get_user_mission().end_mission()
  
  def booty_earned(self, food_item):
    """
    How much booty does this food_item earn?
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
  
  #####################################
  # Helper methods for defining rules #
  #####################################
  
  def log_food(self, food_item):
    # First get the pre-log json
    current_mission_json = self.get_mission_json()
    booty_prize_json = self.booty_prize_json(food_item)
    animation_json = self.get_animation_json(food_item)
    response_json = {
      'bootyPrize' : booty_prize_json,
      'currentMission' : current_mission_json,
      'animation' : animation_json
    }
    # Call the food log callback
    self.on_food_log(food_item)
    # Get new mission json if player levelled up
    if self.get_booty() >= self.target_booty():
      new_mission = self.on_mission_end(food_item)
      new_rules = new_mission.get_rules()
      new_mission_json = new_rules.get_mission_json()
      levelup_animation_json = new_mission.get_levelup_animation_json(food_item, animation_json)
      response_json['newMission'] = new_mission_json
      response_json['animation'] = levelup_animation_json
    return response_json
  
  def get_user_mission(self):
    return self.user_mission
  
  def increment_booty(self, booty):
    self.get_user_mission().increment_booty(booty)
  
  def get_booty(self):
    cur_booty = self.get_user_mission().get_booty()
    if cur_booty > self.target_booty():
      return self.target_booty()
    return cur_booty
  
  def mission_description(self):
    return ' '.join(self.rules_text())
  
  def get_mission_json(self):
    return {
      'missionTitle' : self.mission_name(),
      'missionDescription' : self.mission_description(),
      'currentBooty' : self.get_booty(),
      'targetBooty': self.target_booty(),
    }
  
  def booty_prize_json(self, food_item):
    booty_earned = self.booty_earned(food_item)
    return {
      'breakdown': [
        {
          'title': self.mission_name(),
          'booty': booty_earned
        },
      ],
      'total': booty_earned
    }
  
  def get_animation_json(self, food_item):
    """What is the animation that logging this food item should have?"""
    current_booty = self.get_booty()
    target_booty = self.target_booty()
    booty_earned = self.booty_earned(food_item)
    return {
      'leveledUp': 0,
      'startBootyNumerator': current_booty,
      'endBootyNumerator': booty_earned,
      'bootyDenominator': target_booty,
      'missionDescription': self.mission_description()
    }
  
  def get_levelup_animation_json(self, food_item, old_animation_json):
    """What is the animation that logging this food item should have?"""
    old_booty = old_animation_json['current_booty']
    old_target_booty = old_animation_json['bootyDenominator']
    old_mission_description = old_animation_json['missionDescription']
    
    target_booty = self.target_booty()
    user_level = self.get_user_mission().user.level
    return {
      'leveledUp' : 1,
      'startBootyNumerator' : old_booty,
      'startBootyDenominator' : old_target_booty,
      'endBootyNumerator': 0,
      'endBootyDenominator': target_booty,
      'startMissionDescription': old_mission_description,
      'endMissionDescription': self.mission_description(),
      'startPlayerLevel' : user_level-1,
      'endPlayerLevel' : user_level,
    }