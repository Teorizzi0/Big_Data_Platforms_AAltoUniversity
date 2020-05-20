# Constraints and input for the assignment	

The big data platform, **mysimbdp**, have the following components:
* **mysimbdp-coredms**: MongodDB (Atlas)
* **mysimbdp-daas**: Apache Kafka Connect (Debezium)
* **mysimbdp-dataingest**:  Apche Kafka

Regarding the dataset, I have chosen the Google PlayStore one: 

[Google PlayStore Dataset](https://github.com/Teorizzi0/assignment-01-808914/tree/master/data/googleplaystore.csv).

Finally, as programming language, I have chosen **Python**.


## Part 1: Design

**1.1**

MongoDB and Apache Kafka® have become the heart of many modern big data architectures today. 
Kafka is integrated with an external system like MongoDB through the use of Kafka Connect, in particular Debezium which is a 'source connector' deployed via Kafka Connect. This connector enables users to leverage ready-to-use components that can stream data from external systems into Kafka topics, as well as stream data from Kafka topics into external systems. Talking about Debezium's MongoDB connector, it can monitor a MongoDB replica set or a MongoDB sharded cluster for document changes in databases and collections, recording those changes as events in Kafka topics. Then, the connector handles the addition or removal of shards in a sharded cluster, changes in membership of each replica set, elections within each replica set, and awaiting the resolution of communications problems.
The Debezium MongoDB connector is not capable of monitoring the changes of a standalone MongoDB server, since standalone servers do not have an oplog. Therefore, as written in Part 1, I need at least a replica-set with three nodes because the connector works only with MongoDB replica sets or with sharded clusters where each shard is a separate replica set. In the Part 2, I will explain better how I would design the sharding in a real situation (with an economic support).

In the following diagram, the interactions between main components is better explained: 

![Collaboration among MongoDB-KafkaConnector-Kafka](https://github.com/Teorizzi0/assignment-01-808914/blob/master/reports/mongo_kafka_mongo.png)


**1.2**

The easiest and fastest way to spin up a MongoDB database is to use the MongoDB service [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). No more troubles with provisioning servers, writing config files, and deploying replica set but simply pick a cloud provider, a cluster size, and get a connection string. 
In MongoDB a crucial part is the replica_dataset. It is a group of mongod processes that maintain the same data set. Replication provides redundancy and increases data availability. With multiple copies of data on different database servers, replication provides a level of fault tolerance against the loss of a single database server. In Atlas I had to select the number (3, 5 or 7) and the location of the replicas because the tool provides checks for the selected cross-regional configuration during partial or whole regional outages. To ensure availability during a full region outage, I need at least one node in three different regions. Otherwise during a partial region outage, I should have at least 3 nodes in a region or at least 3 nodes across at least 2 regions.


**1.3**

In this first assignment, I went for a container over VMs basically because I use technologies with a long configuration process (e.g. Debezium, Kafka, Zookeeper) built by different steps. So, using a container (docker), I can have a simplify deployment, in fact, the container technology allows me to "package" the work environment in a single component which can be run in a single code line.


**1.4**

Regarding the question "how would I scale mysimbdp to allow users using this platform?", I can answer showing the following diagram in which different potential users, with different data sources, could push data using specific Debezium kafka connector according to the type of data source. In fact, Debezium’s goal is to build up a library of connectors that capture changes from a variety of DBMSes and produce events with very similar structures, making it far easier for an applications to consume and respond to the events regardless of where the changes originated.

![Collaboration among MongoDB-KafkaConnector-Kafka](https://github.com/Teorizzi0/assignment-01-808914/blob/master/reports/different_input.png)


**1.5**

As industrial cloud infrastructure, I have chosen Google Cloud Platform because it offers fully-support to Atlas MongoDB. Recently, GCP integrated MongoDB Atlas into his platform. They made significant enhancements to the experience for the customers through several integrations:

-   Unified billing;
-   Integrations to better protect and manage data: MongoDB Atlas now works with Cloud Key Management Service (KMS), which allows to better manage sensitive data in MongoDB Atlas on GCP.
-   Scaling globally: MongoDB Atlas is now supported in all 20 Google Cloud regions, so it is possible to scale easily with lower-latency reads and writes for better user performance.



## Part 2 - Development and deployment


**2.1** 

The data structure of mysimbdp-coredms is quite simple: I have a database called **googleplaystore** and a collection called **segment**. Inside it, there are as many documents as many "app reviews" in the selected dataset. 
Regarding the documents, they have the following .json structure:

``` 
  {
    "App": "Photo Editor & Candy Camera & Grid & ScrapBook",
    "Category": "ART_AND_DESIGN",
    "Rating": 4.1,
    "Reviews": 159,
    "Size": "19M",
    "Installs": "10,000+",
    "Type": "Free",
    "Price": 0,
    "Content Rating": "Everyone",
    "Genres": "Art & Design",
    "Last Updated": "January 7, 2018",
    "Current Ver": "1.0.0",
    "Android Ver": "4.0.3 and up"
  }
``` 


**2.2**

The partition in MongoDB is done through the **sharding**.
Sharding is a method for distributing data across multiple machines. MongoDB uses sharding to support deployments with very large data sets and high throughput operations. 
Unfortunately, MongoDB Atlas does not allow sharding for free. By the way, I can figure out how I would build a real BDP: I would apply the **Horizontal scaling** which divides the system dataset over multiple servers, adding additional servers to increase capacity as required. In this way, the overall speed or capacity of a single machine may not be high, each machine handles a subset of the overall workload, potentially providing better efficiency than a single high-speed high-capacity server. Depending on the numbers of writing/reading operations I would decide the number of shards, each one built by at least 3 nodes (due to the written-above reasons). MongoDb Atlas supports three types of sharding policy: range-based sharding, hash-based sharding, location-aware sharding. According to the dataset we have, I would use a **range-based sharding** because documents are partitioned across shards according to the shard key value. Therefore, documents with shard key values close to one another are co-located on the same shard. This approach should be useful because the google play store dataset lands iteself (due to cardinality reasons) to a division according to particular values like rating, price, category and so on. 


**2.3**

In this section. I was asked to write a kind of data-ingest that takes data from the selected sources and stores the data into **mysimpdp**. 
I am not sure to have completely understood the question, but I wrote anyway a python script that, first, takes the whole csv dataset, then convert it in a kind of json format and finnally, upload it into the MongoDB Connection (through my own Atlas connection key).

[Python Script to Upload the Dataset](https://github.com/Teorizzi0/assignment-01-808914/tree/master/code/storedataset.py)
 

**2.4**

First of all, I created multiple users in MongoDB Atlas to check the uploading performance. These users have write/read privileges because I need to check the performance both in writing and in reading. 

![Users Atlas](https://github.com/Teorizzi0/assignment-01-808914/blob/master/reports/usersatlas.png)

Then I wrote a [Python Script](https://github.com/Teorizzi0/assignment-01-808914/tree/master/code/one_user.py) for each user (using their own MongoDB Atlas Key) in which a single document is uploaded into the collection. I have run 1, 2, 3, 5, 10, 30, 50, 100 and 500 concurrent uploading in order to evaluate the performance in each situation. At the end, I checked the result in the overview page of the Atlas' collection:

![Uploading performance in Atlas](https://github.com/Teorizzi0/assignment-01-808914/blob/master/reports/performance.png)

Here the results:

| Concurrent  operations 	| AVG rate of inserts 	|
|------------------------	|:-------------------:	|
| 1                      	| 0.03/s              	|
| 2                      	| 0.05/s              	|
| 3                      	| 0.06/s              	|
| 5                      	| 0.06/s              	|
| 10                     	| 0.08/s              	|
| 30                     	| 0.5/s               	|
| 50                     	| 1.17/s              	|
| 100                    	| 1.34/s              	|
| 500                    	| 1.52/s              	|



**2.5**

The performance is quite good even with 500 concurrent uploading-operations.
I didn't found any problems of consistency, but I expected the above results because MongoDB allows multiple clients to read and write the same data. To ensure consistency, it uses reader-writer locks. In this way, it prevents multiple clients from modifying the same piece of data simultaneously. Therefore, all writes to a single document occur either in full or not at all. 



## Part 3 - Extension with discovery


**3.1**

If different users need a dedicated server, Zookeeper will play a crucial role in the system. It is a centralized service for maintaining configuration information, naming and providing distributed synchronization. In the following schema, you can see how I figure out a hypothetical system under the above conditions: 

![Zookeeper System](https://github.com/Teorizzi0/assignment-01-808914/blob/master/reports/zookeeper_schema.png)

**3.2**

This section is in the [Deployment Document](https://github.com/Teorizzi0/assignment-01-808914/blob/master/reports/Assignment-01-Deployment.md).


**3.3**


If I was asked to change the implementation of mysimbdp-dataingest to integrate a service discovery feature, probably I will use the PyDiscover library of Python. It is composed by client and server:
* Server listens for multicast clients request in the port 50000 (by default);
* Clients send requests using a multicast address to the port 50000.

Client and server must transmit information in the same virtual channel which is a pre-shared word that server/client known. Only messages with this word will be attended, performing the "virtual channel".

I would follow [this GitHub repository](https://github.com/cr0hn/PyDiscover) to implement it. 


**3.4**



**3.5**

