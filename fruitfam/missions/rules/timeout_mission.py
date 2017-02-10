from fruitfam.missions.rules.rule import Rule

class TimeoutMission(Rule):
  """
  A timeout mission gives you points based on a countdown. If the timer reaches
  0, the countdown expires and the number of timeouts reached increments. The
  timer is completely maintained by the client.
  """
  def __init__(self, user_mission):
    super(TimeoutMission, self).__init__(user_mission)
  
  def timeout(self):
    """
    Returns seconds to timeout
    """
    pass
  
  def on_timeout_popup(self):
    """ String to show the user when the timer runs out """
    pass
  
  def increment_timeouts_reached(self):
    """
    Increments the timeouts reached count
    """
    self.get_user_mission().increment_timeouts_reached()
  
  def get_timeouts_reached(self):
    """
    Returns the number of timeouts the user has reached
    """
    return self.get_user_mission().get_timeouts_reached()
  
  def mission_type(self):
    return 'timeout'
  
  def get_mission_json(self):
    # Get normal json
    normal = super(TimeoutMission, self).get_mission_json()
    timeout_mission = {
      'timerSeconds': self.timeout(),
      'onExpiry' : self.on_timeout_popup()
    }
    normal['missionDetails'] = timeout_mission
    return normal
  
  def get_animation_json(self, food_item):
    """
    Tells the client to stop showing the countdown timer if the mission has
    been completed
    """
    current_json = super(TimeoutMission, self).get_animation_json(food_item)
    current_booty = self.get_booty()
    target_booty = self.target_booty()
    booty_earned = self.booty_earned(food_item)
    if current_booty + booty_earned >= target_booty:
      current_json['cameraAnimation'] = {
        'hideTimer':1
      }
    return current_json
  
  def get_levelup_animation_json(self, food_item, old_json):
    """
    Tells the client to stop showing the countdown timer
    """
    current_json = super(TimeoutMission, self).get_levelup_animation_json(food_item, old_json)
    current_json['cameraAnimation'] = {
      'hideTimer':1
    }
    return current_json