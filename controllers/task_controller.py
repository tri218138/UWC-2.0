from flask import Blueprint, request, render_template, session, redirect, url_for, g
from models.backoffficer_model import dbms
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

    today = datetime.datetime.today()
    date_in_current_month = calendar.monthcalendar(today.year, today.month)

    if request.method == 'GET':
        req = request.args.to_dict()
        if "datepicker" in req and "shift" in req:
            global datepicker, shift
            datepicker = req["datepicker"]
            shift = req["shift"]
        if "type" in req and req["type"] == "mcp":
            return redirect(url_for('backofficer_bp.task_bp.assignMCP'))
        elif "type" in req and req["type"] == "route":
            return redirect(url_for('backofficer_bp.task_bp.assignRoute'))

    content = render_template('components/task-assign.html', data= date_in_current_month)
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
            today = datetime.datetime.today()
            if "mcp" in req and "janitor" in req:
                pairs = {
                    "mcp" : req["mcp"], # ["mcpx"]
                    "janitor" : req["janitor"], # ["13132","31231"]
                    "date": f"{datepicker}/{today.month}/{today.year}",
                    "shift" : shift
                }
                dbms.assignJanitor2MCP(pairs)
        elif req["option"][0] == 'delete':
            if "mcp" in req and "janitor" in req:
                pair = {
                    "mcp" : req["mcp"][0], # mcpx
                    "janitor" : req["janitor"][0], #312323
                    "date": f"{datepicker}/{today.month}/{today.year}",
                    "shift" : shift
                }
                dbms.removeWorkAssignedJanitor2MCP(pair)

    data = {}
    data["mcp"] = dbms.selectMCPforAssign()
    data["janitor"] = dbms.selectAllJanitorReady()
    data["assigned"] = dbms.selectTaskAssignedMCP()

    content = render_template('components/task-assign-mcp.html', data=data)
    operator = render_template('layout/operator.html', type="task-assign-mcp")
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = content, operator= operator)
    return render_template('index.html', content=layout)

@task_bp.route('/assign/route', methods=['GET', 'POST'])
def assignRoute():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html')

    # if request.method == 'POST':            
    #     # print(request.form.to_dict(False)) # {"option":["assign"], "janitor": ["31312","1313123"], "mcp":["mcp0"]}
    #     req = request.form.to_dict(False) # user for multivalue in checkbox
    #     if req["option"][0] == 'assign':
    #         if "mcp" in req and "janitor" in req:
    #             pairs = {
    #                 "mcp" : req["mcp"], # ["mcpx"]
    #                 "janitor" : req["janitor"] # ["13132","31231"]
    #             }
    #             dbms.assignJanitor2MCP(pairs)
    #     elif req["option"][0] == 'delete':
    #         if "mcp" in req and "janitor" in req:
    #             pair = {
    #                 "mcp" : req["mcp"][0], # mcpx
    #                 "janitor" : req["janitor"][0] #312323
    #             }
    #             dbms.removeWorkAssignedJanitor2MCP(pair)

    data = {}
    data["route"] = dbms.selectRouteforAssign()
    data["collector"] = dbms.selectAllCollectorReady()
    data["vehicle"] = dbms.selectVehicleforAssign()
    # data["assigned"] = dbms.selectTaskAssignedMCP()

    content = render_template('components/task-assign-route.html', data=data)
    operator = render_template('layout/operator.html', type="task-assign-route")
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = content, operator= operator)
    return render_template('index.html', content=layout)