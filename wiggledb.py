from tinydb import TinyDB, Query
import time
import sys
import threading
import shutil
import os

# Global variables
oldSMS = ""
oldLabData = ""
lock = threading.Lock()

# Create a database instance
river_water_quality = TinyDB('river_water_quality.json')
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

# Function to backup the database
def backup_database():
    while True:
        time.sleep(3600)  # Backup every hour
        try:
            shutil.copyfile('river_water_quality.json', 'backup/river_water_quality_backup.json')
        except Exception as e:
            print(f"Error occurred during backup: {e}")

#data correction
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

def new_cell_data():
    global oldSMS
    if (oldSMS != sys.stdin.read(1024)):
        oldSMS = sys.stdin.read(1024)
        return True

def new_lab_data():
    global oldLabData
    if (oldLabData != "input"):
        oldSMS = "input"
        return True

# Main program logic
if __name__ == "__main__":
    backup_thread = threading.Thread(target=backup_database)
    backup_thread.daemon = True
    backup_thread.start()

    while True:
        if new_cell_data():
            new_data = sys.stdin.read(1024)
            insert_data(new_data)
        if new_lab_data():
            updateData(new_lab_data)
