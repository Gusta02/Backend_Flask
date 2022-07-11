from turtle import position
from flask import Blueprint, render_template,current_app, jsonify, request
import os
from ..controllers.relatorios_index_controller import (select_pedidos_data_atual)
import pandas as pd
from ..controllers.relatorios_index_controller import (select_resumo_infos, select_marca_prazo_fabricacao,select_groupby_saldo_produto, vendas_mes_agrupado)
from ..controllers.controller_logistica import IntegracaoWms
#from ..Dash_Logistica.kpis_luiz.main import kpi_entregues_no_prazo,kpi_pedidos_ja_atrasados,kpi_time_logistica,kpi_time_transporte

def register_handlers(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Skipping error handlers in Debug mode')
        return

    @current_app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        # retorna server error
        return render_template("500.html"), 500

    @current_app.errorhandler(404)
    def TemplateNotFound(*args, **kwargs):
        # retorna template notfound
        return render_template("404.html"), 404

    @current_app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("404.html"), 404
    
    @current_app.errorhandler(500)
    def ModuleNotFoundError(*args, **kwargs):
        return render_template("500.html"), 500

    @current_app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        # do stuff
        return render_template("403.html"), 403

    @current_app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("404.html"), 404

    @current_app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
        # do stuff
        return render_template("405.html"), 405

index = Blueprint("index",__name__
        ,template_folder='templates',static_folder='static',static_url_path='/static/')
        
@index.route("/", methods=["GET","POST"])
def home():   
        return render_template("home.html")

register_handlers(current_app)