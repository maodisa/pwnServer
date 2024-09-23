from flask import Flask
from flask_socketio import SocketIO

# SocketIO-Instanz erstellen
socketio = SocketIO()

def create_admin_app():
    app = Flask(__name__, template_folder='templates')

    # TODO: Herausfinden was das ist und ÄNDERN!!! (Es ist der Secret Key für Sessions und CSRF-Schutz)
    app.secret_key = 'SOME KEY'

    with app.app_context():
        # Importiere die Blueprint-Routes
        from app.admin.blueprints.core.routes import core

        # Registriere den Blueprint mit der App
        app.register_blueprint(core, url_prefix='/')

        # Initialisiere Flask-SocketIO mit der App
        socketio.init_app(app)

    return app
