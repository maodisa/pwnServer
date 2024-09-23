from app.admin import create_admin_app, socketio
import yaml

# import os

# Pfad zur Konfigurationsdatei
# config_path = "../../../../config.yaml"

# Erstelle die Flask-Anwendung
admin_app = create_admin_app()

# # Funktion zum Laden der Konfiguration
# def load_config():
#     with open(config_path, 'r') as file:
#         return yaml.safe_load(file)
# config = load_config()

if __name__ == '__main__':
    # Starte das Flask-SocketIO Interface anstatt nur Flask
    # os.system(f"nmcli dev wifi hotspot ifname wlan0 ssid {config['SSID']} password {config['Password']}")

    # Verwende socketio.run, um die App mit WebSocket-Unterstützung zu starten
    socketio.run(admin_app, host='0.0.0.0', port=3001, debug=True)
