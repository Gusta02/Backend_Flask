from flask import Blueprint, render_template, request, send_file,send_from_directory, Response
from sqlalchemy import true
from ..controllers.controller_logistica import IntegracaoWms, Transporte

finaceiro = Blueprint('finaceiro', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')


@finaceiro.route("/dashboard/financeiro", methods=["GET","POST"])
def home_financeiro():

    return render_template('home_financeiro.html')
