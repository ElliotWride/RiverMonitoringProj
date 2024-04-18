db = [[]] #needs upgrading not a good way to store data especially logn term
#assumes degradation is linear
#Data = [ID,TIME,PH,EC,UPDATED]
data = [1,"12:30",7.141,2.6,0]
db.append(data)
db.pop(0)
print(db)
new_lab_data=False

while(true):
    if (new_lab_data):
        updateData()
                

        
    else:
        if(checkForNewLabData()):
            new_lab_data=True

updateData():
    new_lab_data=False        
    d = getLatestLabData()
    d = [1,"14:10",7.999,2.8] #sample

    ids = [j[0] for j in db]
    start = ids.index(d[0]) #find correct ID
    while(db[start,5]!=0):
        start++
 
    length = len(ids)       
    deltaB = db[length,3] - d[3]

    for i in range(start,length):
        db[i,3] = db[i,3] + deltaB(i/length) #gradient correction of data points
        
    
            
