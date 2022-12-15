from flask import Blueprint, request, render_template, session, redirect, url_for, g
from models.janitor_model import dbms
from controllers.mcp_controller import mcp_bp
import calendar, datetime
from controllers.main_controller import TOKEN, defineToken, getCurrentDateTime

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
    sidebar = render_template('layout/sidebar.html')
    content = f"<h1>{getCurrentDateTime()}</h1>"
    content = render_template('layout/layout.html', header=header, sidebar=sidebar, content=content)
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

    layout = render_template('layout/layout.html',header=header, content=container, sidebar=sidebar)
    return render_template('index.html', content=layout)

@janitor_bp.route('/member', methods=['GET', 'POST'])
def member():
    data = dbms.selectEmployee()
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    content = render_template('components/member.html',
                              role="janitor", data=data)
    layout = render_template('layout/layout.html',
                             header=header, sidebar=sidebar, content=content)
    return render_template('index.html', content=layout)

@janitor_bp.route('/schedule', methods=['GET','POST'])
def schedule():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')

    today = getCurrentDateTime()
    data = {
        "calendar": calendar.monthcalendar(today.year, today.month),
        "empId": auth["idlogin"],
        "worktime": dbms.selectScheduleInMonth(auth["idlogin"], today.month)
    }
    if request.method == 'GET':
        req = request.args.to_dict()
        if 'datepicker' in req:
            datetime = today.replace(day=int(req['datepicker']))
            data["assigned"] = dbms.selectScheduleInDate(auth["idlogin"], datetime)

    content = render_template('components/datepicker.html', data = data)

    layout = render_template('layout/layout.html',header=header, sidebar=sidebar, content=content)
    return render_template('index.html', content=layout)

@janitor_bp.route('/message', methods=['GET','POST'])
def message():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')

    if request.method == 'POST':
        req = request.form.to_dict()
        if "message" in req:
            dbms.addLogMessage({
                "employee_id" : auth["idlogin"], 
                "time": getCurrentDateTime().strftime('%d/%m/%Y-%H:%M:%S'),
                # "time": getCurrentDateTime(),
                "fname": dbms.selectUserProfile(auth["idlogin"])["fname"],
                "message" : req["message"],
            })
    data = {
        "log" : dbms.getLogMessage(),
        "employee_id" : auth["idlogin"]
    }
    content = render_template('components/message.html', data=data)
    layout = render_template('layout/layout.html',header=header, sidebar=sidebar, content=content)
    return render_template('index.html', content=layout)


janitor_bp.register_blueprint(mcp_bp, url_prefix='/mcp')
@janitor_bp.route('/mcp', methods=['GET','POST'])
def mcps():
    return redirect(url_for('janitor_bp.mcp_bp.view'))