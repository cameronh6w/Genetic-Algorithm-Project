# TODO: Update the main function to your needs or remove it.
import Functions
import random
import Schedule


#I did the random assignment here in main, but this will probably change - cameron


def main() -> None:    
   
    #get lists with all the objects 
    rooms = Functions.get_all_rooms()
    facilitators = Functions.get_all_facilitators()
    activites = Functions.get_all_activities()
    times = [10,11,12,1,2,3]
        
    print("\nActivity Data: ")
    #assign facilitator, room, and time to each activity 
    for a in activites:
        #randomly selects an index from those lists
        f = random.randint(0, len(facilitators)-1)
        r = random.randint(0,len(rooms)-1)
        t = random.randint(0,len(times)-1)
        
        #assigns the random object to the activity 
        a.assign_F(facilitators[f])
        a.assign_R(rooms[r])
        a.assign_T(times[t])

        #for testing
        a.print_assigned_data()

    #create schedule from activities 
    schedule_dict = Functions.create_dictionary(activites)
    schedule = Schedule.Schedule(0,schedule_dict)
    print("\nSchedule Data: ")
    schedule.print_data()


    




if __name__ == "__main__":
    main()


