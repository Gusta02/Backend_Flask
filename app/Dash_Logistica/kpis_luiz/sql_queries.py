import os


query_frete_recebido = '''
SELECT FORMAT((SUM(PrecoFrete)*1.0175),'c','pt-br') as FreteRecebido
FROM HauszMapa.Pedidos.PedidoFlexy
WHERE IdEtapaFlexy NOT IN  (1,11,15,16,26,41)
AND MONTH(DataInserido) = MONTH(GETDATE())
'''

query_prazo_na_separacao ='''
SELECT [IdLog]
      ,[CodigoPedido]
      ,[DataAtualizacao]
      ,[ParaPrazo]
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 6
  AND MONTH(DataAtualizacao) = MONTH(GETDATE())-1
'''

query_entregaxprazo = '''
  SELECT DISTINCT entrega.CodigoPedido
				,DataFoiParaSeparacao
				,MAX(entrega.[DataAtualizacao]) OVER (PARTITION BY entrega.codigopedido) DataDeEntrega
				,MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido) Prazo --para pedidos que a aplicação atualizou o prazo mais que uma vez
				--,entrega.IdLog 
				--,UltimaAtualizacao
				--,DATEDIFF(DAY,separacao.DataFoiParaSeparacao,separacao.Prazo) DiasParaEntregar
				--,DATEDIFF(DAY,separacao.DataFoiParaSeparacao,entrega.[DataAtualizacao]) DiasQueLevouParaEntregar
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
  AND separacao.Prazo IS NOT NULL -- Casos onde o sistema não atualizou o prazo na etapa 6, mas sim na próxima etapa
  --AND separacao.Prazo > entrega.DataAtualizacao
  ORDER BY CodigoPedido desc
  '''

query_sem_etapas = '''
SELECT DISTINCT pedidos.CodigoPedido
				,FORMAT(DataFoiParaSeparacao,'d','br') DataFoiParaSeparacao
				,FORMAT(MAX(DataDepedidos) OVER (PARTITION BY pedidos.codigopedido),'d','br') DataDeEntrega
				,FORMAT(MAX(separacao.ParaPrazo) OVER (PARTITION BY pedidos.codigopedido),'d','br') DataMax --para pedidos que a aplicação atualizou o prazo mais que uma vez
				,FORMAT(DataFoiParaTransito,'d','br') AS DataFoiParaTransito
				,FORMAT(DataSaiuParaEntrega,'d','br') AS DataSaiuParaEntrega
  FROM [HauszMapa].[Pedidos].[LogPedidos] pedidos
  JOIN  (SELECT CodigoPedido
		,ParaPrazo
		,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 6
  and IdUsuarioAlteracao = 'Aplicacao'
  AND MONTH(DataAtualizacao) >= 3) separacao
  ON pedidos.CodigoPedido = separacao.CodigoPedido
  LEFT JOIN  (SELECT CodigoPedido
		,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaTransito
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 7
  and IdUsuarioAlteracao = 'Aplicacao'
  ) emtransito
    ON pedidos.CodigoPedido = emtransito.CodigoPedido
  Left JOIN  (SELECT CodigoPedido
		,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataSaiuParaEntrega
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 19
  and IdUsuarioAlteracao = 'Aplicacao') saiuparaentrega
  ON saiuparaentrega.CodigoPedido = pedidos.CodigoPedido
  JOIN (SELECT CodigoPedido
	,MAX([DataAtualizacao]) DataDepedidos
FROM [HauszMapa].[Pedidos].[LogPedidos]
WHERE ParaIdEtapaFlexy = 9
AND IdUsuarioAlteracao = 'Aplicacao' --Remove pedidos que foram dados como entregues mais que uma vez
GROUP BY CodigoPedido) entrega
ON pedidos.CodigoPedido = entrega.CodigoPedido
WHERE separacao.ParaPrazo IS NOT NULL -- Casos onde o sistema não atualizou o prazo na etapa 6, mas sim na próxima etapa
AND DATEDIFF(Month,DataDepedidos,GETDATE()) = 1
  '''

