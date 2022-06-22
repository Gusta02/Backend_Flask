from asyncio import exceptions
from config import get_connection
from sqlalchemy import text
import pandas as pd

#Select tables HauszMapa

def select_resumo_infos():
    lista_dicts = []
    #Select tables ProdutoBasico/Estoque/Marca
    engine = get_connection()
    with engine.connect() as conn:
        querychartindex = (text("""
            SELECT brand.Marca,basico.[SKU],basico.[NomeProduto]
            ,basico.[EstoqueAtual], estoq.NomeEstoque,basico.[SaldoAtual]
            FROM [HauszMapa].[Produtos].[ProdutoBasico] basico
            join [HauszMapa].[Produtos].[Marca] as brand
            on brand.IdMarca = basico.IdMarca
            join [HauszMapa].[Estoque].[Estoque] estoq
            on estoq.IdEstoque = basico.EstoqueAtual
            where estoq.NomeEstoque in ('Fisico')"""))
        excquerychartindex = conn.execute(querychartindex).all()
        for exc in excquerychartindex:
            dict_items = {}
            for keys, values in exc.items():
                
                dict_items[keys] = values
            lista_dicts.append(dict_items)
            
    data = pd.DataFrame(lista_dicts)
    return data

def select_groupby_saldo_produto():
    lista_dicts = []
    #Select tables ProdutoBasico/Estoque/Marca
    engine = get_connection()
    with engine.connect() as conn:
        querychartindex = (text("""
            SELECT count(estoq.[NomeEstoque]) as produtoscomsaldo,estoq.[NomeEstoque]
            ,brand.Marca
            FROM [HauszMapa].[Estoque].[Estoque] AS estoq
            join [HauszMapa].[Produtos].[ProdutoBasico] as basico
            on basico.EstoqueAtual = estoq.IdEstoque
            join [HauszMapa].[Produtos].[Marca] as brand
            on brand.IdMarca = basico.IdMarca
            where estoq.NomeEstoque in ('Matriz','Fisico','Virtual','Fabrica','Encomenda')
            group by estoq.[NomeEstoque],brand.Marca"""))
        excquerychartindex = conn.execute(querychartindex).all()
        for exc in excquerychartindex:

            dict_items = {}
            try:
                for keys, values in exc.items():

                        dict_items[keys] = values
                        
                lista_dicts.append(dict_items)
            except:
                return 'Error'
              
    data = pd.DataFrame(lista_dicts)
 
    return data

def select_marca_prazo_fabricacao():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        querymarcasprazo = (text("""SELECT [Marca],[PrazoFabricacao]
                FROM [HauszMapa].[Produtos].[Marca]"""))
            
        execquerymarcasprazo = conn.execute(querymarcasprazo).all()
        for exec in execquerymarcasprazo:
            dict_items = {}
            for keys, values in exec.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
            
    return lista_dicts


def vendas_mes_agrupado():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        queryvendasprazo = (text("""SELECT sum(iflexy.[PrecoUnitario]) as totalpedido
                            ,sum(pflexy.[PrecoFrete]) as totalfrete
                            ,format(iflexy.[DataInserido], 'd', 'pt-BR') as datainserido
                            ,sum(pflexy.Split) as totalesplit
                            FROM [HauszMapa].[Pedidos].[ItensFlexy] as iflexy
                            join [HauszMapa].[Pedidos].[PedidoFlexy] as pflexy
                            on pflexy.CodigoPedido = iflexy.CodigoPedido
                            where format(iflexy.[DataInserido], 'd', 'pt-BR') like '%/2022%'
                            group by iflexy.[PrecoUnitario], pflexy.[PrecoFrete],pflexy.Split
                            ,format(iflexy.[DataInserido], 'd', 'pt-BR')"""))
            
        execqueryvendasprazo = conn.execute(queryvendasprazo).all()
        for exc in execqueryvendasprazo:
            dict_items = {}
            for keys, values in exc.items():
                
                dict_items[keys] = values
            
            lista_dicts.append(dict_items)

    data = pd.DataFrame(lista_dicts)

    data['datainserido'] = data['datainserido'].astype('datetime64')
    data['mes_ano'] = data['datainserido'].map(lambda x: 100*x.year + x.month)
    data['mes_ano'] = data['mes_ano'].apply(lambda k: str(k).replace("2022","").strip())
    data['mes_ano'] = data['mes_ano'].astype(int)
    data['totalfrete'] = data['totalfrete'].astype(float)
    data['totalesplit'] = data['totalesplit'].astype(float)
    data['totalpedido'] = data['totalpedido'].astype(float)
    

    data = data.groupby(['mes_ano']).sum().reset_index()
    data['Ano'] = '2022'
    data['Ano'] = data['Ano'].astype(int)
    data = data[['totalpedido','Ano','mes_ano','totalfrete','totalesplit']]
    data['totalfrete'] = data['totalfrete'].apply(lambda k: round(k,2))
    data['totalpedido'] = data['totalpedido'].apply(lambda k: round(k,2))
    data['totalesplit'] = data['totalesplit'].apply(lambda k: round(k,2))
    jsons = data.to_dict('records')
    
    return jsons


def select_pedidos_data_atual(data):
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        querpedidosdia = (text("""SELECT pflexy.[CodigoPedido],format(pflexy.DataInserido, 'd', 'pt-BR') as datainserido
                ,format(pflexy.DataInseridoOmie, 'd', 'pt-BR') as datainseridoomie
                ,pflexy.IdEtapaFlexy,etflexy.NomeEtapa
                ,format(pflexy.PrevisaoEntrega, 'd', 'pt-BR') as previsaodeentrega
                FROM [HauszMapa].[Pedidos].[PedidoFlexy] as pflexy

                join [HauszMapa].[Pedidos].[EtapaFlexy] as etflexy
                on etflexy.IdEtapa = pflexy.IdEtapaFlexy
                UNION 
                SELECT pflexy.[CodigoPedidoSw],format(pflexy.DataInserido, 'd', 'pt-BR') as datainserido
                ,format(pflexy.DataInseridoOmie, 'd', 'pt-BR') as datainseridoomie
                ,pflexy.IdEtapaFlexy,etflexy.NomeEtapa
                ,format(pflexy.PrevisaoEntrega, 'd', 'pt-BR') as previsaodeentrega
                FROM [HauszMapa].[ShowRoom].[Pedido] pflexy
                join [HauszMapa].[Pedidos].[EtapaFlexy] as etflexy
                on etflexy.IdEtapa = pflexy.IdEtapaFlexy"""))
            
        execquerpedidosdia = conn.execute(querpedidosdia).all()
        for exc in execquerpedidosdia:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
    datapedido = pd.DataFrame(lista_dicts)
    dataatual = datapedido.loc[datapedido['datainserido'] == data]
    jsons = dataatual.to_dict('records')

    return jsons

