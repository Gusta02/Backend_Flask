from flask import Blueprint, render_template, request
from ..controllers.controller_logistica import IntegracaoWms
import pandas as pd
from datetime import datetime
from ..Dash_Logistica.kpis_luiz.main import kpi_entregues_no_prazo,kpi_pedidos_ja_atrasados,kpi_time_logistica,kpi_time_transporte

home = Blueprint('home', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')


def leadtime():
    tabela = IntegracaoWms.leadtime_log()
    estado = IntegracaoWms.Estados()

    medias = []

    for index, row in estado.iterrows():

        Estado = row['estado']

        media = tabela.query(f'Estado=="{Estado}"')
        media = media['Dias']
        media = media.mean()
        media = f'{media: .0f}'
        medias.append(media)

    tamanho = len(medias)
    contador = 0
    while (contador < tamanho):

        try: 
            medias[contador] = int(medias[contador])
        except:
            medias[contador] = 'Sem Média de'
        
        contador   = contador + 1    

    Media = pd.DataFrame(medias, columns = ['Media'])
    df =pd.concat([estado, Media], axis=1)


    return df

def percentual_atrasado():
    df = IntegracaoWms.percentual()

    tira_na = df['NovaPrevisao'].fillna(df['PrevisaoEntrega'])

    df3 =  df['DataEntrega'] > tira_na 

    Percentual_Entregues_Atrasado = (df3.value_counts()[0] / (df3.value_counts()[0] + df3.value_counts()[1]))
    Percentual_Entregues_Atrasado = f'{Percentual_Entregues_Atrasado: .2%}'

    return Percentual_Entregues_Atrasado

def percentual_na_data():
    df = IntegracaoWms.percentual()

    tira_na = df['NovaPrevisao'].fillna(df['PrevisaoEntrega'])

    df3 =  df['DataEntrega'] > tira_na 

    Percentual_Entregas_no_prazo = (df3.value_counts()[1] / (df3.value_counts()[0] + df3.value_counts()[1]))
    Percentual_Entregas_no_prazo = f'{Percentual_Entregas_no_prazo: .2%}'


    return Percentual_Entregas_no_prazo

def percentual_coleta_Prazo():

    df = IntegracaoWms.coleta_prazo()

    df3 =  df['Coletado'] > df['Previsao'] 

    Percentual_Entregas_no_prazo = (df3.value_counts()[1] / (df3.value_counts()[0] + df3.value_counts()[1]))
    Percentual_Entregas_no_prazo = f'{Percentual_Entregas_no_prazo: .2%}'

    return Percentual_Entregas_no_prazo

def percentual_coleta_fora_prazo():

    df = IntegracaoWms.coleta_prazo()

    df3 =  df['Coletado'] > df['Previsao'] 

    Percentual_Entregas_fora_prazo = (df3.value_counts()[0] / (df3.value_counts()[0] + df3.value_counts()[1]))
    Percentual_Entregas_fora_prazo = f'{Percentual_Entregas_fora_prazo: .2%}'

    return Percentual_Entregas_fora_prazo

@home.route("/dashboard/logistica/home", methods=["GET","POST"])
def RelatorioGeral():

    tabela = leadtime()
    tabela = tabela.to_dict('records')
    Entregues_atraso = percentual_atrasado()
    Entregues_prazo = percentual_na_data()
    Coleta_atraso = percentual_coleta_fora_prazo()
    Coleta_no_prazo = percentual_coleta_Prazo()
    # print(Coleta_no_prazo)
    
    return render_template("index.html", tabela = tabela ,Entregues_atraso = Entregues_atraso, Entregues_prazo = Entregues_prazo, Coleta_atraso = Coleta_atraso, Coleta_no_prazo = Coleta_no_prazo, pedidos_ja_atrasados= kpi_pedidos_ja_atrasados, performance_time_transporte = f'{kpi_time_transporte: .1f}', performance_time_logistica = f'{kpi_time_logistica: .1f}')
