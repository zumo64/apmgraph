from random import randint,gauss

import graph
from datetime import datetime,timezone
import threading
import time
import uuid
import lorem

from elasticapm import Client


class Transactionthread(threading.Thread):
    # Transaction starts
    # g.get_vertex('A')
    def __init__(self, g, starting_vertex, loop_mode=False, run_for=10, time_out=60):
        threading.Thread.__init__(self)
        self.graph = g
        self.starting_vertex = starting_vertex
        self.loop_mode = loop_mode
        self.current_vertex = g.get_vertex(self.starting_vertex)
        self.uid = uuid.uuid1()
        self.step = 0
        #print("Init ", self.current_vertex.name)
        self.start_time = time.time()
        self.transaction_timeout = time_out
        self.run_for = run_for
        self.f = open("events.log", "a+")
        self.state = "ACTIVE"
        self.date_on_hold = None
#       self.client = Client({'Graph-services': 'test-graph'})

    def run(self):
        while True:
            self.step += 1
            current_time = time.time()
            # Check Health of Service
            # Wake up ON_HOLD transactions
            # Log Start Service
            if self.current_vertex.state == "OK":
                self.state = "ACTIVE"
                #self.log_event("Start " + self.current_vertex.name)
                self.log_event(None)
                self.processing_service()
                self.step += 1
                self.log_event(None)

            elif self.current_vertex.state == "FAILED":
                if self.state == "ACTIVE":
                    self.state = "ON_HOLD"
                    self.date_on_hold = current_time
                    continue
                elif self.state == "ON_HOLD":
                    time_on_hold = current_time - self.date_on_hold
                    if time_on_hold > self.transaction_timeout:
                        # print("transaction timed out")
                        time_run = current_time - self.start_time
                        # Go beck to the starting point
                        if self.loop_mode and (time_run < self.run_for):
                            self.step = 0
                            self.current_vertex = self.graph.get_vertex(self.starting_vertex)
                            # reset transaction start time and uuid
                            self.uid = uuid.uuid1()
                            continue
                        else:
                            break

            if self.current_vertex.is_final:
                #self.log_event("End Transaction")
                #self.client.end_transaction(self.uid, "OK")

                # Check end of time reached
                time_run = current_time - self.start_time
                # restart  starting point
                if self.loop_mode and (time_run < self.run_for):

                    # reset transaction start time and uuid
                    self.current_vertex = self.graph.get_vertex(self.starting_vertex)
                    self.step = 0
                    self.uid = uuid.uuid1()
                    time.sleep(10)
                    # self.start_time = time.time()
                    # print("Restarting ..")
                    continue

                else:
                    # print("Transaction Ending ..", self.uid)
                    #self.client.end_transaction(self.uid, "Success")
                    break
            else:
                # Go to next Vertex
                time.sleep(0.22)
                n = self.graph.get_neighbours_of(self.current_vertex)
                if n is not None:
                    length = len(n)
                    next_index = 0
                    if length > 0:
                        next_index = randint(0, length-1)
                    #self.log_event("End " + self.current_vertex.name)
                    self.current_vertex = self.graph.get_vertex(n[next_index])
                else:
                    #self.client.end_transaction(self.uid, "NOK")
                    break

    def processing_service(self):
        st = gauss(self.current_vertex.service_time, self.current_vertex.service_time/10)
        time.sleep(st)
        return

    def log_event(self, message):
        if message is None:
            log_details = {
                #'timestamp': datetime.now(tz=timezone.utc).isoformat(),
                'timestamp': datetime.now().isoformat(),
                'message': lorem.sentence(),
                'log_level': "INFO",
                'step': self.step,
                'flow_name': 'Order Flow',
                'service_name': self.current_vertex.name,
                'transaction_uid': self.uid
            }
        else:
            log_details = {
                #'timestamp': datetime.now(tz=timezone.utc).isoformat(),
                'timestamp': datetime.datetime.now().isoformat(),
                'message': message,
                'log_level': "INFO",
                'step': self.step,
                'flow_name': 'Order Flow',
                'service_name': self.current_vertex.name,
                'transaction_uid': self.uid
            }
        # create log string
        log = "%s|%s|%s|%s|%s|%s|%s\n" % (
            log_details['timestamp'],
            log_details['log_level'],
            log_details['step'],
            log_details['transaction_uid'],
            log_details['message'],
            log_details['service_name'],
            log_details['flow_name']
        )

        self.f.write(log)
        self.f.flush()


    def close(self):
        # close file once finished processing
        self.f.close()