query_pedido_perfeito = '''
SELECT DISTINCT pedidos.CodigoPedido
				--,FORMAT(DataFoiParaSeparacao,'d','br') DataFoiParaSeparacao
				--,FORMAT(MAX(entrega.DataDeEntrega) OVER (PARTITION BY entrega.codigopedido),'d','br') DataDeEntrega
				--,FORMAT(MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido),'d','br') Prazo --para pedidos que a aplicação atualizou o prazo mais que uma vez
  FROM [HauszMapa].[Pedidos].[LogPedidos] pedidos
  JOIN  (SELECT CodigoPedido
		,ParaPrazo Prazo
		,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 6
  and IdUsuarioAlteracao = 'Aplicacao') separacao
  ON pedidos.CodigoPedido = separacao.CodigoPedido
  JOIN (SELECT CodigoPedido
			,MAX([DataAtualizacao]) DataDeEntrega
		FROM [HauszMapa].[Pedidos].[LogPedidos]
		WHERE ParaIdEtapaFlexy = 9
		AND IdUsuarioAlteracao = 'Aplicacao' --Remove pedidos que foram dados como entregues mais que uma vez
		AND DATEDIFF(Month,DataAtualizacao,GETDATE()) = 1
		GROUP BY CodigoPedido) entrega
  ON pedidos.CodigoPedido = entrega.CodigoPedido
  JOIN (SELECT [CodigoPedido]
  FROM [HauszMapa].[Pedidos].[PedidoFlexy]
  WHERE PedidoPai = CodigoPedido
  AND DesmPedido = 0
  AND StatusPedido = 'Entregue'
  AND IdColaborador != 1815
  ) naodesmembrados
  ON naodesmembrados.CodigoPedido = pedidos.CodigoPedido
  WHERE separacao.Prazo IS NOT NULL -- Casos onde o sistema não atualizou o prazo na etapa 6, mas sim na próxima etapa
  AND DATEDIFF(day,DataDeEntrega,Prazo) > 0 --FORMAT(DataDeEntrega,'d') <= FORMAT(Prazo,'d')
  EXCEPT
  SELECT CodigoPedido FROM Logistica.LogReversaOcorrencia
  '''

query_total_de_pedidos = '''
SELECT COUNT(pedidosentregues.CodigoPedido) AS TotalDeEntregas FROM 
(SELECT DISTINCT pf.CodigoPedido
FROM [HauszMapa].[Pedidos].[PedidoFlexy] pf
JOIN (SELECT CodigoPedido
,MAX(IdLog) ultimolog
FROM [HauszMapa].[Pedidos].[LogPedidos]
WHERE IdUsuarioAlteracao = 'Aplicacao'
AND DATEDIFF(Month,DataAtualizacao,GETDATE()) = 1
GROUP BY CodigoPedido) ultimo
ON pf.CodigoPedido = ultimo.CodigoPedido
WHERE pf.StatusPedido = 'Entregue') pedidosentregues
'''

query_pedidos_ja_atrasados = '''
  SELECT COUNT(pedidosatrados.CodigoPedido) FROM (SELECT DISTINCT pedidos.CodigoPedido
				,UltimaAtualizacao
				,EtapaAtual
				,FORMAT(DataFoiParaSeparacao,'d','br') DataFoiParaSeparacao
				,FORMAT(MAX(separacao.Prazo) OVER (PARTITION BY pedidos.codigopedido),'d','br') Prazo --para pedidos que a aplicação atualizou o prazo mais que uma vez
  FROM [HauszMapa].[Pedidos].[LogPedidos] pedidos
  JOIN  (SELECT CodigoPedido
		,ParaPrazo Prazo
		,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 6
  and IdUsuarioAlteracao = 'Aplicacao') separacao
  ON pedidos.CodigoPedido = separacao.CodigoPedido
  JOIN (SELECT CodigoPedido
			,ParaIdEtapaFlexy EtapaAtual
			,IdLog
		FROM [HauszMapa].[Pedidos].[LogPedidos]
		WHERE ParaIdEtapaFlexy IN (6,7,18,19)
		AND IdUsuarioAlteracao = 'Aplicacao' --Remove pedidos que foram dados como entregues mais que uma vez
		AND MONTH(DataAtualizacao) >= 3) etapaatual
  ON pedidos.CodigoPedido = etapaatual.CodigoPedido
  JOIN (SELECT CodigoPedido
			,MAX(IdLog) UltimaAtualizacao
		FROM [HauszMapa].[Pedidos].[LogPedidos]
		GROUP BY CodigoPedido) atualizacao
	ON pedidos.CodigoPedido = atualizacao.CodigoPedido
  WHERE separacao.Prazo IS NOT NULL -- Casos onde o sistema não atualizou o prazo na etapa 6, mas sim na próxima etapa
  AND etapaatual.IdLog = atualizacao.UltimaAtualizacao
  AND GETDATE() > Prazo) pedidosatrados
  '''

