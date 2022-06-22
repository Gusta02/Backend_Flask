from flask import Blueprint, current_app, render_template, jsonify
import os
import pandas as pd
import flask_excel as excel
from datetime import datetime

from ..controllers.relatorios_index_controller import (select_resumo_infos, select_groupby_saldo_produto)
from ..controllers.wmscontroller import (compara_valores_dataframes)
from ..controllers.relatorios_index_controller import (select_pedidos_data_atual)
from config import TEMPLATE_FOLDER,get_connection




relatoriosgraficos = Blueprint("relatoriosgraficos",__name__, 
        template_folder=os.path.join(TEMPLATE_FOLDER, "resources", "templates"), 
        static_folder=os.path.join(TEMPLATE_FOLDER, "resources", "static"))


excel.init_excel(current_app)

def retorna_dataatual():
    data = datetime.today().strftime('%Y-%m-%d')
    data = str(data).split("-")
    atual = data[-1] +'/' + data[-2] +'/' + data[-3]
    return atual



@relatoriosgraficos.route("/indexrelatorios", methods=["GET","POST"])
def retorna_index_relatorios():
        atual = retorna_dataatual()
        jsons = select_pedidos_data_atual(atual)
        print(jsons)
     
        return render_template('relatoriostemplate.html', produtos = jsons)


@relatoriosgraficos.route("/integracoes", methods=["GET","POST"])
def retorna_relatorios_integracoes():
        return "cadastrandotemplateintegracoes"

@relatoriosgraficos.route("/relatoriosprodutos", methods=["GET","POST"])
def retorna_relatorios_produtos():
        return "cadastrandotemplateprodutos"


@relatoriosgraficos.route("/relatoriosprodutoscategorias", methods=["GET","POST"])
def retorna_relatorios_produtos_categorias():
        return "cadastrandotemplateprodutoscategorias"

@relatoriosgraficos.route("/relatoriosfretes", methods=["GET","POST"])
def retorna_relatorios_fretes():
        return "cadastrandotemplatefretes"



@relatoriosgraficos.route("/relatoriospedidos", methods=["GET","POST"])
def retorna_relatorios_pedidos():
        return "cadastrandotemplatepedidos"


@relatoriosgraficos.route("/relatorioswms", methods=["GET","POST"])
def retorna_relatorios_wms():
        data = retorna_dataatual()
        jsons_wms = compara_valores_dataframes()
        jsons = select_pedidos_data_atual(data)
        print(jsons)

        return "cadastrandotemplatepedidos"

@relatoriosgraficos.route("/relatoriosgeral", methods=["GET","POST"])
def relatorios_geral():
        data = retorna_dataatual()
        jsons = compara_valores_dataframes()
        cont = len(jsons)
        jsons = select_pedidos_data_atual(data)
       
        return render_template("telarelatoriosgeral.html", quantidade = cont)

@relatoriosgraficos.route("/exportrelatoriopedidos", methods=["GET","POST"])
def export_relatorio_pedidos_wms():

        jsons = select_pedidos_data_atual()
        print(jsons)
        return excel.make_response_from_array([x.items() for x in jsons], "csv",
                                          file_name="export_data")