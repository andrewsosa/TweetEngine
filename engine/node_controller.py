from EngineNode import EngineNode

#
# This controller needs to be attapted to place nodes on some arbitary
# server, not nessesarily hosted inside the this controller.
#

nodes = []

def getInput():
    return raw_input(">>> ").split()

def boundsDictToArray(bounds):
    return [bounds['west'], bounds['south'], bounds['east'], bounds['north']]

# dispatch [west,south,east,north]
def dispatch(args):

    # Core parameters
    bounds=dict(west=int(args[0]), south=int(args[1]), east=int(args[2]), north=int(args[3]))
    nodeID = str(bounds['west']) + "," + str(bounds['south'])

    # Check for existing node
    if(len(filter(lambda x: x['id'] == nodeID, nodes)) != 0):
        print "Node with ID " + nodeID + " already exists."
        return

    # Init node Entry
    node = dict(id=nodeID, bounds=bounds)

    # Extra params
    if len(args) >= 5:
        node['level'] = args[4]
    if len(args) >= 6:
        node['name'] = args[5]

    # Create and start Node
    orderedBounds = boundsDictToArray(bounds)

    node['node'] = EngineNode(orderedBounds)
    node['node'].start()

    # Store in list of nodes
    nodes.append(node)

def stopAll():
    for node in nodes:
        node['node'].stop()
        print "Stopped node " + node['id']

def nick(args):
    # args[0] : nodeID
    # args[1] : nickname

    node = filter(lambda x: x['id'] == args[0], nodes)[0]
    node['nick'] = args[1]

    print "Saved node with ID " + args[0] + " with nick: " + args[1]


if __name__ == "__main__":

    tokens = getInput()
    while(tokens[0]!="exit"):

        #try:
        #    if(tokens[0] == "dispatch"):
        #        dispatch(tokens[1:])
        #except:
        #    print "Invalid command: " + tokens[0]

        if(tokens[0] == "dispatch"):
            dispatch(tokens[1:])
        if(tokens[0] == "stopall"):
            stopAll()
        if(tokens[0] == "nick"):
            nick(tokens[1:])

        # Get new input and loop
        tokens = getInput()
