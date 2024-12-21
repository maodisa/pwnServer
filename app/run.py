from app.admin import create_admin_app, socket_io
import yaml

# Erstelle die Flask-Anwendung
admin_app = create_admin_app()

if __name__ == '__main__':
    # Verwende socketio.run, um die App mit WebSocket-Unterstützung zu starten
    socket_io.run(admin_app, host='0.0.0.0', port=3001, debug=True, allow_unsafe_werkzeug=True)
