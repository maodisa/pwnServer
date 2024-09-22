import os
import subprocess
from flask import render_template, Blueprint, request, redirect, url_for
from app.admin.python.ducky_script.ducky import execute_payload

core = Blueprint('core', __name__, template_folder='templates')

# Speicherort für die Payloads
payload_dir = "app/admin/static/payloads/duckyScript"

# Funktion zur Ausführung der Duckyscript-Payload
def run_duckyscript(file_path):
    # Die execute_payload Funktion aus ducky.py aufrufen
    execute_payload(file_path)

@core.route('/')
def index():
    # Liste der gespeicherten Payloads laden
    payload_files = os.listdir(payload_dir)
    payloads = [f for f in payload_files if f.endswith('.txt')]
    return render_template('core/index.html', payloads=payloads)

# Route für das Ausführen von Payloads
@core.route('/execute', methods=['POST'])
def execute_payload_route():
    payload = request.form['payload']
    file_path = os.path.join(payload_dir, payload)
    run_duckyscript(file_path)
    return redirect('/')

# Route für das Ausführen eines gespeicherten Payloads
@core.route('/execute_saved/<filename>', methods=['POST'])
def execute_saved_payload(filename):
    file_path = os.path.join(payload_dir, filename)
    run_duckyscript(file_path)
    return redirect('/')

# Route zum Hochladen und Speichern von Payloads
@core.route('/upload', methods=['POST'])
def upload_payload():
    payload = request.form['payload'].strip()  # Entfernt führende und nachfolgende Leerzeichen/Tabs
    filename = request.form['name'] + ".txt"
    with open(os.path.join(payload_dir, filename), "w") as file:
        file.write(payload)
    return redirect('/')

# Route zum Bearbeiten einer Payload
@core.route('/edit/<filename>', methods=['GET'])
def edit_payload(filename):
    file_path = os.path.join(payload_dir, filename)
    with open(file_path, "r") as file:
        edit_payload = file.read()

    # Lade alle gespeicherten Payloads und schalte in den Bearbeitungsmodus
    payload_files = os.listdir(payload_dir)
    payloads = [f for f in payload_files if f.endswith('.txt')]

    # Render mit aktiviertem Bearbeitungsmodus
    return render_template('core/index.html',
                           payloads=payloads,
                           edit_mode=True,
                           edit_payload=edit_payload,
                           edit_payload_name=filename)

# Route zum Speichern der bearbeiteten Payload
@core.route('/update/<filename>', methods=['POST'])
def update_payload(filename):
    payload = request.form['payload'].strip()  # Entfernt führende und nachfolgende Leerzeichen/Tabs
    file_path = os.path.join(payload_dir, filename)
    with open(file_path, "w") as file:
        file.write(payload)
    return redirect('/')

# Route zum Löschen eines Payloads
@core.route('/delete/<filename>', methods=['POST'])
def delete_payload(filename):
    file_path = os.path.join(payload_dir, filename)

    if os.path.exists(file_path):
        os.remove(file_path)  # Löscht die Datei

    return redirect('/')
