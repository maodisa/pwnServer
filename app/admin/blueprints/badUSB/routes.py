# routes.py
import os
from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.admin.python.ducky_script.ducky import execute_payload

badUSB = Blueprint('badUSB', __name__, template_folder='templates')

# Speicherort für die Payloads
payload_dir = "app/admin/static/payloads/duckyScript"

# Funktion zur Ausführung der Duckyscript-Payload
def run_duckyscript(file_path):
    try:
        # Die execute_payload Funktion aus ducky.py aufrufen
        execute_payload(file_path, layout='US')  # Standard auf US setzen
        flash('Payload successfully executed!', 'success')
    except Exception as e:
        flash(f'Error executing payload: {str(e)}', 'danger')


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

    try:
        with open(os.path.join(payload_dir, filename), "w") as file:
            file.write(payload)
        flash('Payload successfully uploaded!', 'success')
    except Exception as e:
        flash(f'Error uploading payload: {str(e)}', 'danger')

    return redirect(url_for('badUSB.index'))


# Route zum Bearbeiten einer Payload
@badUSB.route('/edit/<filename>', methods=['GET'])
def edit_payload(filename):
    file_path = os.path.join(payload_dir, filename)

    try:
        with open(file_path, "r") as file:
            edit_payload = file.read()

        # Liste der gespeicherten Payloads laden
        payload_files = os.listdir(payload_dir)
        payloads = [f for f in payload_files if f.endswith('.txt')]

        return render_template('badUSB/index.html',
                               payloads=payloads,
                               edit_mode=True,
                               edit_payload=edit_payload,
                               edit_payload_name=filename)
    except Exception as e:
        flash(f'Error loading payload: {str(e)}', 'danger')
        return redirect(url_for('badUSB.index'))


# Route zum Speichern der bearbeiteten Payload
@badUSB.route('/update/<filename>', methods=['POST'])
def update_payload(filename):
    payload = request.form['payload'].strip()
    file_path = os.path.join(payload_dir, filename)

    try:
        with open(file_path, "w") as file:
            file.write(payload)
        flash('Payload successfully updated!', 'success')
    except Exception as e:
        flash(f'Error updating payload: {str(e)}', 'danger')

    return redirect(url_for('badUSB.index'))


# Route zum Ausführen des ausgewählten Payloads
@badUSB.route('/execute_selected', methods=['POST'])
def execute_selected_payload():
    payload_content = request.form['payload']
    temp_payload_path = os.path.join(payload_dir, "temp_execution_payload.txt")

    try:
        with open(temp_payload_path, "w") as temp_file:
            temp_file.write(payload_content)

        run_duckyscript(temp_payload_path)
    except Exception as e:
        flash(f'Error executing payload: {str(e)}', 'danger')

    return redirect(url_for('badUSB.index'))
