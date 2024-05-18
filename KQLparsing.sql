//Barbarians.csv
source
| extend TimeGenerated = now()
| extend XY_Coords = iif(Added_This_Turn contains "-", XY_Coords = Added_This_Turn, "")
| extend Added_This_Turn = iif(Added_This_Turn contains "-", Added_This_Turn = "", Added_This_Turn)
| extend X_Coords = toint(extract(@"(\d+)-", 1, XY_Coords))
| extend Y_Coords = toint(extract(@"-(\d+)", 1, XY_Coords))
| extend Unit_Name = iif(Desired_Camps contains "_", Unit_Name = Desired_Camps, "")
| extend Desired_Camps = iif(Desired_Camps contains "_", Desired_Camps = "", Desired_Camps)
| extend Tribe_Name = iif(Num_Camps contains "_", Tribe_Name = Num_Camps, "")
| extend Num_Camps = iif(Num_Camps contains "_", Num_Camps = "", Num_Camps)
| project-away XY_Coords, Land_Plots, No_Visibility

//Barbarian_Unit
source
| extend TimeGenerated = now()
| extend XY_Coords = iif(Added_This_Turn contains "-", XY_Coords = Added_This_Turn, "")
| extend X_Coord = toint(extract(@"(\d+)-", 1, XY_Coords))
| extend Y_Coord = toint(extract(@"-(\d+)", 1, XY_Coords))
| extend Unit_Name = iif(Desired_Camps contains "_", Unit_Name = Desired_Camps, "")
| extend Desired_Camps = iif(Desired_Camps contains "_", Desired_Camps = "", Desired_Camps)
| extend Tribe_Name = iif(Num_Camps contains "_", Tribe_Name = Num_Camps, "")
| extend Num_Camps = iif(Num_Camps contains "_", Num_Camps = "", Num_Camps)
| extend Turn = iif(Unit_Name !contains "UNIT", Turn = "0", tostring(Turn))
| where Turn != "0"
| project TimeGenerated, Turn, Unit_Name, X_Coord, Y_Coord
