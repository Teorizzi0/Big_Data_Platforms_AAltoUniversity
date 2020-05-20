import csv
import os
import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.concurrent import execute_concurrent
import random
import pandas as pd
from kafka import KafkaConsumer
from json import dumps
from kafka import KafkaProducer
import datetime
import time
import threading

filename = []
time_spent = []
statements_and_params = []
app = 'location'
logging.basicConfig(filename='../logs/ingeststream.log', filemode='w+',format='%(asctime)s - %(msg)s', level=logging.INFO)

def start(name):
	print("Begin ingestion",name)

def new_report():
	result = 0
	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
	while True:
		time.sleep(10)
		period_count = len(results) - result
		if 	period_count!=0:
			msg = "Total {} msgs are ingested with avg ingestion time {}".format(period_count,10/period_count)
			result = len(results)
			producer.send("report",value = msg)
		else:
			msg = "No msgs are ingested"
			producer.send("report",value = msg)
		print("msg from client {}".format(msg))
		

def init_cassandra(init,data):
	if init == 0:
		print("Start cassandra")
		start_connection()
		report_thread = threading.Thread(target=new_report)
		report_thread.start()
	return ingest_data(data, session)


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
		
	data_ingest = combine_data(select_statement,data)
	logging.info('Ingestion Start: {}'.format(data))
	start = datetime.datetime.now()
	results = execute_concurrent(session, statements_and_params,concurrency=100, raise_on_first_error=False)

	for (success, result) in results:
		if not success:
			logging.info('Ingestion Failed: {}'.format(data))

	logging.info('Ingestion Success: {}'.format(data))
	end_time = datetime.datetime.now()
	logging.info('Each msg takes {}'.format(end_time-start))
	return 1
		
def combine_data(select_statement,data):
    statements_and_params.append((select_statement,(str(data['App']),str(data['Translated_Review']),str(data['Sentiment']),str(data['Sentiment_Polarity']),str(data['Sentiment_Subjectivity']))))



