class  Schedule:
    score : float
    schedule : dict

    def __init__(self, score : float, schedule : dict):
        self.score  = score
        self.schedule = schedule

    #getters
    def  get_score(self): 
        return self.score
    
    def get_schedule(self): 
        return self.schedule
    
    def  print_data(self):
        for key, value in self.schedule.items():
            print(key,": ", end="")
            for v in value:
                 print(v.get_name(), end=" ")
            print()
