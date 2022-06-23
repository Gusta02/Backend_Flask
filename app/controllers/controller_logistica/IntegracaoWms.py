from asyncio import exceptions
from config import get_connection
from sqlalchemy import text
from datetime import datetime, timedelta,date
from dateutil.relativedelta import *


#Horarios and mes
hoje  = datetime.today()
hoje2 = hoje.strftime('%Y-%m-%d')
ontem = timedelta(days=-1)
data_ontem =  hoje + ontem
data_ontem = data_ontem.strftime('%Y-%m-%d')
amanha = timedelta(days=1)
data_amanha = hoje + amanha
data_amanha = data_amanha.strftime('%Y-%m-%d')

#mes
mes_atual = date.today().strftime('%Y-%m')

Mpassado  =(hoje)+relativedelta(months=-1)
Mpassado2 =  Mpassado.strftime('%Y-%m-%d')

seguinte  =(hoje)+relativedelta(months=1)
seguinte2 = seguinte.strftime('%Y-%m-%d')

only_mes_passado = Mpassado.strftime('%Y-%m')

def codigo():
    engine = get_connection()
    list_dicts = []
    with engine.connect() as conn:
        query_codigo=(text(f""" select CodigoPedido from HauszMapa.Wms.T_Rejeicoes """))
        lista_codigo = conn.execute(query_codigo).all()
        for codigo in lista_codigo:
            dict_codigo = {}
            for keys, values in codigo.items():
                dict_codigo[keys] = values
            list_dicts.append(dict_codigo)

    return list_dicts

def pedido():
    engine = get_connection()
    list_pedido = []
    with engine.connect() as conn:
        query_pedido = (text(f""" select PedidoCorpEM from HauszMapa.Wms.T_Rejeicoes """))
        lista_pedido = conn.execute(query_pedido).all()
        for pedido in lista_pedido:
            dict_pedido = {}
            for keys, values in pedido.items():
                dict_pedido[keys] = values
            list_pedido.append(dict_pedido)

    return list_pedido

def T_sku():
    engine = get_connection()
    list_sku = []
    with engine.connect() as conn:
        query_sku = (text(f""" select SKU from HauszMapa.Produtos.ProdutoBasico  """))
        lista_sku = conn.execute(query_sku).all()
        for sku in lista_sku:
            dict_sku = {}
            for keys, values in sku.items():
                dict_sku[keys] = values
            list_sku.append(dict_sku)

    return list_sku

def T_id():
    engine = get_connection()
    list_id =[]
    with engine.connect() as conn:
        query_id = (text(f"""
         select RejeicaoId as Id from HauszMapa.Wms.T_Rejeicoes
        """))
        lista_id = conn.execute(query_id).all()
        for id_t in lista_id:
            dict_id = {}
            for keys, values in id_t.items():
                dict_id[keys] = values
            list_id.append(dict_id)
    
    return list_id

def quantidade():
    engine = get_connection()
    list_quant = []
    with engine.connect() as conn:
        query_quant = (text(f""" select Quantidade from HauszMapa.Wms.T_RejeicoesItens """))
        lista_quant = conn.execute(query_quant).all()
        for quant in lista_quant:
            dict_quant = {}
            for keys, values in quant.items():
                dict_quant[keys] = values
            list_quant.append(dict_quant)

    return list_quant

