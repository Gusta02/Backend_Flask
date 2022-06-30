query_no_prazo = '''
SELECT DISTINCT PF.CodigoPedido
				,LP.DataAtualizacao
				,(MIN(LOGPRAZO.PrazoAntigo) OVER (PARTITION BY PF.CodigoPedido)) AS PrazoAlterado
				,PF.PrevisaoEntrega
FROM Pedidos.PedidoFlexy PF
INNER JOIN Pedidos.ItensFlexy IFL ON IFL.CodigoPedido = PF.CodigoPedido
Inner JOIN Pedidos.LogPedidos AS LP ON LP.CodigoPedido = PF.CodigoPedido
INNER JOIN Produtos.ProdutoBasico PB ON PB.SKU = IFL.SKU
LEFT JOIN
(SELECT LAP.CodigoPedido, LAP.IdProduto, LAP.PrazoAntigo, LAP.PrazoNovo
FROM Pedidos.LogAlteracaoPrazoPedidoVenda LAP
INNER JOIN
(SELECT CodigoPedido, IdProduto, MIN(IdLogPrazoPedidoVenda) IdLogPrazoPedidoVenda
FROM Pedidos.LogAlteracaoPrazoPedidoVenda
GROUP BY CodigoPedido,IdProduto) AS LAPPV ON LAPPV.CodigoPedido = LAP.CodigoPedido
											AND LAPPV.IdProduto = LAP.IdProduto
											AND LAP.IdLogPrazoPedidoVenda = LAPPV.IdLogPrazoPedidoVenda
) AS LOGPRAZO ON LOGPRAZO.CodigoPedido = ISNULL(PF.PedidoPai, PF.CodigoPedido) --AND LOGPRAZO.IdProduto = PB.IdProduto
WHERE PF.[DataInserido] BETWEEN Convert(datetime, '2022-05-01' ) AND Convert(datetime, '2022-05-31' )
AND StatusPedido = 'Entregue'
AND LP.[ParaIdEtapaFlexy] = 9
AND LP.[DeIdEtapaFlexy]  != 9
'''

query_status_pedidos = '''
SELECT DISTINCT PF.CodigoPedido
				,PF.StatusPedido
FROM Pedidos.PedidoFlexy PF
INNER JOIN Pedidos.ItensFlexy IFL ON IFL.CodigoPedido = PF.CodigoPedido
Inner JOIN Pedidos.LogPedidos AS LP ON LP.CodigoPedido = PF.CodigoPedido
INNER JOIN Produtos.ProdutoBasico PB ON PB.SKU = IFL.SKU
LEFT JOIN
(SELECT LAP.CodigoPedido, LAP.IdProduto, LAP.PrazoAntigo, LAP.PrazoNovo
FROM Pedidos.LogAlteracaoPrazoPedidoVenda LAP
INNER JOIN
(SELECT CodigoPedido, IdProduto, MIN(IdLogPrazoPedidoVenda) IdLogPrazoPedidoVenda
FROM Pedidos.LogAlteracaoPrazoPedidoVenda
GROUP BY CodigoPedido,IdProduto) AS LAPPV ON LAPPV.CodigoPedido = LAP.CodigoPedido
											AND LAPPV.IdProduto = LAP.IdProduto
											AND LAP.IdLogPrazoPedidoVenda = LAPPV.IdLogPrazoPedidoVenda
) AS LOGPRAZO ON LOGPRAZO.CodigoPedido = ISNULL(PF.PedidoPai, PF.CodigoPedido) --AND LOGPRAZO.IdProduto = PB.IdProduto
WHERE PF.[DataInserido] BETWEEN Convert(datetime, '2022-05-01' ) AND Convert(datetime, '2022-05-31' )
ORDER BY CodigoPedido
'''

