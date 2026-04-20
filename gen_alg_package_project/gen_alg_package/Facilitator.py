
class  Facilitator:
    name : float
    preferred_times : list #this will be a list of ints (i didn't end up implementingn enums but this might be  easier anyway)
    avoid_times : list #this will be a list of ints (i didn't end up implementingn enums but this might be  easier anyway)

    def __init__(self, name : float, preferred_times : list, avoid_times :list ):
        self.name = name
        self.preferred_times = preferred_times
 