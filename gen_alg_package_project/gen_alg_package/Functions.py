
import csv
import Room
import Facilitator
import Activity
import Schedule
import random

#PRE: name must be the exact name of one of the csv files in data folder 
#POST: returns a list where each element is a list of strings from one line of the csv
def readCSV(name : str):

    csv_list = []
    with open('gen_alg_package_project/gen_alg_package/data/'+name+'.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader) #skip  first line

        for row in reader:
            csv_list.append(row) 
            

    return csv_list

#POST: returns a list of room objects with data read from the csv 
def get_all_rooms():
    rooms_data = readCSV('Rooms')
    rooms = [] #list of Room objects

    for r in rooms_data:
        lab = True
        if (r[2] == 'FALSE'):
            lab = False
        proj = True
        if (r[3] == 'FALSE'):
            proj = False

        temp = Room.Room(r[0],r[1],lab,proj)
        rooms.append(temp)

    return rooms

#POST: returns a list of facilitator objects with data read from the csv 
def get_all_facilitators():
    facilitator_data = readCSV('Facilitators')
    facilitators = [] #list of Room objects

    for f in facilitator_data:
       

        pref = []
        avoid = []
        if(f[1] != ''):
            pref = f[1].split(",")

        if(f[2] != ''):
            avoid = f[2].split(",")

        temp = Facilitator.Facilitator(f[0], pref, avoid)
        facilitators.append(temp)

        
    return facilitators

#POST: returns a list of activity objects with data read from the csv (room, facilitator, and time not yet assigned)
def get_all_activities():
    activity_data = readCSV('Activities')
    activities = [] #list of Room objects

    for a in activity_data:

        pref = []
        other = []
        if(a[2] != ''):
            pref = a[2] .split(",")

        if(a[3] != ''):
            other = a[3].split(",")

        lab = True
        if (a[4] == 'FALSE'):
            lab = False
        proj = True
        if (a[5] == 'FALSE'):
            proj = False

        temp = Activity.Activity(a[0],a[1],pref,other,lab,proj)
        activities.append(temp)
                

    return activities


#PRE: takes in a  list of activitties that have all been assigned a time, facilitator,  and room
#POST: returns the schedule in a dictionary form
def create_dictionary(activities :  Activity):
    keys = ["10am", "11am", "12pm", "1pm",  "2pm", "3pm"]

    activites_at_10 =[]
    activites_at_11 =[]
    activites_at_12 =[]
    activites_at_1 =[]
    activites_at_2 =[]
    activites_at_3 =[]
    for a in activities:
        if a.get_assigned_time()  == 10:
            activites_at_10.append(a)
        if a.get_assigned_time()  == 11:
            activites_at_11.append(a)
        if a.get_assigned_time()  == 12:
            activites_at_12.append(a)
        if a.get_assigned_time()  == 1:
            activites_at_1.append(a)
        if a.get_assigned_time()  == 2:
            activites_at_2.append(a)
        if a.get_assigned_time()  == 3:
            activites_at_3.append(a)
    
    schedule = dict.fromkeys(keys, 0)
    schedule["10am"] = activites_at_10
    schedule["11am"] = activites_at_11
    schedule["12pm"] = activites_at_12
    schedule["1pm"] = activites_at_1
    schedule["2pm"] = activites_at_2
    schedule["3pm"] = activites_at_3

    return schedule

#POST: returns a schdeule object with random activities
# **NOTE: we probably shouldn't call the csv reader calls in this function, 
#  it can be done outside  of it and have these  first 4 variables  passed in  - cameron   
def  create_random_Schedule():
    #get lists with all the objects 
    rooms = get_all_rooms()
    facilitators = get_all_facilitators()
    activites = get_all_activities()
    times = [10,11,12,1,2,3]
    
    
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

    #create schedule from activities 
    schedule_dict = create_dictionary(activites)
    schedule = Schedule.Schedule(0,schedule_dict)

    return schedule