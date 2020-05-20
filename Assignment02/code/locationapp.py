import csv
import os
import pandas as pd
import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.concurrent import execute_concurrent
import random
import datetime
import time



filename = []
time_spent = []
init = 0
statements_and_params = []
app = 'location'
logging.basicConfig(filename='../logs/ingestapp.log', filemode='w+',format='%(asctime)s - %(message)s', level=logging.INFO)

def start(name):
	print("Begin ingestion",name)

def init_cassandra(filenameca):
	start_connection()
	return ingest_data(filenameca, session)


def start_connection():
	global auth
	global cluster
	global session
	auth = PlainTextAuthProvider(username = 'cassandra', password = 'cassandra')
	cluster = Cluster(['127.0.0.1'], port=9042,auth_provider=auth,cql_version = "3.4.4")
	session = cluster.connect()
	logging.info('Creation Cassandra Environment')
	try:
		sql_statement = "CREATE KEYSPACE IF NOT EXISTS location WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 2};"
		keyspace = session.execute(sql_statement)
	except Exception as e:
		logging.info("KEYSPACE ALREADY EXISTS! Create Table.")
		logging.info(e)

	try:
		new_table = session.execute("CREATE TABLE location.User(uid uuid, part_id,ts_date,ts_time,room)
	except Exception as e:
		logging.info("TABLE ALREADY EXISTS! Insert Table.")
		logging.info(e)

	logging.info("FINISH KEY AND TABLE INIT.")
	init = 1
	return 1

def ingest_data(file, session):
	select_statement = session.prepare(
		"""
		INSERT INTO location.User (uid, part_id,ts_date,ts_time,room)
		VALUES (now(),?,?,?,?,?)
		""")
		
	dataset = pd.read_csv(file)
	dataset = dataset.dropna()
	dataset.apply(lambda x: combine_data(select_statement,x),axis=1)
	logging.info('Ingestion Start: ' + file)
	start_time = datetime.datetime.now()
	results = execute_concurrent(session, statements_and_params,concurrency=100, raise_on_first_error=False)

	for (success, result) in results:
		if not success:
			logging.info('Ingestion Failed: '+ file)

	logging.info('Ingestion Success: '+ file)
	end_time = datetime.datetime.now()
	logging.info('For {} rows and {} columns'.format(dataset.shape[0],dataset.shape[1]))
	logging.info('Each row takes {}'.format(str((end_time-start_time)/dataset.shape[0])))
	logging.info('File {} ingested and removed.'.format(file))
	filename.append(file)
	time_spent.append((end_time-start_time)/dataset.shape[0])
on for file {} with {} rows and current {} results".format(file,len(dataset),len(results)))
	return 1
		
def combine_data(select_statement,row):
    statements_and_params.append((select_statement,(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]))))



