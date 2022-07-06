from flask import Blueprint, render_template, request
from sqlalchemy import true
from app.Dash_Logistica.kpis_luiz import kpi
from ..controllers.controller_logistica import IntegracaoWms, Transporte
import pandas as pd
from datetime import datetime
from ..Dash_Logistica.kpis_luiz.main import kpi_entregues_no_prazo,kpi_pedidos_ja_atrasados,kpi_pedido_perfeito,kpi_dock_stock_time,kpi_acuracidade_do_sistema, IndicadorPerformance

home = Blueprint('home', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

#PLANILHA PIPE EXCEL - ATUALIZAR UMA VEZ POR SEMANA
# data = pd.read_excel('app/Dash_Logistica/planilha/relatorio_kpi3006.xlsx', engine='openpyxl')
data = pd.read_excel('app/Dash_Logistica/planilha/relatorio_kpi3006.xlsx')

def leadtime():
    tabela = IntegracaoWms.leadtime_log()
    estado = IntegracaoWms.Estados()

    medias = []
    mediasprevistas = []

    for index, row in estado.iterrows():

        Estado = row['estado']

        media = tabela.query(f'Estado=="{Estado}"')
        media = media['Dias']
        media = media.mean()
        media = f'{media: .0f}'
        medias.append(media)
        mediaprevista = tabela.query(f'Estado=="{Estado}"')
        mediaprevista = mediaprevista['DiasPrevistos']
        mediaprevista = mediaprevista.mean()
        mediaprevista = f'{mediaprevista: .0f}'
        mediasprevistas.append(mediaprevista)

    tamanho = len(medias)
    contador = 0
    while (contador < tamanho):

        try: 
            medias[contador] = int(medias[contador])
            mediasprevistas[contador] = int(mediasprevistas[contador])
        except:
            medias[contador] = 'Sem Média de'
            mediasprevistas[contador] = 'Sem Média de'

        contador   = contador + 1    

    Media = pd.DataFrame(medias, columns = ['Media'])
    MediaPrevista = pd.DataFrame(mediasprevistas, columns = ['MediaPrevista'])
    df =pd.concat([estado,Media,MediaPrevista], axis=1)


    return df

def percentual_atrasado():
    df = IntegracaoWms.percentual()

    tira_na = df['NovaPrevisao'].fillna(df['PrevisaoEntrega'])

    df3 =  df['DataEntrega'] > tira_na 
    
    try: 

        Percentual_Entregues_Atrasado = (df3.value_counts()[0] / (df3.value_counts()[0] + df3.value_counts()[1]))
        Percentual_Entregues_Atrasado = f'{Percentual_Entregues_Atrasado: .2%}'

    except:
        Percentual_Entregues_Atrasado = 0

    return Percentual_Entregues_Atrasado

def percentual_na_data():
    df = IntegracaoWms.percentual()

    tira_na = df['NovaPrevisao'].fillna(df['PrevisaoEntrega'])

    df3 =  df['DataEntrega'] > tira_na 

    try:
        Percentual_Entregas_no_prazo = (df3.value_counts()[1] / (df3.value_counts()[0] + df3.value_counts()[1]))
        Percentual_Entregas_no_prazo = f'{Percentual_Entregas_no_prazo: .2%}'
    except:
        Percentual_Entregas_no_prazo = 0


    return Percentual_Entregas_no_prazo

def percentual_coleta_Prazo():

    df = IntegracaoWms.coleta_prazo()

    df3 =  df['Coletado'] > df['Previsao'] 

    try:

        Percentual_coletas_no_prazo = (df3.value_counts()[1] / (df3.value_counts()[0] + df3.value_counts()[1]))
        Percentual_coletas_no_prazo = f'{Percentual_coletas_no_prazo: .2%}'
    
    except:

        Percentual_coletas_no_prazo = 0

    return Percentual_coletas_no_prazo

def percentual_coleta_fora_prazo():

    df = IntegracaoWms.coleta_prazo()

    df3 =  df['Coletado'] > df['Previsao'] 

    try: 

        Percentual_coletas_fora_prazo = (df3.value_counts()[0] / (df3.value_counts()[0] + df3.value_counts()[1]))
        Percentual_coletas_fora_prazo = f'{Percentual_coletas_fora_prazo: .2%}'

    except:

        Percentual_coletas_fora_prazo = 0

    return Percentual_coletas_fora_prazo

#///////////////////   MICHEL  /////////////////////////////
def TotalAvaria(): 
    Avaria = Transporte.Quant_avaria()
    TotalAvaria = Avaria[0]['QuantidadeAvaria']

    return TotalAvaria

def TotalEntregue():
    entregue = Transporte.Quant_entregue()
    totalentregue = entregue[0]['Quantidade_Entregue']

    return totalentregue

def QuantidadeErrada():
    #///////// Renomeando colunas /////////////////////
    data.columns = ['CODIGO', 'FASE_ATUAL', 'CRIADOR', 'PV_CRIADO','NUMERO_PV','NUMERO_NF','MOTIVO_SOLICITACAO'
    ,'OBSERVACOES_SOLICITACAO','FASE_INICIAL'
    ,'FASE_GESTAO','FASE_CLIENTE','FASE_IMPLANTACAO_REPOSICAO','FASE_SHOW_ROOM'
    ,'PEDIDOS_REPROVADOS','FASE_AJUSTE_FISCAL','FASE_LOCALIZACAO_MERCADORIA','ROTEIRIZACAO_PV_LOCALIZADO'
    ,'SOLICITACAO_COLETA'
    ,'COLETA_APROVADA','COLETA_REPROVADA','SOLICITACAO_REEMBOLSO','ENVIO_EMAIL','CONCLUIDO','SEM_REPOSICAO'
    ,'LOCALIZACAO_MERCADORIA']

    #selecionando linha com valor especifico em uma coluna
    data['MOTIVO_SOLICITACAO'] == 'Item entregue na quantidade errada'

    Quantia_errada =  data.loc[data['MOTIVO_SOLICITACAO'] == 'Item entregue na quantidade errada',['CODIGO','NUMERO_PV', 'NUMERO_NF','MOTIVO_SOLICITACAO']]
    
    #contagem total de itens na situação 'Item quantidade_errado'    
    quantidade_errado = len(Quantia_errada)

    return quantidade_errado

def EntregueErrado():
    #///////// Renomeando colunas /////////////////////
    data.columns = ['CODIGO', 'FASE_ATUAL', 'CRIADOR', 'PV_CRIADO','NUMERO_PV','NUMERO_NF','MOTIVO_SOLICITACAO'
    ,'OBSERVACOES_SOLICITACAO','FASE_INICIAL'
    ,'FASE_GESTAO','FASE_CLIENTE','FASE_IMPLANTACAO_REPOSICAO','FASE_SHOW_ROOM'
    ,'PEDIDOS_REPROVADOS','FASE_AJUSTE_FISCAL','FASE_LOCALIZACAO_MERCADORIA','ROTEIRIZACAO_PV_LOCALIZADO'
    ,'SOLICITACAO_COLETA'
    ,'COLETA_APROVADA','COLETA_REPROVADA','SOLICITACAO_REEMBOLSO','ENVIO_EMAIL','CONCLUIDO','SEM_REPOSICAO'
    ,'LOCALIZACAO_MERCADORIA']

    #selecionando linha com valor especifico em uma coluna
    data['MOTIVO_SOLICITACAO'] == 'Item entregue errado'
    
    errado = data.loc[data['MOTIVO_SOLICITACAO'] == 'Item entregue errado',['CODIGO','NUMERO_PV', 'NUMERO_NF','MOTIVO_SOLICITACAO']]

    #contagem total de itens na situação 'Item avariado'
    entregueerrado = len(errado)

    return entregueerrado

def NotaItemfaltante():
    #///////// Renomeando colunas /////////////////////
    data.columns = ['CODIGO', 'FASE_ATUAL', 'CRIADOR', 'PV_CRIADO','NUMERO_PV','NUMERO_NF','MOTIVO_SOLICITACAO'
    ,'OBSERVACOES_SOLICITACAO','FASE_INICIAL'
    ,'FASE_GESTAO','FASE_CLIENTE','FASE_IMPLANTACAO_REPOSICAO','FASE_SHOW_ROOM'
    ,'PEDIDOS_REPROVADOS','FASE_AJUSTE_FISCAL','FASE_LOCALIZACAO_MERCADORIA','ROTEIRIZACAO_PV_LOCALIZADO'
    ,'SOLICITACAO_COLETA'
    ,'COLETA_APROVADA','COLETA_REPROVADA','SOLICITACAO_REEMBOLSO','ENVIO_EMAIL','CONCLUIDO','SEM_REPOSICAO'
    ,'LOCALIZACAO_MERCADORIA']

    #selecionando linha com valor especifico em uma coluna
    data['MOTIVO_SOLICITACAO'] == 'Item presente na Nota Fiscal mas não foi entregue'

    NotaDivergente =  data.loc[data['MOTIVO_SOLICITACAO'] == 'Item presente na Nota Fiscal mas não foi entregue',['CODIGO','NUMERO_PV', 'NUMERO_NF','MOTIVO_SOLICITACAO']]

    #contagem total de itens na situação 'Presente na nota, mas nao entregue'    
    faltandoitem = len(NotaDivergente)

    return faltandoitem

# CARD taxa falha separacao X entregue, PERCENTUAL DE FALHA SEPARAÇÃO / ENTREGUE 
def FalhaSeparacao():
    soma =  QuantidadeErrada() + EntregueErrado() + NotaItemfaltante()  #somando todos os motivos de faLhas da logistica Reversa
    entregue = TotalEntregue()

    taxa = soma / entregue
    taxa = "{:.2%}".format(taxa)
    
    return taxa

#///////////////////////// PERCENTUAL DE TODAS AS FALHAS DE ENTREGA E AVARIAS DO SISTEMA ////////////////////////// 
def FALHAS_E_AVARIAS():
     # ///////////////////////// CARD Taxa de Avaria + falha separação / entregue     ///////////////////////////////
    somatoria = QuantidadeErrada() + EntregueErrado() + NotaItemfaltante() + TotalAvaria()
    entregue =  TotalEntregue()

    taxa_fseparacao_avaria = somatoria / entregue
    taxa_fseparacao_avaria = "{:.2%}".format(taxa_fseparacao_avaria)

    return taxa_fseparacao_avaria

def media_separacao_sp():

    # Sp = pd.read_excel('app/Dash_Logistica/planilha/Producao_SaoPaulo.xlsx', engine='openpyxl')
    Sp = pd.read_excel('app/Dash_Logistica/planilha/Producao_SaoPaulo.xlsx')
    Sp = (Sp['Dt_Conf_Sep'] - Sp['Dt_Inclusao'])
    Sp = Sp.mean()
    Sp = str(Sp)
    horas = Sp[7:9]
    minutos = Sp[10:12]
    SP = horas + 'h' + minutos + 'm'
    valor = int(horas) + int(minutos)/60
    return {'texto':SP,'valor':valor}

#localização mercadoria
def Localizacao_MediaDias():
    data.columns = ['CODIGO', 'FASE_ATUAL', 'CRIADOR', 'PV_CRIADO','NUMERO_PV','NUMERO_NF','MOTIVO_SOLICITACAO'
    ,'OBSERVACOES_SOLICITACAO','FASE_INICIAL'
    ,'FASE_GESTAO','FASE_CLIENTE','FASE_IMPLANTACAO_REPOSICAO','FASE_SHOW_ROOM'
    ,'PEDIDOS_REPROVADOS','FASE_AJUSTE_FISCAL','FASE_LOCALIZACAO_MERCADORIA','ROTEIRIZACAO_PV_LOCALIZADO'
    ,'SOLICITACAO_COLETA'
    ,'COLETA_APROVADA','COLETA_REPROVADA','SOLICITACAO_REEMBOLSO','ENVIO_EMAIL','CONCLUIDO','SEM_REPOSICAO'
    ,'LOCALIZACAO_MERCADORIA']

    media = data.apply(lambda x:x['LOCALIZACAO_MERCADORIA']-x['FASE_LOCALIZACAO_MERCADORIA'],axis=1)
    data.loc[:,'MEDIA'] = media
    media= media.mean()
    media = str(media)
    media = media[0:1] + ' dias'
        

    return media

#///////////////////////////////// END MICHEL //////////////////////////////////

def media_separacao_sc():

    # Sc = pd.read_excel('app/Dash_Logistica/planilha/Producao_SantaCatarina.xlsx', engine='openpyxl')
    Sc = pd.read_excel('app/Dash_Logistica/planilha/Producao_SantaCatarina.xlsx')
    Sc = (Sc['Dt_Conf_Sep'] - Sc['Dt_Inclusao'])
    Sc = Sc.mean()
    Sc = str(Sc)
    horas = Sc[7:9]
    minutos = Sc[10:12]
    SC = horas + 'h' + minutos + 'm'
    valor = int(horas) + int(minutos)/60
    return {'texto':SC,'valor':valor}

#################################### Indicadores de Performance do Time De Logística ############################################

dict_performance_time_logistica = dict(
ind_localizacaoLR = IndicadorPerformance(7,4,5,6) #michel
#,ind_tempocicloLR = IndicadorPerformance(25,20,5,23) #Parece que não está no Asana, remover?
,ind_pedidoperfeito = IndicadorPerformance(80,90,5,kpi_pedido_perfeito*100)
,ind_separacao = IndicadorPerformance(24,18,5,(media_separacao_sc()['valor']+media_separacao_sc()['valor'])) #posso dar o mesmo peso para SP e SC?
,ind_dockstocktime = IndicadorPerformance(3,1.5,4,kpi_dock_stock_time['Media'])
)

kpi_time_logistica = IndicadorPerformance.calcula_kpi_time(dict_performance_time_logistica)

@home.route("/", methods=["GET","POST"])
def RelatorioGeral():

    tabela = leadtime()
    tabela = tabela.to_dict('records')

    dict_variaveis = {
    'Percentual Entregue no Prazo':f'{kpi_entregues_no_prazo: .0%}'
    ,'Percentual de Entregas Atrasadas': f'{1-kpi_entregues_no_prazo: .0%}'
    ,'Percentual de Coletas no Prazo': percentual_coleta_Prazo()
    ,'Percentual de Coletas Fora do Prazo': percentual_coleta_fora_prazo()
    ,'Taxa de Falhas na Separação': FalhaSeparacao()
    ,'Taxa de Falhas na Separação e Avarias':FALHAS_E_AVARIAS()
    ,'Pedidos Ativos Atrasados':kpi_pedidos_ja_atrasados
    ,'Pedidos Perfeitos':f'{kpi_pedido_perfeito: .0%}'
    ,'Acuracidade do Sistema':f'{kpi_acuracidade_do_sistema: .1%}'
    ,'Performance do Time de Logística' : f'{kpi_time_logistica: .1f}' 
    ,'Média de Dias para Separação SP' : media_separacao_sp()['texto']
    ,'Média de Dias para Separação SC' : media_separacao_sc()['texto']
    ,'Dock Stock SP' : kpi_dock_stock_time['SP']
    ,'Dock Stock SC' : kpi_dock_stock_time['SC']
    ,'Localização de Mercadoria - LR' : Localizacao_MediaDias()
    }
    
    return render_template("Relatorio_logistica.html", tabela = tabela, cards = dict_variaveis)