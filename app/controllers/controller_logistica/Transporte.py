from asyncio import exceptions
from config import get_connection
from sqlalchemy import text
from datetime import date,datetime
from dateutil.relativedelta import *

import pandas as pd
#relacionando datas 
#dia
hoje  = datetime.today()
#mes
mes_atual = date.today().strftime('%Y-%m')
#mes passado
passado = (hoje)+relativedelta(months=-1)
mespassado = passado.strftime('%Y-%m')

#////////////////////////// CONSULTAS MICHEL   ///////////////////////////////////

#consulta do BD em cima da tabela  select * from HauszMapa.Pedidos.LogPedidos where ParaIdEtapaFlexy = 9
def Quant_entregue():
    engine = get_connection()
    list_entregue = []
    with engine.connect() as conn:
        query_entregue  = (text(f"""
        select COUNT(lg.CodigoPedido) as Quantidade_Entregue from HauszMapa.Pedidos.LogPedidos lg
        JOIN (SELECT CodigoPedido
        ,MAX(IdLog) ultimaetapa
        FROM [HauszMapa].[Pedidos].[LogPedidos]
        WHERE IdUsuarioAlteracao = 'Aplicacao'
        GROUP BY CodigoPedido) maxlog
        ON maxlog.CodigoPedido = lg.CodigoPedido
        where ParaIdEtapaFlexy = 9 
		AND lg.IdLog = maxlog.ultimaetapa
        AND DataAtualizacao between '{mespassado}-01' and '{mes_atual}-01'
		AND IdUsuarioAlteracao = 'Aplicacao'
        """))
        lista_entreguetotal = conn.execute(query_entregue).all()
        for lista in lista_entreguetotal:
            dict_filtro_hoje = {}
            for keys, values in lista.items():
                dict_filtro_hoje[keys] = values
            list_entregue.append(dict_filtro_hoje)

    return list_entregue

#consulta do BD em cima da tabela  select *  from HauszMapa.Logistica.LogReversaOcorrencia = 1
def Quant_avaria():
    engine = get_connection()
    list_avaria = []
    with engine.connect() as conn:
        query_avaria = (text(f"""
        select count(avarias.Avarias) QuantidadeAvaria from
        (select  DISTINCT lr.CodigoPedido Avarias
		from HauszMapa.Logistica.LogReversaOcorrencia lr
		join(select CodigoPedido, max(IdOcorrencia) ultimaetapa ,max(DataInserido) ultimadata
		from HauszMapa.Logistica.LogReversaOcorrencia 
		where IdCausaOcorrencia = 1
		GROUP BY CodigoPedido) maxlog on maxlog.CodigoPedido = lr.CodigoPedido
		--where lr.IdCausaOcorrencia = 1
		and DataInserido between '{mespassado}-01' and '{mes_atual}-01') avarias
        """))
        lista_avaria = conn.execute(query_avaria).all()
        for lista in lista_avaria:
            dict_avaria = {}
            for keys, values in lista.items():
                dict_avaria[keys] = values
            list_avaria.append(dict_avaria)

    return list_avaria

#///////////////////////////// FIM CONSULTAS MICHEL//////////////////

def Valor_arrecadado_frete_pedido():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text(f"""
            SELECT (SUM(PrecoFrete)*1.0175) as FreteRecebido
            FROM HauszMapa.Pedidos.PedidoFlexy
            WHERE IdEtapaFlexy NOT IN  (1,11,15,16,26,41)
            AND MONTH(DataInserido) = MONTH(GETDATE()) and DesmPedido = 0
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
        df = pd.DataFrame(lista_dicts)
    return df

def Valor_arrecadado_frete_showroom():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text(f"""
            SELECT (SUM(PrecoFrete)*1.0175) as FreteRecebido
            FROM HauszMapa.ShowRoom.Pedido
            WHERE IdEtapaFlexy NOT IN  (1,11,15,16,26,41)
            AND MONTH(DataInserido) = MONTH(GETDATE()) and DesmPedido = 0
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
        df = pd.DataFrame(lista_dicts)
    return df

def percentual_coleta_Prazo():

    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text(f"""
            select 
            DISTINCT pc.CodigoPedidoCompra,
            Format(MAX(Coletado.DataAtualizacao),'d','pt-br') as Coletado,
            FORMAT(MAX(pc.PrevisaoEntrega),'d','pt-br') as Previsao
            from HauszMapa.Pedidos.PedidoCompraItens pc
            inner join (select DataAtualizacao, CodigoPedidoCompra from HauszMapa.Pedidos.LogPedidoCompraItens 
            where ParaStatusItem = 15 and DataAtualizacao between '2022-06-01' and '2022-07-01') Coletado on Coletado.CodigoPedidoCompra = pc.CodigoPedidoCompra
            where bitAtivo = 1 and pc.DataLiberadoColeta <> ''
            Group by pc.CodigoPedidoCompra, pc.IdProduto,pc.DataLiberadoColeta, coletado.DataAtualizacao
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
        df = pd.DataFrame(lista_dicts)
    return df

def percentual_coleta_fora_prazo():

    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text(f"""
            select 
            DISTINCT pc.CodigoPedidoCompra,
            Format(MAX(Coletado.DataAtualizacao),'d','pt-br') as Coletado,
            FORMAT(MAX(pc.PrevisaoEntrega),'d','pt-br') as Previsao
            from HauszMapa.Pedidos.PedidoCompraItens pc
            inner join (select DataAtualizacao, CodigoPedidoCompra from HauszMapa.Pedidos.LogPedidoCompraItens 
            where ParaStatusItem = 15 and DataAtualizacao between '2022-05-01' and '2022-06-01') Coletado on Coletado.CodigoPedidoCompra = pc.CodigoPedidoCompra
            where bitAtivo = 1 and pc.DataLiberadoColeta <> ''
            Group by pc.CodigoPedidoCompra, pc.IdProduto,pc.DataLiberadoColeta, coletado.DataAtualizacao
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
        df = pd.DataFrame(lista_dicts)
    return df

