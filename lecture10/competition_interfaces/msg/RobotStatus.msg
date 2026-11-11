# The status of one robot (Lecture 6, rules 1 and 3)
uint8 ACTIVE=0          # 10% or more
uint8 NEEDS_RECHARGE=1  # Below 10%: the robot does no tasks

string name             # The robot's name
uint8 battery_pct       # A whole percent, 0 to 100
uint8 status            # ACTIVE or NEEDS_RECHARGE
