const terminal = document.getElementById("terminal");
const input = document.getElementById("input");

input.addEventListener("keydown", function (event) {
if (event.key === "Enter") {
  event.preventDefault();
  const command = input.value;
  input.value = "";

  terminal.innerHTML += `$ ${command}\n`;

  if (command === "clear") {
    terminal.innerHTML = "";
  } else if (command === "cutdown") {
    terminal.innerHTML += "success\n";
  } else {
    terminal.innerHTML += `Command not found: ${command}\n`;
  }

  terminal.scrollTop = terminal.scrollHeight - terminal.clientHeight;
}
});