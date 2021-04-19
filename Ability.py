class Ability():
  def __init__(self, cfg):
    self.name = cfg["name"]
    self.potency = cfg["potency"]
    self.recast = cfg["recast"]
    self.weave_cost = cfg["weave_cost"]
    self.type = "Ability"