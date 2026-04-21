#this is where the fun begins; the actual genetic algorithm stuff

from Generation import Generation
from Schedule import Schedule
import Functions
import numpy as np
from scipy.special import softmax

class Genetic_Developer:
    
    #come back to this based on what the central loop function ends up requiring
    def __init__(self, target_generations=100, improvement_threshold=0.01, mutation_rate=0.05):

        #We're gonna need a target for how many minimum generations we want to create, and the improvement threshold for how much each generation has to improve from the past generation's (best? average?) fitness score before we just stop
        self.target_generations = target_generations
        self.improvement_threshold = improvement_threshold

        #We're also gonna need a mutation rate
        self.mutation_rate = mutation_rate
    

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

        for i in range(125):
            parent_a = np.random.choice(generation.population, p=probabilities)
            parent_b = np.random.choice(generation.population, p=probabilities)
            
            child = self.crossover(parent_a, parent_b)
            
            next_generation.append(child)
        
        next_generation = self.mutate(next_generation)

        # Now combine our 125 survivors with our 125 new children
        final_generation = Generation(generation.population + next_generation)

        return final_generation

    #So, this is just the actual step of crossover. Take half of one schedule, marry it to half of the other schedule, and then return the child. This works!
    def crossover(self, parent_a: Schedule, parent_b: Schedule):
        child_a = Schedule(schedule={
            "10am": parent_a.schedule['10am'],
            "11am": parent_a.schedule['11am'], 
            "12pm": parent_a.schedule['12pm'], 
            "1pm": parent_b.schedule['1pm'], 
            "2pm": parent_b.schedule['2pm'], 
            "3pm": parent_b.schedule['3pm']
        })

        child_b = Schedule(schedule={
            "10am": parent_b.schedule['10am'],
            "11am": parent_b.schedule['11am'], 
            "12pm": parent_b.schedule['12pm'], 
            "1pm": parent_a.schedule['1pm'], 
            "2pm": parent_a.schedule['2pm'], 
            "3pm": parent_a.schedule['3pm']
        })

        #Now the battle. Whoever's luckier gets to exist and be the promised child. Would allow us to later on return both children, if we want to.
        return child_a if np.random.rand() < 0.5 else child_b


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

if __name__ == "__main__":
    print("Creating two random schedules!")

    schedule_a = Functions.create_random_Schedule()
    schedule_b = Functions.create_random_Schedule()

    head_honcho = Genetic_Developer()

    print("Here are the parents:")
    print("Schedule A:")
    schedule_a.print_data()
    print("Schedule B:")
    schedule_b.print_data()

    print("now kiss")

    child = head_honcho.crossover(schedule_a, schedule_b)

    child.print_data()