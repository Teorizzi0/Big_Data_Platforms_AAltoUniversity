import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
import random

#import just a record in mongo with a test user "user_1" and password "prova"
client = MongoClient('mongodb+srv://new-user_1:prova@bdp19-imzzm.gcp.mongodb.net/test?retryWrites=true&w=majority')
db = client.googleplaystore
n = 1
test = "Test"

app = test + str(n)
row = {
    "App": app,
    "Category": "PRODUCTIVITY",
    "Rating": "3.2",
    "Reviews": 5,
    "Size": "Varies with device",
    "Installs": "10+",
    "Type": "Free",
    "Price": 0,
    "Content Rating": "Everyone",
    "Genres": "Productivity",
    "Last Updated": "May 26, 2018",
    "Current Ver": "Varies with device",
    "Android Ver": "Varies with device"
  }
db.segment.insert_one(row)

