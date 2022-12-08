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

@janitor_bp.route('/profile', methods=['GET','POST'])
def personalInfomation():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    data = dbms.selectUserProfile(auth["idlogin"])
    data["name"] = data["lname"] + " " +  data["fname"]
    container = render_template('pages/profile.html', data=data)
    if request.method == "GET":
        req = request.args.to_dict()
        if "mode" in req:
            if req["mode"] == "edit":
                container = render_template('pages/profile.html', data=data, mode="edit")
    elif request.method == "POST":
        req = request.form.to_dict()
        if req["request"] == "save":
            dbms.saveEmployeeInformation(auth["idlogin"], data=req)
            return redirect(url_for("backofficer_bp.personalInfomation"))
        elif req["request"] == "cancel":
            return redirect(url_for("backofficer_bp.personalInfomation"))

    layout = render_template('layout/layout.html',header=header, content=container)
    return render_template('index.html', content=layout)
