from threading import local
from ..Dash_Financeiro.kpis_michel.pagar import Pagar_15dias, Pagar_30dias, Pagar_60dias, Pagar_90dias, Pagar_12meses
from ..Dash_Financeiro.kpis_michel.main import SOMA_TODASEMPRESAS_APAGAR, TODASEMPRESAS_CONTASARECEBER,fluxoCaixa, empresa
from ..Dash_Financeiro.kpis_michel.classes import dict_empresas
from flask import Blueprint, render_template, request, Response
import locale
import io
import pandas as pd

Contas_Pagar = Blueprint('Contas_Pagar', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@Contas_Pagar.route("/dashboard/financeiro/ContasPagar", methods=["GET","POST"])
def Contas_a_Pagar():

    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  
    
    selecionar_empresa = 'Todas'
    periodicidade = 30

    if request.method == 'POST':
        selecionar_empresa =  request.form.get('empresa')
        
    empresa_selecionada = dict_empresas[selecionar_empresa]

    filtro_empresas = list(dict_empresas.keys())

    #renderizando no front
    fluxodecaixa = locale.currency(empresa_selecionada.get_valor(), grouping=True)
    card_total_pagar = locale.currency(empresa_selecionada.calcula_tipo('CONTAS A PAGAR'), grouping= True)
    card_total_receber = locale.currency(empresa_selecionada.calcula_tipo('CONTAS A RECEBER'), grouping= True)

    return render_template('contas_a_pagar.html', page = 1, card= fluxodecaixa, card1 = card_total_pagar, card2= card_total_receber, filtro_empresa = filtro_empresas, selecionar_empresa = selecionar_empresa )


@Contas_Pagar.route("/download/ContasPagar", methods=["GET","POST"])
def PagarDownload_excel():
    quinze =  Pagar_15dias()
    trinta =  Pagar_30dias()
    sessenta = Pagar_60dias()
    noventa = Pagar_90dias()
    doze = Pagar_12meses()
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        quinze.to_excel(writer, sheet_name = '15Dias', index = False)
        trinta.to_excel(writer, sheet_name = '30Dias', index = False)
        sessenta.to_excel(writer, sheet_name = '60Dias', index = False)
        noventa.to_excel(writer, sheet_name = '90Dias', index = False)
        doze.to_excel(writer, sheet_name = '12Meses', index = False)
    headers = {
    'Content-Disposition': 'attachment; filename=Dados_a_Pagar.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)