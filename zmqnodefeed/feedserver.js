var express = require('express')
var app = express.createServer();
var io = require('socket.io').listen(app);

app.listen(8124);

/* express with http requests */
app.use(app.router);
app.use(express.static(__dirname));

app.get('/', function(req, res){
    res.send('<h1>Please visit <a href="/playbyplay.html">PlayByPlay</a> Page</h1>')
});


/* node.js + io.sockets */
io.sockets.on('connection', function (socket) {
    // we don't do any message handling
});


/* now we play with zeromq and publisher */
var context = require('zmq');
var subscriber = context.socket('sub');
subscriber.subscribe('');

subscriber.on('message', function(data) {
    console.log("message: ",data.toString());
    // send message to iosocket clients
    io.sockets.emit('playbyplay',data.toString());
});

subscriber.connect('tcp://localhost:8101')
