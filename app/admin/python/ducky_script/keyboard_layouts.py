# Null character used for HID communication
NULL_CHAR = chr(0)

# US QWERTY Layout
KEY_CODES_US = {
    'a': 4, 'b': 5, 'c': 6, 'd': 7, 'e': 8, 'f': 9, 'g': 10, 'h': 11,
    'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18,
    'p': 19, 'q': 20, 'r': 21, 's': 22, 't': 23, 'u': 24, 'v': 25,
    'w': 26, 'x': 27, 'y': 28, 'z': 29, '1': 30, '2': 31, '3': 32,
    '4': 33, '5': 34, '6': 35, '7': 36, '8': 37, '9': 38, '0': 39,
    'ENTER': 40, 'ESC': 41, 'BACKSPACE': 42, 'TAB': 43, 'SPACE': 44,
    '!': 30, '@': 31, '#': 32, '$': 33, '%': 34, '^': 35, '&': 36,
    '*': 37, '(': 38, ')': 39, '-': 45, '=': 46, '[': 47, ']': 48,
    '\\': 49, ';': 51, "'": 52, '`': 53, ',': 54, '.': 55, '/': 56,
    'F1': 58, 'F2': 59, 'F3': 60, 'F4': 61, 'F5': 62, 'F6': 63,
    'F7': 64, 'F8': 65, 'F9': 66, 'F10': 67, 'F11': 68, 'F12': 69,
    'CTRL': 224, 'SHIFT': 225, 'ALT': 226, 'GUI': 227  # Windows/Command key
}

# German QWERTZ Layout with special characters and umlauts
KEY_CODES_DE = {
    'a': 4, 'b': 5, 'c': 6, 'd': 7, 'e': 8, 'f': 9, 'g': 10, 'h': 11,
    'i': 12, 'j': 13, 'k': 14, 'l': 15, 'm': 16, 'n': 17, 'o': 18,
    'p': 19, 'q': 20, 'r': 21, 's': 22, 't': 23, 'u': 24, 'v': 25,
    'w': 26, 'x': 27, 'y': 29, 'z': 28, '1': 30, '2': 31, '3': 32,
    '4': 33, '5': 34, '6': 35, '7': 36, '8': 37, '9': 38, '0': 39,
    'ENTER': 40, 'ESC': 41, 'BACKSPACE': 42, 'TAB': 43, 'SPACE': 44,
    '!': 30, '"': 31, '§': 32, '$': 33, '%': 34, '&': 35, '/': 36,
    '(': 37, ')': 38, '=': 39, '?': 45, '`': 46, 'ü': 47, '+': 48,
    '#': 49, 'ö': 51, 'ä': 52, '^': 53, ',': 54, '.': 55, '-': 56,
    'F1': 58, 'F2': 59, 'F3': 60, 'F4': 61, 'F5': 62, 'F6': 63,
    'F7': 64, 'F8': 65, 'F9': 66, 'F10': 67, 'F11': 68, 'F12': 69,
    'CTRL': 224, 'SHIFT': 225, 'ALT': 226, 'GUI': 227
}

# Add more layouts as needed
KEY_LAYOUTS = {
    'US': KEY_CODES_US,
    'DE': KEY_CODES_DE
}

# Define shift mappings for uppercase letters and special characters
SHIFT_REQUIRED = {
    'US': {
        '!': True, '@': True, '#': True, '$': True, '%': True, '^': True,
        '&': True, '*': True, '(': True, ')': True, '_': True, '+': True,
        '~': True, '{': True, '}': True, ':': True, '"': True, '|': True,
        '<': True, '>': True, '?': True
    },
    'DE': {
        '!': True, '"': True, '§': True, '$': True, '%': True, '&': True,
        '/': True, '(': True, ')': True, '=': True, '?': True, '`': True,
        '^': True, '+': True, '#': True, '*': True, ':': True, '_': True
    }
}
