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
  print(name)
  skill = ZP.GCD(name)
  if (skill == -1):
    skill = ZP.Buff(name)
    ZP.cast(skill)
  else:
    ZP.cast(skill)
    ZP.print_state()

for i in range(20):
  name = ZP.next_GCD()
  print(name)
  skill = ZP.GCD(name)
  ZP.cast(skill)
  ZP.print_state()