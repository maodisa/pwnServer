import os
from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.admin.python.ducky_script.ducky import execute_payload

badUSB = Blueprint('badUSB', __name__, template_folder='templates')

# Speicherort für die Payloads
payload_dir = "app/admin/static/payloads/duckyScript"
config_file_path = "app/admin/static/config/auto_run_config.txt"


# Funktion zur Ausführung der Duckyscript-Payload
def run_duckyscript(file_path, layout):
    try:
        # Die execute_payload Funktion aus ducky.py aufrufen
        execute_payload(file_path, layout)
        flash('Payload successfully executed!', 'success')
    except Exception as e:
        flash(f'Error executing payload: {str(e)}', 'danger')


@badUSB.route('/')
def index():
    # Liste der gespeicherten Payloads laden
    payload_files = os.listdir(payload_dir)
    payloads = [f for f in payload_files if f.endswith('.txt')]

    # Auto-Run-Konfiguration laden
    auto_run_config = load_auto_run_config()

    return render_template('badUSB/index.html',
                           payloads=payloads,
                           auto_run_enabled=auto_run_config['enabled'],
                           auto_run_payload=auto_run_config['payload_name'])


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

        # Lade alle gespeicherten Payloads und schalte in den Bearbeitungsmodus
        payload_files = os.listdir(payload_dir)
        payloads = [f for f in payload_files if f.endswith('.txt')]

        # Render mit aktiviertem Bearbeitungsmodus
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
    payload = request.form['payload'].strip()  # Entfernt führende und nachfolgende Leerzeichen/Tabs
    file_path = os.path.join(payload_dir, filename)

    try:
        with open(file_path, "w") as file:
            file.write(payload)
        flash('Payload successfully updated!', 'success')
    except Exception as e:
        flash(f'Error updating payload: {str(e)}', 'danger')

    return redirect(url_for('badUSB.index'))


# Route zum Löschen eines Payloads
@badUSB.route('/delete/<filename>', methods=['POST'])
def delete_payload(filename):
    file_path = os.path.join(payload_dir, filename)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)  # Löscht die Datei
            flash(f'Payload "{filename}" deleted successfully.', 'success')
        else:
            flash(f'Payload "{filename}" does not exist.', 'danger')
    except Exception as e:
        flash(f'Error deleting payload: {str(e)}', 'danger')

    return redirect(url_for('badUSB.index'))


# Neue Route zum Ausführen des ausgewählten Payloads
@badUSB.route('/execute_selected', methods=['POST'])
def execute_selected_payload():
    # Payload aus dem Formular und das ausgewählte Layout abfragen
    payload_content = request.form['payload']
    layout = request.form.get('keyboard_layout', 'US')  # Standardmäßig auf US setzen

    try:
        # Temporär gespeichertes Payload ausführen
        temp_payload_path = os.path.join(payload_dir, "temp_execution_payload.txt")
        with open(temp_payload_path, "w") as temp_file:
            temp_file.write(payload_content)

        # Ausführen des temporären Payloads
        run_duckyscript(temp_payload_path, layout)
    except Exception as e:
        flash(f'Error executing payload: {str(e)}', 'danger')

    return redirect(url_for('badUSB.index'))


# Funktion zum Laden der Auto-Run-Konfiguration
def load_auto_run_config():
    config = {'enabled': False, 'payload_name': ''}
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            lines = file.readlines()
            config['enabled'] = lines[0].split('=')[1].strip() == 'True'
            config['payload_name'] = lines[1].split('=')[1].strip()
    return config


# Funktion zum Speichern der Auto-Run-Konfiguration
def save_auto_run_config(enabled, payload_name):
    with open(config_file_path, 'w') as file:
        file.write(f"enabled={enabled}\n")
        file.write(f"payload_name={payload_name}\n")


# Route zum Aktualisieren der Auto-Run-Einstellungen
@badUSB.route('/update_auto_run', methods=['POST'])
def update_auto_run():
    # Lesen der Formulardaten
    auto_run_enabled = request.form.get('auto_run_enabled') == 'on'
    auto_run_payload = request.form.get('auto_run_payload')

    # Speichern der Konfiguration
    save_auto_run_config(auto_run_enabled, auto_run_payload)

    flash('Auto-Run settings updated!', 'success')
    return redirect(url_for('badUSB.index'))


# Funktion zum Ausführen des Auto-Run-Payloads beim Start
def auto_run_if_enabled():
    config = load_auto_run_config()
    if config['enabled'] and config['payload_name']:
        payload_path = os.path.join(payload_dir, config['payload_name'])
        run_duckyscript(payload_path, layout='US')  # Hier kannst du das Standard-Layout anpassen
