import asyncio
from config import get_connection
from sqlalchemy import text
from datetime import datetime, timedelta,date
from dateutil.relativedelta import *
import pandas as pd

def PedidosBdNovo():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text("""
            	select 
                PF.CodigoPedido,
                FI.SKU,
                NomeProduto,
                Marca,
                FORMAT((Quantidade * PrecoUnitarioDescontado),'c','pt-br') as valorTotal,
                Month(fi.DataInserido) as Mes,
                Year(fi.DataInserido) as Ano
                from HauszMapa.pedidos.itensflexy fi	
                inner join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = fi.SKU
                inner join HauszMapa.Produtos.Marca m on m.IdMarca = pb.IdMarca
                inner join HauszMapa.Pedidos.PedidoFlexy pf on pf.CodigoPedido = fi.CodigoPedido
                where pf.IdEtapaFlexy <> 11 and fi.bitAtivo = 1
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
    
    return lista_dicts

def ShowroomBdNovo():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text("""
            select 
            p.CodigoPedidoSw as CodigoPedido,
            i.SKU,
            NomeProduto,
            Marca,
            FORMAT((i.Quantidade * i.PrecoUnitario),'c','pt-br')as valorTotal,
            month(i.DataInserido) as Mes,
            year(i.DataInserido) as Ano
            from HauszMapa.ShowRoom.ItensPedido i
            inner join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = i.SKU
            inner join HauszMapa.Produtos.Marca m on m.IdMarca = pb.IdMarca
            inner join HauszMapa.ShowRoom.Pedido p on p.CodigoPedidoSw = i.CodigoPedidoSw
            where p.IdEtapaFlexy <> 11 and ValorTotal > 0 and i.bitAtivo = 1
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
    
    return lista_dicts