Select SKU,Marca,NomeProduto FROM (Select SKU, NomeProduto, IdMarca from HauszMapa.Produtos.ProdutoBasico

Union 

Select SKU,NomeProduto,IdMarca from HauszMapa.ShowRoom.ProdutoBasico) todosprodutos
JOIN (SELECT IdMarca,Marca from HauszMapa.Produtos.Marca) marca
ON todosprodutos.IdMarca = marca.IdMarca