from flask import (Flask)



def create_admin_app():
    app = Flask(__name__, template_folder='templates')

    # TODO: Herausfinden was das ist und ÄNDERN!!!
    app.secret_key = 'SOME KEY'


    with app.app_context():
        from app.admin.blueprints.core.routes import core

        app.register_blueprint(core, url_prefix='/')

    return app