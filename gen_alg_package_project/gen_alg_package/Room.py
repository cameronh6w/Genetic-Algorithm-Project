class Room:
    name : str
    capacity : int
    has_lab : bool
    has_projector : bool

    def __init__(self,  name : str, capacity : int, has_lab : bool, has_projector : bool):
        self.name = name
        self.capacity = capacity
        self.has_lab = has_lab
        self.has_projector = has_projector

    #getters
    def get_name(self): 
        return self.name
    
    def get_capacity(self): 
        return self.capacity
    
    def get_has_lab(self): 
        return self.has_lab
    
    def get_has_projector(self): 
        return self.has_projector
    
    def print_data(self):
        print(self.name,": ", self.capacity, " seats", end="")
        if self.has_lab:
            print(", has lab", end="")

        if self.has_projector:
            print(", has projector")
        else:
            print()
