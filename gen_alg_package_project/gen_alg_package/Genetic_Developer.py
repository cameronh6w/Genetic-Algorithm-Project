#this is where the fun begins; the actual genetic algorithm stuff

import Generation

class Genetic_Developer:
    
    #come back to this based on what the central loop function ends up requiring
    def __init__(self):
        pass
    
    
    def evaluate(self, population):
        pass

    def select_parents(self, population):
        pass

    def reproduce(self, population):
        pass

    def mutate(self, population):
        pass


    def run_generation(self, pop, mutation_rate, generation_number):
        #BASE CASE! Check if our generation number is equal to or greater than our limit. If so, call an output function

        ##if not, continue

        #pass our current generation to our evaluator
        evaluate(pop)

        #print generation information, like stats and the number of what generation we're on

        #Pass our population to the Selection function, which will return a list () of all the schedules valid for reproducing
        chosen_ones = select_parents(pop)

        #once we have all schedules valid for reproducing, DELETE ALL SCHEDULES NOT IN THE CHOSEN ONE LIST. WE CULL THE WEAK. DEATH WILL IMPROVE THE EMPIRE.

        #now that we only have our children, pass them to the reproduction function :)
        new_generation = reproduce(pop)

        self.run_generation(new_generation, mutation_rate, (generation_number + 1))