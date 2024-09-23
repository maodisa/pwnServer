from flask import render_template, Blueprint

core = Blueprint('core', __name__, template_folder='templates')

# Speicherort für die Payloads
payload_dir = "app/admin/static/payloads/duckyScript"



@core.route('/')
def index():
    return render_template('core/index.html')
