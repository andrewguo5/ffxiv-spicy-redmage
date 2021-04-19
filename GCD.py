class GCD():
  def __init__(self, cfg):
    self.name = cfg["name"]
    self.potency = cfg["potency"]
    self.mp_cost = cfg["mp_cost"]
    self.cast_time = cfg["cast_time"]
    self.weave_windows = cfg["weave_windows"]
    # If True, there are no limitations to casting. Otherwise False
    self.ready = cfg["ready"]
    self.effect = cfg["effect"]
    self.type = "GCD"