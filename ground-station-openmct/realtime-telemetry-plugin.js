function RealtimeTelemetryPlugin() {
    return function (openmct) {
        let socket = new WebSocket(location.origin.replace(/^http/, 'ws') + '/realtime/');
        let listener = {};

        socket.onmessage = function (event) {
            point = JSON.parse(event.data);
            if (listener[point.id]) {
                listener[point.id](point);
            }
        };

        let provider = {
            supportsSubscribe: function (domainObject) {
                return domainObject.type === 'EOS';
            },
            subscribe: function (domainObject, callback) {
                listener[domainObject.identifier.key] = callback;
                socket.send('subscribe ' + domainObject.identifier.key);
                return function unsubscribe() {
                    delete listener[domainObject.identifier.key];
                    socket.send('unsubscribe ' + domainObject.identifier.key);
                };
            }
        };

        openmct.telemetry.addProvider(provider);
    }
}