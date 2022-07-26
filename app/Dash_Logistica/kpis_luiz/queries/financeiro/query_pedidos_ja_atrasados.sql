SELECT COUNT(pedidosatrados.CodigoPedido) FROM (SELECT DISTINCT pedidos.CodigoPedido
				,UltimaAtualizacao
				,EtapaAtual
				,FORMAT(DataFoiParaSeparacao,'d','br') DataFoiParaSeparacao
				,FORMAT(MAX(separacao.Prazo) OVER (PARTITION BY pedidos.codigopedido),'d','br') Prazo --para pedidos que a aplicacao atualizou o prazo mais que uma vez
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
  WHERE separacao.Prazo IS NOT NULL -- Casos onde o sistema nao atualizou o prazo na etapa 6, mas sim na proxima etapa
  AND etapaatual.IdLog = atualizacao.UltimaAtualizacao
  AND GETDATE() > Prazo) pedidosatrados