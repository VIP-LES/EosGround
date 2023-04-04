function Spacecraft() {
    this.state = {
        "prop.fuel": 77,
        "prop.thrusters": "OFF",
        "comms.recd": 0,
        "comms.sent": 0,
        "pwr.temp": 245,
        "pwr.c": 8.15,
        "pwr.v": 30
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
    1000
  );

  console.log("Example spacecraft launched!");
  console.log("Press Enter to toggle thruster state.");

  process.stdin.on(
    "data",
    function () {
      this.state["prop.thrusters"] =
        this.state["prop.thrusters"] === "OFF" ? "ON" : "OFF";
      this.state["comms.recd"] += 32;
      console.log("Thrusters " + this.state["prop.thrusters"]);
      this.generateTelemetry();
    }.bind(this)
  );
}

Spacecraft.prototype.pull = function () {
  const http = require("http");

  const options = {
    hostname: "127.0.0.1",
    port: 8000,
    path: "/data",
    method: "GET",
  };

  const req = http.request(options, (res) => {
    let data = "";

    res.on("data", (chunk) => {
      data += chunk;
    });

    res.on("end", () => {
      // Parse the data into a JavaScript object or other data type
      const parsedData = JSON.parse(data);

      // Do something with the parsed data
      pos = parsedData.pos;
      vel = parsedData.vel;
      acc = parsedData.acceleration;
    });
  });

  req.on("error", (error) => {
    console.error(error);
  });

  req.end();
};

Spacecraft.prototype.updateState = function () {
  this.state["prop.fuel"] = pos;
  this.state["pwr.temp"] = vel;
  this.state["pwr.v"] = acc;
  if (this.state["prop.thrusters"] === "ON") {
    this.state["pwr.c"] = 8.15;
  } else {
    this.state["pwr.c"] = this.state["pwr.c"] * 0.985;
  }
};

/**
 * Takes a measurement of spacecraft state, stores in history, and notifies
 * listeners.
 */
Spacecraft.prototype.generateTelemetry = function () {
    var timestamp = Date.now(), sent = 0;
    Object.keys(this.state).forEach(function (id) {
        var state = { timestamp: timestamp, value: this.state[id], id: id};
        this.notify(state);
        this.history[id].push(state);
        this.state["comms.sent"] += JSON.stringify(state).length;
    }, this);
};

Spacecraft.prototype.notify = function (point) {
    this.listeners.forEach(function (l) {
        l(point);
    });
};

Spacecraft.prototype.listen = function (listener) {
    this.listeners.push(listener);
    return function () {
        this.listeners = this.listeners.filter(function (l) {
            return l !== listener;
        });
    }.bind(this);
};

module.exports = function () {
    return new Spacecraft()
};