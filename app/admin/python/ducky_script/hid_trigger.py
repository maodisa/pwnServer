import os
import sys

from app.admin.blueprints.badUSB.routes import auto_run_if_enabled
import time

# Den Pfad zum Hauptverzeichnis deiner App hinzufügen
sys.path.append(os.path.abspath('/home/kali/pwnServer/app/admin/python/ducky_script/'))

# Kurze Verzögerung einbauen, um sicherzustellen, dass das Gerät vollständig erkannt wird
time.sleep(2)

# Auto-Run-Funktion aufrufen, wenn HID erkannt wird
auto_run_if_enabled()
