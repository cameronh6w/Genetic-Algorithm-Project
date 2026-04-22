#what's a generation gonna have? A bunch of schedules! 
#Okay, being specific. A generation is gonna use SOME data structure to hold N >= 250 Schedules, and best_score, worst_score, and avg_score variables for the fitness scores. On creation, we're gonna fill that data structure with the given amount of schedules randomly created by our random schedule creation function.

from Schedule import Schedule
import Functions

#make it so that we can create a generation by just passing it a population list
class Generation:
    def __init__(self, population: list[Schedule] = None, gen_size: int = 250):
        
        self.best_score = 0.0
        self.worst_score = 0.0
        self.avg_score = 0.0

        self.gen_size = gen_size

        if population is not None:
            self.population = population
        else:
            self.population = []
    
    def cull_least_half(self):
        #sort the population by fitness score (highest first)
        self.population.sort(key=lambda x: x.score, reverse=True)

        #remove the bottom half (the later half)
        #self.population = self.population[:len(self.population)//2]
        self.population = self.population[:max(1, len(self.population) // 10)]

        print(f"The weak have been culled. Remaining population: {len(self.population)}")
    
    def get_best(self) -> Schedule:
        # Return the schedule with the maximum fitness score
        return max(self.population, key=lambda x: x.score)
    
    def get_worst(self) -> Schedule:
        # Return the schedule with the minimum fitness score
        return min(self.population, key=lambda x: x.score)
            