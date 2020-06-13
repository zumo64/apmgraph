

import graph
import datetime
import threading
import time
from random import random



class Eventthread(threading.Thread):


    def __init__(self, g):
        threading.Thread.__init__(self)
        self.graph = g
        self.setDaemon(True)

    def run(self):
        while True:
            time.sleep(10)

            # Loop the nodes
            vertices = list(self.graph.vertices.values())
            for a_vertex in vertices:
                rnd = random()
                # don't fail Terminal Nodes

                if a_vertex.state == "OK":
                    if rnd <= a_vertex.p_fail:
                        a_vertex.state = "FAILED"
                        print(a_vertex.name, "failed at ", datetime.datetime.now().isoformat())
                elif a_vertex.state == "FAILED":
                    if rnd <= a_vertex.p_recovery:
                        a_vertex.state = "OK"
                        a_vertex.p_recovery = a_vertex.p_fail
                        print(a_vertex.name, "recovery at ", datetime.datetime.now().isoformat())
                    else:
                        # increase chance of recovery
                        a_vertex.p_recovery *= 1.2



        print("Stopped event Thread")


