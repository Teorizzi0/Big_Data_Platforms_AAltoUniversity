import os
import shutil
import requests
import json
import pandas as pd
import sys
import time


userID = sys.argv[1]
clientapp = sys.argv[2]
path = '../data/client-input-directory/'+str(userID)
response = requests.get("http://127.0.0.1:5000/users/account/"+str(userID))

whole_size = 0
numb_files = 0
input_files = []
check = True

response = requests.get("http://127.0.0.1:5000/users/account/"+str(userID))
print(response.content)
user_constraints = json.loads(response.content)

for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        file_size = os.path.getsize(dirpath+"/"+filename)
        if filename[-4:]!= user_constraints['fileFormat']:
            print('Not allowed format:',filenames)
        elif file_size/500000 > user_constraints['maxSize']:
            print('Out of dimension',file_size/500000,'MB')
        else:
            numb_files = numb_files + 1
            whole_size = whole_size + file_size
            input_files.append(filename)

if numb_files >user_constraints['maxFiles]:
    print('Too many files uploaded.')
    check = False

if check:
    print(" {} files, total size {}".format(numb_files,whole_size))
    for input_file in input_files:
        with open('{}/{}'.format(path,input_file)) as fp:
            content = fp.read()
        print('Sent post request: http://127.0.0.1:5000/files/{}/{}'.format(userID,input_file))
        response = requests.post('http://127.0.0.1:5000/files/{}/{}'.format(userID,input_file),data = content.encode('utf-8'))
