
#This class is mostly just a wrapper for the titular schedule dictionary, which will hold key value pairs corresponding to each timeslot, holding a list of all Activities scheduled during that time. So...
# "10am": (Activity, Activity, Activity)
# "11am": (Activity, Activity, )
#...and so on.

#NOTE: This is the wild west. Both scores and the schedule dictionary itself have no error handling to enforce concrete values, so lowkey, anything can go. Beware of possible errors like checking for "10AM" instead of lowercase "10am", or accidentally adding extra times.
#SECOND NOTE: We'll enforce -1 as the "empty" value; a schedule with a score of 0 genuinely does suck, but assume a score of -1 is one that hasn't been graded, yet.

class Schedule:
    score : float
    schedule : dict

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

    #getters
    def get_score(self): 
        return self.score
    
    def get_schedule(self): 
        return self.schedule
    
    def print_data(self):
        for key, value in self.schedule.items():
            print(key,": ", end="")
            for v in value:
                 print(v.get_name(), end=" ")
            print()
