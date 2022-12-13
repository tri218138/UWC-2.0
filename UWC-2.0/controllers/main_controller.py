from flask import Blueprint, request, render_template, session, redirect, url_for, g
from models.authetication_model import authService
from controllers.helper_function import *

# from controllers.collector_controller import collector_bp
# from controllers.janitor_controller import janitor_bp
# from controllers.mcp_controller import mcp_bp

main_bp = Blueprint('main_bp', __name__)

TOKEN = [] # {"idlogin": "", "username": "", "role": ""}

def defineToken(idlogin):
    for auth in TOKEN:
        if idlogin == auth["idlogin"]:
            return True, auth
    return False, None

@main_bp.before_request
def auth():
    print("before request")
    print(session) # <SecureCookieSession {'idlogin': 'backofficer'}>
    print(request.endpoint) # main_bp.login
    print(request.path) # /login
    if request.endpoint == 'main_bp.login':        
        return 
    if 'idlogin' not in session:
        return redirect('/login', code=302)
    global auth
    exists, auth = defineToken(session['idlogin'])
    if not exists:
        return redirect('/login', code = 302)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form.to_dict()
        verify, token = authService.checkLogin(data['username'], data['password'])
        if verify:
            session["idlogin"] = token["id"]
            TOKEN.append({"idlogin": token["id"], "username" : token["username"], "role": token["role"]})
            return redirect(url_for(f'{token["role"]}_bp.home'))
    elif request.method == 'GET':
        pass
    loginPage = render_template('pages/login.html')
    return render_template('index.html', content=loginPage)

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/home', methods=['GET', 'POST'])
def home():
    if 'idlogin' not in session:
        return redirect('/login', code=302)
    return redirect(url_for(f'{auth["role"]}_bp.home'))

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_bp.login'))

@main_bp.errorhandler(404)
def page_not_found(e):
    if 'idlogin' not in session:
        return redirect('/login', code=302)
    return render_template('error/404.html'), 404

@main_bp.app_errorhandler(404)
def page_not_found(e):
    if 'idlogin' not in session:
        return redirect('/login', code=302)
    err = render_template('error/404.html')
    return render_template('index.html', content=err)