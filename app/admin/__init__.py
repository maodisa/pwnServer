from flask import (Flask)



def create_admin_app():
    app = Flask(__name__, template_folder='templates')

    # TODO: Herausfinden was das ist und ÄNDERN!!!
    app.secret_key = 'SOME KEY'


    with app.app_context():
        from app.admin.blueprints.core.routes import core
        from app.admin.blueprints.badUSB.routes import badUSB
        from app.admin.blueprints.terminal.routes import terminal

        app.register_blueprint(core, url_prefix='/')
        app.register_blueprint(badUSB, url_prefix='/badUSB')
        app.register_blueprint(terminal, url_prefix='/terminal')

    return app