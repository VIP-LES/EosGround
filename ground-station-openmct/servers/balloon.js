let temp = 0;
let pressure = 0;
let humidity = 0;
let x = 0;
let y = 0;
let z = 0;

function Balloon() {
    this.state = {
        "prop.temp": 77,
        "prop.pressure": 10,
        "prop.humidity": 23,
        "comms.recd": 0,
        "comms.sent": 0
    };
    this.history = {};
    this.listeners = [];
    Object.keys(this.state).forEach(function (k) {
        this.history[k] = [];
    }, this);

    setInterval(function () {
              this.pull();
      this.updateState();
      this.generateTelemetry();
    }.bind(this),
    3000
  );

  console.log("Graphs booting up!");
}

Balloon.prototype.pull = function () {
    const fetch = require('node-fetch');

    fetch('http://127.0.0.1:8000/data/1')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      temp = data.pk;
      pressure = data.packet;
      humidity = data.random_int;
    })
    .catch(error => {
      console.error('Failed to fetch data from endpoint:', error);
    });
};

Balloon.prototype.updateState = function () {
  this.state["prop.temp"] = temp;
  this.state["prop.pressure"] = pressure;
  this.state["prop.humidity"] = humidity;
};

/**
 * Takes a measurement of spacecraft state, stores in history, and notifies
 * listeners.
 */
Balloon.prototype.generateTelemetry = function () {
    var timestamp = Date.now(), sent = 0;
    Object.keys(this.state).forEach(function (id) {
        var state = { timestamp: timestamp, value: this.state[id], id: id};
        this.notify(state);
        this.history[id].push(state);
        this.state["comms.sent"] += JSON.stringify(state).length;
    }, this);
};

Balloon.prototype.notify = function (point) {
    this.listeners.forEach(function (l) {
        l(point);
    });
};

Balloon.prototype.listen = function (listener) {
    this.listeners.push(listener);
    return function () {
        this.listeners = this.listeners.filter(function (l) {
            return l !== listener;
        });
    }.bind(this);
};

module.exports = function () {
    return new Balloon()
};