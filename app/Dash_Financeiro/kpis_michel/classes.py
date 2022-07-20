import pandas as pd
from datetime import  timedelta, date
import os
from dateutil.relativedelta import *




class Empresa():

    hoje = date.today() 

    def __init__(self, planilha=None) -> None:

        if planilha:
            self.planilha = self.set_planilha(planilha)
            self.planilha_filtrada = self.planilha 
    
    def set_planilha(self,planilha):

        df_contas_pagar = pd.read_excel(planilha)

        df_contas_pagar.columns =  ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
        'OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

        df_contas_pagar.loc[:,'TIPO'] = df_contas_pagar.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())

        return df_contas_pagar

    def filtra_dias(self,dias=0) -> object:

        def entre_datas (dia_referencia,dia1,dia2):

           return pd.Timestamp(dia1) <= pd.Timestamp(dia_referencia) <= pd.Timestamp(dia2)

        dias_timedelta = timedelta(days=dias)
        periodo = __class__.hoje + dias_timedelta
        
        mask = self.planilha['DATA_VENCIMENTO'].apply(lambda x: entre_datas(x,__class__.hoje,periodo))
        df_filtrada_dias = self.planilha[mask]

        self.planilha_filtrada = df_filtrada_dias

        return df_filtrada_dias                   
   
    def get_valor(self):
        
        soma = self.planilha_filtrada['VALOR_CONTA'].sum()
        return soma

    def filtra_tipo(self, tipo:str=''):
        
        if tipo:
            df_tipoconta = self.planilha_filtrada.query(f'TIPO == "{tipo}"')

        return df_tipoconta

    def calcula_tipo(self,tipo:str=''):
        
        somatipo = self.filtra_tipo(tipo).VALOR_CONTA.sum()

        return  somatipo
    
    @staticmethod
    def get_todas_empresas(dicionario):

        def pega_dfs (objeto):
            return objeto.planilha

        lista_dfs = list(map(pega_dfs,dicionario.values()))

        df_todas_empresas = pd.concat(lista_dfs,axis=0)

        return df_todas_empresas
    





dict_empresas = dict(
Artse = Empresa('app/Dash_Financeiro/planilhas/artse.xlsx')
,Easy = Empresa('app/Dash_Financeiro/planilhas/easy.xlsx')
,Hausz = Empresa('app/Dash_Financeiro/planilhas/hausz.xlsx')
,Logz = Empresa('app/Dash_Financeiro/planilhas/logz.xlsx')
,Supply = Empresa('app/Dash_Financeiro/planilhas/supply.xlsx')
,Uhome = Empresa('app/Dash_Financeiro/planilhas/uhome.xlsx')
,Vns = Empresa('app/Dash_Financeiro/planilhas/VNS.xlsx')
)

lista_planilhas = Empresa.get_todas_empresas(dict_empresas)

todas_empresas = Empresa()

todas_empresas.planilha = lista_planilhas

dict_empresas['Todas'] = todas_empresas


uhome = Empresa('app/Dash_Financeiro/planilhas/uhome.xlsx')

valor_pagar = uhome.calcula_tipo(tipo='CONTAS A PAGAR')

artse = Empresa('app/Dash_Financeiro/planilhas/artse.xlsx')

colunas_fc = []
colunas_cp = []
colunas_cr = []
periodos = [15,30,60,90,360]

for i in periodos:
    linha_fc = []
    linha_cp = []
    linha_cr = []
    for j in dict_empresas.values():
        j.filtra_dias(i)
        linha_fc.append(j.get_valor())
        linha_cp.append(j.calcula_tipo('CONTAS A PAGAR'))
        linha_cr.append(j.calcula_tipo('CONTAS A RECEBER'))
    colunas_fc.append(linha_fc)
    colunas_cp.append(linha_cp)
    colunas_cr.append(linha_cr)

df_fc = pd.DataFrame(colunas_fc,index=periodos,columns=dict_empresas.keys())
df_fc = df_fc.transpose()

df_cp = pd.DataFrame(colunas_cp,index=periodos,columns=dict_empresas.keys())
df_cp = df_cp.transpose()

df_cr = pd.DataFrame(colunas_cr,index=periodos,columns=dict_empresas.keys())
df_cr = df_cr.transpose()