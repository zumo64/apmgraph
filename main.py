import transactionthread
import graph
import time
import datetime
import threading
import yaml
import eventthread
import sys


file = open("tree.yml", "r")
yaml_graph = yaml.safe_load(file)

# Create the graph
# Load config into Graph
g = graph.Graph()
g.load_yaml(yaml_graph)

g.print_graph()

max_threads = yaml_graph['simpleGraph']['max_threads']
timeout = yaml_graph['simpleGraph']['transaction_timeout']
run_for = yaml_graph['simpleGraph']['run_for']
auto_loop = yaml_graph['simpleGraph']['auto_loop']
start_v = yaml_graph['simpleGraph']['start_vertex']

start_time = time.time()
transactionPool = []
print("Starting at ", datetime.datetime.now().isoformat())

for i in range(0, max_threads):
    transactionPool.append(transactionthread.Transactionthread(g, start_v, auto_loop, run_for, timeout))
    transactionPool[i].start()
    time.sleep(.250)

events = eventthread.Eventthread(g)
events.start()

while threading.active_count() > 2:
    now = time.time()
    print(" *** nb transactions ", threading.active_count()-2," elapsed ", round(now - start_time))
    time.sleep(5)

for i in range(0, max_threads):
    transactionPool[i].close()

now = time.time()
print("Ending simulation.."," elapsed ", round(now - start_time))


sys.exit()