# routes.py
from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.admin.python.ducky_script.hid_emulator import execute_duckyscript
from datetime import datetime
import os
# import pyautogui
import time

badUSB = Blueprint('badUSB', __name__, template_folder='templates')

payload_dir = "app/admin/static/payloads/duckyScript/"


# def execute_duckyscript(file_path):
#     # Standard-Delay in Sekunden
#     default_delay = 0
#     ducky_commands = {
#         "WINDOWS": "win", "GUI": "win", "APP": "optionleft", "MENU": "optionleft",
#         "SHIFT": "shift", "ALT": "alt", "CONTROL": "ctrl", "CTRL": "ctrl",
#         "DOWNARROW": "down", "DOWN": "down", "LEFTARROW": "left", "LEFT": "left",
#         "RIGHTARROW": "right", "RIGHT": "right", "UPARROW": "up", "UP": "up",
#         "BREAK": "pause", "PAUSE": "pause", "CAPSLOCK": "capslock", "DELETE": "delete",
#         "END": "end", "ESC": "escape", "ESCAPE": "escape", "HOME": "home", "INSERT": "insert",
#         "NUMLOCK": "numlock", "PAGEUP": "pageup", "PAGEDOWN": "pagedown",
#         "PRINTSCREEN": "printscreen", "SCROLLLOCK": "scrolllock", "SPACE": "space",
#         "TAB": "tab", "ENTER": "enter"
#     }
#
#     with open(file_path, 'r', encoding='utf-8') as f:
#         # Entfernt leere Zeilen aus der Datei
#         lines = [line.strip() for line in f.readlines() if line.strip()]
#
#     for line in lines:
#         command = line.strip()
#         if command.startswith("DEFAULT_DELAY"):
#             default_delay = int(command.split()[1]) / 1000  # ms to seconds
#         elif command.startswith("REM"):
#             continue  # Kommentar ignorieren
#         elif command.startswith("DELAY"):
#             time.sleep(int(command.split()[1]) / 1000.0)
#         elif command.startswith("STRING"):
#             # Sicherstellen, dass nach "STRING" Text vorhanden ist
#             parts = command.split(' ', 1)
#             if len(parts) > 1:
#                 pyautogui.typewrite(parts[1])
#             else:
#                 print("Warnung: Leerer STRING-Befehl ignoriert.")
#
#         else:
#             # Kombinationsbefehle wie "CTRL ALT DELETE" oder "GUI r"
#             keys = command.split()
#             if all(key in ducky_commands for key in keys):
#                 with pyautogui.hold([ducky_commands[key] for key in keys[:-1]]):
#                     pyautogui.press(ducky_commands[keys[-1]])
#             elif len(keys) == 2 and keys[0] in ducky_commands:
#                 # Sonderfall für Kombinationen mit einer Taste (z.B. "GUI r")
#                 with pyautogui.hold(ducky_commands[keys[0]]):
#                     pyautogui.press(keys[1])  # Direkte Eingabe der zweiten Taste
#             elif command.isalnum():
#                 # Falls es eine Einzelbuchstabeneingabe ist (z.B. "r")
#                 pyautogui.press(command.lower())
#             else:
#                 print(f"Warnung: Unbekannter Befehl '{command}' ignoriert.")
#
#         if default_delay > 0:
#             time.sleep(default_delay)


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
    duckyscript_file = os.path.join(payload_dir, "newTest.txt")
    try:
        if not os.path.exists(duckyscript_file):
            raise FileNotFoundError(f"Die Datei {duckyscript_file} existiert nicht.")

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