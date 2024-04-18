from tinydb import TinyDB, Query

# Create a database instance
river_water_quality = TinyDB('river_water_quality.json')

# Define the table schema
table = river_water_quality.table('readings')

# Function to insert data into the database
def insert_data(id, time, ph, ec, validated):
    table.insert({'ID': id, 'TIME': time, 'PH': ph, 'EC': ec, 'VALIDATED': validated})

# Function to retrieve all data from the database
def get_all_data():
    return table.all()

# Function to retrieve data by ID
def get_data_by_id(id):
    return table.get(Query().ID == id)

# Function to update data by ID
def update_data_by_id(id, time=None, ph=None, ec=None, validated=None):
    data = {}
    if time is not None:
        data['TIME'] = time
    if ph is not None:
        data['PH'] = ph
    if ec is not None:
        data['EC'] = ec
    if validated is not None:
        data['VALIDATED'] = validated
    
    table.update(data, Query().ID == id)

# Function to delete data by ID
def delete_data_by_id(id):
    table.remove(Query().ID == id)


#data correction
def updateData():
    def updateData():
    new_lab_data = False        
    d = getLatestLabData()
    d = [1,"14:10",7.999,2.8]  # sample
    ids = [j['ID'] for j in table.all()]
    start = ids.index(d[0])  # find correct ID
    while table.get(Query().ID == ids[start])['VALIDATED'] != 0:
        start += 1

    length = len(ids)       
    deltaPH = table.get(Query().ID == ids[length - 1])['PH'] - d[2]
    deltaEC = table.get(Query().ID == ids[length - 1])['EC'] - d[3]

    for i in range(start, length):
        table.update({'PH': table.get(Query().ID == ids[i])['PH'] + deltaPH * (i / length)}, Query().ID == ids[i])
        table.update({'EC': table.get(Query().ID == ids[i])['EC'] + deltaEC * (i / length)}, Query().ID == ids[i])

def checkForNewLabData():
    # Implementation to check for new lab data
    pass

def getLatestLabData():
    # Implementation to get the latest lab data
    pass

# Main program logic
new_lab_data = False

while True:
    if new_lab_data:
        updateData()
    else:
        if checkForNewLabData():
            new_lab_data = True
