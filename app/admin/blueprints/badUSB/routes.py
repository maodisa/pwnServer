from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.admin.python.ducky_script.hid_emulator import execute_duckyscript
import os
import time

badUSB = Blueprint('badUSB', __name__, template_folder='templates')

payload_dir = "app/admin/static/payloads/duckyScript/"



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
    duckyscript_file = os.path.join(payload_dir, "test2.txt")
    try:
        if not os.path.exists(duckyscript_file):
            raise FileNotFoundError(f"Die Datei {duckyscript_file} existiert nicht.")
        time.sleep(3)
        # test_all_keys()
        execute_duckyscript(duckyscript_file)
        flash("Payload erfolgreich ausgeführt!", "success")
    except Exception as e:
        flash(f"Fehler bei der Ausführung des Payloads: {e}", "danger")

    return redirect(url_for('badUSB.index'))

# Route zum Löschen eines Payloads
@badUSB.route('/delete/<filename>', methods=['POST'])
def delete_payload(filename):
    file_path = os.path.join(payload_dir, filename)

    if os.path.exists(file_path):
        os.remove(file_path)  # Löscht die Datei

    return redirect(url_for('badUSB.index'))