from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import ControllerFinanceiro, IntegracaoWms
from ..Dash_Logistica.kpis_luiz.kpi import Unidades
from datetime import date,datetime
import locale
import io
import pandas as pd

vendas_unidade = Blueprint('vendas_unidade', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

unidades = Unidades()

@vendas_unidade.route("/dashboard/financeiro/vendas_por_unidade", methods=["GET","POST"])
def vendas_por_unidade():

    # teste = grafico_volumeXfinanceiro()

    ################# Seleção da moeda brasileira e do ano atual
    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  
    ano = date.today().year
    
    ################## Back dos Cards de inventário, vendas 2022 e gráfico #########################
    unidade_selecionada = ''
  
    if request.method == 'POST':
        unidade_selecionada = request.form.get('unidade')
    
    lista_de_unidades = unidades.retorna_unidades()
    #inventario_total = locale.currency(unidades.inventario(marca=marca_selecionada).Inventário.sum(), grouping=True)
    venda_total = locale.currency(unidades.calcula_venda_total(unidade=unidade_selecionada), grouping=True)
    
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    labels_vendas = meses[:date.today().month]
    values_vendas = unidades.filtra_unidade(unidade_selecionada).ValorVenda.tolist()
    values_vendas_pct = unidades.calcula_pct(unidade_selecionada)
        
    ################# Dicionário para a geração automática de cards ######################
    dict_variaveis = {
    # 'Inventário': inventario_total
    }
    
    return render_template('vendas_por_unidade.html', cards = dict_variaveis, venda_total = venda_total, ano = ano,labels_vendas = labels_vendas, values_vendas = values_vendas, lista_de_unidades = lista_de_unidades, unidade_selecionada = unidade_selecionada, values_vendas_pct = values_vendas_pct)


@vendas_unidade.route('/download/<df>/<filename>',methods=['GET']) # Gera Arquivos em Excel para Download
def download_excel(df,filename):

    tabela = getattr(unidades, df)
    buffer = io.BytesIO()
    tabela.to_excel(buffer)
    headers = {
    'Content-Disposition': 'attachment; filename={}.xlsx'.format(filename),
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)