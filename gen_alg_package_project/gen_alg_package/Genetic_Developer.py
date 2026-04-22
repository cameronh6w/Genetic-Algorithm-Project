#this is where the fun begins; the actual genetic algorithm stuff

from Generation import Generation
from Schedule import Schedule
from Fitness_Scorer import FitnessScorer
import Functions
import numpy as np
import random
import sys
from scipy.special import softmax
import copy
import plotext as plt
import csv
import os
import datetime

class Genetic_Developer:
    
    #come back to this based on what the central loop function ends up requiring
    def __init__(self, target_generations=100, improvement_threshold=0.01, mutation_rate=0.05):

        #We're gonna need a target for how many minimum generations we want to create, and the improvement threshold for how much each generation has to improve from the past generation's (best? average?) fitness score before we just stop
        self.target_generations = target_generations
        self.improvement_threshold = improvement_threshold

        #We're also gonna need a mutation rate
        self.mutation_rate = mutation_rate
        self.initial_mutation_rate = mutation_rate
        self.mutation_decay_interval = 5  # halve mutation rate every N generations

        self.current_generation: Generation = None
        self.scores_over_time: list[float] = []
        self.best_schedule_log: list[str] = []

        self.setup()
    
    def setup(self):
        print("Genetic Developer initialized!")
        print("Populating first generation...")

        first_generation = Generation(gen_size=250)

        for i in range(0, first_generation.gen_size):
            first_generation.population.append(Functions.create_random_Schedule())
        
        print(f"Generation 1 size: {len(first_generation.population)}")

        self.current_generation = first_generation

        print("Ready to begin evolution.")
        self.ready = True

    #The head honcho of evaluation! Based on our fitness function code, this will run it on every single schedule in the generation, giving them each their individual fitness scores, and then it'll call the function to calculate and assign the highest and/or worst fitness scores out of the generation. 
    def evaluate(self, generation: Generation):

        #TODO: Update this with what the ACTUAL evaluation will be. Right now, this just does some random numbers. NOTE: DO NOT KEEP THIS!
        total_score = 0.0

        for schedule in generation.population:
            # Assigning a random mock score between 0 and 10
            # schedule.score = random.uniform(0.0, 10.0)
            #NOTE: TODO: REPLACE THIS! ^^^^^^^^^^^^^
            #with something like this. Just uncomment this line once this function works.
            schedule.score = FitnessScorer.score(schedule)
            
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
        schedules_created = 0

        for i in range(125):
            parent_a = np.random.choice(generation.population, p=probabilities)
            parent_b = np.random.choice(generation.population, p=probabilities)
            
            child = self.crossover(parent_a, parent_b)
            schedules_created += 1
            
            next_generation.append(child)
        
        self.mutate(next_generation)
        print(f"Total new schedules created: {schedules_created}")

        # We mutate BEFORE we append the 125 parents back with their 125 children.
        final_generation = Generation(population=(generation.population + next_generation))

        return final_generation

    #So, this is just the actual step of crossover. Take half of one schedule, marry it to half of the other schedule, and then return the child. This works!
    def crossover(self, parent_a: Schedule, parent_b: Schedule):
        child_a = Schedule(schedule={
            "10am": copy.deepcopy(parent_a.schedule['10am']),
            "11am": copy.deepcopy(parent_a.schedule['11am']), 
            "12pm": copy.deepcopy(parent_a.schedule['12pm']), 
            "1pm": copy.deepcopy(parent_b.schedule['1pm']), 
            "2pm": copy.deepcopy(parent_b.schedule['2pm']), 
            "3pm": copy.deepcopy(parent_b.schedule['3pm'])
        })

        child_b = Schedule(schedule={
            "10am": copy.deepcopy(parent_b.schedule['10am']),
            "11am": copy.deepcopy(parent_b.schedule['11am']), 
            "12pm": copy.deepcopy(parent_b.schedule['12pm']), 
            "1pm": copy.deepcopy(parent_a.schedule['1pm']), 
            "2pm": copy.deepcopy(parent_a.schedule['2pm']), 
            "3pm": copy.deepcopy(parent_a.schedule['3pm'])
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
            print("-----------------------------------")
            print("Beginning evolution!")

            self.run_generation(self.current_generation, 1, 0)

    def run_generation(self, generation: Generation, generation_number:int, last_avg: float):
        last_average = last_avg
        print("----------------------------------")
        #pass our current generation to our evaluator
        self.evaluate(generation)

        #print generation information, like stats and the number of what generation we're on
        print(f"{generation_number}: Generation information:")
        print(f"Best Fitness Score:    {generation.best_score:.4f}")
        print(f"Average Fitness Score: {generation.avg_score:.4f}")
        print(f"Worst Fitness Score:   {generation.worst_score:.4f}")
        print(f"Mutation Rate:         {self.mutation_rate:.5f}")

        self.scores_over_time.append([generation.best_score, generation.avg_score, generation.worst_score, self.mutation_rate])

        # Capture formatted best schedule string for the log
        best = generation.get_best()
        log_lines = [f"[ Generation {generation_number} | Score: {best.score:.4f} ]"]
        for slot, activities in best.schedule.items():
            if not activities:
                log_lines.append(f"  {slot}: (empty)")
            else:
                for i, a in enumerate(activities):
                    slot_label = slot if i == 0 else " " * len(slot)
                    log_lines.append(
                        f"  {slot_label}  {a.get_name():<10} "
                        f"Room: {a.get_assigned_room().get_name():<14} "
                        f"Fac: {a.get_assigned_facilitator().get_name()}"
                    )
        self.best_schedule_log.append("\n".join(log_lines))

        # Adaptive mutation decay: halve every N generations, never below 0.001
        if generation_number % self.mutation_decay_interval == 0:
            self.mutation_rate = max(0.001, self.mutation_rate / 2)
            print(f"  --> Mutation rate decayed to {self.mutation_rate:.5f}")

        if last_average > 0:
            improvement_rate = ((generation.avg_score - last_average) / last_average * 100)
            print(f"Improvement Rate: {improvement_rate:.4f}%")

        #BASE CASE! Check if our generation number is equal to or greater than our limit. If so, call it quits.

        if generation_number >= 100:
            print(f"{generation_number}: Current generation greater than 100! Will check improvement rate.")

            improvement_rate = ((generation.avg_score - last_avg) / last_avg * 100)
            print(f"{generation_number}: Improvement Rate - {improvement_rate}%")

            if improvement_rate < self.improvement_threshold:
                print(f"{generation_number}: Improvement rate is below improvement threshold, {self.improvement_threshold}! Genetic evolution is finished. Terminating.")

                self.finish(generation, generation_number)
                return

            else:
                print(f"{generation_number}: Improvement rate sufficient for another generation. Continuing.")

        #CULL THE WEAK. Basically, we entirely delete the later half of the generation, who have the worst half of fitness scores.
        print(f"{generation_number}: Thanos-snapping worst half of generation...")
        generation.cull_least_half()

        #Then, pass our remaining half to the reproduction function to fill out the generation with a population stronger than that which came before
        print(f"{generation_number}: Beginning reproduction process...")
        new_generation = self.reproduce(generation)

        print(f"{generation_number}: New generation created! Population: {len(new_generation.population)}")

        #input("Ready to continue?")
        self.run_generation(new_generation, (generation_number + 1), generation.avg_score)
    
    def write_outputs(self, gen_number: int):
        results_dir = os.path.join(os.path.dirname(__file__), "results")
        os.makedirs(results_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # --- fitness_history.csv ---
        csv_path = os.path.join(results_dir, f"fitness_history_{timestamp}.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["generation", "best_score", "avg_score", "worst_score", "mutation_rate"])
            for i, row in enumerate(self.scores_over_time, start=1):
                writer.writerow([i, f"{row[0]:.6f}", f"{row[1]:.6f}", f"{row[2]:.6f}", f"{row[3]:.6f}"])
        print(f"Fitness history written to: {csv_path}")

        # --- best_schedule_log.txt ---
        log_path = os.path.join(results_dir, f"best_schedule_log_{timestamp}.txt")
        with open(log_path, "w") as f:
            f.write(f"Genetic Algorithm Run — {timestamp}\n")
            f.write(f"Finished at generation {gen_number}\n")
            f.write(f"Initial mutation rate: {self.initial_mutation_rate} | Final mutation rate: {self.mutation_rate:.5f}\n")
            f.write("=" * 60 + "\n\n")
            for entry in self.best_schedule_log:
                f.write(entry + "\n\n")
        print(f"Best schedule log written to: {log_path}")

    def plot_scores(self):
        data = self.scores_over_time

        if not data:
            print("No score data to plot.")
            return

        best_scores  = [row[0] for row in data]
        avg_scores   = [row[1] for row in data]
        worst_scores = [row[2] for row in data]
        generations  = list(range(1, len(data) + 1))

        plt.clf()
        plt.plot(generations, best_scores,  label="Best",    color="green")
        plt.plot(generations, avg_scores,   label="Average", color="yellow")
        plt.plot(generations, worst_scores, label="Worst",   color="red")
        plt.title("Fitness Scores Over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Fitness Score")
        plt.show()

    def finish(self, generation: Generation, gen_number:int):
        print("--------------------------------------------")
        print(f"Finished at generation {gen_number}!")

        best = generation.get_best()
        print("Best schedule:")
        best.print_formatted()

        self.write_outputs(gen_number)
        self.plot_scores()