from fruitfam.missions.rules.rule import Rule

class Level1(Rule):
  """Log a fruit in two minutes!"""
  def __init__(self, user_challenge):
    super(Level1, self).__init__()
    self.user_challenge = user_challenge
  
  def mission_name(self):
    return 'Mission 1'