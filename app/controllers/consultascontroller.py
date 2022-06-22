from asyncio import exceptions
from config import get_connection
from sqlalchemy import text

from flask import render_template,abort


def retorna_produtos_estoques(skus):
    lista_dicts = []
    try:
        for sku in skus:
            if type(sku) == dict:
                try:
                    referencia = sku["SKU"]
                    print(referencia)
                    saldos = sku["SALDO"]
                    prazos = sku["PRAZO"]
                    dataatual= sku["DATA"]
                    engine = get_connection()
                    with engine.connect() as conn:
                        queryskuproduto = (text("""SELECT brand.IdMarca,brand.Marca,basico.[SKU],basico.[NomeProduto],basico.[SaldoAtual],basico.[EAN]
                        FROM [HauszMapa].[Produtos].[ProdutoBasico] as basico
                        join Produtos.Marca as brand
                        on brand.IdMarca = basico.IdMarca
                        where basico.SKU IN ('{}')
                        """.format(referencia)))
                        execquerysku = conn.execute(queryskuproduto).all()
                        
                        cont = len(execquerysku)

                        if cont >0:
                            for produto in execquerysku:
                                dict_items = {
                                    "SKU":str(produto["SKU"]),
                                    "NomeProduto":produto["NomeProduto"],
                                    "SALDO":saldos,
                                    "IDMarca":produto["IdMarca"],
                                    "MARCA":produto["Marca"],
                                    "DATAATUAL":dataatual}

                            
                                lista_dicts.append(dict_items)
                except exceptions as e:

                    print("no retorno dos dicts errorr")

        return lista_dicts
    except:
        print("error")
        
def select_produtos():

    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = (text("""
            DECLARE @PageNumber AS INT
            DECLARE @RowsOfPage AS INT
            SET @PageNumber= 1
            SET @RowsOfPage= 6
            SELECT   basico.IdProduto,brand.IdMarca,brand.Marca,basico.[SKU],basico.[NomeProduto]
            ,basico.[EAN],basico.[SaldoAtual]
            FROM [HauszMapa].[Produtos].[ProdutoBasico] as basico
            join Produtos.Marca as brand
            on brand.IdMarca = basico.IdMarca
            ORDER BY basico.IdProduto
            OFFSET (@PageNumber-1)*@RowsOfPage ROWS
            FETCH NEXT @RowsOfPage ROWS ONLY"""))
        produtos = conn.execute(query_produtos)
        for produto in produtos:
            dict_items = {}
            for keys, values in produto.items():
                dict_items[keys] = values
                lista_dicts.append(dict_items)

    return lista_dicts
  
  
def retorna_all_produtos(page):
    lista_produtos = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = (text("""
            DECLARE @PageNumber AS INT
            DECLARE @RowsOfPage AS INT
            SET @PageNumber= {}
            SET @RowsOfPage= 10
            SELECT brand.Marca,detalhe.UrlImagem,basico.[SKU],basico.[NomeProduto],basico.[SaldoAtual]
            ,basico.[Peso],basico.[PesoCubado],detalhe.Descricao,detalhe.FatorMultiplicador,
            detalhe.FatorUnitario,detalhe.FatorVenda,detalhe.Garantia,detalhe.TamanhoBarra
            ,detalhe.QuantidadeMinima,detalhe.Altura,detalhe.Largura,detalhe.Comprimento
            FROM [HauszMapa].[Produtos].[ProdutoBasico] as basico
            join Produtos.ProdutoDetalhe as detalhe
            on detalhe.SKU = basico.SKU
            join Produtos.Marca as brand
            on brand.IdMarca = basico.IdMarca
            ORDER BY basico.IdProduto
            OFFSET (@PageNumber-1)*@RowsOfPage ROWS
            FETCH NEXT @RowsOfPage ROWS ONLY """.format(page)))
        
        produtos = conn.execute(query_produtos)
        for produto in produtos:
            dict_items = {}
            for keys, values in produto.items():
            
                dict_items[keys] = values
                print("ESTARTOUOOOOOOOOOOOOOOOO all produtos")
                
            lista_produtos.append(dict_items)

    return lista_produtos

