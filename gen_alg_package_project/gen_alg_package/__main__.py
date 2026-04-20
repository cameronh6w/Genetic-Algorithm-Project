# TODO: Update the main function to your needs or remove it.
import Functions
import random




def main() -> None:    
   
    rooms = Functions.get_all_rooms()
    facilitators = Functions.get_all_facilitators()
    activites = Functions.get_all_activities()
    times = [10,11,12,1,2,3]
        
    for a in activites:
        f = random.randint(0, len(facilitators)-1)
        r = random.randint(0,len(rooms)-1)
        t = random.randint(0,len(times)-1)
        
        a.assign_F(facilitators[f])
        a.assign_R(rooms[r])
        a.assign_T(times[t])


        a.print_assigned_data()



if __name__ == "__main__":
    main()