query_fator_multiplicador_prod ='''
  SELECT SKU
      ,[FatorMultiplicador]
FROM [HauszMapa].[Produtos].[ProdutoDetalhe]
WHERE bitAtivo = 1 
'''
query_fator_multiplicador_show_room ='''
SELECT [SKU]
      ,[FatorMultiplicador]
  FROM [HauszMapa].[ShowRoom].[ProdutoBasico]
  WHERE bitAtivo = 1
'''

query_quantidade_do_sistema = '''
SELECT (SELECT SUM(Quantidade * TipoOperacao) AS Expr1
                  FROM      Estoque.XMovimentacaoEstoque AS E
                  WHERE   (IdProduto = EM.IdProduto) AND (IdEstoque = EM.IdEstoque) AND (IdTipoMovimentacao <> 1)) AS Quantidade, IdProduto, CodigoProduto, IdEstoque
FROM     Estoque.XMovimentacaoEstoque AS EM WITH (NOLOCK)
WHERE  (IdEstoque in (1,5))
GROUP BY IdProduto, CodigoProduto, IdEstoque
'''

query_entregas_por_estado = '''
SELECT 
            DISTINCT sr.CodigoPedidoSw as CodigoPedido
            ,est.Nome as Estado,
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
'''

query_produtos_por_pedido = '''
Select CodigoPedido
			,SKU
			,Quantidade AS QuantidadePedida
			,IdEstoque
			,StatusPedido
			,TipoPedido
from (SELECT StatusPedido
		,itens.CodigoPedido
		,itens.SKU
		,itens.Quantidade
		,itens.IdEstoque
		,'Cliente' AS TipoPedido
		FROM [HauszMapa].[Pedidos].[PedidoFlexy] pedidos
		JOIN (SELECT CodigoPedido,SKU, Quantidade,IdEstoque,bitAtivo FROM [HauszMapa].[Pedidos].[ItensFlexy]
		WHERE IdEstoque IN (1,5)) itens
		ON pedidos.CodigoPedido = itens.CodigoPedido
		WHERE itens.bitAtivo = 1
		UNION
	SELECT StatusPedido
			,itens.CodigoPedidoSw as CodigoPedido
			,itens.SKU
			,itens.Quantidade
			,itens.IdEstoque
			,'Showroom' AS TipoPedido
	FROM [HauszMapa].[ShowRoom].[Pedido] showroom
	JOIN (SELECT CodigoPedidoSw,SKU,Quantidade,IdEstoque,bitAtivo  FROM  [HauszMapa].[ShowRoom].[ItensPedido]
	WHERE IdEstoque IN (1,5)) itens
	ON showroom.CodigoPedidoSw = itens.CodigoPedidoSw
	WHERE itens.bitAtivo = 1) AS pedidos_ativos
	WHERE pedidos_ativos.StatusPedido IN ('Pago','Aguardando Arquiteto','Aguardando confirmação do cliente','Entrega Futura','Verificando Estoque')
	ORDER BY CodigoPedido
'''

query_preco_produtos_estoque = '''
SELECT pp.[SKU]
      ,[Preco]
	  ,prodsfornec.NomeFantasia
  FROM [HauszMapa].[Produtos].[ProdutoPreco] pp
  JOIN (SELECT SKU, prods.IdMarca, fornec.NomeFantasia 
		FROM HauszMapa.Produtos.ProdutoBasico prods
		JOIN (SELECT fornecmarca.CnpjFornecedor,IdMarca,fornecnome.NomeFantasia FROM [HauszMapa].[Produtos].[FornecedorMarca] fornecmarca 
		JOIN (SELECT NomeFantasia, CnpjFornecedor FROM [HauszMapa].[Cadastro].[Fornecedor]) fornecnome 
			ON fornecmarca.CnpjFornecedor = fornecnome.CnpjFornecedor
		WHERE IdMarca NOT IN (71)) fornec
	ON fornec.IdMarca = prods.IdMarca) prodsfornec	
	ON prodsfornec.SKU = pp.SKU
	WHERE IdUnidade = 1
	AND IdEstoque IN (1,5)
'''

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_venda_por_marca_ajustada.sql')) as f:
	query_vendas_ano_atual = f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_venda_por_SKU_por_mes_com_nome.sql')) as f:
	query_venda_SKU_mensal = f.read()