let temp = 0;
let pressure = 0;
let humidity = 0;
let x = 0;
let y = 0;
let z = 0;
let lat = 0;
let long = 0;
let altitude = 0;
let speed = 0;
let num_sat = 0;
let flight_state = 0;
let telCounter = 1;
let posCounter = 1;

function Balloon() {
    this.state = {
        "prop.temp": 0,
        "prop.pressure": 0,
        "prop.humidity": 0,
        "prop.x_rotation": 0,
        "prop.y_rotation": 0,
        "prop.z_rotation": 0,
        "prop.latitude": 0,
        "prop.longitude": 0,
        "prop.altitude": 0,
        "prop.speed": 0,
        "prop.num_sat": 0,
        "prop.flight_state": 0,
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
    2000
  );

  console.log("Graphs booting up!");
}

Balloon.prototype.pull = function () {
    const fetch = require('node-fetch');

    fetch(`http://127.0.0.1:8000/data/tel/${telCounter}`)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      temp = data.temperature;
      pressure = data.pressure;
      humidity = data.humidity;
      x = data.x_rotation;
      y = data.y_rotation;
      z = data.z_rotation;
    })
    .catch(error => {
      console.error('Failed to fetch data from endpoint:', error);
      telCounter--;
    })
    telCounter++;

    fetch(`http://127.0.0.1:8000/data/pos/${posCounter}`)
    .then (response => response.json())
    .then(data => {
        lat = data.latitude;
        long = data.longitude;
        altitude = data.altitude;
        speed = data.speed;
        num_sat = data.num_satellites;
        flight_state = data.flight_state;
    })
    .catch(error => {
      console.error('Failed to fetch data from endpoint:', error);
      posCounter--;
    })
    posCounter++;
};

Balloon.prototype.updateState = function () {
  this.state["prop.temp"] = temp;
  this.state["prop.pressure"] = pressure;
  this.state["prop.humidity"] = humidity;
  this.state["prop.x_rotation"] = x;
  this.state["prop.y_rotation"] = y;
  this.state["prop.z_rotation"] = z;
  this.state["prop.latitude"] = lat;
  this.state["prop.longitude"] = long;
  this.state["prop.altitude"] = altitude;
  this.state["prop.speed"] = speed;
  this.state["prop.num_sat"] = num_sat;
  this.state["prop.flight_state"] = flight_state;
};

/**
 * Takes a measurement of spacecraft state, stores in history, and notifies
 * listeners.
 */
Balloon.prototype.generateTelemetry = function () {
    let timestamp = Date.now(), sent = 0;
    Object.keys(this.state).forEach(function (id) {
        let state = { timestamp: timestamp, value: this.state[id], id: id};
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