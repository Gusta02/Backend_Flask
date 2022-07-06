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
        # df_pipefy = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/pedidos_pipefy.xlsx',usecols=['Numero do pedido'], engine='openpyxl')
        df_pipefy = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/pedidos_pipefy.xlsx',usecols=['Numero do pedido'])
        total_de_pedidos = sql_to_pd(sql.query_total_de_pedidos).iloc[0,0]
        df_pedidos_sem_pipefy = pd.merge(self.df, df_pipefy, left_on=['CodigoPedido'], right_on=['Numero do pedido'], how="outer", indicator=True).query('_merge=="left_only"')
        pedidos_perfeitos = df_pedidos_sem_pipefy.shape[0]
        return round(pedidos_perfeitos/total_de_pedidos,2)

#,tempoLR,pedidoperfeito,separacao,dockstock

class IndicadorPerformance():

    def __init__(self,nota7,nota10,peso=5,notaobtida=0):
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

class DockStockTime(KPI):

    def __init__(self):
        self.df = None
        # self.df1 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 1.xlsx',usecols=['Dt. Inclusão', 'Dt. Fechamento','DockStockTime','DockStockTimeAjustado'], engine='openpyxl')
        self.df1 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 1.xlsx',usecols=['Dt. Inclusão', 'Dt. Fechamento','DockStockTime','DockStockTimeAjustado'])
        # self.df2 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 2.xlsx',usecols=['Dt. Inclusão', 'Dt. Fechamento','DockStockTime'], engine='openpyxl')
        self.df2 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 2.xlsx',usecols=['Dt. Inclusão', 'Dt. Fechamento','DockStockTime'])
        self.nome = "DockStockTime"
        self.indice = self.calcula_indice()

    
    def calcula_indice(self):
        dockmediocliente1 = str(self.df1['DockStockTimeAjustado'].iloc[-1])[:5]
        dockmediocliente2 = str(self.df2['DockStockTime'].iloc[-1])[:5]
        media = (int(dockmediocliente1[0:2]) + int(dockmediocliente1[3:5])/60 + int(dockmediocliente2[0:2]) + int(dockmediocliente2[3:5])/60)/2  #Converte as horas e minutos em ints e calcula a media em horas
        dockformatado1 = dockmediocliente1[0:2] + 'h' + dockmediocliente1[3:5] + 'm'
        dockformatado2 = dockmediocliente2[0:2] + 'h' + dockmediocliente2[3:5] + 'm'
        return {'SP':dockformatado2,'SC':dockformatado1,'Media':media}

class Estoque(KPI):

    def __init__(self):
        self.df = self.multiplica_fator()
        self.indice = self.calcula_indice()
        self.nome = 'Acuracidade_do_Sistema'

    def multiplica_fator(self):
        # df1 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WQ4 - Estoque Mercadorias Cliente WMS - cliente 1.xlsx',usecols=['Cód. Merc.','Qt. Disp.'], engine='openpyxl')
        df1 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WQ4 - Estoque Mercadorias Cliente WMS - cliente 1.xlsx',usecols=['Cód. Merc.','Qt. Disp.'])
        # df2 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WQ4 - Estoque Mercadorias Cliente WMS - cliente 2.xlsx',usecols=['Cód. Merc.','Qt. Disp.'], engine='openpyxl')
        df2 = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/WQ4 - Estoque Mercadorias Cliente WMS - cliente 2.xlsx',usecols=['Cód. Merc.','Qt. Disp.'])
        df_concat = pd.concat([df1,df2])
        df_fator_multiplicador = sql_to_pd(sql.query_fator_multiplicador_prod)
        df_com_fator = pd.merge(df_concat,df_fator_multiplicador.drop_duplicates(subset='SKU'),how='left',left_on='Cód. Merc.',right_on='SKU')
        df_fator_multiplicador = sql_to_pd(sql.query_fator_multiplicador_show_room)
        df_com_fator = df_com_fator.merge(df_fator_multiplicador.drop_duplicates(subset='SKU'),how='left',left_on='Cód. Merc.',right_on='SKU')
        df_com_fator['FatorMultiplicador'] = df_com_fator['FatorMultiplicador_x'].fillna(df_com_fator['FatorMultiplicador_y'])
        df_com_fator.drop(columns=['SKU_x','SKU_y','FatorMultiplicador_x','FatorMultiplicador_y'])
        df_com_fator['QuantidadeAjustada'] = df_com_fator['Qt. Disp.']*df_com_fator['FatorMultiplicador']
        return df_com_fator

    #Acuracidade do Sistema
    def calcula_indice(self):
        df_quantidade_do_sistema = sql_to_pd(sql.query_quantidade_do_sistema)
        df_quantidade_do_sistema['Quantidade'] = df_quantidade_do_sistema['Quantidade'].apply(lambda x: x if x>=0 else 0)
        soma_wms = self.multiplica_fator()['QuantidadeAjustada'].sum()
        soma_sistema = df_quantidade_do_sistema['Quantidade'].sum()
        return soma_wms/soma_sistema

    #Rejeicoes Futuras
    def rejeicoes_futuras(self):
        df_produtos_por_pedido = sql_to_pd(sql.query_produtos_por_pedido)
        grupos_SKU = df_produtos_por_pedido.groupby('SKU')
        return grupos_SKU

class LeadTime(KPI):

    def __init__(self):
        self.df = sql_to_pd(sql.query_entregas_por_estado)
        self.indice = self.calcula_indice()
        self.nome = 'LeadTimeNacional'

    def calcula_indice(self):
        df_por_estado = self.df.groupby(['Estado'])
        entregas_totais = 0
        soma = 0
        for i in df_por_estado.groups.keys():
            grupo = df_por_estado.get_group(i)
            entregas = grupo.shape[0]
            entregas_totais += entregas
            media =  (grupo.loc[:,'DiasPrevistos'] - grupo.loc[:,'Dias']).mean()
            soma += entregas*media
        return soma/entregas_totais
    


    