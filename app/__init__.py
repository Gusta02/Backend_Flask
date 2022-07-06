from flask import Flask
from flask_admin import Admin
from flask import abort, render_template
#Tutorial base
#https://stackoverflow.com/questions/53566832/access-app-decorator-in-flask-using-factory-pattern
#https://flask.palletsprojects.com/en/2.1.x/api/#flask.Flask.errorhandler
#https://www.askpython.com/python-modules/flask/flask-error-handling

def register_handlers(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Skipping error handlers in Debug mode')
        return

    @app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        # retorna server error
        return render_template("500.html"), 500

    @app.errorhandler(404)
    def TemplateNotFound(*args, **kwargs):
        # retorna template notfound
        return render_template("404.html"), 404

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("404.html"), 404
    
    @app.errorhandler(500)
    def ModuleNotFoundError(*args, **kwargs):
        return render_template("500.html"), 500

    @app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        # do stuff
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
        # do stuff
        return render_template("405.html"), 405


def create_app():
    app = Flask(__name__,static_folder='static',static_url_path='/app/index/static')
    
    with app.app_context():
        #imports Blueprints
        from .index.index import index
        from .Dash_Logistica.Integracao_wms import wms
        from .Dash_Logistica.home_log import home
        from .Dash_Logistica.transporte import transporte
        # from .uploads.uploads import uploads
        # from .relatorios.relatorios import relatorios
        # from .admin_app.admin_app import admin_app
        # from .relatorios.relatorios_graficos import relatoriosgraficos
        # from .login.login import login

        register_handlers(app)

        #app.register_blueprint(uploads)
        app.register_blueprint(index)
        app.register_blueprint(wms)
        app.register_blueprint(home)
        app.register_blueprint(transporte)
        #app.register_blueprint(relatorios)
        #app.register_blueprint(admin_app)
        #app.register_blueprint(relatoriosgraficos)
        #app.register_blueprint(login)
        
    return app