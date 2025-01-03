# hid_emulator.py
import time

DUCKY_HID_MAPPING = {
    "a": (0x00, 0x04), "b": (0x00, 0x05), "c": (0x00, 0x06), "d": (0x00, 0x07),
    "e": (0x00, 0x08), "f": (0x00, 0x09), "g": (0x00, 0x0A), "h": (0x00, 0x0B),
    "i": (0x00, 0x0C), "j": (0x00, 0x0D), "k": (0x00, 0x0E), "l": (0x00, 0x0F),
    "m": (0x00, 0x10), "n": (0x00, 0x11), "o": (0x00, 0x12), "p": (0x00, 0x13),
    "q": (0x00, 0x14), "r": (0x00, 0x15), "s": (0x00, 0x16), "t": (0x00, 0x17),
    "u": (0x00, 0x18), "v": (0x00, 0x19), "w": (0x00, 0x1A), "x": (0x00, 0x1B),
    "z": (0x00, 0x1C), "y": (0x00, 0x1D),

    "ä": (0x00, 0x34), "ö": (0x00, 0x33), "ü": (0x00, 0x2F),

    "1": (0x00, 0x1E), "!": (0x02, 0x1E),
    "2": (0x00, 0x1F), '"': (0x02, 0x1F),
    "3": (0x00, 0x20), "§": (0x02, 0x20),
    "4": (0x00, 0x21), "$": (0x02, 0x21),
    "5": (0x00, 0x22), "%": (0x02, 0x22),
    "6": (0x00, 0x23), "&": (0x02, 0x23),
    "7": (0x00, 0x24), "/": (0x02, 0x24), "{": (0x40, 0x24),
    "8": (0x00, 0x25), "(": (0x02, 0x25), "[": (0x40, 0x25),
    "9": (0x00, 0x26), ")": (0x02, 0x26), "]": (0x40, 0x26),
    "0": (0x00, 0x27), "=": (0x02, 0x27), "}": (0x40, 0x27),
    "ß": (0x00, 0x2D), "?": (0x02, 0x2D), "\\": (0x40, 0x2D),

    "#": (0x00, 0x32), "'": (0x02, 0x32),
    "^": (0x00, 0x35), "°": (0x02, 0x35),
    ",": (0x00, 0x36), ";": (0x02, 0x36),
    ".": (0x00, 0x37), ":": (0x02, 0x37),
    "-": (0x00, 0x38), "_": (0x02, 0x38),
    "+": (0x00, 0x57),

    "CAPSLOCK": (0x00, 0x39),
    " ": (0x00, 0x2C),
    "ENTER": (0x00, 0x28),
    "ESC": (0x00, 0x29),
    "GUI": (0x00, 0xE3),
    "GUI_RIGHT": (0x00, 0xE7)
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
    except Exception as e:
        print(f"Error while sending HID report: {e}")


def execute_duckyscript(file_path):
    """Parse and execute a Ducky Script with cleanup for empty and trimmed lines."""
    default_delay = 0.1
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

    for line in lines:
        if line.startswith("DEFAULT_DELAY"):
            default_delay = int(line.split()[1]) / 1000.0
        elif line.startswith("DELAY"):
            time.sleep(int(line.split()[1]) / 1000.0)
        elif line.startswith("STRING"):
            text = line[7:]  # Entferne 'STRING '
            for char in text:
                if char.lower() in DUCKY_HID_MAPPING:
                    modifier, keycode = DUCKY_HID_MAPPING[char.lower()]
                    if char.isupper():
                        modifier |= 0x02  # SHIFT hinzufügen für Großbuchstaben
                    send_hid_report(modifier, keycode)
                    time.sleep(default_delay)
                else:
                    print(f"Unsupported character: {char}")
        elif line in DUCKY_HID_MAPPING:
            modifier, keycode = DUCKY_HID_MAPPING[line]
            send_hid_report(modifier, keycode)
            time.sleep(default_delay)
        else:
            print(f"Unknown command: {line}")