from flask import Flask
from controllers.main_controller import main_bp
from controllers.backofficer_controller import backofficer_bp
from controllers.collector_controller import collector_bp
from controllers.janitor_controller import janitor_bp


app = Flask(
    __name__,
    template_folder='./views/',
)

app.register_blueprint(main_bp)
app.register_blueprint(backofficer_bp, url_prefix='/backofficer')
app.register_blueprint(collector_bp, url_prefix='/collector')
app.register_blueprint(janitor_bp, url_prefix='/janitor')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run('0.0.0.0', port=5000, debug=True)
