## Part 3

First of all, a Docker Zookeeper image must be pulled: 
 ```
docker pull zookeeper
 ```
 
 Then run Zookeeper server: 
 ```
  docker run -it --rm --link some-zookeeper:zookeeper zookeeper zkCli.sh -server zookeeper
  ```
  
  Now Zookeeper should be works, so we use the python script to publish into zookeeper the service information. To do this I used Kazoo: it is a Python library designed to make working with Zookeeper in a more handly experience. 

To install Kazoo:
```
pip3 install kazoo
```
Finally running the [zookeeper.py](https://github.com/Teorizzi0/assignment-01-808914/blob/master/code/zookeeper.py) from the terminal in which there is: connection, listener, creation of a node and file push.
