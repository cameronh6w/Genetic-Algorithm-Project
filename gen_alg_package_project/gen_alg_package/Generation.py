#what's a generation gonna have? A bunch of schedules! 
#Okay, being specific. A generation is gonna use SOME data structure to hold N >= 250 Schedules, and best_score, worst_score, and avg_score variables for the fitness scores. On creation, we're gonna fill that data structure with the given amount of schedules randomly created by our random schedule creation function.

import Schedule
import Functions

#make it so that we can create a generation by just passing it a population list
class Generation:
    def __init__(self, gen_size: int):
        
        self.best_score = -1.0
        self.worst_score = -1.0
        self.avg_score = -1.0

        self.population = []

        for i in range(0, gen_size):

            #implementing  what I did would look something like this - cameron 
            #yippee - tomie
            self.population.append(Functions.create_random_Schedule()) 
            