def tabela_filtro(Page,codigoPedido, SKU, RejeicaoID, DataFim, DataIni):
    engine = get_connection()
    list_dicts = []
    with engine.connect() as conn:
        query_tabela=(text(f"""		
        DECLARE @PageNumber as INT
        DECLARE @RowsOfPage as INT
		DECLARE @codigo as INT
		DECLARE @sku as Varchar(30)
		DECLARE @rejeicaoID as INT
		DECLARE @DataIni as Varchar(23)
		DECLARE @DataFim as Varchar(23)

        SET @PageNumber = {Page}
        SET @RowsOfPage = 10
		SET @codigo = {codigoPedido}
		SET @sku = {SKU}
		SET @rejeicaoID = {RejeicaoID}
		SET @DataFim = {DataFim}
		SET @DataIni = {DataIni}

		select  
		ri.CodigoPedido,
        ri.PedidoCorpEM,
        pb.sku,
        r.RejeicaoId as Id,
        pb.NomeProduto as Produto,
        RI.Quantidade,
        RI.QuantidadeAtendida,
        (RI.Quantidade - RI.QuantidadeAtendida) as Quantidade_faltante,
        format(r.Data,'d', 'pt-br') as Data_Rejeicao
        from HauszMapa.wms.T_RejeicoesItens ri
        inner join HauszMapa.Wms.T_Rejeicoes r on ri.CodigoPedido = r.CodigoPedido
        inner join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        where r.RejeicaoId <> 0 
		AND r.CodigoPedido = CASE @codigo WHEN '' THEN r.CodigoPedido ELSE @codigo END
		AND pb.SKU like CASE @SKU WHEN '' THEN pb.SKU ELSE '%' + @SKU + '%' END
		AND r.RejeicaoId = CASE @rejeicaoID WHEN '' THEN r.RejeicaoId ELSE @rejeicaoID END
		AND r.Data >= CASE @DataIni WHEN '' THEN '1900-01-01' ELSE @DataIni END
		AND r.Data < CASE @DataFim WHEN '' THEN '2025-01-01' ELSE @DataFim END
		order  by r.Data DESC 
        OFFSET (@PageNumber-1)*@RowsOfPage ROWS
        FETCH NEXT @RowsOfPage ROWS ONLY
        """))
        lista_tabela = conn.execute(query_tabela).all()
        for tabela in lista_tabela:
            dict_tabela = {}
            for keys, values in tabela.items():
                dict_tabela[keys] =values
            list_dicts.append(dict_tabela)
            
    return list_dicts

def tabela_filtro1(Page):
    engine = get_connection()
    list_dicts = []
    with engine.connect() as conn:
        query_tabela=(text(f"""		
        DECLARE @PageNumber as INT
        DECLARE @RowsOfPage as INT
		
        SET @PageNumber = {Page}
        SET @RowsOfPage = 10
		
		select  
		ri.CodigoPedido,
        ri.PedidoCorpEM,
        pb.sku,
        r.RejeicaoId as Id,
        pb.NomeProduto as Produto,
        RI.Quantidade,
        RI.QuantidadeAtendida,
        (RI.Quantidade - RI.QuantidadeAtendida) as Quantidade_faltante,
        format(r.Data,'d', 'pt-br') as Data_Rejeicao
        from HauszMapa.wms.T_RejeicoesItens ri
        inner join HauszMapa.Wms.T_Rejeicoes r on ri.CodigoPedido = r.CodigoPedido
        inner join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        where r.RejeicaoId <> 0 
		order  by r.Data DESC 
        OFFSET (@PageNumber-1)*@RowsOfPage ROWS
        FETCH NEXT @RowsOfPage ROWS ONLY
        """))
        lista_tabela = conn.execute(query_tabela).all()
        for tabela in lista_tabela:
            dict_tabela = {}
            for keys, values in tabela.items():
                dict_tabela[keys] =values
            list_dicts.append(dict_tabela)
            
    return list_dicts

def filtro_todos(CodigoPedido,Versao,sku, Id,Data_ini, Data_f):
    engine = get_connection()
    list_dicts = []
    with engine.connect() as conn:
        query_filtro = (text(f"""select 
        Ri.CodigoPedido, 
		RI.PedidoCorpEM,
        pb.sku,
		r.RejeicaoId as Id,
        pb.NomeProduto as Produto,
        RI.Quantidade,
        RI.QuantidadeAtendida,
        (RI.Quantidade - RI.QuantidadeAtendida) as Quantidade_faltante,
        ri.data as Data
        from HauszMapa.Wms.T_Rejeicoes r
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.RejeicaoItemId = r.RejeicaoId
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        left join HauszMapa.Wms.T_Rejeicoes p on p.PedidoCorpEM =ri.PedidoCorpEM
        where pb.BitAtivo = 1 and ri.CodigoPedido like '{CodigoPedido}' and ri.PedidoCorpEM like '{Versao}' and pb.sku like '{sku}'
		and r.Id like '{Id}' and ri.data between '{Data_ini} 00:00:00' and '{Data_f} 00:00:00' 
        """))
        filtro_resultados = conn.execute(query_filtro).all()
        for tabela in filtro_resultados:
            dict_filtro={}
            for keys, values in tabela.items():
                dict_filtro[keys] = values 
            list_dicts.append(dict_filtro)
    
    return list_dicts
    
