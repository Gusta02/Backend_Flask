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