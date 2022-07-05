from asyncio import exceptions
from config import get_connection
from sqlalchemy import text
from datetime import datetime, timedelta,date
from dateutil.relativedelta import *
import pandas as pd

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

#mes seguinte
seguinte  =(hoje)+relativedelta(months=1)
seguinte2 = seguinte.strftime('%Y-%m-%d')
seguinte3 = seguinte.strftime('%Y-%m')
# print(seguinte2)

#mes passado
Mpassado  =(hoje)+relativedelta(months=-1)
mespassado = Mpassado.strftime('%Y-%m') 



def tabela_filtro(codigoPedido, SKU, RejeicaoID, DataFim, DataIni):
    engine = get_connection()
    list_dicts = []
    with engine.connect() as conn:
        query_tabela=(text(f"""		
		DECLARE @codigo as INT
		DECLARE @sku as Varchar(30)
		DECLARE @rejeicaoID as INT
		DECLARE @DataIni as Varchar(23)
		DECLARE @DataFim as Varchar(23)

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

#CARD REJEICAO DIA ATUAL
def card_hoje():
    engine = get_connection()
    list_rhj = []
    with engine.connect() as conn:

        query_rejeicao_hoje =(text(f"""select COUNT (RejeicaoId) as quantidade_de_rejeicao from HauszMapa.wms.T_Rejeicoes
        where RejeicaoId <> 0 and Data between '{hoje2}' and '{data_amanha}' """))
        lista_filtro_hoje = conn.execute(query_rejeicao_hoje).all()
        for lista in lista_filtro_hoje:
            dict_filtro_hoje ={}
            for keys, values in lista.items():
                dict_filtro_hoje[keys] = values
            list_rhj.append(dict_filtro_hoje)
        
    return list_rhj

#CARD TOTAL DE REJEICOES DIA ANTERIOR
def card_ontem():
    engine = get_connection()
    list_rontem = []
    with engine.connect() as conn:
        query_rejeicao_ontem =(text(f"""
        select COUNT(CodigoPedido) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes 
        where  data between '{data_ontem}' and '{hoje2}' and RejeicaoId <> 0 
        """))
        lista_filtro_ontem = conn.execute(query_rejeicao_ontem).all()
        for lista in lista_filtro_ontem:
            dict_filtro_ontem={}
            for keys, values in lista.items():
                dict_filtro_ontem[keys] = values
            list_rontem.append(dict_filtro_ontem)

    return list_rontem

#CARD TOTAL DE REJEICOES DO MES ANTERIOR
def card_mes_passado():
    engine = get_connection()
    list_mes = []
    with engine.connect() as conn:
        query_rejeicao_mes =(text(f"""
        select  count(CodigoPedido) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes 
        where  data between '{mespassado}-01' and '{mes_atual}-01' and RejeicaoId <> 0
        """))
        lista_filtro_mes = conn.execute(query_rejeicao_mes).all()
        for lista in lista_filtro_mes:
            dict_filtro_mes={}
            for keys, values in lista.items():
                dict_filtro_mes[keys] = values
            list_mes.append(dict_filtro_mes)

    return list_mes
    
#CARD TOTAL DE REJEICOES DO MES ATUAL 
def card_mes_seguinte():
    engine = get_connection()
    list_mes_seguinte = []
    with engine.connect() as conn:
        query_mes_seguinte = (text(f"""
        select  count(CodigoPedido) as quantidade_de_rejeicao
        from HauszMapa.wms.T_Rejeicoes 
        where data between '{mes_atual}-01' and '{seguinte3}-01' and RejeicaoId <> 0
        """))
        lista_filtro_seguinte = conn.execute(query_mes_seguinte).all()
        for lista in lista_filtro_seguinte:
            dict_filtro_seguinte={}
            for keys, values in lista.items():
                dict_filtro_seguinte[keys] = values
            list_mes_seguinte.append(dict_filtro_seguinte)

    return list_mes_seguinte

#CARD TOTAL VERICANDO ESTOQUE =  PRE REJEICAO
def Verificando():
    engine = get_connection()
    lista_pre = []
    with engine.connect() as conn:
        query_pre = (text(f"""
        select COUNT(CodigoPedido) as VerificandoEstoque from V_Pedidos where StatusItem like '%Verificando%'
        
        """))
        query_cont = conn.execute(query_pre).all()
        for contagem in query_cont:
            dict_cont = {}
            for keys, values in contagem.items():
                dict_cont[keys] = values
            lista_pre.append(dict_cont)

    return lista_pre

# CONSULTAS GUI
def select_wms_rejeicoes():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_etapas_flexy = (text("""
            select * from wms.T_Rejeicoes """))

        execqueryetapas = conn.execute(query_etapas_flexy).all()
        for exc in execqueryetapas:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
    
    return lista_dicts

def select_pedido_compra_nota_entrada():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query__pcentrada = ((text("""
                SELECT pcentrada.[ChaveNF]
                ,pcentrada.[CodigoPedidoCompra],pcentrada.[SKU],pcentrada.[DataInserido]
                ,pcentrada.[bitAtivo],pcentrada.[Quantidade]
                ,pcentrada.[NumNfOmie],pcentrada.[IdStatusItem]    
                FROM [HauszMapa].[Pedidos].[PedidoCompraNotaEntrada] as pcentrada
                where pcentrada.DataInserido like '%2022%'""")))
        execquery__pcentrada = conn.execute(query__pcentrada).all()
        for exc in execquery__pcentrada:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
    
    return lista_dicts

def select_logpedidos_compras_itens():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_log_notaentrada = ((text("""
                SELECT lpcitens.[CodigoPedidoCompra],lpcitens.[IdProduto],lpcitens.[DeStatusItem]
                ,lpcitens.[ParaStatusItem],lpcitens.[Quantidade]
                ,lpcitens.[QuantidadeColeta]as quantidadecoletadalog
                ,lpcitens.[DataAtualizacao] as dataatualizacaolog ,lpcitens.[bitAtivo]
                ,lpcitens.[TipoAlteracao] 
                FROM [HauszMapa].[Pedidos].[LogPedidoCompraItens] as lpcitens
                where ParaStatusItem in ('5')""")))

        execquert_log_notaentrada = conn.execute(query_log_notaentrada).all()
        for exc in execquert_log_notaentrada:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
    
    return lista_dicts

def select_produtos_sku():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text("""
            SELECT pmarca.[Marca],pbasico.[SKU],pbasico.[CodOmie],pbasico.[NomeProduto]
            ,pbasico.[EAN],pbasico.[EstoqueAtual],pbasico.[SaldoAtual]
            ,pbasico.[bitAtualizadoPreco],pbasico.[bitPrecoAtualizado]
            ,pbasico.[PesoCubado],pbasico.[Peso],pdetalhe.[TamanhoBarra],pdetalhe.[Unidade]
            ,pdetalhe.[FatorVenda],pdetalhe.[FatorMultiplicador],pdetalhe.[FatorUnitario]
            FROM [HauszMapa].[Produtos].[ProdutoBasico] as pbasico
            join [HauszMapa].[Produtos].[ProdutoDetalhe] as pdetalhe
            on pdetalhe.SKU = pbasico.SKU
            join [HauszMapa].[Produtos].[Marca] as pmarca
            on pmarca.IdMarca = pbasico.IdMarca""")))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
    
    return lista_dicts

def select_log_wms_pedidos():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_log = (text("""
                SELECT  lgpedido.[IdLog],lgpedido.[DeIdEtapaFlexy],lgpedido.[ParaIdEtapaFlexy]
                ,lgpedido.[CodigoPedido],pflexy.DataInserido as datainserido
                ,pflexy.DataInseridoOmie as datainseridoomie
                ,pflexy.IdEtapaFlexy,etflexy.NomeEtapa,etflexy.NomeEtapaFlexy
                ,pflexy.PrevisaoEntrega as previsaodeentrega
                ,pflexy.StatusPedido,lgpedido.[EnviadoWpp]
                ,lgpedido.[DataAtualizacao] as dataatualizacao
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
    return lista_dicts

def retorna_dataatual():
    data = datetime.today().strftime('%Y-%m-%d')

    return data

def leadtime_log():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text("""
            SELECT 
            DISTINCT sr.CodigoPedidoSw,
            est.Nome as Estado,
            FORMAT(prazo.DataFoiParaSeparacao,'d','pt-br') as DataIni,
            FORMAT(prazo.DataDeEntrega,'d','pt-br') as DataFim,
			FORMAT(prazo.Prazo,'d','pt-br') as DataPrevista,
            DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.DataDeEntrega) as Dias,
			DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.Prazo) as DiasPrevistos
            FROM  [HauszMapa].[ShowRoom].[Pedido] sr
            inner join HauszLogin.Cadastro.Cliente cli on cli.IdCliente = sr.IdCliente
            inner join HauszLogin.Cadastro.Usuario u on u.IdUsuario = cli.IdUsuario
            inner join HauszLogin.Cadastro.Cidade cit on cit.IdCidade = u.IdCidade
            inner join HauszLogin.Cadastro.Estado est on est.IdEstado = cit.IdEstado
			left join (  SELECT DISTINCT entrega.CodigoPedido
				,DataFoiParaSeparacao
				,MAX(entrega.[DataAtualizacao]) OVER (PARTITION BY entrega.codigopedido) DataDeEntrega
				,MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido) Prazo --para pedidos que a aplicação atualizou o prazo mais que uma vez
				  FROM [HauszMapa].[Pedidos].[LogPedidos] entrega
				  JOIN  (SELECT CodigoPedido
						,ParaPrazo Prazo
						,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
				  FROM [HauszMapa].[Pedidos].[LogPedidos]
				  WHERE ParaIdEtapaFlexy = 6
				  and IdUsuarioAlteracao IN ('Aplicacao','NT SERVICE\SQLSERVERAGENT')) separacao
				  ON entrega.CodigoPedido = separacao.CodigoPedido
				  JOIN (SELECT CodigoPedido
							,MAX([IdLog]) UltimaAtualizacao
						FROM [HauszMapa].[Pedidos].[LogPedidos]
						WHERE DATEDIFF(Month,DataAtualizacao,GETDATE()) = 1
						--WHERE IdUsuarioAlteracao = 'Aplicacao'
						GROUP BY CodigoPedido) atualizacao
					ON entrega.CodigoPedido = atualizacao.CodigoPedido
				  WHERE entrega.ParaIdEtapaFlexy = 9
				  --AND entrega.IdUsuarioAlteracao = 'Aplicacao' --Remove pedidos que foram dados como entregues mais que uma vez
				  AND entrega.IdLog = atualizacao.UltimaAtualizacao -- Remove pedidos que após serem entregues voltam para outro status
				  AND separacao.Prazo IS NOT NULL) prazo 
				  ON prazo.CodigoPedido = sr.CodigoPedidoSw
			where datediff(month,prazo.DataDeEntrega,getdate()) = 1
            --GROUP BY pf.CodigoPedido, est.Nome, ini.DataAtualizacao, fim.DataAtualizacao,Prazo

			UNION

SELECT 
            DISTINCT pf.CodigoPedido,
            est.Nome as Estado,
            FORMAT(prazo.DataFoiParaSeparacao,'d','pt-br') as DataIni,
            FORMAT(prazo.DataDeEntrega,'d','pt-br') as DataFim,
			FORMAT(prazo.Prazo,'d','pt-br') as DataPrevista,
            DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.DataDeEntrega) as Dias,
			DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.Prazo) as DiasPrevistos
            FROM HauszMapa.Pedidos.PedidoFlexy pf
            inner join HauszLogin.Cadastro.Cliente cli on cli.IdCliente = pf.IdCliente
            inner join HauszLogin.Cadastro.Usuario u on u.IdUsuario = cli.IdUsuario
            inner join HauszLogin.Cadastro.Cidade cit on cit.IdCidade = u.IdCidade
            inner join HauszLogin.Cadastro.Estado est on est.IdEstado = cit.IdEstado
			left join (  SELECT DISTINCT entrega.CodigoPedido
				,DataFoiParaSeparacao
				,MAX(entrega.[DataAtualizacao]) OVER (PARTITION BY entrega.codigopedido) DataDeEntrega
				,MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido) Prazo --para pedidos que a aplicação atualizou o prazo mais que uma vez
				  FROM [HauszMapa].[Pedidos].[LogPedidos] entrega
				  JOIN  (SELECT CodigoPedido
						,ParaPrazo Prazo
						,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
				  FROM [HauszMapa].[Pedidos].[LogPedidos]
				  WHERE ParaIdEtapaFlexy = 6
				  and IdUsuarioAlteracao IN ('Aplicacao','NT SERVICE\SQLSERVERAGENT')) separacao
				  ON entrega.CodigoPedido = separacao.CodigoPedido
				  JOIN (SELECT CodigoPedido
							,MAX([IdLog]) UltimaAtualizacao
						FROM [HauszMapa].[Pedidos].[LogPedidos]
						WHERE DATEDIFF(Month,DataAtualizacao,GETDATE()) = 1
						--WHERE IdUsuarioAlteracao = 'Aplicacao'
						GROUP BY CodigoPedido) atualizacao
					ON entrega.CodigoPedido = atualizacao.CodigoPedido
				  WHERE entrega.ParaIdEtapaFlexy = 9
				  --AND entrega.IdUsuarioAlteracao = 'Aplicacao' --Remove pedidos que foram dados como entregues mais que uma vez
				  AND entrega.IdLog = atualizacao.UltimaAtualizacao -- Remove pedidos que após serem entregues voltam para outro status
				  AND separacao.Prazo IS NOT NULL) prazo 
				  ON prazo.CodigoPedido = pf.CodigoPedido
			where datediff(month,prazo.DataDeEntrega,getdate()) = 1
            --GROUP BY pf.CodigoPedido, est.Nome, ini.DataAtualizacao, fim.DataAtualizacao,Prazo
            """)))
        execquery_produtos = conn.execute(query_produtos).all()
        
        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
            df = pd.DataFrame(lista_dicts)
    
    return df

