SELECT DISTINCT entrega.CodigoPedido
				,DataFoiParaSeparacao
				,entrega.ParaIdEtapaFlexy EtapaAtual
				,MAX(entrega.[DataAtualizacao]) OVER (PARTITION BY entrega.codigopedido) DataEntrouEtapaAtual
				,MAX(pagamento.PrazoOriginal) OVER (PARTITION BY entrega.codigopedido) PrazoOriginal
				,MAX(separacao.PrazoAtualizado) OVER (PARTITION BY entrega.codigopedido) PrazoAtualizado
				,DATEDIFF(DAY,separacao.DataFoiParaSeparacao,separacao.PrazoAtualizado) LeadTime
  FROM [HauszMapa].[Pedidos].[LogPedidos] entrega
  JOIN  (SELECT CodigoPedido
		,ParaPrazo PrazoAtualizado
		,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 6
  and IdUsuarioAlteracao IN ('Aplicacao','NT SERVICE\SQLSERVERAGENT')) separacao
  ON entrega.CodigoPedido = separacao.CodigoPedido
  JOIN  (SELECT CodigoPedido
		,ParaPrazo PrazoOriginal
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE DeIdEtapaFlexy = 2
  and IdUsuarioAlteracao IN ('Aplicacao','NT SERVICE\SQLSERVERAGENT')) pagamento
  ON entrega.CodigoPedido = pagamento.CodigoPedido
  JOIN (SELECT CodigoPedido
			,MAX([IdLog]) UltimaAtualizacao
		FROM [HauszMapa].[Pedidos].[LogPedidos]
		WHERE DATEDIFF(Month,DataAtualizacao,GETDATE()) < 5
		GROUP BY CodigoPedido) atualizacao
  ON entrega.CodigoPedido = atualizacao.CodigoPedido
  JOIN (SELECT CodigoPedido
		,IdEtapaFlexy
		FROM HauszMapa.Pedidos.PedidoFlexy
		) pf 
		ON entrega.CodigoPedido = pf.CodigoPedido
  WHERE entrega.ParaIdEtapaFlexy in (6,7,9,18,19)
  AND entrega.IdLog = UltimaAtualizacao
  ORDER BY CodigoPedido desc