from operator import index
from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from ..Dash_Financeiro.kpis_michel.receber import Receber_15dias,Receber_30dias,Receber_60dias,Receber_90dias, Receber_12meses
from datetime import date,datetime
import locale
import io
import pandas as pd


Contas_Receber = Blueprint('Contas_Receber', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@Contas_Receber.route("/dashboard/financeiro/ContasReceber", methods=["GET","POST"])
def Contas_a_Receber():
    return render_template('contas_a_receber.html', page = 1)


@Contas_Receber.route('/download/Contas_a_Receber',methods=['GET'])
def Receber_Contas():
    quinze = Receber_15dias()
    trinta = Receber_30dias()
    sessenta = Receber_60dias()
    noventa = Receber_90dias()
    doze = Receber_12meses()

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        quinze.to_excel(writer, sheet_name = '15Dias', index = False)
        trinta.to_excel(writer, sheet_name = '30Dias', index = False)
        sessenta.to_excel(writer, sheet_name = '60Dias', index = False)
        noventa.to_excel(writer, sheet_name = '90Dias', index = False)
        doze.to_excel(writer, sheet_name = '12Meses', index = False)
    headers = {
    'Content-Disposition': 'attachment; filename=Dados_a_Receber.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)