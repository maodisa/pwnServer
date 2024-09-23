import socketio
from flask_socketio import emit
import subprocess  # To run system commands
from flask import render_template, Blueprint, emit

terminal = Blueprint('terminal', __name__, template_folder='templates')

@terminal.route('/')
def index():
    return render_template('terminal/index.html')


# Terminal route to run commands
@socketio.on('run_command')
def handle_command(data):
    command = data['data']
    try:
        # Run the command and get the output
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        output = f"Error: {str(e)}"

    # Send the command output back to the client
    emit('command_output', {'data': output})