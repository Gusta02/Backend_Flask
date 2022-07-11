from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import IntegracaoWms, Transporte
from ..Dash_Logistica.kpis_luiz.main import estoque
from datetime import date
import locale
import io

financeiro = Blueprint('financeiro', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@financeiro.route("/dashboard/financeiro", methods=["GET","POST"])
def home_financeiro():

    # if request.method == 'POST':
    #     if request.form.get('action1') == 'VALUE1':
    #         pass # do something
    #     elif  request.form.get('action2') == 'VALUE2':
    #         pass # do something else
    #     else:
    #         pass # unknown
    # elif request.method == 'GET':
    #     return render_template('index.html', form=form)
    



    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")
    
    ano = date.today().year
    inventario_total = locale.currency(estoque.inventario().Inventário.sum(), grouping=True)
    venda_anual = locale.currency(estoque.vendas_ano_atual().ValorVenda.sum(), grouping=True)
    marcas = ['Itagres','Elizabeth','Gaudi','Level']

    marca_selecionada = ''

    labels_vendas = []
    for row in range(1,8):
        labels_vendas.append(row)
    values_vendas = estoque.df_vendas_por_mes.ValorVenda.tolist()

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