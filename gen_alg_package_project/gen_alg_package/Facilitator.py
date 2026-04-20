
class  Facilitator:
    name : float
    preferred_times : list #this will be a list of ints (i didn't end up implementingn enums but this might be  easier anyway)
    avoid_times : list #this will be a list of ints (i didn't end up implementingn enums but this might be  easier anyway)

    def __init__(self, name : float, preferred_times : list, avoid_times :list ):
        self.name = name
        self.preferred_times = preferred_times
        self.avoid_times = avoid_times

    #getters
    def get_name(self): 
        return self.name
    

    def get_preferred_times(self): 
        return self.preferred_times
    
    def get_avoid_times(self): 
        return self.avoid_times
    
    def print_data(self):
        print(self.name,": ", end="")

        if(self.preferred_times !=  []):
            print("prefers ", end="")
            for p in self.preferred_times:
                print(p," ",end="")
        
        
        if(self.avoid_times !=  []):
            print("avoids ", end="")
            for a in self.avoid_times:
                print(a," ", end="")
            print()

        else:
            print()

       


    
    
    