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