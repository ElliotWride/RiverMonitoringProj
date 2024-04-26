import os

try:
    os.system('python /RiverMonitoringProject/wiggledb.py | /RiverMonitoringProject sms_thread')
except:
    print("fail")
