import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
import random

#Replace path with the path of the csv file to upload
path = r'C:/Users/matte/Documents/Polimi/Erasmus/Big_Data_Platforms/I_assignment_materials/googleplaystore.csv'
csvfile = open(path, encoding="utf8")
reader = csv.DictReader( csvfile )

#Replace <password> with the password, for sensitive reason I didn't keep it written.
client = MongoClient('mongodb+srv://teorizla93:<password>@bdp19-imzzm.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = mongo_client.googleplaystore
db.segment.drop()
header= [ "App", "Category", "Rating", "Reviews", "Size", "Installs", "Type", "Price", "Content Rating", "Genres", "Last Updated", "Current Ver", "Android Ver"]

for each in reader:
    row={}
    for field in header:
        row[field]=each[field]

    db.segment.insert_one(row)




