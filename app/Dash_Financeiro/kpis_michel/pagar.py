import pandas as pd
from datetime import timedelta, date
from dateutil.relativedelta import *

hoje = date.today() 
Atual = hoje.strftime('%Y-%m-%d')

#filtro 15 dias 
quinze = timedelta(days=15)
quinze_dias =  hoje + quinze
quinze_dias = quinze_dias.strftime('%Y-%m-%d')

#filtro 30 dias 
trinta = timedelta(days=30)
trinta_dias =hoje + trinta
trinta_dias= trinta_dias.strftime('%Y-%m-%d')

#filtro 60 dias
sessenta = timedelta(days=60)
sessenta_dias =  hoje + sessenta
sessenta_dias = sessenta_dias.strftime('%Y-%m-%d')

#filtro 90 dias
noventa = timedelta(days=90)
noventa_dias =  hoje+ noventa
noventa_dias = noventa_dias.strftime('%Y-%m-%d')

#filtro 12 meses
doze =  (hoje) + relativedelta(months= 12)
doze_meses =  doze.strftime('%Y-%m-%d')


# filtro os dados do dia atual até os proximos 15 dias
def Pagar_15dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/uhome.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
        'OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= quinze_dias)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]

    return Filtro_pagar


# filtro os dados do dia atual até os proximos 30 dias
def Pagar_30dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/uhome.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
        'OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= trinta_dias)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]

    return Filtro_pagar


# filtro os dados do dia atual até os proximos 60 dias
def Pagar_60dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/uhome.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
        'OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= sessenta_dias)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]
    
    return Filtro_pagar


# filtro os dados do dia atual até os proximos 90 dias
def Pagar_90dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/uhome.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
        'OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= noventa_dias)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]

    return Filtro_pagar


# filtro os dados do dia atual até os proximos 12 meses
def Pagar_12meses():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/uhome.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
        'OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= doze_meses)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]

    return Filtro_pagar
