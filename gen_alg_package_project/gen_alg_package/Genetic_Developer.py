#this is where the fun begins; the actual genetic algorithm stuff

import Generation
import numpy as np
from scipy.special import softmax

class Genetic_Developer:
    
    #come back to this based on what the central loop function ends up requiring
    def __init__(self):

        #We're gonna need a target for how many minimum generations we want to create, and the improvement threshold for how much each generation has to improve from the past generation's (best? average?) fitness score before we just stop
        #We're also gonna need a mutation rate

        pass
    

    #The head honcho of evaluation! Based on our fitness function code, this will run it on every single schedule in the generation, giving them each their individual fitness scores, and then it'll call the function to calculate and assign the highest and/or worst fitness scores out of the generation. 
    def evaluate(self, population):
        pass

    #Combines both the selection and reproduction steps of the genetic algorithm. Converts fitness scores to probability, then runs the wheel to select the parents that get to reproduce, then...reproduces them!
    def reproduce(self, generation: Generation):

        #Turn our fitness scores into a numpy array, like... 
        fitness_scores = np.array([schedule.score for schedule in generation.population])

        #Get our softmax probability distribution
        probabilities = softmax(fitness_scores)

        next_generation = []

        # 3. The actual breeding loop
        for i in range(125):
            # np.random.choice spins the wheel, based on 
            # You pass it the list of objects, and the 'p' argument takes your probabilities.
            parent_a = np.random.choice(generation.population, p=probabilities)
            parent_b = np.random.choice(generation.population, p=probabilities)
            
            # Create your offspring (assuming your crossover makes 1 child)
            child = self.crossover(parent_a, parent_b)
            
            next_generation.append(child)
        
        next_generation = self.mutate(next_generation)

        # Now combine our 125 survivors with your 125 new children
        final_generation = Generation(generation.population + next_generation)

        return final_generation

    #So, rewrite! This is just the actual step of crossover. Take half of one schedule, marry it to half of the other schedule, and then return the child.
    def crossover(self, parent_a, parent_b):
        
        pass

    #Given our particular mutation rate, we take each schedule in the population and roll our chance to mutate. If mutate is true, take that particular schedule and...mutate it? TBA, TODO: will vary based on the implementation of how a schedule works 
    def mutate(self, generation: Generation):


        pass


    def run_generation(self, pop, mutation_rate, generation_number):
        #BASE CASE! Check if our generation number is equal to or greater than our limit. If so, call an output function

        ##if not, continue

        #pass our current generation to our evaluator
        self.evaluate(pop)

        #print generation information, like stats and the number of what generation we're on

        #CULL THE WEAK. Basically, we entirely delete the later half of the generation, who have the worst half of fitness scores.

        #Then, pass our remaining half to the reproduction function to fill out the generation with a population stronger than that which came before
        new_generation = self.reproduce(pop)

        self.run_generation(new_generation, mutation_rate, (generation_number + 1))