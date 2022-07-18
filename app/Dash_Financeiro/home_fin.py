from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import ControllerFinanceiro, IntegracaoWms
from ..Dash_Logistica.kpis_luiz.main import estoque
from datetime import date,datetime
import locale
import io
import pandas as pd

financeiro = Blueprint('financeiro', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')


@financeiro.route("/dashboard/financeiro", methods=["GET","POST"])
def home_financeiro():

    # teste = grafico_volumeXfinanceiro()

    ################# Seleção da moeda brasileira e do ano atual
    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  
    #ano = date.today().year
    
    ################## Back dos Cards de inventário, vendas 2022 e gráfico #########################
    marca_selecionada = ''
    ano_selecionado = 2022
    
    if request.method == 'POST':
        try:
            ano_selecionado = int(request.form.get('ano'))
        except:
            ano_selecionado = 0

    if request.method == 'POST':
        marca_selecionada = request.form.get('marca')

    venda_total_showroom = locale.currency(estoque.calcula_venda_total(ano=ano_selecionado,marca=marca_selecionada,tipo='showroom'), grouping=True)
    venda_total = locale.currency(estoque.calcula_venda_total(ano=ano_selecionado,marca=marca_selecionada), grouping=True)
    
    if ano_selecionado:
        meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
        labels_vendas = meses[estoque.filtra(ano=ano_selecionado).columns.get_level_values('Mes').min()-1:estoque.filtra(ano=ano_selecionado).columns.get_level_values('Mes').max()]
    else:
        labels_vendas = ['2020','2021','2022']

    values_vendas = estoque.calcula_venda_mensal(marca=marca_selecionada,ano=ano_selecionado).tolist()
    values_vendas_pct = estoque.calcula_pct(ano = ano_selecionado, marca = marca_selecionada)
    values_vendas_cliente = estoque.calcula_venda_mensal(marca= marca_selecionada,ano=ano_selecionado,tipo='cliente').tolist()
    values_vendas_showroom = estoque.calcula_venda_mensal(marca= marca_selecionada,ano=ano_selecionado,tipo='showroom').tolist()
    marcas = estoque.marcas
    inventario_total = locale.currency(estoque.inventario(marca=marca_selecionada).Inventário.sum(), grouping=True)
 
    ################# Dicionário para a geração automática de cards ######################
    dict_variaveis = {
    # 'Inventário': inventario_total
    }
    
    return render_template('home_financeiro.html',cards = dict_variaveis, inventario_total = inventario_total,venda_total = venda_total,labels_vendas = labels_vendas, values_vendas = values_vendas, marcas = marcas,marca_selecionada = marca_selecionada, values_vendas_pct = values_vendas_pct,venda_total_showroom=venda_total_showroom, values_vendas_cliente=values_vendas_cliente,values_vendas_showroom=values_vendas_showroom,ano_selecionado=ano_selecionado)

@financeiro.route('/download/<df>/<filename>',methods=['GET']) # Gera Arquivos em Excel para Download
def download_excel(df,filename):

    tabela = getattr(estoque, df)
    buffer = io.BytesIO()
    tabela.to_excel(buffer)
    headers = {
    'Content-Disposition': 'attachment; filename={}.xlsx'.format(filename),
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)