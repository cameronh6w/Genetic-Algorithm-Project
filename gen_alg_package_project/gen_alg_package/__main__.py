# TODO: Update the main function to your needs or remove it.
import Functions
import random

#I did the random assignment here in main, but this will probably change - cameron


def main() -> None:   
   #for testing 
   schedule = Functions.create_random_Schedule()
   random_timeslot = random.choice(list(schedule.schedule.keys()))
        
   schedule.mutate_timeslot(random_timeslot)
   


    




if __name__ == "__main__":
    main()


