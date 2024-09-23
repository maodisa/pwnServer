from app.admin.blueprints.badUSB.routes import auto_run_if_enabled
import time

# Kurze Verzögerung einbauen, um sicherzustellen, dass das Gerät vollständig erkannt wird
time.sleep(2)

# Auto-Run-Funktion aufrufen, wenn HID erkannt wird
auto_run_if_enabled()
