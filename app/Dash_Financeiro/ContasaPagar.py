from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import ControllerFinanceiro, IntegracaoWms
from ..Dash_Logistica.kpis_luiz.main import estoque
from datetime import date,datetime
import locale
import io
import pandas as pd

Contas_Pagar = Blueprint('Contas_Pagar', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@Contas_Pagar.route("/dashboard/financeiro/ContasPagar", methods=["GET","POST"])
def Contas_a_Pagar():
    return render_template('contas_a_pagar.html', page = 1)