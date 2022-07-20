SELECT [IdLog]
      ,[CodigoPedido]
      ,[DataAtualizacao]
      ,[ParaPrazo]
  FROM [HauszMapa].[Pedidos].[LogPedidos]
  WHERE ParaIdEtapaFlexy = 6
  AND MONTH(DataAtualizacao) = MONTH(GETDATE())-1