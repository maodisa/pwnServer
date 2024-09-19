import os
import subprocess
from flask import Flask, render_template, request, redirect
import yaml

# Pfad zur Konfigurationsdatei
config_path = "./config.yaml"

# Funktion zum Laden der Konfiguration
def load_config():
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Webserver (Flask) einrichten
app = Flask(__name__)

# Lade Konfiguration
config = load_config()

# Verzeichnis, in dem die Payloads gespeichert sind
payload_dir = "./payloads"

# Funktion zur Ausführung der Duckyscript-Payload
def run_duckyscript(file_path):
    with open(file_path, "r") as file:
        payload = file.read()
    with open("/tmp/payload.txt", "w") as tmp_file:
        tmp_file.write(payload)
    subprocess.run(["bash", "./run_payload.sh"])

# Route für die Hauptseite des Webinterfaces
@app.route('/')
def index():
    # Liste der gespeicherten Payloads laden
    payload_files = os.listdir(payload_dir)
    payloads = [f for f in payload_files if f.endswith('.txt')]
    return render_template('templates/index.html', payloads=payloads)

# Route für das Ausführen von Payloads
@app.route('/execute', methods=['POST'])
def execute_payload():
    payload = request.form['payload']
    run_duckyscript(payload)
    return redirect('/')

# Route für das Ausführen eines gespeicherten Payloads
@app.route('/execute_saved/<filename>', methods=['POST'])
def execute_saved_payload(filename):
    file_path = os.path.join(payload_dir, filename)
    run_duckyscript(file_path)
    return redirect('/')

# Route zum Hochladen und Speichern von Payloads
@app.route('/upload', methods=['POST'])
def upload_payload():
    payload = request.form['payload']
    filename = request.form['name'] + ".txt"
    with open(os.path.join(payload_dir, filename), "w") as file:
        file.write(payload)
    return redirect('/')

# Webserver starten
if __name__ == '__main__':
    # Starte Hotspot
    os.system(f"nmcli dev wifi hotspot ifname wlan0 ssid {config['SSID']} password {config['Password']}")
    app.run(host="0.0.0.0", port=80)
