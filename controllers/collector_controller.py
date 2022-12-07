from flask import Blueprint, request, render_template, session, redirect, url_for, g
from models.collector_model import dbms
from controllers.main_controller import TOKEN, defineToken

collector_bp = Blueprint('collector_bp', __name__, template_folder="./views")

@collector_bp.before_request
def auth():
    if request.endpoint == 'main_bp.login':
        return
    if 'idlogin' not in session:
        return redirect(url_for('main_bp.login'))
    global auth
    sign, auth = defineToken(session["idlogin"])
    if not sign:
        return redirect(url_for('main_bp.login'))