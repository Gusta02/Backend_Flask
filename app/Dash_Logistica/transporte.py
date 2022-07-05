from flask import Blueprint, render_template, request
from sqlalchemy import true
from ..controllers.controller_logistica import Transporte
import pandas as pd
from datetime import datetime
import locale
from ..Dash_Logistica.kpis_luiz.main import kpi_entregues_no_prazo,kpi_pedidos_ja_atrasados,pct_entregas_sem_etapa_19,pct_entregas_sem_etapa_7,IndicadorPerformance

transporte = Blueprint('transporte', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

def frete_arrecadado():
        locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")

        pedido = Transporte.Valor_arrecadado_frete_pedido()
        showroom = Transporte.Valor_arrecadado_frete_showroom()

        pedido = pedido.to_dict('records')
        showroom = showroom.to_dict('records')

        pedido = pedido[0]['FreteRecebido']
        showroom = showroom[0]['FreteRecebido']

        resultado = (int(pedido) + int(showroom))

        resultado = locale.currency(resultado)

        return resultado

#//////////////////// MICHEL //////////////////////////
#///////////////  CARD TOTAL AVARIAS =  Card 6 //////////////////////// 
def TotalAvaria(): 

    Avaria = Transporte.Quant_avaria()
    TotalAvaria = Avaria[0]['QuantidadeAvaria']

    return TotalAvaria
#////////////////    CARD PERCENTUAL AVARIAS / ENTREGUE (TAXA)  = Card 7 ////////////////
def Perc_TaxaAvaria(): 

    Avaria = Transporte.Quant_avaria()
    TotalAvaria = Avaria[0]['QuantidadeAvaria']

    Entregue = Transporte.Quant_entregue()
    TotalEntregue = Entregue[0]['Quantidade_Entregue']
    TaxaAvaria = TotalAvaria / TotalEntregue 

    # Percentual taxa Avaria
    #TaxaAvaria = "{:.2%}".format(TaxaAvaria)

    return TaxaAvaria

def percentual_coleta_prazo():

    df = Transporte.percentual_coleta_Prazo()
    df3 =  df['Coletado'] > df['Previsao'] 

    Percentual_Entregas_no_prazo = (df3.value_counts()[1] / (df3.value_counts()[0] + df3.value_counts()[1]))
    #Percentual_Entregas_no_prazo = f'{Percentual_Entregas_no_prazo: .2%}'
    return Percentual_Entregas_no_prazo


def percentual_coleta_fora_prazo():

    df = Transporte.percentual_coleta_fora_prazo()
    df3 =  df['Coletado'] > df['Previsao'] 

    Percentual_Entregas_fora_prazo = (df3.value_counts()[0] / (df3.value_counts()[0] + df3.value_counts()[1]))
    #Percentual_Entregas_fora_prazo = f'{Percentual_Entregas_fora_prazo: .2%}'
    return Percentual_Entregas_fora_prazo

#################################### Indicadores de Performance do Time De Transporte ############################################
dict_performance_time_transporte = dict(
ind_leadtime = IndicadorPerformance(15,10,5) #tirar a média nacional?
,ind_coletasnoprazo = IndicadorPerformance(85,95,5,percentual_coleta_prazo()*100)
,ind_entregasnoprazo = IndicadorPerformance(85,95,5,kpi_entregues_no_prazo*100)
,ind_avarias = IndicadorPerformance(5,2.5,Perc_TaxaAvaria())
#,ind_nps = IndicadorPerformance(7,8,4)
)

kpi_time_transporte = IndicadorPerformance.calcula_kpi_time(dict_performance_time_transporte)



@transporte.route("/dashboard/logistica/transporte", methods=["GET","POST"])
def Transporte_rota():


    frete_total = frete_arrecadado()
    card6 = TotalAvaria() 
    card7 = f'{Perc_TaxaAvaria(): .2%}'
    card8 = f'{percentual_coleta_prazo(): .2%}'
    card9 = f'{percentual_coleta_fora_prazo(): .2%}'
    card1 = f'{kpi_entregues_no_prazo: .0%}'

    return render_template('Relatorio_transporte.html', card8 = card8, card9 = card9, frete = frete_total, card1=card1,card2 = kpi_pedidos_ja_atrasados, card3 = f'{pct_entregas_sem_etapa_7: .0%}', card4 = f'{pct_entregas_sem_etapa_19: .0%}', card5 = f'{kpi_time_transporte: .1f}', card6 = card6, card7 = card7)