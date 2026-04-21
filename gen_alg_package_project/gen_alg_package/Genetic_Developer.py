#this is where the fun begins; the actual genetic algorithm stuff

from Generation import Generation
from Schedule import Schedule
import Functions
import numpy as np
import random
import sys
from scipy.special import softmax

class Genetic_Developer:
    
    #come back to this based on what the central loop function ends up requiring
    def __init__(self, target_generations=100, improvement_threshold=0.01, mutation_rate=0.05):

        #We're gonna need a target for how many minimum generations we want to create, and the improvement threshold for how much each generation has to improve from the past generation's (best? average?) fitness score before we just stop
        self.target_generations = target_generations
        self.improvement_threshold = improvement_threshold

        #We're also gonna need a mutation rate
        self.mutation_rate = mutation_rate

        self.current_generation: Generation = None

        self.setup()
    
    def setup(self):
        print("Genetic Developer initialized!")
        print("Populating first generation...")

        first_generation = Generation(gen_size=250)

        for i in range(0, first_generation.gen_size):
            first_generation.population.append(Functions.create_random_Schedule())
        
        print(f"Generation 1 size: {len(first_generation.population)}")
        print("Starting generation information:")
        print(f"Best Score: {first_generation.best_score}")
        print(f"Average Score: {first_generation.avg_score}")
        print(f"Worst Score: {first_generation.worst_score}")

        self.current_generation = first_generation

        print("Ready to begin evolution.")
        self.ready = True

    #The head honcho of evaluation! Based on our fitness function code, this will run it on every single schedule in the generation, giving them each their individual fitness scores, and then it'll call the function to calculate and assign the highest and/or worst fitness scores out of the generation. 
    def evaluate(self, generation: Generation):

        #TODO: Update this with what the ACTUAL evaluation will be. Right now, this just does some random numbers. NOTE: DO NOT KEEP THIS!
        total_score = 0.0

        for schedule in generation.population:
            # Assigning a random mock score between 0 and 10
            schedule.score = random.uniform(0.0, 10.0)
            total_score += schedule.score
        
        # Calculate generation stats
        generation.best_score = generation.get_best().score
        generation.worst_score = generation.get_worst().score
        generation.avg_score = total_score / len(generation.population)

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
        
        self.mutate(next_generation)

        # We mutate BEFORE we append the 125 parents back with their 125 children.
        final_generation = Generation(population=(generation.population + next_generation))

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


    #Given our particular mutation rate, we take each schedule in the population and roll our chance to mutate. If mutate is true, take that particular schedule and call a function to regenerate that timeslot!
    def mutate(self, population):

        total_mutated = 0

        for schedule in population:
            if np.random.rand() < self.mutation_rate:
                total_mutated += 1
                
                random_timeslot = random.choice(list(schedule.schedule.keys()))
                
                #calls the really cool function to randomly redo that timeslot
                schedule.mutate_timeslot(random_timeslot)
                

        print(f"Total mutated: {total_mutated}")


    def begin(self):
        if self.ready:
            print("Beginning evolution!")

            self.run_generation(self.current_generation, 1)

    def run_generation(self, generation: Generation, generation_number:int, last_avg: float):

        #pass our current generation to our evaluator
        self.evaluate(generation)

        #print generation information, like stats and the number of what generation we're on
        print(f"{generation_number}: Generation information:")
        print(f"Best Fitness Score: {generation.best_score}")
        print(f"Average Fitness Score: {generation.avg_score}")
        print(f"Worst Fitness Score: {generation.worst_score}")

        #BASE CASE! Check if our generation number is equal to or greater than our limit. If so, call it quits. 

        if generation_number >= 100:
            print(f"{generation_number}: Current generation greater than 100! Will check improvement rate.")

            improvement_rate = (generation.avg_score / last_avg * 100)
            print(f"{generation_number}: Improvement Rate - {improvement_rate}%")

            if improvement_rate < self.improvement_threshold:
                print(f"{generation_number}: Improvement rate is below improvement threshold, {self.improvement_threshold}! Genetic evolution is finished. Terminating.")

                self.finish(generation, generation_number)

            else:
                print(f"{generation_number}: Improvement rate sufficient for another generation. Continuing.")

                last_average = generation.avg_score

        #CULL THE WEAK. Basically, we entirely delete the later half of the generation, who have the worst half of fitness scores.
        print(f"{generation_number}: Thanos-snapping worst half of generation...")
        generation.cull_least_half()

        #Then, pass our remaining half to the reproduction function to fill out the generation with a population stronger than that which came before
        print(f"{generation_number}: Beginning reproduction process...")
        new_generation = self.reproduce(generation)

        print(f"{generation_number}: New generation created!")

        input("Ready to continue?")
        self.run_generation(new_generation, (generation_number + 1), last_average)
    
    def finish(self, generation: Generation, gen_number:int):
        print(f"Finished at generation {gen_number}!")

        best = generation.get_best()
        print("Best schedule:")
        best.print_data()

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