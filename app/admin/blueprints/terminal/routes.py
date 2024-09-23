import os
from flask import render_template, Blueprint, request, redirect, url_for
from app.admin.python.ducky_script.ducky import execute_payload

terminal = Blueprint('terminal', __name__, template_folder='templates')

@terminal.route('/')
def index():
    return render_template('terminal/index.html')

