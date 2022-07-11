SELECT SUM(Quantidade*PrecoUnitarioDescontado) ValorVenda
	  ,prodsfornec.NomeFantasia
	  ,FORMAT(itens.DataInserido, 'd', 'pt-br') DataDaVenda
  FROM [HauszMapa].[Pedidos].[ItensFlexy] itens
  JOIN (SELECT CodigoPedido
			,IdEtapaFlexy
		FROM [HauszMapa].[Pedidos].[PedidoFlexy]
		WHERE IdEtapaFlexy != 11 -- remove cancelados
		) pedidos
	ON itens.CodigoPedido = pedidos.CodigoPedido
	JOIN (SELECT SKU, prods.IdMarca, fornec.NomeFantasia 
		FROM HauszMapa.Produtos.ProdutoBasico prods
		JOIN (SELECT fornecmarca.CnpjFornecedor,IdMarca,fornecnome.NomeFantasia FROM [HauszMapa].[Produtos].[FornecedorMarca] fornecmarca 
		JOIN (SELECT NomeFantasia, CnpjFornecedor FROM [HauszMapa].[Cadastro].[Fornecedor]) fornecnome 
			ON fornecmarca.CnpjFornecedor = fornecnome.CnpjFornecedor
		WHERE IdMarca NOT IN (71)) fornec
	ON fornec.IdMarca = prods.IdMarca) prodsfornec
	ON itens.SKU = prodsfornec.SKU
	WHERE DATEDIFF(YEAR,itens.DataInserido,GETDATE()) = 0
	AND bitAtivo = 1
  Group by prodsfornec.NomeFantasia, FORMAT(itens.DataInserido, 'd', 'pt-br')

  UNION

  SELECT SUM(Quantidade*PrecoUnitario) ValorVenda
	  ,prodsfornec.NomeFantasia
	  ,FORMAT(itens.DataInserido, 'd', 'pt-br') DataDaVenda
  FROM [HauszMapa].[ShowRoom].[ItensPedido] itens
  JOIN (SELECT CodigoPedidoSw
			,IdEtapaFlexy
		FROM [HauszMapa].[ShowRoom].[Pedido]
		WHERE IdEtapaFlexy != 11 -- remove cancelados
		) pedidos
	ON itens.CodigoPedidoSw = pedidos.CodigoPedidoSw
	JOIN (SELECT SKU, prods.IdMarca, fornec.NomeFantasia 
		FROM HauszMapa.Produtos.ProdutoBasico prods
		JOIN (SELECT fornecmarca.CnpjFornecedor,IdMarca,fornecnome.NomeFantasia FROM [HauszMapa].[Produtos].[FornecedorMarca] fornecmarca 
		JOIN (SELECT NomeFantasia, CnpjFornecedor FROM [HauszMapa].[Cadastro].[Fornecedor]) fornecnome 
			ON fornecmarca.CnpjFornecedor = fornecnome.CnpjFornecedor
		WHERE IdMarca NOT IN (71)) fornec
	ON fornec.IdMarca = prods.IdMarca) prodsfornec
	ON itens.SKU = prodsfornec.SKU
	WHERE DATEDIFF(YEAR,itens.DataInserido,GETDATE()) = 0
	AND bitAtivo = 1
  Group by prodsfornec.NomeFantasia, FORMAT(itens.DataInserido, 'd', 'pt-br')