import random
import Schedule
import Activity
import Facilitator
import Room

class FitnessScorer:

    #NOTE: This is a temporary function. Feel free to overwrite, rename, anything, but this is what's currently being called in Genetic_Developer.evaluate(). Take in a schedule, return its fitness score.
    @staticmethod
    def score(schedule: Schedule) -> float:
        #give everyone one's! we all win! yippee
        return 1.0