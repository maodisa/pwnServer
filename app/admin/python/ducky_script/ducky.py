import pyautogui
import time


# Funktion zur Ausgabe eines Tasteneingabeberichts (nur für spezielle Hardware)
def write_report(report):
    # Diese Funktion wäre für USB HID spezifisch und hängt von der Hardware ab
    print("Report geschrieben:", report)  # Debugging-Ausgabe (für echte HID erforderlich)


# Funktion zur Freigabe aller Tasten (für HID-Geräte erforderlich)
def release_keys():
    # In pyautogui können wir keine "alle Tasten loslassen" Methode direkt aufrufen
    # Für HID wäre dies ein "alle Tasten freigeben" Signal
    pyautogui.keyUp('ctrl')  # Beispielhaftes Loslassen einer Modifikatortaste
    pyautogui.keyUp('alt')
    pyautogui.keyUp('shift')
    print("Alle Tasten freigegeben")  # Debugging-Ausgabe


# Funktion zum Drücken einer einzelnen Taste
def press_key(key_code):
    # Drückt die Taste basierend auf dem angegebenen Schlüsselcode
    pyautogui.press(key_code)
    print(f"Taste '{key_code}' gedrückt")  # Debugging-Ausgabe


# Funktion zum Drücken einer Tasten-Kombination (z.B. STRG + ALT + ENTF)
def press_combination(modifiers, key_code, layout='US'):
    # Drückt eine Kombination von Modifikatortasten und einer Haupttaste
    with pyautogui.hold(modifiers):
        pyautogui.press(key_code)
    print(f"Kombination '{modifiers} + {key_code}' gedrückt")  # Debugging-Ausgabe


# Funktion zum Eingeben eines einzelnen Zeichens, angepasst an Tastaturlayout
def write_character(char, layout_name='US'):
    # Nutzt pyautogui zum Tippen eines Zeichens
    pyautogui.typewrite(char)
    print(f"Zeichen '{char}' mit Layout '{layout_name}' geschrieben")  # Debugging-Ausgabe


# Dictionary for DuckyScript to pyautogui key mappings
ducky_commands = {
    "WINDOWS": "win", "GUI": "win", "APP": "optionleft", "MENU": "optionleft",
    "SHIFT": "shift", "ALT": "alt", "CONTROL": "ctrl", "CTRL": "ctrl",
    "DOWNARROW": "down", "DOWN": "down", "LEFTARROW": "left", "LEFT": "left",
    "RIGHTARROW": "right", "RIGHT": "right", "UPARROW": "up", "UP": "up",
    "BREAK": "pause", "PAUSE": "pause", "CAPSLOCK": "capslock", "DELETE": "delete",
    "END": "end", "ESC": "escape", "ESCAPE": "escape", "HOME": "home", "INSERT": "insert",
    "NUMLOCK": "numlock", "PAGEUP": "pageup", "PAGEDOWN": "pagedown",
    "PRINTSCREEN": "printscreen", "SCROLLLOCK": "scrolllock", "SPACE": "space",
    "TAB": "tab", "ENTER": "enter"
}


# Function to execute individual commands in a DuckyScript file
def execute_duckyscript(file_path, layout='US'):
    # Set default delay (if defined in the script)
    default_delay = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        command = line.strip()
        if command.startswith("DEFAULT_DELAY"):
            default_delay = int(command.split()[1]) / 1000  # Convert ms to seconds
            continue  # Skip to next command after setting delay

        # Process each command type
        if command.startswith("DELAY"):
            time.sleep(int(command.split()[1]) / 1000.0)
        elif command.startswith("STRING"):
            for char in command.split(' ', 1)[1]:
                write_character(char, layout)
        elif command.startswith("REPEAT"):
            repeat_count = int(command.split()[1])
            for _ in range(repeat_count):
                execute_duckyscript(file_path, layout)
        elif command in ducky_commands:
            press_key(ducky_commands[command])
        elif command.startswith("REM"):
            continue  # Comment line, do nothing
        else:
            # Check if it’s a combination like "CTRL ALT DELETE"
            keys = command.split()
            if all(key in ducky_commands for key in keys):
                modifiers = [ducky_commands[key] for key in keys[:-1]]
                key_code = ducky_commands[keys[-1]]
                press_combination(modifiers, key_code, layout)

        # Apply default delay if specified
        if default_delay > 0:
            time.sleep(default_delay)


# Wrapper function to execute the payload
def execute_payload(file_path, layout='US'):
    if os.path.exists(file_path):
        execute_duckyscript(file_path, layout)
    else:
        print(f"File {file_path} does not exist.")
