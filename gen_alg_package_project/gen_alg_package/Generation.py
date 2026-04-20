#what's a generation gonna have? A bunch of schedules! 
#Okay, being specific. A generation is gonna use SOME data structure to hold N >= 250 Schedules, and best_score, worst_score, and avg_score variables for the fitness scores. On creation, we're gonna fill that data structure with the given amount of schedules randomly created by our random schedule creation function.

import Schedule
import Functions

class Generation:
    def __init__(self, gen_size: int):
        
        self.best_score = 0
        self.worst_score = 0
        self.avg_score = 0

        self.population = []

        for i in range(0, gen_size):
            #This is where we'll add the randomized schedule creation...TODO: IF WE HAD SOME! (not angry, this is a fairlyoddparents reference)
            self.population.append(ScheduleGenerator.new()) #or some shit

            #implementing  what I did would look something like this - cameron
            self.population.append(Functions.create_random_Schedule()) 
            