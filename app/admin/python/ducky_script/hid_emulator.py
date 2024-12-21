# hid_emulator.py
import time
import os

DUCKY_HID_MAPPING = {
    "a": 0x04, "b": 0x05, "c": 0x06, "d": 0x07, "e": 0x08, "f": 0x09, "g": 0x0A, "h": 0x0B,
    "i": 0x0C, "j": 0x0D, "k": 0x0E, "l": 0x0F, "m": 0x10, "n": 0x11, "o": 0x12, "p": 0x13,
    "q": 0x14, "r": 0x15, "s": 0x16, "t": 0x17, "u": 0x18, "v": 0x19, "w": 0x1A, "x": 0x1B,
    "y": 0x1C, "z": 0x1D, "1": 0x1E, "2": 0x1F, "3": 0x20, "4": 0x21, "5": 0x22, "6": 0x23,
    "7": 0x24, "8": 0x25, "9": 0x26, "0": 0x27, "ENTER": 0x28, "ESC": 0x29, "BACKSPACE": 0x2A,
    "TAB": 0x2B, "SPACE": 0x2C, "CTRL": 0xE0, "SHIFT": 0xE1, "ALT": 0xE2, "GUI": 0xE3,
    "LEFT": 0x50, "DOWN": 0x51, "RIGHT": 0x4F, "UP": 0x52
}

HID_DEVICE = "/dev/hidg0"

def send_hid_report(modifier, keycode):
    """Send a HID report."""
    try:
        with open(HID_DEVICE, "wb") as hid:
            report = bytes([modifier, 0, keycode, 0, 0, 0, 0, 0])
            hid.write(report)
            hid.write(bytes(8))  # Key Release
    except FileNotFoundError:
        print("HID device not found. Ensure the device is configured properly.")

def execute_duckyscript(file_path):
    """Parse and execute a Ducky Script."""
    default_delay = 0.1
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            command = line.strip()
            if command.startswith("DEFAULT_DELAY"):
                default_delay = int(command.split()[1]) / 1000.0
            elif command.startswith("DELAY"):
                time.sleep(int(command.split()[1]) / 1000.0)
            elif command.startswith("STRING"):
                text = command[7:]
                for char in text:
                    if char in DUCKY_HID_MAPPING:
                        modifier, keycode = (0x00, DUCKY_HID_MAPPING[char])
                        if char.isupper():
                            modifier |= 0x02
                        send_hid_report(modifier, keycode)
                        time.sleep(default_delay)
                    else:
                        print(f"Warning: Unsupported character '{char}'.")
            elif command.split()[0] in DUCKY_HID_MAPPING:
                keys = command.split()
                if len(keys) == 1:
                    send_hid_report(0x00, DUCKY_HID_MAPPING[keys[0]])
                elif len(keys) > 1:
                    modifier = 0x00
                    for key in keys[:-1]:
                        modifier |= DUCKY_HID_MAPPING[key]
                    send_hid_report(modifier, DUCKY_HID_MAPPING[keys[-1]])
                time.sleep(default_delay)
            else:
                print(f"Unknown command: {command}")
