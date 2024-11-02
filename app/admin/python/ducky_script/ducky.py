# ducky.py
import time
import os


# Placeholder functions for hardware-level keypresses
def write_report(report):
    pass  # Implement actual report writing for USB HID if needed


def release_keys():
    pass  # Implement release of all keys if needed


def press_key(key_code):
    pass  # Implement key press based on key code


def press_combination(modifiers, key_code, layout='US'):
    pass  # Implement key combination press with modifiers


def write_character(char, layout_name='US'):
    pass  # Implement character typing for different layouts if needed


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
