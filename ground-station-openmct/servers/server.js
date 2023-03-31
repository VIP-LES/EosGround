var Spacecraft = require('./spacecraft');
var RealtimeServer = require('./realtime-server');
var StaticServer = require('./static-server');

var expressWs = require('express-ws');
var app = require('express')();
expressWs(app);

var spacecraft = new Spacecraft();
var realtimeServer = new RealtimeServer(spacecraft);
var staticServer = new StaticServer();

app.use('/realtime', realtimeServer);
app.use('/', staticServer);

var port = process.env.PORT || 8081

app.listen(port, function () {
    console.log('Open MCT hosted at http://localhost:' + port);
    console.log('Realtime hosted at ws://localhost:' + port + '/realtime');
});