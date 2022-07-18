import pandas as pd
from datetime import  timedelta, date
import os
from dateutil.relativedelta import *


hoje = date.today() 

class Empresa():

    def __init__(self, planilha) -> None:
        self.planilha = self.set_planilha(planilha)    
    
    def set_planilha(self,planilha):

        df_contas_pagar = pd.read_excel(planilha)

        df_contas_pagar.columns = ['DATA_EMITIDA','DATA_VENCIMENTO','TIPO','ORIGEM','SITUACAO','GRUPO','CATEGORIA',
        'CLIENTE_FORNECEDOR','CNPJ_CPF','OBSERVACAO_CONTA','DOCUMENTO_TIPO','VALOR_CONTA','PAGO_RECEBIDO','A_RECEBER_PAGAR']

        df_contas_pagar.loc[:,'TIPO'] = df_contas_pagar.loc[:,'TIPO'].apply(lambda x: str(x).split('.')[-1].strip().upper())

        return df_contas_pagar

    def filtra_dias(self,dias=0):

        def entre_datas (dia_referencia,dia1,dia2):

            return dia1 <= dia_referencia <= dia2

        dias_timedelta = timedelta(days=dias)
        periodo = __class__.hoje + dias_timedelta
        
        mask = self.planilha['DATA_VENCIMENTO'].apply(lambda x: entre_datas(x,hoje,periodo))
        df_filtrada_dias = self.planilha[mask]

        return df_filtrada_dias                   
   
    def get_valor(self):
        
        soma = self.planilha['VALOR_CONTA'].sum()
        return soma

    def filtra_tipo(self, tipo:str=''):
        
        if tipo:
            df_tipoconta = self.planilha.query(f'TIPO == "{tipo}"')

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
uhome = Empresa('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
,easy = Empresa('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
,implantadora = Empresa('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')
)
uhome = Empresa('app/Dash_Financeiro/planilhas/pivot_202207.xlsx')

valor_pagar = uhome.calcula_tipo('CONTAS A PAGAR')