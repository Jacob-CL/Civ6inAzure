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


//Barbarian_Units_CL
source
| extend TimeGenerated = now()
| extend XY_Coords = iif(Added_This_Turn contains "-", XY_Coords = Added_This_Turn, "")
| extend X_Coord = toint(extract(@"(\d+)-", 1, XY_Coords))
| extend Y_Coord = toint(extract(@"-(\d+)", 1, XY_Coords))
| extend Unit_Name = iif(Desired_Camps contains "_", Unit_Name = Desired_Camps, "")
| extend Turn = iif(Unit_Name !contains "UNIT", Turn = "0", tostring(Turn))
| where Turn != "0"
| project TimeGenerated, Turn, Unit_Name, X_Coord, Y_Coord


//Barbarian_Camps_CL
source
| extend TimeGenerated = now()
| extend Desired_Camps = iif(Desired_Camps contains "_", Desired_Camps = "", Desired_Camps)
| extend Num_Camps = iif(Num_Camps contains "_", Num_Camps = "", Num_Camps)
| extend Turn = iif(Num_Camps == "", Turn = "0", tostring(Turn))
| where Turn != "0"
| project TimeGenerated, Turn, Num_Camps, Desired_Camps


//AStar_GC (Unit_Movement_CL)
source
| extend TimeGenerated = now()
| extend Turn = trim_start("0", GameTurn)
| extend Turn = trim_start("0", Turn)
| extend Unit = trim_start(@"UNIT_", Unit)
| extend Unit = trim_end(@" \(\d+\)", Unit)
| extend Player = trim_start(@"LOC_CIVILIZATION_", Player)
| extend Player = trim_end(@"_NAME", Player)
| extend ToX = iif(ToX == (-9999), FromX, ToX)
| extend ToY = iif(ToY == (-9999), FromY, ToY)
| project-away Checksum, GameTurn, Info

//Lua.log (Map_Generation)
source
| extend TimeGenerated = now()
| where strlen(Event) >= 4
| where strlen(Message) >= 4
| where Event == "Map Script" or Event == "AdvancedSetup"

//GameCore.log (Player_Generation_CL)
source
| extend TimeGenerated = now() 
| where Message startswith "Player "
| extend Player = extract(@"^Player \d{1,2}", 0, Message)
| extend Player_Type = iif(Player == "Player 0", PlayerType = "Human", "A.I Civilization")
| extend Player_Type = iff(Player == "Player 63", Player_Type = "Barbarian", Player_Type)
| project-away Event

//AI_CityBuild.csv (Civ_production_queue)
source
| extend TimeGenerated = now()
| extend Turn = Game_Turn
| extend Turn = iif(Construct == "", Turn = "0", tostring(Turn))
| where Turn != "0"
| extend City = trim_start(@"LOC_CITY_NAME_", City)
| project TimeGenerated, Player, Turn, City, Construct, Order_Source



//Player_Stats (Player_Stats_1)
source
| extend TimeGenerated = now()
| extend Player = trim_start(@"CIVILIZATION_", Player)
| extend Turn = Game_Turn
| project-away Game_Turn

//Player_Stats_2 (Player_Stats_2)