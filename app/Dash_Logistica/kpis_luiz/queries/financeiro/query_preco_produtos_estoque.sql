SELECT pp.[SKU]
      ,[Preco]
	  ,prodsfornec.NomeFantasia
  FROM [HauszMapa].[Produtos].[ProdutoPreco] pp
  JOIN (SELECT SKU, prods.IdMarca, fornec.NomeFantasia 
		FROM HauszMapa.Produtos.ProdutoBasico prods
		JOIN (SELECT fornecmarca.CnpjFornecedor,IdMarca,fornecnome.NomeFantasia FROM [HauszMapa].[Produtos].[FornecedorMarca] fornecmarca 
		JOIN (SELECT NomeFantasia, CnpjFornecedor FROM [HauszMapa].[Cadastro].[Fornecedor]) fornecnome 
			ON fornecmarca.CnpjFornecedor = fornecnome.CnpjFornecedor
		WHERE IdMarca NOT IN (71)) fornec
	ON fornec.IdMarca = prods.IdMarca) prodsfornec	
	ON prodsfornec.SKU = pp.SKU
	WHERE IdUnidade = 1
	AND IdEstoque IN (1,5)