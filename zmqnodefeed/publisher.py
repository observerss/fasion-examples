import zmq
import time

class Publisher:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:8101")

    def publish(self, msg):
        print 'message:'
        print msg
        self.socket.send(msg)
