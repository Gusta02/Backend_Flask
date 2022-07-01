from turtle import position
from flask import Blueprint, render_template,current_app, jsonify, request
import os
from ..controllers.relatorios_index_controller import (select_pedidos_data_atual)
import pandas as pd
from ..controllers.relatorios_index_controller import (select_resumo_infos, select_marca_prazo_fabricacao
,select_groupby_saldo_produto, vendas_mes_agrupado)
from ..controllers.controller_logistica import IntegracaoWms

def register_handlers(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Skipping error handlers in Debug mode')
        return

    @current_app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        # retorna server error
        return render_template("500.html"), 500

    @current_app.errorhandler(404)
    def TemplateNotFound(*args, **kwargs):
        # retorna template notfound
        return render_template("404.html"), 404

    @current_app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("404.html"), 404
    
    @current_app.errorhandler(500)
    def ModuleNotFoundError(*args, **kwargs):
        return render_template("500.html"), 500

    @current_app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
        # do stuff
        return render_template("403.html"), 403

    @current_app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        # do stuff
        return render_template("404.html"), 404

    @current_app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
        # do stuff
        return render_template("405.html"), 405

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

index = Blueprint("index",__name__
        ,template_folder='templates',static_folder='static',static_url_path='/static/imagens')
        
@index.route("/", methods=["GET","POST"])
def home():
        tabela = leadtime()
        tabela = tabela.to_dict('records')
        Entregues_atraso = percentual_atrasado()
        Entregues_prazo = percentual_na_data()
        Coleta_atraso = percentual_coleta_fora_prazo()
        Coleta_no_prazo = percentual_coleta_Prazo()
        print(Coleta_no_prazo)
       
        return render_template("index.html", tabela = tabela ,Entregues_atraso = Entregues_atraso, Entregues_prazo = Entregues_prazo, Coleta_atraso = Coleta_atraso, Coleta_no_prazo = Coleta_no_prazo)

register_handlers(current_app)