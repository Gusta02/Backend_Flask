from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import IntegracaoWms, Transporte
from ..Dash_Logistica.kpis_luiz.main import estoque
from datetime import date
from..Dash_Financeiro.kpis_michel.contas import Pagar_30dias,Pagar_60dias,Pagar_90dias, Receber_30dias,Receber_60dias,Receber_90dias
import locale
import io
import pandas as pd


financeiro = Blueprint('financeiro', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@financeiro.route("/dashboard/financeiro", methods=["GET","POST"])
def home_financeiro():

    ################# Seleção da moeda brasileira e do ano atual
    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  
    ano = date.today().year
    
    ################## Back dos Cards de inventário, vendas 2022 e gráfico #########################
    marca_selecionada = ''
  
    if request.method == 'POST':
        marca_selecionada = request.form.get('marca')
    
    marcas = estoque.vendas_ano_atual().NomeFantasia.unique().tolist()
    inventario_total = locale.currency(estoque.inventario(marca=marca_selecionada).Inventário.sum(), grouping=True)
    venda_anual = locale.currency(estoque.vendas_ano_atual(marca=marca_selecionada).ValorVenda.sum(), grouping=True)
    
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    labels_vendas = meses[:date.today().month]
    values_vendas = estoque.vendas_por_mes(marca_selecionada).ValorVenda.tolist()

    ################# Dicionário para a geração automática de cards ######################
    dict_variaveis = {
    # 'Inventário': inventario_total
    }
    
    return render_template('home_financeiro.html',cards = dict_variaveis, inventario_total = inventario_total,venda_anual = venda_anual, ano = ano,labels_vendas = labels_vendas, values_vendas = values_vendas, marcas = marcas,marca_selecionada = marca_selecionada)

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

@finaceiro.route('/download/pagar',methods=['GET']) # Gera Arquivos em Excel para Download
def pagar_excel():
    trinta =  Pagar_30dias()
    sessenta = Pagar_60dias()
    noventa = Pagar_90dias()

    buffer = io.BytesIO()
    with pd.ExcelWriter (buffer) as writer:
        trinta.to_excel(writer, sheet_name = '30dias')
        sessenta.to_excel(writer, sheet_name = '60Dias')
        noventa.to_excel(writer, sheet_name = '90Dias')

    headers = {
    'Content-Disposition': 'attachment; filename=PivotDadosPagar.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)

@finaceiro.route('/download/receber',methods=['GET'])
def receber_excel():
    trinta = Receber_30dias()
    sessenta = Receber_60dias()
    noventa = Receber_90dias()

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        trinta.to_excel(writer, sheet_name = '30Dias')
        sessenta.to_excel(writer, sheet_name = '60Dias')
        noventa.to_excel(writer, sheet_name = '90Dias')

    headers = {
    'Content-Disposition': 'attachment; filename=PivotDadosReceber.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
