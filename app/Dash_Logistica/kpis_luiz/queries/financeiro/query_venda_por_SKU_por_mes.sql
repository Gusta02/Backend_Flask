	SELECT SUM(Quantidade*PrecoUnitarioDescontado) valorTotal
		,itens.SKU
		,NomeProduto
	  ,Marca
	  ,MONTH(itens.DataInserido) Mes
	  ,YEAR(itens.DataInserido) Ano
	  --,'cliente' AS Tipo
  FROM [HauszMapa].[Pedidos].[ItensFlexy] itens
  JOIN (SELECT CodigoPedido
			,IdEtapaFlexy
		FROM [HauszMapa].[Pedidos].[PedidoFlexy]
		WHERE IdEtapaFlexy != 11 -- remove cancelados
		) pedidos
	ON itens.CodigoPedido = pedidos.CodigoPedido
	JOIN	(Select SKU,Marca,NomeProduto FROM (Select SKU, NomeProduto, IdMarca from HauszMapa.Produtos.ProdutoBasico

	Union 

	Select SKU,NomeProduto,IdMarca from HauszMapa.ShowRoom.ProdutoBasico) todosprodutos
	JOIN (SELECT IdMarca,Marca from HauszMapa.Produtos.Marca) marca
	ON todosprodutos.IdMarca = marca.IdMarca) todos
	ON itens.SKU = todos.SKU
	WHERE itens.bitAtivo = 1
	AND Marca != 'Hausz'
	GROUP BY itens.SKU, MONTH(itens.DataInserido), YEAR(itens.DataInserido), Marca, NomeProduto
 
  UNION ALL

  SELECT SUM(Quantidade*PrecoUnitario) valorTotal
		,itens.SKU
		,NomeProduto Produto
	  ,Marca
	  ,MONTH(itens.DataInserido) Mes
	  ,YEAR(itens.DataInserido) Ano
	  --,'showroom' AS Tipo
  FROM [HauszMapa].[ShowRoom].[ItensPedido] itens
  JOIN (SELECT CodigoPedidoSw
			,IdEtapaFlexy
		FROM [HauszMapa].[ShowRoom].[Pedido]
		WHERE IdEtapaFlexy != 11 -- remove cancelados
		) pedidos
	ON itens.CodigoPedidoSw = pedidos.CodigoPedidoSw
	JOIN	(Select SKU,Marca,NomeProduto FROM (Select SKU, NomeProduto, IdMarca from HauszMapa.Produtos.ProdutoBasico

	Union 

	Select SKU,NomeProduto,IdMarca from HauszMapa.ShowRoom.ProdutoBasico) todosprodutos
	JOIN (SELECT IdMarca,Marca from HauszMapa.Produtos.Marca) marca
	ON todosprodutos.IdMarca = marca.IdMarca) todos
	ON itens.SKU = todos.SKU
	WHERE itens.bitAtivo = 1
	AND Marca != 'Hausz'
	GROUP BY itens.SKU, MONTH(itens.DataInserido), YEAR(itens.DataInserido), NomeProduto, Marca
	