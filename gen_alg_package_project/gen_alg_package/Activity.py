import Facilitator
import Room

class Activity: 
    name: str
    enrollment : int
    preferrd : list #this will be a list of Facilitators 
    other :list     #this will be a list of Facilitators
    need_lab : bool
    need_projector : bool

    assigned_facilitator : Facilitator 
    assigned_room : Room
    assigned_time : int   #im doing int instead of enum

    

    def __init__(self, name: str, enrollment: int, preferred: list, other: list,
                 need_lab: bool, need_projector: bool):
        self.name = name
        self.enrollment = enrollment
        self.preferred = preferred
        self.other = other
        self.need_lab = need_lab
        self.need_projector = need_projector

    #getters
    def get_name(self):
        return self.name

    def get_enrollment(self):
        return self.enrollment

    def get_preferred(self):
        return self.preferred

    def get_other(self):
        return self.other

    def get_need_lab(self):
        return self.need_lab

    def get_need_projector(self):
        return self.need_projector

    def get_assigned_facilitator(self):
        return self.assigned_facilitator

    def get_assigned_room(self):
        return self.assigned_room

    def get_assigned_time(self):
        return self.assigned_time
    
    #setters
    def assign_F(self, f : Facilitator):
        self.assigned_facilitator = f

    def assign_R(self, r : Room):
        self.assigned_room = r

    def assign_T(self, t : int):
        self.assigned_time = t