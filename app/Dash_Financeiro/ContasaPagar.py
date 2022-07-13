from app.Dash_Financeiro.kpis_michel.receber import Receber_15dias
from ..Dash_Financeiro.kpis_michel.pagar import Pagar_15dias, Pagar_30dias, Pagar_60dias, Pagar_90dias, Pagar_12meses
from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from datetime import date,datetime
import locale
import io
import pandas as pd

Contas_Pagar = Blueprint('Contas_Pagar', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@Contas_Pagar.route("/dashboard/financeiro/ContasPagar", methods=["GET","POST"])
def Contas_a_Pagar():
    return render_template('contas_a_pagar.html', page = 1)


@Contas_Pagar.route("/download/Contas_a_Pagar", methods=["GET","POST"])
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