#!/usr/bin/env python3
import time
import os

# Null character used for HID communication
NULL_CHAR = chr(0)

# HID keycodes for common keys
KEY_CODES = {
    'a': 4, 'b': 5, 'c': 6, 'd': 7, 'e': 8, 'f': 9, 'g': 10, 'h': 11,
    'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18,
    'p': 19, 'q': 20, 'r': 21, 's': 22, 't': 23, 'u': 24, 'v': 25,
    'w': 26, 'x': 27, 'y': 28, 'z': 29, '1': 30, '2': 31, '3': 32,
    '4': 33, '5': 34, '6': 35, '7': 36, '8': 37, '9': 38, '0': 39,
    'ENTER': 40, 'ESC': 41, 'BACKSPACE': 42, 'TAB': 43, 'SPACE': 44,
    'F1': 58, 'F2': 59, 'F3': 60, 'F4': 61, 'F5': 62, 'F6': 63,
    'F7': 64, 'F8': 65, 'F9': 66, 'F10': 67, 'F11': 68, 'F12': 69,
    'CTRL': 224, 'SHIFT': 225, 'ALT': 226, 'GUI': 227  # Windows/Command key
}

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
def press_combination(modifiers, key_code):
    modifier_code = sum([KEY_CODES[mod] for mod in modifiers])
    write_report(chr(modifier_code) + NULL_CHAR + chr(key_code) + NULL_CHAR * 5)
    release_keys()

# Write a character (for printable characters)
def write_character(char):
    if char.islower():
        key_code = KEY_CODES[char]
        press_key(key_code)
    elif char.isupper():
        key_code = KEY_CODES[char.lower()]
        press_combination(['SHIFT'], key_code)
    elif char == ' ':
        press_key(KEY_CODES['SPACE'])
    elif char.isdigit():
        press_key(KEY_CODES[char])
    else:
        # Handle other characters (punctuation, etc.)
        pass

# Parse and execute a line of Duckyscript
def execute_duckyscript(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            command = line.strip()
            if command.startswith("DELAY"):
                delay_time = int(command.split()[1])
                time.sleep(delay_time / 1000.0)
            elif command.startswith("STRING"):
                text = command.split(' ', 1)[1]
                for char in text:
                    write_character(char)
            elif command.startswith("ENTER"):
                press_key(KEY_CODES['ENTER'])
            elif command.startswith("CTRL") or command.startswith("ALT") or command.startswith("SHIFT") or command.startswith("GUI"):
                parts = command.split()
                modifiers = parts[:-1]
                key = parts[-1]
                if key in KEY_CODES:
                    press_combination(modifiers, KEY_CODES[key])
            # Add more commands as needed (e.g., FUNCTION KEYS, SPECIAL CHARS)

# Execute the payload
def execute_payload(file_path):
    # Ensure file exists before executing
    if os.path.exists(file_path):
        execute_duckyscript(file_path)
    else:
        print(f"File {file_path} does not exist.")

if __name__ == "__main__":
    execute_payload("duckyscript.txt")
