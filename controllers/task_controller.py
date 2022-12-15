from flask import Blueprint, request, render_template, session, redirect, url_for, g
from models.backoffficer_model import dbms
from controllers.main_controller import TOKEN, defineToken, getCurrentDateTime
import calendar, datetime

task_bp = Blueprint('task_bp', __name__, template_folder="./views")

@task_bp.before_request
def auth():
    if request.endpoint == 'main_bp.login':        
        return 
    if 'idlogin' not in session:
        return redirect(url_for('main_bp.login'))

@task_bp.route('/assign', methods=['GET', 'POST'])
def assign():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')

    today = getCurrentDateTime()
    date_in_current_month = calendar.monthcalendar(today.year, today.month)

    if request.method == 'GET':
        req = request.args.to_dict()
        if "datepicker" in req and "shift" in req:
            global datepicker, shift
            datepicker = datetime.datetime(2022, today.month, int(req["datepicker"]))
            print("req shift: ", req["shift"])
            shift = "sáng" if req["shift"] == "morning" else "chiều"
        if "type" in req and req["type"] == "mcp":
            return redirect(url_for('backofficer_bp.task_bp.assignMCP'))
        elif "type" in req and req["type"] == "route":
            return redirect(url_for('backofficer_bp.task_bp.assignRoute'))
    data = {
        "date_in_current_month": date_in_current_month,
        "month": today.month,
        "year": today.year
    }

    content = render_template('components/task-assign.html', data= data)
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = content)
    return render_template('index.html', content=layout)

@task_bp.route('/assign/mcp', methods=['GET', 'POST'])
def assignMCP():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')
    if request.method == 'POST':            
        # print(request.form.to_dict(False)) # {"option":["assign"], "janitor": ["31312","1313123"], "mcp":["mcp0"]}
        req = request.form.to_dict(False) # user for multivalue in checkbox
        if req["option"][0] == 'assign':
            if "mcp" in req and "janitor" in req:
                data = {
                    "mcp" : req["mcp"], # ["mcpx"]
                    "janitor" : req["janitor"], # ["13132","31231"]
                    "datetime": [datepicker], # call datetime.year/month/day/hour/minute/second
                    "shift" : [shift]
                }
                dbms.assignJanitor2MCP(data)
        elif req["option"][0] == 'delete':
            if "mcp" in req and "janitor" in req:
                pair = {
                    "mcp" : req["mcp"][0], # mcpx
                    "janitor" : req["janitor"][0], #312323
                    "datetime": [datepicker],
                    "shift": [shift]
                }
                dbms.removeWorkAssignedJanitor2MCP(pair)

    data = {}
    data["mcp"] = dbms.selectMCPforAssign()
    # print(date.month)
    data["janitor"] = dbms.selectAllJanitorReady(datepicker, shift)
    data["assigned"] = dbms.selectTaskAssignedMCP(datepicker, shift)

    content = render_template('components/task-assign-mcp.html', data=data)
    operator = render_template('layout/operator.html', type="task-assign-mcp")
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = content, operator= operator)
    return render_template('index.html', content=layout)

@task_bp.route('/assign/route', methods=['GET', 'POST'])
def assignRoute():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')

    if request.method == 'POST':            
        # print(request.form.to_dict(False)) # {"option":["assign"], "janitor": ["31312","1313123"], "mcp":["mcp0"]}
        req = request.form.to_dict(False) # user for multivalue in checkbox
        print(req)
        if req["option"][0] == 'assign':
            today = getCurrentDateTime()
            if "route" in req and "collector" in req and "vehicle" in req:
                data = {
                    "route" : req["route"], # ["route0"]
                    "collector" : req["collector"], # ["collector0"]
                    "vehicle" : req["vehicle"], # ["50B-1231"]
                    "datetime": [datepicker],
                    "shift" : [shift]
                }
                dbms.assignCollector2Route(data)
        elif req["option"][0] == 'delete':
            if "route" in req and "collector" in req:
                pair = {
                    "route" : req["route"][0], # route
                    "collector" : req["collector"][0], #312323
                    "vehicle" : req["vehicle"][0],
                    "datetime": datepicker, 
                    "shift" : shift
                }
                dbms.removeWorkAssignedCollector2Route(pair)

    data = {}
    data["route"] = dbms.selectRouteforAssign()
    data["collector"] = dbms.selectAllCollectorReady()
    data["vehicle"] = dbms.selectVehicleforAssign()
    data["assigned"] = dbms.selectTaskAssignedRoute()

    content = render_template('components/task-assign-route.html', data=data)
    operator = render_template('layout/operator.html', type="task-assign-route")
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = content, operator= operator)
    return render_template('index.html', content=layout)