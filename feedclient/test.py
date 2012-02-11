import gevent
import sys
from gevent import monkey
monkey.patch_all()

import websocket
import thread
import time
import httplib

def on_message(ws, message):
    if message == '2::':
        ws.send(message)
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### opened ###"

def connect() :
    #websocket.enableTrace(True)
    conn  = httplib.HTTPConnection('localhost:8124')
    conn.request('POST','/socket.io/1/')
    resp  = conn.getresponse() 
    hskey = resp.read().split(':')[0]

    ws = websocket.WebSocketApp(
                            'ws://localhost:8124/socket.io/1/websocket/'+hskey,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.onopen = on_open
    ws.run_forever()

if __name__ == "__main__":
    c = int(sys.argv[1]) if len(sys.argv) >= 2 else 10
    gevent.joinall([gevent.spawn(connect) for _ in range(c)])