" Filtros da Tabela "
def CodigoPedido():
    engine = get_connection()
    lista_dicts = []
    with engine.connect() as conn:
        query_codigopedido= (text("""select 
        Ri.CodigoPedido
        from HauszMapa.Wms.T_Rejeicoes r
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.RejeicaoItemId = r.RejeicaoId
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        left join HauszMapa.Wms.T_Rejeicoes p on p.PedidoCorpEM =ri.PedidoCorpEM
        where pb.BitAtivo = 1 and ri.data between '2022-06-01 00:00:00' and '2022-06-08 00:00:00' """))
        lista_codigopedido = conn.execute(query_codigopedido).all()
        for codigopedido in lista_codigopedido:
            dict_CodigoPedido = {}
            for keys, values in codigopedido.items():
                dict_CodigoPedido[keys] = values
            lista_dicts.append(dict_CodigoPedido)

    return lista_dicts

def PedidoVersao():
    engine =  get_connection()
    lista_pedido =[]
    with engine.connect() as conn:
        query_versaopedido = (text("""select  
		RI.PedidoCorpEM
        from HauszMapa.Wms.T_Rejeicoes r
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.RejeicaoItemId = r.RejeicaoId
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        left join HauszMapa.Wms.T_Rejeicoes p on p.PedidoCorpEM =ri.PedidoCorpEM
        where pb.BitAtivo = 1 and ri.data between '2022-06-01 00:00:00' and '2022-06-08 00:00:00' 
        """))

        lista_versaopedido = conn.execute(query_versaopedido).all()
        for lista in lista_versaopedido:
            dict_Pedidoversao = {}
            for keys, values in lista.items():
                dict_Pedidoversao[keys] = values 
            lista_pedido.append(dict_Pedidoversao)

    return lista_pedido

def SKU():
    engine =  get_connection()
    lista_sku = []
    with engine.connect() as conn:
        query_sku = (text("""select 
        pb.sku
        from HauszMapa.Wms.T_Rejeicoes r
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.RejeicaoItemId = r.RejeicaoId
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        left join HauszMapa.Wms.T_Rejeicoes p on p.PedidoCorpEM =ri.PedidoCorpEM
        where pb.BitAtivo = 1 and ri.data between '2022-06-01 00:00:00' and '2022-06-08 00:00:00'
        """))
        sku_lista = conn.execute(query_sku).all()
        for lista in sku_lista:
            dict_sku = {}
            for keys, values in lista.items():
                dict_sku[keys] = values
            lista_sku.append(dict_sku)

    return lista_sku

def Cons_Id():
    engine = get_connection()
    lista_id = []
    with engine.connect() as conn:
        query_id = (text(f"""
        select 
		r.RejeicaoId as Id
        from HauszMapa.Wms.T_Rejeicoes r
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.RejeicaoItemId = r.RejeicaoId
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        left join HauszMapa.Wms.T_Rejeicoes p on p.PedidoCorpEM =ri.PedidoCorpEM
        where pb.BitAtivo = 1 and ri.data between '2022-06-01 00:00:00' and '2022-06-08 00:00:00'
        """))
        id_lista = conn.execute(query_id).all()
        for lista in id_lista:
            dict_id={}
            for keys, values in lista.items():
                dict_id[keys] = values
            lista_id.append(dict_id)

    return lista_id

#CARD DIA ATUAL
def card_hoje():
    engine = get_connection()
    list_rhj = []
    with engine.connect() as conn:
        query_rejeicao_hoje =(text(f"""select  count(r.RejeicaoId) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes r 
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.CodigoPedido = r.CodigoPedido
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        where pb.BitAtivo = 1 and r.data between '{hoje2} 00:00:00' and '{data_amanha} 00:00:00' and r.RejeicaoId <> 0 """))
        lista_filtro_hoje = conn.execute(query_rejeicao_hoje).all()
        for lista in lista_filtro_hoje:
            dict_filtro_hoje ={}
            for keys, values in lista.items():
                dict_filtro_hoje[keys] = values
            list_rhj.append(dict_filtro_hoje)
        
    return list_rhj

