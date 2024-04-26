import os

try:
    os.system('python wiggledb.py | sms_thread')
except:
    print("fail")
