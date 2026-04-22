
#This class is mostly just a wrapper for the titular schedule dictionary, which will hold key value pairs corresponding to each timeslot, holding a list of all Activities scheduled during that time. So...
# "10am": (Activity, Activity, Activity)
# "11am": (Activity, Activity, )
#...and so on.

#NOTE: This is the wild west. Both scores and the schedule dictionary itself have no error handling to enforce concrete values, so lowkey, anything can go. Beware of possible errors like checking for "10AM" instead of lowercase "10am", or accidentally adding extra times.
#SECOND NOTE: We'll enforce -1 as the "empty" value; a schedule with a score of 0 genuinely does suck, but assume a score of -1 is one that hasn't been graded, yet.

import random
import Functions

class Schedule:
    score : float
    schedule : dict
    activities : list

    def __init__(self, score: float = -1.0, schedule: dict = {
        "10am": [], 
        "11am": [], 
        "12pm": [], 
        "1pm": [], 
        "2pm": [], 
        "3pm": []
    }):
        self.score  = score
        self.schedule = schedule
        self.set_activities()
    
    #getters
    def get_score(self): 
        return self.score
    
    def get_schedule(self): 
        return self.schedule
    
    def print_data(self):
        for key, value in self.schedule.items():
            print(key,": ", end="")
            for v in value:
                 print(v.get_name(),
                       "R=",v.get_assigned_room().get_name(),
                       "F=",v.get_assigned_facilitator().get_name(),
                       ":",
                         end=" ")
            print()

    def print_formatted(self):
        # Column widths
        col_slot  = 6
        col_name  = 10
        col_room  = 14
        col_fac   = 12
        col_enrol = 10

        header = (f"{'SLOT':<{col_slot}} {'ACTIVITY':<{col_name}} "
                  f"{'ROOM':<{col_room}} {'FACILITATOR':<{col_fac}} {'ENROLLED':<{col_enrol}}")
        divider = "-" * len(header)

        print(divider)
        print(header)
        print(divider)

        for slot, activities in self.schedule.items():
            if not activities:
                print(f"{slot:<{col_slot}} {'(empty)':<{col_name}}")
            else:
                for i, a in enumerate(activities):
                    slot_label = slot if i == 0 else ""
                    room_name  = a.get_assigned_room().get_name() if hasattr(a, 'get_assigned_room') else "?"
                    fac_name   = a.get_assigned_facilitator().get_name() if hasattr(a, 'get_assigned_facilitator') else "?"
                    print(f"{slot_label:<{col_slot}} {a.get_name():<{col_name}} "
                          f"{room_name:<{col_room}} {fac_name:<{col_fac}} {a.get_enrollment():<{col_enrol}}")

        print(divider)

    def set_activities(self):
        self.activities = []
        for key, value in self.schedule.items():
            for a in value:
                self.activities.append(a)



        



    #PRE: key must be one of the keys of the schedule dictionary 
    #POST: Returns nothing, but the scedule dictionary has all the activities from the selected time slot randomly reassign facilitator and room
    def mutate_timeslot(self, key):
        rooms = Functions.get_all_rooms()
        facilitators = Functions.get_all_facilitators()
        
        activites = self.schedule.get(key)
        
        for a in activites:
            #randomly selects an index from those lists
            f = random.randint(0, len(facilitators)-1)
            r = random.randint(0,len(rooms)-1)
            
            #assigns the random object to the activity 
            a.assign_F(facilitators[f])
            a.assign_R(rooms[r])

        self.schedule[key] = activites


        
