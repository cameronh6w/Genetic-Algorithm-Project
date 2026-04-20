
import csv
import Room
import Facilitator
import Activity

def readCSV(name : str):

    csv_list = []
    with open('gen_alg_package_project/gen_alg_package/data/'+name+'.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader) #skip  first line

        for row in reader:
            csv_list.append(row) 
            

    return csv_list

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




