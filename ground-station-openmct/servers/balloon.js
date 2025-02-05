// initialize all telemetry and position data to 0
let temp = undefined;
let pressure = undefined;
let humidity = undefined;
let x = undefined;
let y = undefined;
let z = undefined;
let lat = undefined;
let long = undefined;
let altitude = undefined;
let speed = undefined;
let num_sat = undefined;
let flight_state = undefined;
// keeps track of most updated endpoint number
let telCounter = 1;
let posCounter = 1;


// initialize all states to 0
function Balloon() {
    this.state = {
        "prop.temp": undefined,
        "prop.pressure": undefined,
        "prop.humidity": undefined,
        "prop.x_rotation": undefined,
        "prop.y_rotation": undefined,
        "prop.z_rotation": undefined,
        "prop.latitude": undefined,
        "prop.longitude": undefined,
        "prop.altitude": undefined,
        "prop.speed": undefined,
        "prop.num_sat": undefined,
        "prop.flight_state": undefined,
        "comms.recd": 0,
        "comms.sent": 0
    };
    // Pulls old data for the historical graph

    this.history = {};
    this.listeners = [];
    Object.keys(this.state).forEach(function (k) {
        this.history[k] = [];
    }, this);


    // Will pull data from django endpoints here and update the on graph based on interval
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
    // use fetch request here to call django endpoints using the counters to grab most recent data
    // currently, if the response is not valid, it will not error, so decrementing inside catch block does not work
    const fetch = require('node-fetch');

    fetch(`http://django:8000/data/tel/${telCounter}`)
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

    fetch(`http://django:8000/data/pos/${posCounter}`)
    .then (response => response.json())
    .then(data => {
        console.log(data);
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

// this will update all the states after data is pulled using endpoints
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
        if (this.state[id] != undefined) {
            let state = { timestamp: timestamp, value: this.state[id], id: id};
            this.notify(state);
            this.history[id].push(state);
            this.state["comms.sent"] += JSON.stringify(state).length;
        }

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