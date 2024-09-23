import os
from flask import render_template, Blueprint, request, redirect
from app.admin.python.ducky_script.ducky import execute_payload

badUSB = Blueprint('badUSB', __name__, template_folder='templates')

# Speicherort für die Payloads
payload_dir = "app/admin/static/payloads/duckyScript"


# Funktion zur Ausführung der Duckyscript-Payload
def run_duckyscript(file_path, layout):
    # Die execute_payload Funktion aus ducky.py aufrufen
    execute_payload(file_path, layout)


@badUSB.route('/')
def index():
    # Liste der gespeicherten Payloads laden
    payload_files = os.listdir(payload_dir)
    payloads = [f for f in payload_files if f.endswith('.txt')]
    return render_template('badUSB/index.html', payloads=payloads)


# Route zum Hochladen und Speichern von Payloads
@badUSB.route('/upload', methods=['POST'])
def upload_payload():
    payload = request.form['payload'].strip()  # Entfernt führende und nachfolgende Leerzeichen/Tabs
    filename = request.form['name'] + ".txt"
    with open(os.path.join(payload_dir, filename), "w") as file:
        file.write(payload)
    return redirect('/')


# Route zum Bearbeiten einer Payload
@badUSB.route('/edit/<filename>', methods=['GET'])
def edit_payload(filename):
    file_path = os.path.join(payload_dir, filename)
    with open(file_path, "r") as file:
        edit_payload = file.read()

    # Lade alle gespeicherten Payloads und schalte in den Bearbeitungsmodus
    payload_files = os.listdir(payload_dir)
    payloads = [f for f in payload_files if f.endswith('.txt')]

    # Render mit aktiviertem Bearbeitungsmodus
    return render_template('badUSB/index.html',
                           payloads=payloads,
                           edit_mode=True,
                           edit_payload=edit_payload,
                           edit_payload_name=filename)


# Route zum Speichern der bearbeiteten Payload
@badUSB.route('/update/<filename>', methods=['POST'])
def update_payload(filename):
    payload = request.form['payload'].strip()  # Entfernt führende und nachfolgende Leerzeichen/Tabs
    file_path = os.path.join(payload_dir, filename)
    with open(file_path, "w") as file:
        file.write(payload)
    return redirect('/')


# Route zum Löschen eines Payloads
@badUSB.route('/delete/<filename>', methods=['POST'])
def delete_payload(filename):
    file_path = os.path.join(payload_dir, filename)

    if os.path.exists(file_path):
        os.remove(file_path)  # Löscht die Datei

    return redirect('/')


# Neue Route zum Ausführen des ausgewählten Payloads
@badUSB.route('/execute_selected', methods=['POST'])
def execute_selected_payload():
    # Payload aus dem Formular und das ausgewählte Layout abfragen
    payload_content = request.form['payload']
    layout = request.form.get('keyboard_layout', 'US')  # Standardmäßig auf US setzen

    # Temporär gespeichertes Payload ausführen
    temp_payload_path = os.path.join(payload_dir, "temp_execution_payload.txt")
    with open(temp_payload_path, "w") as temp_file:
        temp_file.write(payload_content)

    # Ausführen des temporären Payloads
    run_duckyscript(temp_payload_path, layout)

    # Zurück zur Hauptseite
    return redirect('/')