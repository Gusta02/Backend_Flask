/****** Script for SelectTopNRows command from SSMS  ******/
SELECT --pedido.[IdUnidade]
		unidade.Nome 
		,MONTH(pedido.DataInserido) AS MesInserido
		,YEAR(pedido.DataInserido) AS AnoInserido
		,SUM([ValorTotalDescontado]) ValorVenda
      --,CONCAT (Month([DataInserido]), '/', Year([DataInserido])) AS MesInserido
      
  FROM [HauszMapa].[Pedidos].[PedidoFlexy] pedido
  JOIN HauszMapa.Cadastro.Unidade AS unidade
  ON pedido.IdUnidade = unidade.IdUnidade
  WHERE IdEtapaFlexy NOT IN ('11') --Remove Cancelados
  Group BY Nome,MONTH(pedido.DataInserido), YEAR(pedido.DataInserido)
  ORDER BY Nome, AnoInserido, MesInserido