def retorna_cadastros_novos(page):
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = (text("""
            DECLARE @PageNumber AS INT
            DECLARE @RowsOfPage AS INT
            SET @PageNumber= {}
            SET @RowsOfPage= 10
            SELECT basico.IdProduto,detalhe.UrlImagem,detalhe.Descricao,brand.IdMarca,brand.Marca
            ,basico.[SKU],basico.[NomeProduto],basico.[EAN]
            FROM [HauszMapa].[Produtos].[ProdutoBasico] as basico
            join [HauszMapa].[Produtos].[ProdutoDetalhe] as detalhe
            on detalhe.SKU = basico.SKU
            join Produtos.Marca as brand
            on brand.IdMarca = basico.IdMarca
            where detalhe.UrlImagem IS NOT NULL and detalhe.UrlImagem <> '0'
            ORDER BY basico.IdProduto
            OFFSET (@PageNumber-1)*@RowsOfPage ROWS
            FETCH NEXT @RowsOfPage ROWS ONLY""".format(page)))
            
        produtos = conn.execute(query_produtos)
        for produto in produtos:
            dict_items = {}
            for keys, values in produto.items():
                dict_items[keys] = values
                print("ESTARTOUOOOOOOOOOOOOOOOO all cadastro novo")

            lista_dicts.append(dict_items)
                
    return lista_dicts

def select_prazos_fabricantes(page):
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_prazosprodutos = (text("""
            DECLARE @PageNumber AS INT
            DECLARE @RowsOfPage AS INT
            SET @PageNumber= {}
            SET @RowsOfPage= 10
            SELECT brand.Marca,brand.IdMarca,brand.PrazoFabricacao,basico.NomeProduto,prazo.[SKU],prazo.[PrazoEstoqueFabrica],prazo.[PrazoProducao]
            ,prazo.[PrazoOperacional],prazo.[PrazoFaturamento],prazo.[PrazoTotal]
            FROM [HauszMapa].[Produtos].[ProdutoPrazoProducFornec] as prazo
            join Produtos.ProdutoBasico as basico
            on basico.SKU = prazo.SKU
            join Produtos.Marca as brand
            on brand.IdMarca = basico.IdMarca
            ORDER BY basico.IdProduto
            OFFSET (@PageNumber-1)*@RowsOfPage ROWS
            FETCH NEXT @RowsOfPage ROWS ONLY""".format(page)))

        produtos = conn.execute(query_prazosprodutos)
        for produto in produtos:
            dict_items = {}
            for keys, values in produto.items():
                
                dict_items[keys] = values
            lista_dicts.append(dict_items)

    return lista_dicts

def select_sku_unitario_referencia(idproduto):
    lista_produtos = []
    engine = get_connection()
    with engine.connect() as conn:
        query_prazosprodutos = (text("""
            SELECT detalhe.UrlImagem,detalhe.Descricao,brand.IdMarca,brand.Marca
            ,basico.[SKU],basico.[NomeProduto],basico.[EAN]
            FROM [HauszMapa].[Produtos].[ProdutoBasico] as basico
            join [HauszMapa].[Produtos].[ProdutoDetalhe] as detalhe
            on detalhe.SKU = basico.SKU
            join Produtos.Marca as brand
            on brand.IdMarca = basico.IdMarca
            where basico.IdProduto in ({})""".format(idproduto)))
        produtos = conn.execute(query_prazosprodutos)
        for produto in produtos:
            dict_items = {}
            for keys, values in produto.items():
                dict_items[keys] = values
            lista_produtos.append(dict_items)

    return lista_produtos


def select_sku_coletado_especificacao(idproduto):
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_prazosprodutos = (text("""SELECT
                            esp.[NomeEspecificacao], esp.[ValorEspecificacao]
                            FROM [HauszMapa].[Produtos].[ProdutoBasico] as basico
                            join [HauszMapa].[Produtos].[ProdutoDetalhe] as detalhe
                            on detalhe.SKU = basico.SKU
                            join Produtos.Marca as brand
                            on brand.IdMarca = basico.IdMarca
                            join [HauszMapaDev2].[Produtos].[EspecificacaoProdutos] as esp
                            on esp.SKU = basico.SKU
                            where basico.IdProduto in ({})""".format(idproduto)))

        produtos = conn.execute(query_prazosprodutos)
        for produto in produtos:
            dict_items = {} 
            for keys, values in produto.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)

    return lista_dicts


def select_resumo_marcas():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_resumomarca = (text("""
                SELECT brand.BitAtivo,brand.PedidoMinimo, brand.PrazoFabricacao,brand.IdMarca
                ,brand.Marca, COUNT(brand.IdMarca) as quantidade
                from Produtos.Marca as brand
                join Produtos.ProdutoBasico as basico
                on basico.IdMarca = brand.IdMarca
                group by brand.BitAtivo,brand.PedidoMinimo, brand.PrazoFabricacao,brand.IdMarca
                ,brand.Marca"""))

        marcas = conn.execute(query_resumomarca)
        for marca in marcas:
            dict_marcas = {}
            for keys, values in marca.items():
                dict_marcas[keys] = values
            lista_dicts.append(dict_marcas)

    return lista_dicts

                




       






    
       
    
    
    