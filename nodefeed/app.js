var io = require('socket.io').listen(8124);
    
// send helloworld to every client every 5 sec
setInterval(function(){
   io.sockets.emit('hello','Hello World!')
},5000);

io.sockets.on('connection', function (socket) {
    // we don't do any message handling
});
