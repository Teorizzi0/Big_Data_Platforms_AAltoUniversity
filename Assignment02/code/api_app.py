import flask
from flask import jsonify,request, Flask
import os
import threading
import atexit
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.concurrent import execute_concurrent
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import sys
import time
import logging
import json
from locationapp import init_cassandra

global user_accounts

PATH = '../data/server/'
DESTINATION_PATH = PATH + 'server_files/' 
file_ingested = list()
logging.basicConfig(filename='../logs/ingest.log', filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)
with open(PATH + 'user_accounts.json', 'r') as f:
    user_accounts =  json.load(f)

class _CustomHandler(FileSystemEventHandler):
    def on_created(self, event):
        path = event.src_path
        userID = path.split('/')[4]
        if path[-3:] == "csv":
            if path not in file_ingested:
                file_ingested.append(path)
                print("Customer {} ingests in {} with app name {} ".format(userID,path,user_accounts[userID]['clientapp']))
                mod = __import__(user_accounts[userID]['clientapp'])
                fun_to_call = getattr(mod, 'init_cassandra')
                fun_to_call(path)

def create_app():
    global db
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = DESTINATION_PATH

app = create_app() 

def batchingestmanager():
    observer = Observer()
    handler = _CustomHandler()
    observer.schedule(handler, DESTINATION_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

Ingest_thread = threading.Thread(target=batchingestmanager)
Ingest_thread.daemon = True
Ingest_thread.start()
return app

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World</h1>"

@app.route('/users/account/wholedb',methods=['GET'])
def useraccount_all():
	return jsonify([user_accounts])

@app.route('/users/account/<userID>', methods=['GET'])
def useraccount(userID):
    results = []
    print("Get",userID,"account:",user_accounts)
    try:
        usr_account = user_accounts[userID]
    except:
        return 400
    results.append(usr_account)

    return jsonify(usr_account)

@app.route('/users/account/adduser',methods=['POST'])
def add_useraccount():
    userID = request.form['userID']
    clientapp = request.form['clientapp']
    if userID not in user_accounts.keys():
        useraccount = {
            'userID':userID,
            'extension':'.csv',
            'maxSize':10,            
            'maxFiles':50,            
            'clientapp': clientapp,
        }

        user_accounts[userID] = useraccount

        with open( PATH + 'user_accounts.json', 'w') as f:  # writing JSON object
            json.dump(user_accounts, f)
        print("User {} account created".format(userID))
        return "Profile created"

@app.route("/data/<userID>/<filename>", methods=["POST"])
def post_file(userID,filename):
    """Upload a dataset."""
    UPLOAD_DIRECTORY = DESTINATION_PATH+userID
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    new_filename = UPLOAD_DIRECTORY+"/"+filename
   
    with open(new_filename, "wb") as fp:
        fp.write(request.data)
    print("File {} uploaded for customer {}".format(filename,userID))
    # Return 201 CREATED
    return "", 201

app.run()