def Estados():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text("""
            select nome as estado from HauszLogin.Cadastro.Estado
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)

            df = pd.DataFrame(lista_dicts)
    
    return df

def percentual():
    lista_dicts = []
    engine = get_connection()
    with engine.connect() as conn:
        query_produtos = ((text(f"""
        SELECT 
        DISTINCT PF.CodigoPedido,
        FORMAT(PF.PrevisaoEntrega,'d', 'pt-br') as PrevisaoEntrega, 
        FORMAT(MIN(LOGPRAZO.PrazoAntigo) OVER (PARTITION BY PF.CodigoPedido), 'd', 'pt-br') as NovaPrevisao, 
        FORMAT(LP.DataAtualizacao, 'd', 'pt-br') as DataEntrega
        FROM Hauszmapa.Pedidos.PedidoFlexy PF
        INNER JOIN Hauszmapa.Pedidos.ItensFlexy IFL ON IFL.CodigoPedido = PF.CodigoPedido
        INNER JOIN Hauszmapa.Produtos.ProdutoBasico PB ON PB.SKU = IFL.SKU
        INNER JOIN HauszMapa.Wms.T_Rejeicoes sep on sep.CodigoPedido = pf.CodigoPedido
        iNNER JOIN HauszMapa.Pedidos.LogPedidos LP ON LP.CodigoPedido = PF.CodigoPedido
        LEFT JOIN (SELECT LAP.CodigoPedido, LAP.IdProduto, LAP.PrazoAntigo, LAP.PrazoNovo,LAP.DataAlteracao
        FROM Hauszmapa.Pedidos.LogAlteracaoPrazoPedidoVenda LAP
        INNER JOIN (SELECT CodigoPedido, IdProduto, MIN(IdLogPrazoPedidoVenda) IdLogPrazoPedidoVenda
        FROM Hauszmapa.Pedidos.LogAlteracaoPrazoPedidoVenda
        GROUP BY CodigoPedido,IdProduto, DataAlteracao) AS LAPPV ON LAPPV.CodigoPedido = LAP.CodigoPedido AND LAPPV.IdProduto = LAP.IdProduto AND LAP.IdLogPrazoPedidoVenda = LAPPV.IdLogPrazoPedidoVenda) 

        AS LOGPRAZO ON LOGPRAZO.CodigoPedido = ISNULL(PF.PedidoPai, PF.CodigoPedido) --AND LOGPRAZO.IdProduto = PB.IdProduto
        where LP.DataAtualizacao BETWEEN Convert(datetime, '{mes_atual}-01' ) AND Convert(datetime, '{seguinte3}-01' ) and LP.ParaIdEtapaFlexy = 9 AND RejeicaoId = 0
        ORDER BY PF.CodigoPedido
            """)))
        execquery_produtos = conn.execute(query_produtos).all()

        for exc in execquery_produtos:
            dict_items = {}
            for keys, values in exc.items():
                dict_items[keys] = values
            lista_dicts.append(dict_items)
        df = pd.DataFrame(lista_dicts)
    return df

def coleta_prazo():
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
            where ParaStatusItem = 15 and DataAtualizacao between '{mes_atual}-01' and '{seguinte3}-01') Coletado on Coletado.CodigoPedidoCompra = pc.CodigoPedidoCompra
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