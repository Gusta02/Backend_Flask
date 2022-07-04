from flask import Blueprint, render_template, request
from sqlalchemy import true
from ..controllers.controller_logistica import Transporte
import pandas as pd
from datetime import datetime
import locale
from ..Dash_Logistica.kpis_luiz.main import kpi_entregues_no_prazo,kpi_pedidos_ja_atrasados,pct_entregas_sem_etapa_19,pct_entregas_sem_etapa_7

transporte = Blueprint('transporte', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')


def frete_arrecadado():

    pedido = Transporte.Valor_arrecadado_frete_pedido()
    showroom = Transporte.Valor_arrecadado_frete_showrrom()

    pedido = pedido[0]['FreteRecebido']
    showroom = showroom[0]['FreteRecebido']

    resultado = (int(pedido) + int(showroom))

    resultado = locale.currency(resultado)
    return resultado


@transporte.route("/dashboard/logistica/transporte", methods=["GET","POST"])
def Transporte_rota():

    frete_total = frete_arrecadado()
    print(frete_total)

    return render_template('Relatorio_transporte.html',frete = frete_total, card1=f'{kpi_entregues_no_prazo: .0%}',card2 = kpi_pedidos_ja_atrasados, card3 = f'{pct_entregas_sem_etapa_7: .0%}', card4 = f'{pct_entregas_sem_etapa_19: .0%}', card5 = '', card6 = '', card7 = '')