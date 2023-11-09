const terminal = document.getElementById("terminal");
const input = document.getElementById("input");
const form = document.getElementById("terminalForm");
const output = ""
let ack = 0

form.addEventListener("submit", function (event) {
    event.preventDefault();
    const command = input.value;
    input.value = "";

    if (command === "clear") {
      terminal.innerHTML = "";
    } else if (command == "cutdown" || command == "ping") {
        terminal.innerHTML += `$ ${command}\n`;
        let response = fetch('http://127.0.0.1:8000/data/insertTransmitTable/', {
            method: 'POST',
            body: JSON.stringify({input: command, ack: ack})
        })
        .then((response) => response.json())
        .then((response) => {
          console.log(response);
          return response;
        })
        .then((response) => {
          terminal.innerHTML += `$ ${response.message}\n`;
        })
        .catch(error => {
          console.error('Failed to fetch data from endpoint:', error);
        })
        ack = (1+ack)%256
    } else {
      terminal.innerHTML += `Command not found: ${command}\n`;
    }

    terminal.scrollTop = terminal.scrollHeight - terminal.clientHeight;
});