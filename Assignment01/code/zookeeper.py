from kazoo.client import KazooClient
from kazoo.client import KazooState


zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

#----------------------It can be useful to know when the Zookeeper session has expired--------------------------
def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
    else:
        # Handle being connected/reconnected to Zookeeper

zk.add_listener(my_listener)

# ---------------------Now I create a node on Zookeeper----------------------------------------------------

# Ensure a path, create if necessary
zk.ensure_path("/test")

#Push file
zk.create("/test/node1", "/usr/config.yaml")


