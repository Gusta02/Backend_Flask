from flask import Blueprint, render_template, request
from sqlalchemy import true
from ..controllers.controller_logistica import Transporte
import pandas as pd
from datetime import datetime
#import locale
from ..Dash_Logistica.kpis_luiz.main import kpi_entregues_no_prazo,kpi_pedidos_ja_atrasados,pct_entregas_sem_etapa_19,pct_entregas_sem_etapa_7,IndicadorPerformance,kpi_leadtime_nacional

transporte = Blueprint('transporte', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

def frete_arrecadado():
        #locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")

        pedido = Transporte.Valor_arrecadado_frete_pedido()
        showroom = Transporte.Valor_arrecadado_frete_showroom()

        pedido = pedido.to_dict('records')
        showroom = showroom.to_dict('records')

        pedido = pedido[0]['FreteRecebido']
        showroom = showroom[0]['FreteRecebido']

        resultado = (int(pedido) + int(showroom))

        resultado = 'R$ ' + str(resultado)  #locale.currency(resultado,grouping=True)

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
ind_leadtime = IndicadorPerformance(15,10,5,kpi_leadtime_nacional) 
,ind_coletasnoprazo = IndicadorPerformance(85,95,5,percentual_coleta_prazo()*100)
,ind_entregasnoprazo = IndicadorPerformance(85,95,5,kpi_entregues_no_prazo*100)
,ind_avarias = IndicadorPerformance(5,2.5,Perc_TaxaAvaria())
#,ind_nps = IndicadorPerformance(7,8,4)
)

kpi_time_transporte = IndicadorPerformance.calcula_kpi_time(dict_performance_time_transporte)



@transporte.route("/bi/dashboard/logistica/transporte", methods=["GET","POST"])
def Transporte_rota():

    dict_variaveis_transporte = {

    'Frete Total':frete_arrecadado()
    ,'Total de Avarias' : TotalAvaria() 
    ,'Taxa de Avaria' : f'{Perc_TaxaAvaria(): .2%}'
    ,'Percentual de Coletas no Prazo' : f'{percentual_coleta_prazo(): .2%}'
    ,'Percentual de Coletas Fora do Prazo' : f'{percentual_coleta_fora_prazo(): .2%}'
    ,'Entregas no Prazo' : f'{kpi_entregues_no_prazo: .0%}'
    ,'Entregas que Pularam a Etapa "Em Transporte"' : f'{pct_entregas_sem_etapa_7: .0%}'
    ,'Entregas que Pularam a Etapa "Saiu para Entrega"' : f'{pct_entregas_sem_etapa_19: .0%}'
    ,'Performance do Time de Transportes' : f'{kpi_time_transporte: .1f}'
    }

    return render_template('Relatorio_transporte.html', cards = dict_variaveis_transporte)