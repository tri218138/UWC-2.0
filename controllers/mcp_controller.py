from flask import Blueprint, request, render_template, session, redirect, url_for, g
from controllers.main_controller import TOKEN, defineToken
from models.backoffficer_model import dbms

mcp_bp = Blueprint('mcp_bp', __name__, template_folder="./views")

@mcp_bp.before_request
def auth():
    if request.endpoint == 'main_bp.login':
        return
    if 'idlogin' not in session:
        return redirect(url_for('main_bp.login'))
    global auth
    sign, auth = defineToken(session["idlogin"])
    if not sign:
        return redirect(url_for('main_bp.login'))

@mcp_bp.route('/view', methods=['GET', 'POST'])
def view():
    role = request.blueprint.split('.')[0][:-3]
    data = {}
    data['mcp'] = dbms.selectMCPforView()
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role = role)
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role = role)
    content = render_template('components/mcp.html', role = role, data= data)
    operator = render_template('components/mcp-operator.html', role = role)
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, operator=operator, content = content)
    return render_template('index.html', content=layout, role = role)

@mcp_bp.route('/search', methods=['GET', 'POST'])
def search():
    role = request.blueprint.split('.')[0][:-3]
    data = {
        "mcp" : []
    }
    if request.method == 'GET':
        req = request.args.to_dict()
        if "id" in req:
            data['mcp'] = dbms.selectMCPbyId(req["id"])
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role = role)
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role = role)
    content = render_template('components/mcp.html', role = role, data= data)
    operator = render_template('components/mcp-operator.html', role = role)
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, operator=operator, content = content)
    return render_template('index.html', content=layout, role = role)