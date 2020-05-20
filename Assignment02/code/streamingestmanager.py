from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from time import sleep
from json import dumps
import json
import logging
import threading


customerAppNames = []
customerTopicNames = ['locationstreamapp','googlestreamapp']
logging.basicConfig(filename='../logs/ingeststream.log', filemode='w+',format='%(asctime)s - %(message)s', level=logging.INFO)

def call_clientstreamingapp(clientapp,data):
	global fun_to_call
	if clientapp not in customerAppNames:
		mod = __import__(clientapp)
		fun_to_call = getattr(mod, 'init_cassandra')
		customerAppNames.append(clientapp)
		fun_to_call(0,data)
	else:
		fun_to_call(1,data)

def kafka_stream_ingestion(appName):
	consumer = KafkaConsumer(appName, group_id = "client_streaming_group", bootstrap_servers='localhost:9092')
	for msg in consumer:
		data = json.loads(msg.value)
		call_clientstreamingapp(data['clientapp'],data['data'])

def report_reciever():
	admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
	print("report reciever thread created")
	consumer = KafkaConsumer('report', group_id = "client_streaming_group", bootstrap_servers='localhost:9092')
	for msg in consumer:
		logging.info("Manager recieve message {}".format(msg.value))

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    threads = []
    topics = []
    topics.append(NewTopic(name="report",num_partitions=3,replication_factor=1))
    try:
    	admin_client.create_topics(new_topics=topics,validate_only=False)
    except:
    	print("Topic already created")

    threads.append(threading.Thread(target = report_reciever))
    for topic in customerTopicNames:
	    for i in range(0,3):
		    print("Do before creating thread {}".format(i))
		    threads.append(threading.Thread(target=kafka_stream_ingestion, args=(topic,)))

    for thread in threads:
	    thread.start()


