SELECT FORMAT((SUM(PrecoFrete)*1.0175),'c','pt-br') as FreteRecebido
FROM HauszMapa.Pedidos.PedidoFlexy
WHERE IdEtapaFlexy NOT IN  (1,11,15,16,26,41)
AND MONTH(DataInserido) = MONTH(GETDATE())