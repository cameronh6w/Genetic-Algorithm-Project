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