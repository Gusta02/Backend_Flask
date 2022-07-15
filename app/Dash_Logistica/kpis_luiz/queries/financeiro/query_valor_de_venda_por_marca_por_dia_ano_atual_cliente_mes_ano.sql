SELECT Quantidade*PrecoUnitario valorTotal
	  ,prodsfornec.NomeFantasia Marca
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
	JOIN (SELECT SKU, prods.IdMarca, fornec.NomeFantasia 
		FROM HauszMapa.Produtos.ProdutoBasico prods
		JOIN (SELECT fornecmarca.CnpjFornecedor,IdMarca,fornecnome.NomeFantasia FROM [HauszMapa].[Produtos].[FornecedorMarca] fornecmarca 
		JOIN (SELECT NomeFantasia, CnpjFornecedor FROM [HauszMapa].[Cadastro].[Fornecedor]) fornecnome 
			ON fornecmarca.CnpjFornecedor = fornecnome.CnpjFornecedor
		WHERE IdMarca NOT IN (71)) fornec
	ON fornec.IdMarca = prods.IdMarca) prodsfornec
	ON itens.SKU = prodsfornec.SKU
	AND bitAtivo = 1