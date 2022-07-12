import pandas as pd
from datetime import datetime, timedelta, date
from openpyxl import Workbook

hoje = date.today() 
Atual = hoje.strftime('%Y-%m-%d')

trinta = timedelta(days=30)
trinta_dias =hoje + trinta
trinta_dias= trinta_dias.strftime('%Y-%m-%d')

#filtro sessenta dias
sessenta = timedelta(days=60)
sessenta_dias =  hoje + sessenta
sessenta_dias = sessenta_dias.strftime('%Y-%m-%d')

#filtro noventa dias
noventa = timedelta(days=90)
noventa_dias =  hoje+ noventa
noventa_dias = noventa_dias.strftime('%Y-%m-%d')

# A PAGAR FUNÇÕES

def Pagar_30dias():
    
    data = pd.read_excel('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
    'CLIENTE_FORNECEDOR','CNPJ_CPF','OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= trinta_dias)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]

    return Filtro_pagar

def Pagar_60dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
    'CLIENTE_FORNECEDOR','CNPJ_CPF','OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= sessenta_dias)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]
    
    return Filtro_pagar

def Pagar_90dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
    'CLIENTE_FORNECEDOR','CNPJ_CPF','OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= noventa_dias)

    data = data[f1]

    data['TIPO'] == 'CONTAS A PAGAR'
    
    Filtro_pagar = data.loc[data['TIPO'] == 'CONTAS A PAGAR',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]
    
    
    return Filtro_pagar

# A RECEBER FUNÇÕES

def Receber_30dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
    'CLIENTE_FORNECEDOR','CNPJ_CPF','OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= trinta_dias)

    data = data[f1]
    
    data['TIPO'] == 'CONTAS A RECEBER'
    
    Filtro_receber = data.loc[data['TIPO'] == 'CONTAS A RECEBER',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]

    return  Filtro_receber

def Receber_60dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
    'CLIENTE_FORNECEDOR','CNPJ_CPF','OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= sessenta_dias)

    data = data[f1]
    
    data['TIPO'] == 'CONTAS A RECEBER'
    
    Filtro_receber = data.loc[data['TIPO'] == 'CONTAS A RECEBER',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]
  
    return  Filtro_receber

def Receber_90dias():
    data = pd.read_excel('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
    
    data.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
    'CLIENTE_FORNECEDOR','CNPJ_CPF','OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

    data.loc[:,'TIPO'] = data.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())
    data['DATA_VENCIMENTO'] = data['DATA_VENCIMENTO'].apply(lambda k: str(k).split()[0])

    f1 = (data['DATA_VENCIMENTO'] >= Atual) & (data['DATA_VENCIMENTO'] <= noventa_dias)

    data = data[f1]
    
    data['TIPO'] == 'CONTAS A RECEBER'
    
    Filtro_receber = data.loc[data['TIPO'] == 'CONTAS A RECEBER',['DATA_VENCIMENTO','TIPO','CATEGORIA','SITUACAO',
    'CLIENTE_FORNECEDOR','OBSERVACAO_CONTA','VALOR_CONTA']]

    return Filtro_receber