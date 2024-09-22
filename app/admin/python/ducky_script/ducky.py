#!/usr/bin/env python3
import time
import os
from app.admin.python.ducky_script.keyboard_layouts import KEY_LAYOUTS, SHIFT_REQUIRED, NULL_CHAR

# Send a HID report
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

# Release all keys
def release_keys():
    write_report(NULL_CHAR * 8)

# Press a single key
def press_key(key_code):
    write_report(NULL_CHAR * 2 + chr(key_code) + NULL_CHAR * 5)
    release_keys()

# Press a modifier key with another key (e.g., CTRL + ALT + DEL)
def press_combination(modifiers, key_code, layout):
    modifier_code = sum([layout[mod] for mod in modifiers])
    write_report(chr(modifier_code) + NULL_CHAR + chr(key_code) + NULL_CHAR * 5)
    release_keys()

# Write a character (including special characters)
def write_character(char, layout_name):
    layout = KEY_LAYOUTS[layout_name]
    shift_required = SHIFT_REQUIRED[layout_name]

    if char.islower():
        key_code = layout[char]
        press_key(key_code)
    elif char.isupper() or shift_required.get(char, False):
        key_code = layout[char.lower()] if char.isupper() else layout[char]
        press_combination(['SHIFT'], key_code, layout)
    elif char == ' ':
        press_key(layout['SPACE'])
    elif char.isdigit():
        press_key(layout[char])
    else:
        # Handle special characters
        if char in layout:
            if shift_required.get(char, False):
                press_combination(['SHIFT'], layout[char], layout)
            else:
                press_key(layout[char])

# Parse and execute a line of Duckyscript
def execute_duckyscript(file_path, layout_name):
    layout = KEY_LAYOUTS.get(layout_name, KEY_LAYOUTS['US'])  # Default to US layout
    with open(file_path, 'r') as f:
        for line in f:
            command = line.strip()
            if command.startswith("DELAY"):
                delay_time = int(command.split()[1])
                time.sleep(delay_time / 1000.0)
            elif command.startswith("STRING"):
                text = command.split(' ', 1)[1]
                for char in text:
                    write_character(char, layout_name)
            elif command.startswith("ENTER"):
                press_key(layout['ENTER'])
            elif command.startswith("CTRL") or command.startswith("ALT") or command.startswith("SHIFT") or command.startswith("GUI"):
                parts = command.split()
                modifiers = parts[:-1]
                key = parts[-1]
                if key in layout:
                    press_combination(modifiers, layout[key], layout)
            # Add more commands as needed (e.g., FUNCTION KEYS, SPECIAL CHARS)

# Execute the payload
def execute_payload(file_path, layout_name):
    if os.path.exists(file_path):
        execute_duckyscript(file_path, layout_name)
    else:
        print(f"File {file_path} does not exist.")
