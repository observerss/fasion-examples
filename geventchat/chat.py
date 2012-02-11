#!/usr/bin/env python

from gevent import monkey; monkey.patch_all()
from socketio import SocketIOServer


class Application(object):
    def __init__(self):
        self.buffer = []
        self.cache = {
            'nicknames': set()
        }

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].strip('/')

        if not path:
            start_response('200 OK', [('Content-Type', 'text/html')])
            return ['<h1>Welcome. Try the <a href="/chat.html">chat</a> example.</h1>']

        if path in ['socket.io.js', 'chat.html', 'stylesheets/style.css', 'WebSocketMain.swf']:
            try:
                data = open(path).read()
            except Exception:
                return not_found(start_response)

            if path.endswith(".js"):
                content_type = "text/javascript"
            elif path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".swf"):
	        content_type = "application/octect-stream"
            else:
                content_type = "text/html"

            start_response('200 OK', [('Content-Type', content_type)])
            return [data]

        if path.startswith("game"):
            socketio = environ['socketio']

            if socketio.session is None:
                return []

            while True:
                message = socketio.receive()

		# Connection closed
		if message is None:
		    break

                print message

                if message['type'] == "event":
                    self.handle_event(message, socketio)
		if message['type'] == "message":
		    socketio.send("3:::" + message['data'])
        else:
            return not_found(start_response)

    def handle_event(self, message, socketio):
        if message['name'] == "nickname":
            nickname = message['args'][0]
            socketio.session.nickname = nickname

            self.cache['nicknames'].add(nickname)

            socketio.ack(message['id'], [False])
            socketio.broadcast_event("announcement", "%s connected" % nickname)
            socketio.broadcast_event("nicknames", list(self.cache['nicknames']), include_self=True)

        elif message['name'] == "user message":
            socketio.broadcast_event("user message", socketio.session.nickname, message['args'][0])


def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']


if __name__ == '__main__':
    print 'Listening on port 8124 and on port 843 (flash policy server)'
    SocketIOServer(('0.0.0.0', 8124), Application(), namespace="game", policy_server=True).serve_forever()
