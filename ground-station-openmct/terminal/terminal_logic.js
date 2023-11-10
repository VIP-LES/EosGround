const terminal = document.getElementById("terminal");
const input = document.getElementById("input");
const form = document.getElementById("terminalForm");
let output = null
let output_pk = 1

setInterval(function() {
    fetch(`http://127.0.0.1:8000/data/terminalOutput/${output_pk}/`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        output = data.terminal_output;
    })
    .catch(error => {
      console.error('Failed to fetch data from endpoint:', error);
    })

    console.log(output)
    if (output) {
        terminal.innerHTML += `$ ${output}\n`;
        output_pk++;
    }
}, 3000);


form.addEventListener("submit", function (event) {
    event.preventDefault();
    const fullCommand = input.value;
    let ack = fullCommand.match(/(\d+)/)[0];
    ack = parseInt(ack)
    const command = fullCommand.replace(/ .*/,'');

    input.value = "";

    if (command === "clear") {
      terminal.innerHTML = "";
    } else if (command == "cutdown" || command == "ping") {
        terminal.innerHTML += `$ ${fullCommand}\n`;
        let response = fetch('http://127.0.0.1:8000/data/insertTransmitTable/', {
            method: 'POST',
            body: JSON.stringify({"input": command, "ack": ack})
        })
        .then((response) => response.json())
        .then((response) => {
          console.log(response);
          return response;
        })
        .then((response) => {
          terminal.innerHTML += `$ ${response.message + response.ack}\n`;
        })
        .catch(error => {
          console.error('Failed to fetch data from endpoint:', error);
        })
    } else {
      terminal.innerHTML += `Command not found: ${command}\n`;
    }

    terminal.scrollTop = terminal.scrollHeight - terminal.clientHeight;
});