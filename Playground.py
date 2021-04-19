import RDM as RDM

standard_opener = [
  "Acceleration",
  "Verthunder",
  "Veraero",
  "Verstone",
  "Veraero",
  "Verfire",
  "Verthunder",
  "Verstone",
  "Verthunder",
  "Manafication",
  "Enchanted Riposte",
  "Enchanted Zwerchhau",
  "Enchanted Redoublement",
  "Verholy",
  "Scorch",
]

ZP = RDM.RedMage()
for name in standard_opener:
  skill = ZP.GCD(name)
  if (skill == -1):
    print(name)
    skill = ZP.Buff(name)
    ZP.cast(skill)
  else:
    print(name)
    ZP.cast(skill)
  print("\tMana:", ZP.white_mana, "/", ZP.black_mana)
  print("\tProcs:", ZP.verstone_ready, "/", ZP.verfire_ready)
  print("\tWeaves:", ZP.weave_windows, "/ Dualcast:", ZP.dualcast)

for i in range(20):
  name = ZP.next_GCD()
  print(name)
  skill = ZP.GCD(name)
  ZP.cast(skill)
  print("\tMana:", ZP.white_mana, "/", ZP.black_mana)
  print("\tProcs:", ZP.verstone_ready, "/", ZP.verfire_ready)
  print("\tWeaves:", ZP.weave_windows, "/ Dualcast:", ZP.dualcast)

# Is there a machine learning application to learn when is best to cast acceleration and manification in a given fight duration??
# Yes! There is! We can give a vector of features (white mana, black mana, verstone ready, verfire ready, remaining duration) and 
# the objective is to maximize potency!! Need to discuss this with lawrence.