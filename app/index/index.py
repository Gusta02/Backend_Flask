from flask import Blueprint, render_template,current_app, jsonify, request
import os

import pandas as pd
from ..controllers.relatorios_index_controller import (select_resumo_infos, select_marca_prazo_fabricacao
,select_groupby_saldo_produto, vendas_mes_agrupado)


def register_handlers(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Skipping error handlers in Debug mode')
        return

    @current_app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        # retorna server error
        return render_template("error_500.html"), 500

    @current_app.errorhandler(404)
    def TemplateNotFound(*args, **kwargs):
        # retorna template notfound
        return render_template("error_404.html"), 404

    @current_app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("error_404.html"), 404
    
    @current_app.errorhandler(500)
    def ModuleNotFoundError(*args, **kwargs):
        return render_template("error_500.html"), 500

    @current_app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        # do stuff
        return render_template("error_403.html"), 403

    @current_app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("error_404.html"), 404

    @current_app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
        # do stuff
        return render_template("error_405.html"), 405


index = Blueprint("index",__name__
        ,template_folder='templates',static_folder='static',static_url_path='/static/imagens')
        

@index.route("/", methods=["GET","POST"])
def home():
        datas = vendas_mes_agrupado()

        group_by_infos = select_resumo_infos()
        group_by_infos = group_by_infos[['Marca','SKU','NomeEstoque']]
        group_by_infos.groupby(['Marca','SKU','NomeEstoque']).size()
        #group_by_infos = group_by_infos.groupby(['Marca','NomeEstoque']).size().reset_index(name="Frequencia")
        #print(group_by_infos)
        frequencia = group_by_infos.groupby(['NomeEstoque'])['Marca'].value_counts().rename("Frequencia").groupby(level = 0).transform(lambda x: x/float(x.sum())) * 100
        frequencia = frequencia.reset_index(name='Frequencia')
        frequencia['Frequencia'] = frequencia['Frequencia'].apply(lambda x: round(float(x),2))
        jsons = frequencia.to_dict('records')
      

        marcasinfos = select_marca_prazo_fabricacao()

        #return render_template("index2.html",produtos = jsons, marcas = marcasinfos,datas=datas)
        return render_template("index.html")


register_handlers(current_app)