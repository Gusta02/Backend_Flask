from ..Dash_Financeiro.kpis_michel.pagar import Pagar_15dias, Pagar_30dias, Pagar_60dias, Pagar_90dias, Pagar_12meses
from ..Dash_Financeiro.kpis_michel.main import valor_total, conta_pagar
from flask import Blueprint, render_template, request, Response
import locale
import io
import pandas as pd

Contas_Pagar = Blueprint('Contas_Pagar', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@Contas_Pagar.route("/dashboard/financeiro/ContasPagar", methods=["GET","POST"])
def Contas_a_Pagar():

    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  
    
    empresa_selecionada = ''
    periodicidade = 30

    if request.method == 'POST':
        try:
            periodicidade = int(request.form.get('periodociade'))
        except:
            periodicidade = 0

    

    #renderizando no front
    card_total_pagar = locale.currency(conta_pagar, grouping= True)

    return render_template('contas_a_pagar.html', page = 1, card2 = card_total_pagar )


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