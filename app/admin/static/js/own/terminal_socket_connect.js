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

// Eingabefeld auf Enter-Taste reagieren lassen
document.getElementById('command-input').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        sendCommand();
        event.preventDefault(); // Verhindert das Standardverhalten (z.B. Formularübermittlung)
    }
});

// Funktion zum Senden von Ctrl+C
document.addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.key === 'c') {
        socket.emit('run_command', {data: 'Ctrl+C'});
        event.preventDefault(); // Verhindert das Standardverhalten
    }
});
