from flask import Blueprint, request, render_template, session, redirect, url_for, g
from controllers.task_controller import task_bp
from controllers.mcp_controller import mcp_bp
from models.backoffficer_model import dbms
import calendar, datetime
from controllers.main_controller import TOKEN, defineToken, getCurrentDateTime
from controllers.create_route import create_optimized_route

backofficer_bp = Blueprint('backofficer_bp', __name__,
                           template_folder="./views")

backofficer_bp.register_blueprint(task_bp, url_prefix='/task')

@backofficer_bp.before_request
def auth():
    if request.endpoint == 'main_bp.login':
        return
    if 'idlogin' not in session:
        return redirect(url_for('main_bp.login'))
    global auth
    sign, auth = defineToken(session["idlogin"])
    if not sign:
        return redirect(url_for('main_bp.login'))



@backofficer_bp.route('/', methods=['GET', 'POST'])
@backofficer_bp.route('/home', methods=['GET', 'POST'])
# @login_required
def home():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    content = f"<h1>{getCurrentDateTime()}</h1>"
    content = render_template('layout/layout.html', header=header, sidebar=sidebar, content=content)
    return render_template('index.html', content=content)


@backofficer_bp.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('backofficer_bp.home'))




@backofficer_bp.route('/vehicle', methods=['GET', 'POST'])
# @login_required
def vehicle():
    # by Nguyen Tien Manh
    try:
        req_data = request.get_json()
        dbms.handleActionVehicle(req_data)
    except:
        print('Error!!')
    
    # tmppdata = dbms.selectVehicle()
    vehicle_list = dbms.selectVehicle()
    vec_type_list = set(())
    data = []

    for val in vehicle_list:
        vec_type_list.add(val['type'])

    for vec_type in vec_type_list:
        tmp = [x for x in vehicle_list if x['type'] == vec_type]
        data.append(tmp)

    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    content = render_template(
        'components/vehicle.html', role='backofficer', data=data)
    layout = render_template('layout/layout.html',
                             header=header, sidebar=sidebar, content=content)
    return render_template('index.html', content=layout)

    # end by Nguyen Tien Manh


backofficer_bp.register_blueprint(mcp_bp, url_prefix='/mcp')


@backofficer_bp.route('/mcp', methods=['GET', 'POST'])
def mcp():
    if request.method == "POST":
        req_data = request.get_json() #
        if "action" in req_data:
            dbms.handleActionMcp(req_data)
    return redirect(url_for('backofficer_bp.mcp_bp.view'))

@backofficer_bp.route('/route/search', methods=['GET', 'POST'])
def routeSearch():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    data = {
        "route" : [],
        "mcp": [],
        "step": "route-search"
    }
    if request.method == 'GET':
        req = request.args.to_dict()
        if "id" in req:
            data['route'] = [dbms.selectRouteById(req["id"])]
            data["mcp"] = dbms.selectMCPinRouteId(req["id"])

    mcp = render_template('components/mcp.html', data= data, step = data["step"])

    operator = render_template('layout/operator.html', type='create-route', step=data["step"])
    layout = render_template('layout/layout.html',header=header, sidebar=sidebar, content=mcp, operator= operator)
    return render_template('index.html', content=layout)

@backofficer_bp.route('/member', methods=['GET', 'POST'])
def member():
    data = {
        "member": dbms.selectEmployee()
    }
    if request.method == 'GET':
        req = request.args.to_dict()
        if "request" in req:
            if req["request"] == "search":
                if "id" in req:
                    member = dbms.selectEmployeeById(req["id"])
                    if not member is None:
                        data["member"] = [member]
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    operator = render_template('layout/operator.html', type='search-member')
    content = render_template('components/member.html', role="backofficer", data=data)
    layout = render_template('layout/layout.html', header=header, sidebar=sidebar, content=content, operator=operator)
    return render_template('index.html', content=layout)

# #################################################

@backofficer_bp.route('/assign-task', methods=['GET', 'POST'])
def assignTask():
    return redirect(url_for('backofficer_bp.task_bp.assign'))


@backofficer_bp.route('/route/create', methods=['POST', 'GET'])
def createRoute():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    data = {"step": 'overview'}

    if request.method == 'POST':
        postData = request.form.to_dict(False)
        create_optimized_route()        
        if 'step' in postData:
            data["step"] = postData['step'][0]

    data["mcp"] = dbms.selectMCPforView()
    data["route"] = dbms.selectRoute()

    mcp = render_template('components/mcp.html', data= data, step = data["step"])

    operator = render_template('layout/operator.html', type='create-route', step=data["step"])
    layout = render_template('layout/layout.html',header=header, sidebar=sidebar, content=mcp, operator= operator)
    return render_template('index.html', content=layout)

@backofficer_bp.route('/schedule', methods=['GET','POST'])
def schedule():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')

    data = {}
    today = getCurrentDateTime()
    data["calendar"] = calendar.monthcalendar(today.year, today.month)
    if request.method == 'GET':
        req = request.args.to_dict()
        if 'datepicker' in req:
            datetime = today.replace(day=int(req['datepicker']))
            data["assigned"] = dbms.selectScheduleInDate(datetime)

    content = render_template('components/datepicker.html', data = data)

    layout = render_template('layout/layout.html',header=header, sidebar=sidebar, content=content)
    return render_template('index.html', content=layout)

@backofficer_bp.route('/profile', methods=['GET','POST'])
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
            dbms.saveUserName(auth["username"], data=req)
            return redirect(url_for("backofficer_bp.personalInfomation"))
        elif req["request"] == "cancel":
            return redirect(url_for("backofficer_bp.personalInfomation"))
    content = render_template('layout/layout.html', header=header, container=container if container is not None else "")
    return render_template('index.html', content=content)  

    layout = render_template('layout/layout.html',header=header, content=container)
    return render_template('index.html', content=layout)

@backofficer_bp.route('/message', methods=['GET','POST'])
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

