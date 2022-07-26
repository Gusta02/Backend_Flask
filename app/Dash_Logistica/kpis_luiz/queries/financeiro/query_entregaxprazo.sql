SELECT DISTINCT entrega.CodigoPedido
				,DataFoiParaSeparacao
				,MAX(entrega.[DataAtualizacao]) OVER (PARTITION BY entrega.codigopedido) DataDeEntrega
				,MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido) Prazo --para pedidos que a aplicacao atualizou o prazo mais que uma vez
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
  AND entrega.IdLog = atualizacao.UltimaAtualizacao -- Remove pedidos que apos serem entregues voltam para outro status
  AND separacao.Prazo IS NOT NULL -- Casos onde o sistema nao atualizou o prazo na etapa 6, mas sim na proxima etapa
  --AND separacao.Prazo > entrega.DataAtualizacao
  ORDER BY CodigoPedido desc