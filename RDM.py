import GCD
import Ability
import Buff
import random

class RedMage():
  def __init__(self):
    self.reset()
    self.init_GCDs()
    self.init_abilities()
    self.init_buffs()

  def GCD(self, name):
    for skill in self.GCDs:
      if skill.name == name:
        return skill
    return -1

  def Ability(self, name):
    for skill in self.abilities:
      if skill.name == name:
        return skill
    return -1

  def Buff(self, name):
    for skill in self.buffs:
      if skill.name == name:
        return skill
    return -1

  # Cast any skill
  def cast(self, skill):
    if skill.type == "GCD":
      if self.dualcast or skill.cast_time == 0:
        self.weave_windows = skill.weave_windows
      else:
        self.weave_windows = 0
      self.potency += skill.potency
      skill.effect(self)
      self.dualcast = not self.dualcast
    elif skill.type == "Ability":
      self.weave_windows -= skill.weave_cost
      self.potency += skill.potency
    else: # Buff
      self.weave_windows -= skill.weave_cost
      skill.effect(self)
    if self.weave_windows < 0:
      raise NameError("Clipping detected.\n")

  def next_GCD(self):
    if self.combo_location == 4:
      return "Scorch"
    elif self.combo_location == 3:
      if self.white_mana < self.black_mana:
        if not self.verstone_ready or self.verfire_ready:
          # If verfire is ready, no matter what we'll want to cast verholy
          return "Verholy"
        elif self.black_mana + 21 <= self.white_mana + 30:
          # If we want to snipe verfire ready and we won't overcap by casting verflare
          return "Verflare"
        else:
          # We have no choice but to lose a proc
          return "Verholy"
      elif self.black_mana < self.white_mana:
        if not self.verfire_ready or self.verstone_ready:
          # If verstone is ready, no matter what we'll want to cast verflare
          return "Verflare"
        elif self.white_mana + 21 <= self.black_mana + 30:
          # If we want to snipe verstone ready and we won't overcap by casting verholy
          return "Verholy"
        else: 
          # We have no choice but to lose a proc
          return "Verflare"
      else:
        # Both mana are the same
        if self.verfire_ready:
          return "Verholy"
        else:
         return "Verflare"
    elif self.combo_location == 2:
      return "Enchanted Redoublement"
    elif self.combo_location == 1:
      return "Enchanted Zwerchhau"
    else:
      # We are not in a combo currently
      if self.dualcast:
        # We need to dualcast either veraero or verthunder. Similar logic to verholy vs verflare
        if self.white_mana < self.black_mana:
          if not self.verstone_ready or self.verfire_ready:
            # Simple case. Need white mana, no proc to lose or both procs active.
            return "Veraero"
          elif self.black_mana + 11 <= self.white_mana + 30:
            # In order to not lose a proc chance, we cast the opposite unless we overcap
            return "Verthunder"
          else:
            return "Veraero"
        elif self.black_mana < self.white_mana:
          if not self.verfire_ready or self.verstone_ready:
            # Simple case. Need black mana, no proc to lose or both procs active.
            return "Verthunder"
          elif self.white_mana + 11 <= self.black_mana + 30:
            # In order to not lose a proc chance, we cast the opposite unless we overcap
            return "Veraero"
          else: 
            return "Verthunder"
        else: 
          # Both mana are the same
          if self.verfire_ready:
            return "Veraero"
          else:
            return "Verthunder"
      else:
        # We do not have a dualcast proc
        if self.white_mana >= 80 and self.black_mana >= 80:
          # TODO Ignore fixing procs for now
          if not self.verfire_ready and not self.verstone_ready:
            return "Enchanted Riposte"
          else:
            return "Enchanted Riposte"
        else:
          # We are not ready for our melee combo yet
          if self.verfire_ready and self.verstone_ready:
            # Easy case, both procs are ready. Cast the lower mana
            if self.white_mana < self.black_mana:
              return "Verstone"
            else:
              return "Verfire"
          elif self.verfire_ready:
            # Only verfire is ready. Cast verfire unless you'll overcap
            if self.black_mana + 9 <= self.white_mana + 30:
              return "Verfire"
            else:
              return "Jolt"
          elif self.verstone_ready:
            # Only verstone is ready. Cast verstone unless you'll overcap
            if self.white_mana + 9 <= self.black_mana + 30:
              return "Verstone"
            else: 
              return "Jolt"
          else:
            # Neither proc is ready. Cast jolt.
            return "Jolt"

  def reset(self):
    self.dualcast = False
    self.verfire_ready = False
    self.verstone_ready = False
    self.acceleration = 0
    self.buffs = []
    self.white_mana = 0
    self.black_mana = 0
    self.combo_location = 0
    self.GCD_timer = 0
    self.weave_windows = 99
    self.potency = 0

  def init_GCDs(self):
    self.GCDs = []

    # Jolt
    def _effect_jolt(RDM):
      RDM.white_mana += 3
      RDM.black_mana += 3
    self.GCDs.append(
      GCD.GCD({
      "name" : "Jolt",
      "potency" : 290,
      "cast_time" : 200,
        "weave_windows" : 2,
      "mp_cost" : 200,
      "ready" : True,
      "effect" : _effect_jolt
      })
    )

    # Verthunder
    def _effect_verthunder(RDM):
      RDM.black_mana += 11
      if RDM.acceleration > 0:
        RDM.verfire_ready = True
        RDM.acceleration -= 1
      elif random.random() < 0.5:
        RDM.verfire_ready = True
    self.GCDs.append(
      GCD.GCD({
        "name" : "Verthunder", 
        "potency" : 370,
        "cast_time" : 500,
        "weave_windows" : 2,
        "mp_cost" : 300,
        "ready" : True,
        "effect" : _effect_verthunder
        })
      )

    # Veraero
    def _effect_veraero(RDM):
      RDM.white_mana += 11
      if RDM.acceleration > 0:
        RDM.verstone_ready = True
        RDM.acceleration -= 1
      elif random.random() < 0.5:
        RDM.verstone_ready = True
    self.GCDs.append(
      GCD.GCD({
        "name" : "Veraero", 
        "potency" : 370,
        "cast_time" : 500,
        "weave_windows" : 2,
        "mp_cost" : 300,
        "ready" : True,
        "effect" : _effect_veraero
        })
      )

    # Verfire
    def _effect_verfire(RDM):
      if RDM.verfire_ready:
        RDM.black_mana += 9
        RDM.verfire_ready = False
      else:
        raise NameError('Verfire casted when not ready.\n')
    self.GCDs.append(
      GCD.GCD({
        "name" : "Verfire",
        "potency": 310,
        "cast_time" : 200,
        "weave_windows" : 2,
        "mp_cost" : 200,
        "ready" : False,
        "effect" : _effect_verfire
        })
      )

    # Verstone
    def _effect_verstone(RDM):
      if RDM.verstone_ready:
        RDM.white_mana += 9
        RDM.verstone_ready = False
      else:
        raise NameError('Verstone casted when not ready.\n')
    self.GCDs.append(
      GCD.GCD({
        "name" : "Verstone",
        "potency": 310,
        "cast_time" : 200,
        "weave_windows" : 2,
        "mp_cost" : 200,
        "ready" : False,
        "effect" : _effect_verstone
        })
      )

    # Riposte
    def _effect_riposte(RDM):
      RDM.white_mana -= 30
      RDM.black_mana -= 30
      RDM.combo_location = 1
    self.GCDs.append(
      GCD.GCD({
        "name" : "Enchanted Riposte",
        "potency" : 220,
        "cast_time" : 0,
        "weave_windows" : 1,
        "mp_cost" : 0,
        "ready" : False,
        "effect" : _effect_riposte
        })
    )

    # Zwerchhau
    def _effect_zwerchhau(RDM):
      RDM.white_mana -= 25
      RDM.black_mana -= 25
      RDM.combo_location = 2
    self.GCDs.append(
      GCD.GCD({
        "name" : "Enchanted Zwerchhau",
        "potency" : 290,
        "cast_time" : 0,
        "weave_windows" : 1,
        "mp_cost" : 0,
        "ready" : False,
        "effect" : _effect_zwerchhau
        })
    )

    # Redoublement
    def _effect_redoublement(RDM):
      RDM.white_mana -= 25
      RDM.black_mana -= 25
      RDM.combo_location = 3
    self.GCDs.append(
      GCD.GCD({
        "name" : "Enchanted Redoublement",
        "potency" : 470,
        "cast_time" : 0,
        "weave_windows" : 2,
        "mp_cost" : 0,
        "ready" : False,
        "effect" : _effect_redoublement
        })
    )

    # Verholy
    def _effect_verholy(RDM):
      if RDM.white_mana < RDM.black_mana:
        RDM.verstone_ready = True
      else:
        if random.random() < 0.2:
          RDM.verstone_ready = True
      RDM.white_mana += 21
      RDM.combo_location = 4
    self.GCDs.append(
      GCD.GCD({
        "name" : "Verholy",
        "potency" : 600,
        "cast_time" : 0,
        "weave_windows" : 2,
        "mp_cost" : 400,
        "ready" : False,
        "effect" : _effect_verholy
        })
      )

    # Verflare
    def _effect_verflare(RDM):
      if RDM.black_mana < RDM.white_mana:
        RDM.verfire_ready = True
      else:
        if random.random() < 0.2:
          RDM.verfire_ready = True
      RDM.black_mana += 21
      RDM.combo_location = 4
    self.GCDs.append(
      GCD.GCD({
        "name" : "Verflare",
        "potency" : 600,
        "cast_time" : 0,
        "weave_windows" : 2,
        "mp_cost" : 400,
        "ready" : False,
        "effect" : _effect_verflare
        })
      )

    # Scorch
    def _effect_scorch(RDM):
      RDM.white_mana += 7
      RDM.black_mana += 7
      RDM.combo_location = 0
    self.GCDs.append(
      GCD.GCD({
        "name" : "Scorch",
        "potency" : 700,
        "cast_time" : 0,
        "weave_windows" : 2,
        "mp_cost" : 400,
        "ready" : False,
        "effect" : _effect_scorch
        })
      )

  def init_abilities(self):
    self.abilities = []

    # Fleche
    self.abilities.append(
      Ability.Ability({
        "name" : "Fleche",
        "potency" : 440,
        "recast" : 25,
        "weave_cost" : 1,
        })
      )

    # Contre Sixte
    self.abilities.append(
      Ability.Ability({
        "name" : "Contre Sixte",
        "potency" : 400,
        "recast" : 35,
        "weave_cost" : 1,
        })
      )

    # Corps-a-corps
    self.abilities.append(
      Ability.Ability({
        "name" : "Corps-a-corps",
        "potency" : 130,
        "recast" : 40,
        "weave_cost" : 1,
        })
      )

    # Engagement
    self.abilities.append(
      Ability.Ability({
        "name" : "Engagement",
        "potency" : 150,
        "recast" : 35,
        "weave_cost" : 1,
        })
      )

    # Displacement
    self.abilities.append(
      Ability.Ability({
        "name" : "Displacement",
        "potency" : 200,
        "recast" : 35,
        "weave_cost" : 2,
        })
      )

  # TODO
  def init_buffs(self):
    self.buffs = []

    def _effect_manafication(RDM):
      RDM.white_mana *= 2
      RDM.black_mana *= 2
    self.buffs.append(
      Buff.Buff({
        "name" : "Manafication",
        "effect" : _effect_manafication,
        "recast" : 110,
        "weave_cost" : 1,
        })
      )

    def _effect_acceleration(RDM):
      RDM.acceleration = 3
    self.buffs.append(
      Buff.Buff({
        "name" : "Acceleration",
        "effect" : _effect_acceleration,
        "recast" : 55,
        "weave_cost" : 1,
      })
    )

def test():
  ZP = RedMage()
  print(ZP.white_mana)
  print(ZP.black_mana)
  ZP.GCDs[0].effect(ZP)
  print(ZP.white_mana)
  print(ZP.black_mana)
