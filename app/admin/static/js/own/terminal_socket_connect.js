// Connect to the WebSocket server
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Function to send a command
function sendCommand() {
    var command = document.getElementById('command-input').value;
    if (command.trim() !== '') { // Check for empty input
        socket.emit('run_command', {data: command});
        document.getElementById('command-input').value = ''; // Clear the input
    }
}

// Listen for terminal output from the server
socket.on('command_output', function (msg) {
    var terminal = document.getElementById('terminal-output');
    terminal.innerHTML += '<p>' + msg.data + '</p>';
    terminal.scrollTop = terminal.scrollHeight; // Auto-scroll to the bottom
});

// Auf die Terminalausgabe vom Server hören
socket.on('command_output', function (msg) {
    var terminal = document.getElementById('terminal-output');
    terminal.innerHTML += '<p>' + msg.data + '</p>';
    terminal.scrollTop = terminal.scrollHeight; // Automatisches Scrollen nach unten
});