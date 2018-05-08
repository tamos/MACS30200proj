import sys
import csv

with open('flee/my_settings.csv') as f:
  # [2, 0.5, 300, 1000, 0.3, 0.4, 0.1]
  my_setting_list = f.readline().split('|')
  my_camp_weight = float(my_setting_list[0])
  my_conflict_weight = float(my_setting_list[1])
  my_min_move = float(my_setting_list[2])
  my_max_move = float(my_setting_list[3])
  my_conflict_move_chance = float(my_setting_list[4])
  my_camp_move_chance = float(my_setting_list[5])
  my_default_move_chance = float(my_setting_list[6])

class SimulationSettings:

    Softening = 0.0
    #TurnBackAllowed = True # feature disabled for now.
    AgentLogLevel = 0 # set to 1 for basic agent information.
    CampLogLevel = 0  # set to 1 to obtain average times for agents to reach camps at any time step (aggregate info).
    InitLogLevel  = 0 # set to 1 for basic information on locations added and conflict zones assigned.
    TakeRefugeesFromPopulation = True

    CampWeight = my_camp_weight # attraction factor for camps.
    ConflictWeight = my_conflict_weight # reduction factor for refugees entering conflict zones.
    MinMoveSpeed = my_min_move # least number of km that we expect refugees to traverse per time step.
    MaxMoveSpeed = my_max_move # most number of km that we expect refugees to traverse per time step.
    UseDynamicCampWeights = True # overrides CampWeight depending on characteristics of the ecosystem.
    CapacityBuffer = 1.0

    #default move chances
    ConflictMoveChance = my_conflict_move_chance
    CampMoveChance = my_camp_move_chance
    DefaultMoveChance = my_default_move_chance


    AwarenessLevel = 1 #-1, no weighting at all, 0 = road only, 1 = location, 2 = neighbours, 3 = region.
    UseDynamicAwareness = False # Refugees become smarter over time.
    UseIDPMode = True


##  def ReadFromCSV(csv_name):
##    """
##    Reads simulation settings from CSV
##    """
##    number_of_steps = -1
##
##    with open(csv_name, newline='') as csvfile:
##      values = csv.reader(csvfile)
##
##      for row in values:
##        if row[0][0] == "#":
##          pass
##        elif row[0] == "AgentLogLevel":
##          SimulationSettings.AgentLogLevel = int(row[1])
##        elif row[0] == "CampLogLevel":
##          SimulationSettings.CampLogLevel = int(row[1])
##        elif row[0] == "InitLogLevel":
##          SimulationSettings.InitLogLevel = int(row[1])
##        elif row[0] == "MinMoveSpeed":
##          SimulationSettings.MinMoveSpeed = int(row[1])
##        elif row[0] == "MaxMoveSpeed":
##          SimulationSettings.MaxMoveSpeed = int(row[1])
##        elif row[0] == "NumberOfSteps":
##          number_of_steps = int(row[1])
##        elif row[0] == "CampWeight":
##          SimulationSettings.CampWeight = float(row[1])
##        elif row[0] == "ConflictWeight":
##          SimulationSettings.ConflictWeight = float(row[1])
##        elif row[0] == "ConflictMoveChance":
##          SimulationSettings.ConflictMoveChance = float(row[1])
##        elif row[0] == "CampMoveChance":
##          SimulationSettings.CampMoveChance = float(row[1])
##        elif row[0] == "DefaultMoveChance":
##          SimulationSettings.DefaultMoveChance = float(row[1])
##        elif row[0] == "AwarenessLevel":
##          SimulationSettings.AwarenessLevel = int(row[1])
##        else:
##          print("FLEE Initialization Error: unrecognized simulation parameter:",row[0])
##          sys.exit()
##
##    return number_of_steps
##
