let Balloon = require('./balloon');
let RealtimeServer = require('./realtime-server');
let HistoryServer = require('./history-server');
let StaticServer = require('./static-server');

let expressWs = require('express-ws');
let app = require('express')();
expressWs(app);

let balloon = new Balloon();
let realtimeServer = new RealtimeServer(balloon);
let historyServer = new HistoryServer(balloon);
let staticServer = new StaticServer();

app.use('/realtime', realtimeServer);
app.use('/history', historyServer);
app.use('/', staticServer);

let port = process.env.PORT || 8081

app.listen(port, function () {
    console.log('Open MCT hosted at http://localhost:' + port);
});