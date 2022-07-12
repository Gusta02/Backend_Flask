from re import T
from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import ControllerFinanceiro, IntegracaoWms
from ..Dash_Logistica.kpis_luiz.main import estoque
from datetime import date,datetime
import locale
import io
import pandas as pd

financeiro = Blueprint('financeiro', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

def grafico_volumeXfinanceiro():
    pedidonovos = ControllerFinanceiro.PedidosBdNovo()
    pedidonovos = pd.DataFrame(pedidonovos)

    showroomnovo = ControllerFinanceiro.ShowroomBdNovo()
    showroomnovo = pd.DataFrame(showroomnovo)

    Pedidosantigos = pd.read_csv('app/Dash_Financeiro/planilhas/dados_banco_antigo.csv')

    tabelao = pd.concat([pedidonovos,showroomnovo,Pedidosantigos], sort=False, ignore_index=True)
    tabelao = tabelao.groupby(['Marca','Mes','Ano']).agg('sum')
    tabelao.valorTotal = tabelao.valorTotal.apply(lambda x: round(float(x),2))

    
    return tabelao


@financeiro.route("/dashboard/financeiro", methods=["GET","POST"])
def home_financeiro():

    teste = grafico_volumeXfinanceiro()

    ################# Seleção da moeda brasileira e do ano atual
    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  
    ano = date.today().year
    
    ################## Back dos Cards de inventário, vendas 2022 e gráfico #########################
    marca_selecionada = ''
  
    if request.method == 'POST':
        marca_selecionada = request.form.get('marca')
    
    marcas = estoque.marcas
    inventario_total = locale.currency(estoque.inventario(marca=marca_selecionada).Inventário.sum(), grouping=True)
    venda_anual = locale.currency(estoque.calcula_venda_total(marca=marca_selecionada), grouping=True)
    
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    labels_vendas = meses[:date.today().month]
    values_vendas = estoque.filtra_marca(marca_selecionada).ValorVenda.tolist()
    values_vendas_pct = estoque.calcula_pct(marca_selecionada)
        

    ################# Dicionário para a geração automática de cards ######################
    dict_variaveis = {
    # 'Inventário': inventario_total
    }
    
    return render_template('home_financeiro.html',cards = dict_variaveis, inventario_total = inventario_total,venda_anual = venda_anual, ano = ano,labels_vendas = labels_vendas, values_vendas = values_vendas, marcas = marcas,marca_selecionada = marca_selecionada, values_vendas_pct = values_vendas_pct)

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

@financeiro.route('/download/pagar',methods=['GET'])
def Pagar_Contas():
    trinta =  Pagar_30dias()
    sessenta = Pagar_60dias()
    noventa = Pagar_90dias()
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        trinta.to_excel(writer, sheet_name = '30Dias', index = False)
        sessenta.to_excel(writer, sheet_name = '60Dias')
        noventa.to_excel(writer, sheet_name = '90Dias')

    headers = {
    'Content-Disposition': 'attachment; filename=DadosPagar.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)

@financeiro.route('/download/receber',methods=['GET'])
def Receber_Contas():
    trinta = Receber_30dias()
    sessenta = Receber_60dias()
    noventa = Receber_90dias()

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        trinta.to_excel(writer, sheet_name = '30Dias', index = False)
        sessenta.to_excel(writer, sheet_name = '60Dias')
        noventa.to_excel(writer, sheet_name = '90Dias')
    
    headers = {
    'Content-Disposition': 'attachment; filename=DadosReceber.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)