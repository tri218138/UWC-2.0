from flask import Blueprint, request, render_template, session, redirect, url_for, g

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
        return redirect('login')
    global auth
    exists, auth = defineToken(session['idlogin'])
    if not exists:
        return redirect('/login', code = 302)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form.to_dict()
        if data["username"] == "backofficer" and data["password"] == "backofficer":
            session["idlogin"] = data["username"]
            TOKEN.append({"idlogin": data["username"], "username" : data["username"], "role": data["username"]})
            return redirect(url_for('backofficer_bp.home'))
            # return redirect(url_for('main_bp.home'))
        elif data["username"] == "janitor" and data["password"] == "janitor":
            session["idlogin"] = data["username"]
            TOKEN.append({"idlogin": data["username"], "username" : data["username"], "role": data["username"]})
            return redirect(url_for('janitor_bp.home'))
    elif request.method == 'GET':
        pass
    loginPage = render_template('pages/login.html')
    return render_template('index.html', content=loginPage)

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    return redirect(url_for(f'{g.user["role"]}_bp.home'))

@main_bp.route('/vehicle', methods=['GET', 'POST'])
def vehicle():
    return redirect(url_for(f'{g.user["role"]}_bp.vehicle'))

@main_bp.route('/mcp', methods=['GET', 'POST'])
def mcp():
    return redirect(url_for(f'{g.user["role"]}_bp.mcp'))

# https://flask-login.readthedocs.io/en/latest/
# pip install flask-login


@main_bp.route('/profile', methods=['GET', 'POST'])
def personalInfomation():
    pass

@main_bp.route('/setting', methods=['GET', 'POST'])
def setting():
    pass

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@main_bp.errorhandler(404)
def page_not_found(e):
    # print('main_bp')
    return render_template('error/404.html'), 404

@main_bp.app_errorhandler(404)
def page_not_found(e):
    # print('app')
    # print(request.path)
    # print(TOKEN)
    # print(session["idlogin"])
    err = render_template('error/404.html')
    return render_template('index.html', content=err)