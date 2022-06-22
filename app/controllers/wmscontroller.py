from asyncio import exceptions
from config import get_connection
from sqlalchemy import text
import pandas as pd
import os
import re

def ajuste_referencia_pedido_corpem(refs_pedido):
    try:
        if re.search('Ped.:', refs_pedido, re.IGNORECASE):
            valor = str(refs_pedido).replace("Ped.:","").strip().split("-")[0]
            return valor
        else:
            return refs_pedido
    except:
        return "error"


def select_log_wms_pedidos():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_log = (text("""
                SELECT  lgpedido.[IdLog],lgpedido.[DeIdEtapaFlexy],lgpedido.[ParaIdEtapaFlexy]
                ,lgpedido.[CodigoPedido],format(pflexy.DataInserido, 'd', 'pt-BR') as datainserido
                ,format(pflexy.DataInseridoOmie, 'd', 'pt-BR') as datainseridoomie
                ,pflexy.IdEtapaFlexy,etflexy.NomeEtapa,etflexy.NomeEtapaFlexy
                ,format(pflexy.PrevisaoEntrega, 'd', 'pt-BR') as previsaodeentrega
                ,pflexy.StatusPedido,lgpedido.[EnviadoWpp]
                ,format(lgpedido.[DataAtualizacao], 'd', 'pt-BR') as dataatualizacao
                ,lgpedido.[DePrazo] ,lgpedido.[ParaPrazo]
                ,lgpedido.[bitSplit],lgpedido.[TipoAlteracao],lgpedido.[IdUsuarioAlteracao]

                FROM [HauszMapa].[Pedidos].[LogPedidos] as lgpedido

                join [HauszMapa].[Pedidos].[PedidoFlexy] as pflexy
                on pflexy.CodigoPedido = lgpedido.CodigoPedido

                join [HauszMapa].[Pedidos].[EtapaFlexy] as etflexy
                on etflexy.IdEtapa = pflexy.IdEtapaFlexy"""))
        excquerylog = conn.execute(query_log).all()
        for exc in excquerylog:
            dict_items = {}
            for keys, values in exc.items():
                
                dict_items[keys] = values
            lista_dicts.append(dict_items)

    data = pd.DataFrame(lista_dicts)

    resumo_data_bdhausz = data[['CodigoPedido','StatusPedido','NomeEtapa','dataatualizacao']]
    atualresumodatahausz = resumo_data_bdhausz.loc[resumo_data_bdhausz['dataatualizacao'] == '09/06/2022']
    atualresumodatahausz['CodigoPedido'] = atualresumodatahausz['CodigoPedido'].astype(str)
    hauszdf = atualresumodatahausz.loc[:,['CodigoPedido']]
    dfhausz = hauszdf['CodigoPedido'].unique()
    return dfhausz


def get_informacoes_wms_corpem():

    datacorpem1 = pd.read_excel(
    'D:\\estatisticas_hausz\\arquivosexcelcorpem\\WD6part1.xlsx',skiprows=[0,1,2,3,4,5])
    datacorpem1.fillna(0, inplace=True)
    datacorpem1['UNIDADECD'] = 'HAUSZ-SC'
    datacorpem2 = pd.read_excel(
        'D:\\estatisticas_hausz\\arquivosexcelcorpem\\WD6part2.xlsx',skiprows=[0,1,2,3,4,5])
    datacorpem2.fillna(0, inplace=True)
    datacorpem2['UNIDADECD'] = 'HAUSZ-SP'

    #filtra todos os valores iniciados em Ped
    datacorpem1['Observação Resumida'].str.contains('^Ped.: ')
    datacorpem2['Observação Resumida'].str.contains('^Ped.: ')
    datacorpem1['REFERENCIASPEDIDOS'] = datacorpem1['Observação Resumida'].apply(
        lambda k: ajuste_referencia_pedido_corpem(k))
    datacorpem1['HAUSZUN'] = 'HAUSZ-SC'
    datacorpem2['REFERENCIASPEDIDOS'] = datacorpem2['Observação Resumida'].apply(
        lambda k: ajuste_referencia_pedido_corpem(k))
    datacorpem2['HAUSZUN'] = 'HAUSZ-SP'
    datacorpem2['REFERENCIASPEDIDOS'] = datacorpem2['REFERENCIASPEDIDOS'].astype(str)
    datacorpem2['REFERENCIASPEDIDOS'] = datacorpem2['REFERENCIASPEDIDOS'].astype(str)

    return datacorpem2


def compara_valores_dataframes():
    datacorpem2 = get_informacoes_wms_corpem()
    dfhausz = select_log_wms_pedidos()
    datahausz = pd.DataFrame(dfhausz, columns=['CodigoPedido'])
    lista_hausz = datahausz['CodigoPedido'].to_list()
    lista_wms = datacorpem2['REFERENCIASPEDIDOS'].to_list()

    valores_em_coum = set(lista_hausz) & set(lista_wms)
    
    
    return valores_em_coum
   


    
   