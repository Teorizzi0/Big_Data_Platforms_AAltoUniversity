# Deployment
### Steps

This code require docker and python3 (with pip) installed on the machine. Then in the docker-compose.yml is required to change the kafka host to its own 
host.

Then just follow the following steps:
1. `docker-compose up` 
2. `pip3 install -r ./requirements.txt` make sure all the python packages are installed

#### Batch Ingestion
1. `python3 app.py` 
2. test: `python3 fetchdataapp.py <userID> <clientapp>`
	- user1: `python3 fetchdataapp.py 1 locationapp`

	- user2: `python3 fetchdataapp.py 2 googleapp`

#### Stream Ingestion
1. `python3 streamingestmanager.py` 
2. test: `python3 streamingester.py <userID> <clientapp> <csv>`
	- user1: `python3 streamingtester.py 1 locationstreamapp ../data/client-input-directory/1/file.csv`

	- user2: `python3 streamingtester.py 2 googlestreamapp ../data/client-input-directory/2/file.csv`



