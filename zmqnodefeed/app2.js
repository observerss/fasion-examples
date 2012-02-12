var io = require('socket.io').listen(8124);

var context = require('zmq');
var subscriber = context.socket('sub');
subscriber.subscribe('');

subscriber.on('message', function(data) {
    console.log("message: ",data.toString());
    // send message to iosocket clients
    io.sockets.emit('hello',data.toString());
});

io.sockets.on('connection', function (socket) {
    // we don't do any message handling
});

subscriber.connect('tcp://localhost:8101')
