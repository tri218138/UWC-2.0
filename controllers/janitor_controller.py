from flask import Blueprint, request, render_template, session, redirect, url_for, g
from models.janitor_model import dbms
from controllers.main_controller import TOKEN, defineToken

janitor_bp = Blueprint('janitor_bp', __name__, template_folder="./views")

@janitor_bp.before_request
def auth():
    if request.endpoint == 'main_bp.login':
        return
    if 'idlogin' not in session:
        return redirect(url_for('main_bp.login'))
    global auth
    sign, auth = defineToken(session["idlogin"])
    if not sign:
        return redirect(url_for('main_bp.login'))

@janitor_bp.route('/', methods=['GET', 'POST'])
@janitor_bp.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role="janitor")
    content = render_template('layout/layout.html',
                              header=header, sidebar=sidebar)
    return render_template('index.html', content=content)