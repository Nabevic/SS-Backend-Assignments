#Force Ranks
force_ranks = ['youngling', 'padawan', 'knight', 'master', 'council_member', 'grand']

clearance = { #make sure to fix master and grandmaster. 
  "Basic": ['youngling', 'padawan','knight','master','council_member', 'grand', 'grand_master'],
  "Padawan": ['padawan','knight','master','council_member', 'grand', 'grand_master'],
  "Knight": ['knight','master','council_member', 'grand', 'grand_master'],
  "Master": ['master','council_member', 'grand', 'grand_master'],
  "Council": ['council_member', 'grand','grand_master'],
  "GrandMaster": 'grand_master'
}