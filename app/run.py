from app.admin import create_admin_app
import yaml


# Pfad zur Konfigurationsdatei
# config_path = "../../../../config.yaml"

admin_app = create_admin_app()

# # Funktion zum Laden der Konfiguration
# def load_config():
#     with open(config_path, 'r') as file:
#         return yaml.safe_load(file)
# config = load_config()

if __name__ == '__main__':
    # os.system(f"nmcli dev wifi hotspot ifname wlan0 ssid {config['SSID']} password {config['Password']}")
    admin_app.run(host='0.0.0.0', port=3001, debug=True)
