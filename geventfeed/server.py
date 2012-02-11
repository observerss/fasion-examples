import traceback
import threading
import time
import random
from gevent import monkey; monkey.patch_all()
from socketio import SocketIOServer

class Application(object):
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')
        if path.startswith("socket.io"):
            return []
        else:
            start_response('404 Not Found', [])
            return ['<h1>Not Found</h1>']

class FeedGenerater(threading.Thread):
    def __init__(self, server, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.server = server
       
    def run(self):
        while True:
            time.sleep(5)
            for key, session in server.sessions.iteritems():
                print "### send %s:Hello World ###" % repr(key)
                session.put_client_msg({'hello':'Hello World!'})

app = Application()

if __name__ == "__main__":
    server = SocketIOServer(('', 8124), app, namespace="socket.io")
    FeedGenerater(server).start()
    server.serve_forever()
            
