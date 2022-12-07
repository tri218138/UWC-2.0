from flask import Blueprint, request, render_template, session, redirect, url_for, g

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
    sidebar = render_template('layout/sidebar.html', role = "backofficer")
    selection = render_template('components/assign-task.html')
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = selection)
    return render_template('index.html', content=layout)

@task_bp.route('/assign/mcp', methods=['GET', 'POST'])
def assignMCP():
    header = render_template('layout/header.html')
    sidebar = render_template('layout/sidebar.html', role = "backofficer")
    selection = render_template('components/assign-task.html')
    layout = render_template('layout/layout.html', header= header, sidebar=sidebar, content = selection)
    return render_template('index.html', content=layout)