query_atraso_compras = '''
SELECT DISTINCT PF.CodigoPedido
				,LP.DataAtualizacao
				,(MIN(LOGPRAZO.PrazoAntigo) OVER (PARTITION BY PF.CodigoPedido)) AS PrazoAlterado
				,PF.PrevisaoEntrega
FROM Pedidos.PedidoFlexy PF
INNER JOIN Pedidos.ItensFlexy IFL ON IFL.CodigoPedido = PF.CodigoPedido
Inner JOIN Pedidos.LogPedidos AS LP ON LP.CodigoPedido = PF.CodigoPedido
INNER JOIN Produtos.ProdutoBasico PB ON PB.SKU = IFL.SKU
LEFT JOIN
(SELECT LAP.CodigoPedido, LAP.IdProduto, LAP.PrazoAntigo, LAP.PrazoNovo
FROM Pedidos.LogAlteracaoPrazoPedidoVenda LAP
INNER JOIN
(SELECT CodigoPedido, IdProduto, MIN(IdLogPrazoPedidoVenda) IdLogPrazoPedidoVenda
FROM Pedidos.LogAlteracaoPrazoPedidoVenda
GROUP BY CodigoPedido,IdProduto) AS LAPPV ON LAPPV.CodigoPedido = LAP.CodigoPedido
											AND LAPPV.IdProduto = LAP.IdProduto
											AND LAP.IdLogPrazoPedidoVenda = LAPPV.IdLogPrazoPedidoVenda
) AS LOGPRAZO ON LOGPRAZO.CodigoPedido = ISNULL(PF.PedidoPai, PF.CodigoPedido) --AND LOGPRAZO.IdProduto = PB.IdProduto
WHERE PF.[DataInserido] BETWEEN Convert(datetime, '2022-05-01' ) AND Convert(datetime, '2022-05-31' )
AND StatusPedido = 'Entregue'
AND LP.[ParaIdEtapaFlexy] = 6
AND LP.[DeIdEtapaFlexy]  != 6
'''

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
      SELECT DISTINCT pedidos.CodigoPedido
				,DataFoiParaSeparacao
				,MAX(entrega.DataDeEntrega) OVER (PARTITION BY entrega.codigopedido) DataDeEntrega
				,MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido) Prazo --para pedidos que a aplicação atualizou o prazo mais que uma vez
				--,DATEDIFF(DAY,separacao.DataFoiParaSeparacao,separacao.Prazo) DiasParaEntregar
				--,DATEDIFF(DAY,separacao.DataFoiParaSeparacao,entrega.[DataAtualizacao]) DiasQueLevouParaEntregar
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
		AND MONTH(DataAtualizacao) = 5
		GROUP BY CodigoPedido) entrega
  ON pedidos.CodigoPedido = entrega.CodigoPedido
  WHERE separacao.Prazo IS NOT NULL -- Casos onde o sistema não atualizou o prazo na etapa 6, mas sim na próxima etapa
  ORDER BY DataDeEntrega desc
  '''

query_em_processo = '''
SELECT DISTINCT FoiParaEntrega.CodigoPedido
				,FoiParaEntrega.ParaIdEtapaFlexy IDAtual
				,MAX(separacao.DataFoiParaSeparacao) OVER (PARTITION BY separacao.CodigoPedido) DataFoiParaSeparacao
				,FoiParaEntrega.[DataAtualizacao] DataFoiParaEntrega
				,separacao.Prazo DataMaxDeEntrega
				,DATEDIFF(DAY,separacao.DataFoiParaSeparacao,separacao.Prazo) + FoiParaEntrega.[DataAtualizacao] - 3 DataPrevistaParaEntrega
				,FORMAT(DATEDIFF(DAY,separacao.DataFoiParaSeparacao,separacao.Prazo),'d','br') TempoMaximo
  FROM [HauszMapa].[Pedidos].[LogPedidos] FoiParaEntrega
  JOIN  (SELECT CodigoPedido
		,MAX([ParaPrazo]) OVER (PARTITION BY CodigoPedido) Prazo
		,DataAtualizacao DataFoiParaSeparacao
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 6) separacao
  ON FoiParaEntrega.CodigoPedido = separacao.CodigoPedido
  JOIN (SELECT CodigoPedido
			,MAX([DataAtualizacao]) UltimaAtualizacao
		FROM [HauszMapa].[Pedidos].[LogPedidos]
		GROUP BY CodigoPedido) atualizacao
	ON FoiParaEntrega.CodigoPedido = atualizacao.CodigoPedido
  WHERE ParaIdEtapaFlexy in (6,7,18,19)
  AND FoiParaEntrega.DataAtualizacao = atualizacao.UltimaAtualizacao
  ORDER BY FoiParaEntrega.CodigoPedido
  '''

query_sem_etapas = '''
SELECT DISTINCT pedidos.CodigoPedido
				,FORMAT(DataFoiParaSeparacao,'d','br') DataFoiParaSeparacao
				,FORMAT(MAX(pedidos.[DataAtualizacao]) OVER (PARTITION BY pedidos.codigopedido),'d','br') DataDeEntrega
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
  and IdUsuarioAlteracao = 'Aplicacao') emtransito
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
AND MONTH(DataAtualizacao) = 5
GROUP BY CodigoPedido) entrega
ON pedidos.CodigoPedido = entrega.CodigoPedido
WHERE separacao.ParaPrazo IS NOT NULL -- Casos onde o sistema não atualizou o prazo na etapa 6, mas sim na próxima etapa
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
		AND MONTH(DataAtualizacao) = MONTH(GETDATE())-1
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
  AND FORMAT(DataDeEntrega,'d') <= FORMAT(Prazo,'d')
  EXCEPT
  SELECT CodigoPedido FROM Logistica.LogReversaOcorrencia
  '''

query_total_de_pedidos_maio = '''
SELECT COUNT(pai.codigopedido) TotalDePedidos FROM
(SELECT DISTINCT pai.CodigoPedido
FROM [HauszMapa].[Pedidos].[PedidoFlexy] pai
JOIN (SELECT CodigoPedido
,MAX(DataAtualizacao) DataAtualizacao
FROM [HauszMapa].[Pedidos].[LogPedidos]
WHERE IdUsuarioAlteracao = 'Aplicacao'
GROUP BY CodigoPedido) maio
ON pai.CodigoPedido = maio.CodigoPedido
WHERE pai.StatusPedido = 'Entregue'
--AND pai.PedidoPai = pai.CodigoPedido -- Usado para desconsiderar pedidos filho
AND maio.DataAtualizacao BETWEEN Convert(datetime, '2022-05-01') AND Convert(datetime, '2022-06-01')) pai
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
