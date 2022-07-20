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