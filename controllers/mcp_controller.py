from flask import Blueprint, request, render_template, session, redirect, url_for, g

mcp_bp = Blueprint('mcp_bp', __name__, template_folder="./views")

@mcp_bp.before_request
def auth():
    if request.endpoint == 'main_bp.login':        
        return 
    if 'idlogin' not in session:
        return redirect(url_for('main_bp.login'))

@mcp_bp.route('/view', methods=['GET', 'POST'])
def view():
    data = {}
    data['mcp'] = [
            {'id': 'mcp0', 'long': 106.8024652, 'lat': 10.8790426, 'available': 2, 'color': '#ff0000'},
            {'id': 'mcp1', 'long': 106.8044608, 'lat': 10.8763453, 'available': 2, 'color': '#00ff72'},
            {'id': 'mcp2', 'long': 106.8087309, 'lat': 10.8826458, 'available': 2, 'color' : '#00d8ff'},
            {'id': 'mcp3', 'long': 106.8059628, 'lat': 10.884458, 'available': 2, 'color' : '#e1ff00'},
            {'id': 'mcp4', 'long': 106.807379, 'lat': 10.8805597, 'available': 2, 'color' : '#00d8ff'},
            {'id': 'mcp5', 'long': 106.8035167, 'lat': 10.8858698, 'available': 2, 'color' : '#e1ff00'},
            {'id': 'mcp6', 'long': 106.8007701, 'lat': 10.8830251, 'available': 2, 'color' : '#e1ff00'},
            {'id': 'mcp7', 'long': 106.8109852, 'lat': 10.8813063, 'available': 2, 'color' : '#00d8ff'},
            {'id': 'mcp8', 'long': 106.8065005, 'lat': 10.8746475, 'available': 2, 'color' : '#00ff72'},
            {'id': 'mcp9', 'long': 106.7998701, 'lat': 10.8753008, 'available': 2, 'color' : '#00ff72'},
            {'id': 'mcp10', 'long': 106.8026811, 'lat': 10.8735307, 'available': 2, 'color' : '#00ff72'},
            {'id': 'mcp11', 'long': 106.799238, 'lat': 10.8790468, 'available': 2, 'color' : '#e1ff00'},
        ]
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role = "backofficer")
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role = "backofficer")
    content = render_template('components/mcp.html', role = "backofficer", data= data)
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = content)
    return render_template('index.html', content=layout)