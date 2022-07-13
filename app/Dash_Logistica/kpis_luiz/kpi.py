# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 14:23:23 2022

@author: Luiz Gagliardi

"""
from app.Dash_Logistica.kpis_luiz import sql_queries as sql
from app.Dash_Logistica.kpis_luiz.data_extractor import sql_to_pd
from datetime import datetime, date
import dateutil.relativedelta
import math
import pandas as pd
import locale
import numpy as np



locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")

class Entregas():

    def __init__(self):
        self.df = sql_to_pd(sql.query_entregaxprazo)
        self.nome = f"entregas_{(date.today() + dateutil.relativedelta.relativedelta(months=-1)).strftime('%m_%y')}"
        self.indice = self.calcula_indice()

    
    def calcula_indice(self) -> float:
        self.df.drop_duplicates(subset=['CodigoPedido'], inplace=True)
        self.df['entregue_no_prazo'] = self.df['DataDeEntrega'] <= self.df['Prazo']
        self.df['TempoMaximo'] = self.df['Prazo'] - self.df['DataFoiParaSeparacao']
        self.df['TempoDeEntrega'] = self.df['DataDeEntrega'] - self.df['DataFoiParaSeparacao']
        entregues_no_prazo = self.df['entregue_no_prazo'].value_counts(normalize=True)
        return entregues_no_prazo


class SemEtapas():

    def __init__(self):
        self.df = sql_to_pd(sql.query_sem_etapas)
        self.nome = 'entregas_por_estado'

    def calcula_sem_19(self) -> float:
        return self.df['DataSaiuParaEntrega'].isna().value_counts(normalize=True)

    
    def calcula_sem_7(self) -> float:
        return self.df['DataFoiParaTransito'].isna().value_counts(normalize=True)


class PedidoPerfeito():

    def __init__(self):
        self.df = sql_to_pd(sql.query_pedido_perfeito)
        self.indice = None
        self.nome = 'pedido_perfeito'

    
    def calcula_indice(self) -> float:
        df_pipefy = pd.read_excel('app/Dash_Logistica/kpis_luiz/planilha/pedidos_pipefy.xlsx',
                                  usecols=['Numero do pedido'], engine='openpyxl')
        total_de_pedidos = sql_to_pd(sql.query_total_de_pedidos).iloc[0, 0]
        df_pedidos_sem_pipefy = pd.merge(self.df, df_pipefy, left_on=['CodigoPedido'], right_on=['Numero do pedido'],
                                         how="outer", indicator=True).query('_merge=="left_only"')
        pedidos_perfeitos = df_pedidos_sem_pipefy.shape[0]
        return round(pedidos_perfeitos / total_de_pedidos, 2)


class IndicadorPerformance():

    def __init__(self, nota7: float, nota10: float, peso: int = 5, notaobtida: float = 0):
        self.peso: int = peso
        self.nota7: float = nota7
        self.nota10: float = nota10
        self.notaobtida: float = int(notaobtida) if type(notaobtida) == str else notaobtida
        self.fatornota7: float = abs(nota7 - nota10) / math.log(4, 10)

    def trunca_nota(self, nota):

        if nota > 10:
            return 10
        if nota < 0:
            return 0

        return nota

    def calcula_nota_ajustada(self):

        try:
            return self.trunca_nota(11 - 10 ** ((
                                                            self.notaobtida - self.nota10) / self.fatornota7) if self.nota7 - self.nota10 >= 0 else 11 - 10 ** (
                        (self.nota10 - self.notaobtida) / self.fatornota7))
                        
        except:
            pass

    @staticmethod
    def calcula_kpi_time(ind: dict) -> float:

        peso_total = 0
        valor_total = 0
        for i in ind.values():
            peso_total += i.peso
            valor_total += i.calcula_nota_ajustada() * i.peso

        return valor_total / peso_total


class DockStockTime():

    def __init__(self):
        self.df = None
        self.df1 = pd.read_excel(
            'app/Dash_Logistica/kpis_luiz/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 1.xlsx',
            usecols=['Dt. Inclusão', 'Dt. Fechamento', 'DockStockTime', 'DockStockTimeAjustado'], engine='openpyxl')
        self.df2 = pd.read_excel(
            'app/Dash_Logistica/kpis_luiz/planilha/WEQ - Documentos Entrada - Periodo - Global - cliente 2.xlsx',
            usecols=['Dt. Inclusão', 'Dt. Fechamento', 'DockStockTime'], engine='openpyxl')
        self.nome = "DockStockTime"
        self.indice = self.calcula_indice()

    def calcula_indice(self):
        dockmediocliente1 = str(self.df1['DockStockTimeAjustado'].iloc[-1])[:5]
        dockmediocliente2 = str(self.df2['DockStockTime'].iloc[-1])[:5]
        media = (int(dockmediocliente1[0:2]) + int(dockmediocliente1[3:5]) / 60 + int(dockmediocliente2[0:2]) + int(
            dockmediocliente2[3:5]) / 60) / 2  # Converte as horas e minutos em ints e calcula a media em horas
        dockformatado1 = dockmediocliente1[0:2] + 'h' + dockmediocliente1[3:5] + 'm'
        dockformatado2 = dockmediocliente2[0:2] + 'h' + dockmediocliente2[3:5] + 'm'
        return {'SP': dockformatado2, 'SC': dockformatado1, 'Media': media}


class Estoque():

    def __init__(self):
        self.df, self.df_produtos_nao_encontrados_sistema = self.multiplica_fator()
        self.df_quantidade_do_sistema = self.quantidade_do_sistema()
        self.nome = 'estoque'
        self.indice = self.calcula_indice()
        self.df_rejeicoes_futuras = self.rejeicoes_futuras()
        self.df_produtos_nao_encontrados_wms = self.find_produtos_nao_econtrados_wms()
        self.df_produtos_excesso_wms, self.df_produtos_falta_wms = self.count_estoque()
        self.df_inventario_por_marca = self.inventario().loc[:,['NomeFantasia','Inventário']].groupby('NomeFantasia').agg('sum')
        self.df_inventario_por_marca.Inventário = self.df_inventario_por_marca.Inventário.apply(lambda x: locale.currency(x, grouping=True))
        self.df_vendas_por_mes_por_marca = self.vendas_por_mes_por_marca()
        self.marcas = self.df_vendas_por_mes_por_marca.index.tolist()


    def multiplica_fator(self):
        df1 = pd.read_excel(
            'app/Dash_Logistica/kpis_luiz/planilha/WQ4 - Estoque Mercadorias Cliente WMS - cliente 1.xlsx',
            usecols=['Cód. Merc.', 'Qt. Disp.'], engine='openpyxl')
        df2 = pd.read_excel(
            'app/Dash_Logistica/kpis_luiz/planilha/WQ4 - Estoque Mercadorias Cliente WMS - cliente 2.xlsx',
            usecols=['Cód. Merc.', 'Qt. Disp.'], engine='openpyxl')
        df_concat = pd.concat([df1, df2])
        df_concat['Cód. Merc.'] = df_concat['Cód. Merc.'].apply(lambda x: str(x).strip().upper())
        df_fator_multiplicador = sql_to_pd(sql.query_fator_multiplicador_prod)
        df_fator_multiplicador['SKU'] = df_fator_multiplicador['SKU'].apply(lambda x: str(x).strip().upper())
        df_com_fator = pd.merge(df_concat, df_fator_multiplicador, how='left', left_on='Cód. Merc.', right_on='SKU')
        df_fator_multiplicador = sql_to_pd(sql.query_fator_multiplicador_show_room)
        df_fator_multiplicador['SKU'] = df_fator_multiplicador['SKU'].apply(lambda x: str(x).strip().upper())
        df_com_fator = df_com_fator.merge(df_fator_multiplicador, how='left', left_on='Cód. Merc.', right_on='SKU')
        df_com_fator['FatorMultiplicador'] = df_com_fator['FatorMultiplicador_x'].fillna(
            df_com_fator['FatorMultiplicador_y'])
        df_produtos_nao_encontrados_sistema = df_com_fator[df_com_fator['FatorMultiplicador'].isna()]
        df_produtos_nao_encontrados_sistema = df_produtos_nao_encontrados_sistema.drop(
            columns=['SKU_x', 'SKU_y', 'FatorMultiplicador_x', 'FatorMultiplicador_y', 'FatorMultiplicador'])
        df_com_fator['FatorMultiplicador'] = df_com_fator['FatorMultiplicador'].fillna(1)
        df_com_fator.drop(columns=['SKU_x', 'SKU_y', 'FatorMultiplicador_x', 'FatorMultiplicador_y'], inplace=True)
        df_com_fator['QuantidadeAjustada'] = df_com_fator['Qt. Disp.'] * df_com_fator['FatorMultiplicador']
        return (df_com_fator, df_produtos_nao_encontrados_sistema)

    def quantidade_do_sistema(self):
        df_quantidade_do_sistema = sql_to_pd(sql.query_quantidade_do_sistema)
        df_quantidade_do_sistema = df_quantidade_do_sistema.drop(columns=['IdProduto', 'IdEstoque'])
        df_quantidade_do_sistema.dropna(inplace=True)
        df_quantidade_do_sistema['Quantidade'] = df_quantidade_do_sistema['Quantidade'].apply(
            lambda x: x if x >= 0 else 0)
        df_quantidade_do_sistema['CodigoProduto'] = df_quantidade_do_sistema['CodigoProduto'].apply(
            lambda x: str(x).strip().upper())
        df_quantidade_do_sistema = df_quantidade_do_sistema.groupby('CodigoProduto').agg('sum')
        return df_quantidade_do_sistema.reset_index()

    def find_produtos_nao_econtrados_wms(self):
        df_produtos_com_estoque = self.df_quantidade_do_sistema[self.df_quantidade_do_sistema['Quantidade'] > 0]
        df_merge = self.df.merge(df_produtos_com_estoque, how='right', left_on='Cód. Merc.', right_on='CodigoProduto')
        df_merge = df_merge[df_merge['Cód. Merc.'].isna()]
        df_merge = df_merge.drop(columns=['Cód. Merc.', 'Qt. Disp.', 'FatorMultiplicador', 'QuantidadeAjustada'])
        return df_merge

    # Acuracidade do Sistema
    def calcula_indice(self):
        soma_wms = self.df['QuantidadeAjustada'].sum()
        soma_sistema = self.df_quantidade_do_sistema['Quantidade'].sum()
        return soma_wms / soma_sistema

    def rejeicoes_futuras(self):
        df_produtos_por_pedido = sql_to_pd(sql.query_produtos_por_pedido)
        grupos_SKU = df_produtos_por_pedido.groupby('SKU', observed=True)
        pedidos_rejeicao = pd.DataFrame(
            columns=['CodigoPedido', 'SKU', 'QuantidadePedida', 'IdEstoque', 'StatusPedido', 'TipoPedido'])
        for k in grupos_SKU.groups.keys():
            try:
                temp = self.df[self.df['Cód. Merc.'] == k]
                qt_estoque = temp.QuantidadeAjustada.iloc[0]
                grupo = grupos_SKU.get_group(k)
                for index, row in grupo.iterrows():
                    qt_estoque -= row['QuantidadePedida']
                    if qt_estoque < 0:
                        qt_estoque += row['QuantidadePedida']
                        pedidos_rejeicao = pd.concat([pedidos_rejeicao, grupo.loc[index:index,
                                                                        ['CodigoPedido', 'SKU', 'QuantidadePedida',
                                                                         'IdEstoque', 'StatusPedido', 'TipoPedido']]])
            except:
                pass

        return pedidos_rejeicao

    def count_estoque(self):

        def classify(x):
            if x == 0:
                return 0
            if x > 0:
                return 'excesso'
            if x < 0:
                return 'falta'

        diff = pd.merge(self.df_quantidade_do_sistema, self.df, how='outer', left_on='CodigoProduto',
                        right_on='Cód. Merc.')
        # return diff
        diff['diferenca'] = diff['QuantidadeAjustada'] - diff['Quantidade']
        diff['situacao'] = diff['diferenca'].apply(lambda x: classify(x))
        df_excesso = diff.query('situacao == "excesso"')
        df_excesso = df_excesso.drop(columns=['Cód. Merc.', 'FatorMultiplicador', 'Qt. Disp.', 'diferenca', 'situacao'])
        df_excesso.rename(columns={'Quantidade': 'Quantidade Sistema', 'QuantidadeAjustada': 'Quantidade WMS'})
        df_excesso.reset_index(inplace=True)
        df_falta = diff.query('situacao == "falta"')
        df_falta = df_falta.drop(columns=['Cód. Merc.', 'FatorMultiplicador', 'Qt. Disp.', 'diferenca', 'situacao'])
        df_falta.rename(columns={'Quantidade': 'Quantidade Sistema', 'QuantidadeAjustada': 'Quantidade WMS'})
        df_falta.reset_index(inplace=True)
        return df_excesso, df_falta

    def inventario(self,marca:str='')->object:

        df_preco = sql_to_pd(sql.query_preco_produtos_estoque)

        if marca:
            df_preco = df_preco.query(f'NomeFantasia == "{marca}"')

        df_preco_com_estoque = self.df.merge(df_preco,left_on='Cód. Merc.',right_on='SKU')
        df_preco_com_estoque['Inventário'] = df_preco_com_estoque['Preco']*df_preco_com_estoque['QuantidadeAjustada']
        return df_preco_com_estoque

    def vendas_por_mes_por_marca(self)->object:
        
        df_vendas = sql_to_pd(sql.query_vendas_ano_atual)
        df_vendas = df_vendas.loc[:,['NomeFantasia','DataDaVenda','ValorVenda']]
        df_vendas.DataDaVenda = df_vendas.DataDaVenda.apply(lambda x: datetime.strptime(x,'%d/%m/%Y').month)
        df_vendas = df_vendas.groupby(['DataDaVenda','NomeFantasia']).agg('sum').unstack(0)
        df_vendas = df_vendas.fillna(0)
        df_vendas = df_vendas.applymap(lambda x: round(float(x),2))

        return df_vendas

    def calcula_venda_total(self,marca:str=''):

        return self.filtra_marca(marca).sum()


    def filtra_marca(self,marca:str=''):

        if marca:
            df_vendas = self.df_vendas_por_mes_por_marca.query(f'NomeFantasia == "{marca}"').sum()
        else:
            df_vendas = self.df_vendas_por_mes_por_marca.sum()

        return df_vendas
    
    def calcula_pct(self,marca:str=''):
        pct = self.filtra_marca(marca).ValorVenda.pct_change().apply(lambda x: round(x*100,1)).fillna(0)
        pct = pct.replace([np.inf, -np.inf], 0)
        pct = pct.tolist()
        pct[0] = 0
        return pct

        
class LeadTime():

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
            media = (grupo.loc[:, 'DiasPrevistos'] - grupo.loc[:, 'Dias']).mean()
            soma += entregas * media
        return soma / entregas_totais
