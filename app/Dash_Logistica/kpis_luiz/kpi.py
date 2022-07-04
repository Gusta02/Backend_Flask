# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 14:23:23 2022

@author: Hausz

"""
from app.Dash_Logistica.kpis_luiz import sql_queries as sql
from app.Dash_Logistica.kpis_luiz.data_extractor import sql_to_pd
from abc import ABC, abstractmethod
from datetime import datetime,date
import dateutil.relativedelta
import math
import pandas as pd

class KPI(ABC):

    @abstractmethod
    def __init__(self):
        self.df = None
        self.indice = None
        self.nome = 'semnome'

    @abstractmethod
    def calcula_indice(self):
        pass

    def gera_excel(self):
        self.df.to_excel(f'out/{self.nome}.xlsx')


class Entregas(KPI):

    def __init__(self):
        self.df = sql_to_pd(sql.query_entregaxprazo)
        self.nome = f"entregas_{(date.today()+dateutil.relativedelta.relativedelta(months=-1)).strftime('%m_%y')}"
        self.indice = self.calcula_indice()

    def calcula_indice(self):
        self.df.drop_duplicates(subset =['CodigoPedido'],inplace=True)
        self.df['entregue_no_prazo'] = self.df['DataDeEntrega'] <= self.df['Prazo']
        self.df['TempoMaximo'] =  self.df['Prazo'] - self.df['DataFoiParaSeparacao']
        self.df['TempoDeEntrega'] = self.df['DataDeEntrega'] - self.df['DataFoiParaSeparacao']
        entregues_no_prazo = self.df['entregue_no_prazo'].value_counts(normalize=True)
        return entregues_no_prazo

class SemEtapas(KPI):

    def __init__(self):
        self.df = sql_to_pd(sql.query_sem_etapas)
        self.nome = 'entregas_por_estado'

    def calcula_indice(self):
        pass

    def calcula_sem_19(self):
        return self.df['DataSaiuParaEntrega'].isna().value_counts(normalize=True)

    def calcula_sem_7(self):
        return self.df['DataFoiParaTransito'].isna().value_counts(normalize=True)

class PedidoPerfeito(KPI):

    def __init__(self):
        self.df = sql_to_pd(sql.query_pedido_perfeito)
        self.indice = None
        self.nome = 'pedido_perfeito'

    def calcula_indice(self):
        df_pipefy = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/pedidos_pipefy.xlsx',usecols=['Numero do pedido'])
        total_de_pedidos = sql_to_pd(sql.query_total_de_pedidos).iloc[0,0]
        df_pedidos_sem_pipefy = pd.merge(self.df, df_pipefy, left_on=['CodigoPedido'], right_on=['Numero do pedido'], how="outer", indicator=True).query('_merge=="left_only"')
        pedidos_perfeitos = df_pedidos_sem_pipefy.shape[0]
        return round(pedidos_perfeitos/total_de_pedidos,2)

#,tempoLR,pedidoperfeito,separacao,dockstock

class IndicadorPerformance():

    def __init__(self,nota7,nota10,peso,notaobtida=0):
        self.peso = peso
        self.nota7 = nota7
        self.nota10 = nota10
        self.notaobtida = notaobtida
        self.fatornota7 = abs(nota7-nota10)/math.log(4,10)

    def trunca_nota(self,nota):

        if nota > 10:
            return 10
        if nota < 0:
            return 0

        return nota
    
    def calcula_nota_ajustada(self):

        try:
            return self.trunca_nota(11-10**((self.notaobtida-self.nota10)/self.fatornota7) if self.nota7-self.nota10 >=0 else 11-10**((self.nota10-self.notaobtida)/self.fatornota7))
        except:
            pass

    @staticmethod
    def calcula_kpi_time(ind):

        peso_total = 0
        valor_total = 0
        for i in ind.values():
            peso_total += i.peso
            valor_total += i.calcula_nota_ajustada()*i.peso
        
        return valor_total/peso_total

class DockStockStime(KPI):

    def __init__(self):
        self.df = None
        self.df1 = pd.read_excel('/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 1.xlsx',usecols=['Dt. Inclusão', 'Dt. Fechamento','DockStockTime','DockStockTimeAjustado'])
        self.df2 = pd.read_excel('/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 2.xlsx',usecols=['Dt. Inclusão', 'Dt. Fechamento','DockStockTime'])
        self.nome = "DockStockTime"
        self.indice = self.calcula_indice()

    
    def calcula_indice(self):
        dockmediocliente1 = self.df1['DockStockTimeAjustado'].iloc[-1]
        dockmediocliente2 = self.df2['DockStockTime'].iloc[-1]
        return {'SP':dockmediocliente2,'SC':dockmediocliente1}