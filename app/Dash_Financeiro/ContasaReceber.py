from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import ControllerFinanceiro, IntegracaoWms
from ..Dash_Logistica.kpis_luiz.main import estoque
from datetime import date,datetime
import locale
import io
import pandas as pd


Contas_Receber = Blueprint('Contas_Receber', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@Contas_Receber.route("/dashboard/financeiro/ContasReceber", methods=["GET","POST"])
def Contas_a_Receber():
    return render_template('contas_a_receber.html', page = 1)