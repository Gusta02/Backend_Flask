SELECT 
            DISTINCT sr.CodigoPedidoSw as CodigoPedido
            ,est.Nome as Estado,
            FORMAT(prazo.DataFoiParaSeparacao,'d','pt-br') as DataIni,
            FORMAT(prazo.DataDeEntrega,'d','pt-br') as DataFim,
			FORMAT(prazo.Prazo,'d','pt-br') as DataPrevista,
            DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.DataDeEntrega) as Dias,
			DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.Prazo) as DiasPrevistos
            FROM  [HauszMapa].[ShowRoom].[Pedido] sr
            inner join HauszLogin.Cadastro.Cliente cli on cli.IdCliente = sr.IdCliente
            inner join HauszLogin.Cadastro.Usuario u on u.IdUsuario = cli.IdUsuario
            inner join HauszLogin.Cadastro.Cidade cit on cit.IdCidade = u.IdCidade
            inner join HauszLogin.Cadastro.Estado est on est.IdEstado = cit.IdEstado
			left join (  SELECT DISTINCT entrega.CodigoPedido
				,DataFoiParaSeparacao
				,MAX(entrega.[DataAtualizacao]) OVER (PARTITION BY entrega.codigopedido) DataDeEntrega
				,MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido) Prazo --para pedidos que a aplicacao atualizou o prazo mais que uma vez
				  FROM [HauszMapa].[Pedidos].[LogPedidos] entrega
				  JOIN  (SELECT CodigoPedido
						,ParaPrazo Prazo
						,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
				  FROM [HauszMapa].[Pedidos].[LogPedidos]
				  WHERE ParaIdEtapaFlexy = 6
				  and IdUsuarioAlteracao IN ('Aplicacao','NT SERVICE\SQLSERVERAGENT')) separacao
				  ON entrega.CodigoPedido = separacao.CodigoPedido
				  JOIN (SELECT CodigoPedido
							,MAX([IdLog]) UltimaAtualizacao
						FROM [HauszMapa].[Pedidos].[LogPedidos]
						WHERE DATEDIFF(Month,DataAtualizacao,GETDATE()) = 1
						--WHERE IdUsuarioAlteracao = 'Aplicacao'
						GROUP BY CodigoPedido) atualizacao
					ON entrega.CodigoPedido = atualizacao.CodigoPedido
				  WHERE entrega.ParaIdEtapaFlexy = 9
				  --AND entrega.IdUsuarioAlteracao = 'Aplicacao' --Remove pedidos que foram dados como entregues mais que uma vez
				  AND entrega.IdLog = atualizacao.UltimaAtualizacao -- Remove pedidos que apos serem entregues voltam para outro status
				  AND separacao.Prazo IS NOT NULL) prazo 
				  ON prazo.CodigoPedido = sr.CodigoPedidoSw
			where datediff(month,prazo.DataDeEntrega,getdate()) = 1
            --GROUP BY pf.CodigoPedido, est.Nome, ini.DataAtualizacao, fim.DataAtualizacao,Prazo

			UNION

SELECT 
            DISTINCT pf.CodigoPedido,
            est.Nome as Estado,
            FORMAT(prazo.DataFoiParaSeparacao,'d','pt-br') as DataIni,
            FORMAT(prazo.DataDeEntrega,'d','pt-br') as DataFim,
			FORMAT(prazo.Prazo,'d','pt-br') as DataPrevista,
            DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.DataDeEntrega) as Dias,
			DATEDIFF(day, prazo.DataFoiParaSeparacao, prazo.Prazo) as DiasPrevistos
            FROM HauszMapa.Pedidos.PedidoFlexy pf
            inner join HauszLogin.Cadastro.Cliente cli on cli.IdCliente = pf.IdCliente
            inner join HauszLogin.Cadastro.Usuario u on u.IdUsuario = cli.IdUsuario
            inner join HauszLogin.Cadastro.Cidade cit on cit.IdCidade = u.IdCidade
            inner join HauszLogin.Cadastro.Estado est on est.IdEstado = cit.IdEstado
			left join (  SELECT DISTINCT entrega.CodigoPedido
				,DataFoiParaSeparacao
				,MAX(entrega.[DataAtualizacao]) OVER (PARTITION BY entrega.codigopedido) DataDeEntrega
				,MAX(separacao.Prazo) OVER (PARTITION BY entrega.codigopedido) Prazo --para pedidos que a aplicacao atualizou o prazo mais que uma vez
				  FROM [HauszMapa].[Pedidos].[LogPedidos] entrega
				  JOIN  (SELECT CodigoPedido
						,ParaPrazo Prazo
						,MAX(DataAtualizacao) OVER (PARTITION BY CodigoPedido) DataFoiParaSeparacao
				  FROM [HauszMapa].[Pedidos].[LogPedidos]
				  WHERE ParaIdEtapaFlexy = 6
				  and IdUsuarioAlteracao IN ('Aplicacao','NT SERVICE\SQLSERVERAGENT')) separacao
				  ON entrega.CodigoPedido = separacao.CodigoPedido
				  JOIN (SELECT CodigoPedido
							,MAX([IdLog]) UltimaAtualizacao
						FROM [HauszMapa].[Pedidos].[LogPedidos]
						WHERE DATEDIFF(Month,DataAtualizacao,GETDATE()) = 1
						--WHERE IdUsuarioAlteracao = 'Aplicacao'
						GROUP BY CodigoPedido) atualizacao
					ON entrega.CodigoPedido = atualizacao.CodigoPedido
				  WHERE entrega.ParaIdEtapaFlexy = 9
				  --AND entrega.IdUsuarioAlteracao = 'Aplicacao' --Remove pedidos que foram dados como entregues mais que uma vez
				  AND entrega.IdLog = atualizacao.UltimaAtualizacao -- Remove pedidos que apos serem entregues voltam para outro status
				  AND separacao.Prazo IS NOT NULL) prazo 
				  ON prazo.CodigoPedido = pf.CodigoPedido
			where datediff(month,prazo.DataDeEntrega,getdate()) = 1
            --GROUP BY pf.CodigoPedido, est.Nome, ini.DataAtualizacao, fim.DataAtualizacao,Prazo