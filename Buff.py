class Buff():
  def __init__(self, cfg):
    self.name = cfg["name"]
    self.effect = cfg["effect"]
    self.recast = cfg["recast"]
    self.weave_cost = cfg["weave_cost"]
    self.type = "Buff"