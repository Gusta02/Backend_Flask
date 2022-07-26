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
	WHERE pedidos_ativos.StatusPedido IN ('Pago','Aguardando Arquiteto','Entrega Futura','Verificando Estoque') --aguardando confimarcao do cliente deu pau por causa do acento
	ORDER BY CodigoPedido