#CARD TOTAL REJEICOES ONTEM
def card_ontem():
    engine = get_connection()
    list_rontem = []
    with engine.connect() as conn:
        query_rejeicao_ontem =(text(f"""select  count(r.RejeicaoId) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes r 
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.CodigoPedido = r.CodigoPedido
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        where pb.BitAtivo = 1 and r.data between '{data_ontem} 00:00:00' and '{hoje2} 00:00:00' and r.RejeicaoId <> 0 """))
        lista_filtro_ontem = conn.execute(query_rejeicao_ontem).all()
        for lista in lista_filtro_ontem:
            dict_filtro_ontem={}
            for keys, values in lista.items():
                dict_filtro_ontem[keys] = values
            list_rontem.append(dict_filtro_ontem)

    return list_rontem

#CARD PARA CONSULTA DE TOTAL DE REJEICOES MES PASSADO ( PARA CALCULAR PORCENTAGEM)
def card_mes_passado():
    engine = get_connection()
    list_mes = []
    with engine.connect() as conn:
        query_rejeicao_mes =(text(f"""select  count(r.RejeicaoId) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes r 
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.CodigoPedido = r.CodigoPedido
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        where pb.BitAtivo = 1 and r.data between '{Mpassado2} 00:00:00' and '{hoje2} 00:00:00' and r.RejeicaoId <> 0 """))
        lista_filtro_mes = conn.execute(query_rejeicao_mes).all()
        for lista in lista_filtro_mes:
            dict_filtro_mes={}
            for keys, values in lista.items():
                dict_filtro_mes[keys] = values
            list_mes.append(dict_filtro_mes)

    return list_mes
    
#CARD PARA CONSULTA DE TOTAL DE REJEICOES MES SEGUINTE ( PARA CALCULAR PORCENTAGEM)
def card_mes_seguinte():
    engine = get_connection()
    list_mes_seguinte = []
    with engine.connect() as conn:
        query_mes_seguinte = (text(f"""select  count(r.RejeicaoId) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes r 
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.CodigoPedido = r.CodigoPedido
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        where pb.BitAtivo = 1 and r.data between '{Mpassado2} 00:00:00' and '{seguinte2} 00:00:00' and r.RejeicaoId <> 0  """))
        lista_filtro_seguinte = conn.execute(query_mes_seguinte).all()
        for lista in lista_filtro_seguinte:
            dict_filtro_seguinte={}
            for keys, values in lista.items():
                dict_filtro_seguinte[keys] = values
            list_mes_seguinte.append(dict_filtro_seguinte)

    return list_mes_seguinte

#CARD TOTAL DE REJEICOES MES PASSADO
def qtd_mes_passado():
    engine = get_connection()
    list_qtd_passado = []
    with engine.connect() as conn:
        query_qtd_mespassado = (text(f"""select  count(r.RejeicaoId) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes r 
        inner join HauszMapa.Wms.T_RejeicoesItens ri on ri.CodigoPedido = r.CodigoPedido
        left join HauszMapa.Produtos.ProdutoBasico pb on pb.SKU = ri.CodigoProduto
        where pb.BitAtivo = 1 and r.data between '{only_mes_passado}-01 00:00:00' and '{mes_atual}-01 00:00:00' and r.RejeicaoId <> 0 """))
        qtde_filtrada = conn.execute(query_qtd_mespassado).all()
        for lista in qtde_filtrada:
            dict_filtro_qtde={}
            for keys, values in lista.items():
                dict_filtro_qtde[keys] = values
            list_qtd_passado.append(dict_filtro_qtde)

    return list_qtd_passado
    
#CARD DE POSSIVEIS REJEICOES ATUAIS E SHOWROOM
def Pre_rejeicao():
    engine = get_connection()
    lista_pre = []
    with engine.connect() as conn:
        query_pre = (text(f"""select count(v.StatusItem) Pre_rejeicoes from V_Pedidos v where StatusItem like  '%Verificando%'
          """))
        query_cont = conn.execute(query_pre).all()
        for contagem in query_cont:
            dict_cont = {}
            for keys, values in contagem.items():
                dict_cont[keys] = values
            lista_pre.append(dict_cont)

    return lista_pre
