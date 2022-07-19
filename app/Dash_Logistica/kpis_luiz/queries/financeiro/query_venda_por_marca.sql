SELECT Quantidade*PrecoUnitarioDescontado valorTotal
	  ,Marca
	  ,MONTH(itens.DataInserido) Mes
	  ,YEAR(itens.DataInserido) Ano
	  ,'cliente' AS Tipo
  FROM [HauszMapa].[Pedidos].[ItensFlexy] itens
  JOIN (SELECT CodigoPedido
			,IdEtapaFlexy
		FROM [HauszMapa].[Pedidos].[PedidoFlexy]
		WHERE IdEtapaFlexy != 11 -- remove cancelados
		) pedidos
	ON itens.CodigoPedido = pedidos.CodigoPedido
	LEFT JOIN (SELECT SKU, NomeProduto
		FROM HauszMapa.Produtos.ProdutoBasico
		WHERE IdMarca NOT IN (71)
		) prodsb
	ON itens.SKU = prodsb.SKU
	LEFT JOIN (SELECT SKU, marca.Marca
	FROM HauszMapa.Produtos.ProdutoDetalhe prod
	JOIN [HauszMapa].[Produtos].[Marca] marca ON prod.IdMarca = marca.IdMarca
	WHERE prod.IdMarca NOT IN (71)
		) prodsd
	ON itens.SKU = prodsd.SKU
	WHERE itens.bitAtivo = 1
 
  UNION ALL

  SELECT Quantidade*PrecoUnitario valorTotal
	  ,Marca
	  ,MONTH(itens.DataInserido) Mes
	  ,YEAR(itens.DataInserido) Ano
	  ,'showroom' AS Tipo
  FROM [HauszMapa].[ShowRoom].[ItensPedido] itens
  JOIN (SELECT CodigoPedidoSw
			,IdEtapaFlexy
		FROM [HauszMapa].[ShowRoom].[Pedido]
		WHERE IdEtapaFlexy != 11 -- remove cancelados
		) pedidos
	ON itens.CodigoPedidoSw = pedidos.CodigoPedidoSw
	LEFT JOIN (SELECT SKU, NomeProduto
		FROM HauszMapa.Produtos.ProdutoBasico
		WHERE IdMarca NOT IN (71)
		) prodsb
	ON itens.SKU = prodsb.SKU
	LEFT JOIN (SELECT SKU, marca.Marca
	FROM HauszMapa.Produtos.ProdutoDetalhe prod
	JOIN [HauszMapa].[Produtos].[Marca] marca ON prod.IdMarca = marca.IdMarca
	WHERE prod.IdMarca NOT IN (71)
		) prodsd
	ON itens.SKU = prodsd.SKU
	WHERE itens.bitAtivo = 1
  