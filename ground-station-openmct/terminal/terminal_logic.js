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
    const fullCommand = input.value; //stores the user input in fullCommand
    input.value = "";

    if (fullCommand === "clear") {
      terminal.innerHTML = "";
    }

    terminal.innerHTML += `$ ${fullCommand}\n`;
    let response = fetch('http://127.0.0.1:8000/data/insertTransmitTable/', {
        method: 'POST',
        body: JSON.stringify({"input": fullCommand})
    })
    .then((response) => response.json())
    .then((response) => {
      console.log(response);
      return response;
    })
    .then((response) => {
        if (response.ack !== undefined) {
            terminal.innerHTML += `$ ${response.message + response.ack}\n`;
        }
    })
    .catch(error => {
      console.error('Failed to fetch data from endpoint:', error);
    })


    terminal.scrollTop = terminal.scrollHeight - terminal.clientHeight;
});