from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from time import sleep
from json import dumps
import json
import logging
import threading

userID = sys.argv[1]
clientapp = sys.argv[2]
test_csv = sys.argv[3]


admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
topics = [] 
topics.append(NewTopic(name=clientapp,num_partitions=3,replication_factor=1))

try:
	admin_client.create_topics(new_topics=topics,validate_only=False)
except:
	print("Topic already created")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
def combine_message(row):
    data = {'userID' : userID, 'clientapp':clientapp,'data':json.loads(row.to_json())}
    producer.send(clientapp, value=data)
    print("send data {}".format(data))
    return(data)

df = pd.read_csv(test_csv)
df = df.dropna()
df.apply(lambda x: combine_message(x),axis = 1)
