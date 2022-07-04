from config import get_connection
from sqlalchemy import text


#consulta do BD em cima da tabela  select * from HauszMapa.Pedidos.LogPedidos where ParaIdEtapaFlexy = 9
def Quant_entregue():
    engine = get_connection()
    list_entregue = []
    with engine.connect() as conn:
        query_entregue  = (text(f"""
        select COUNT(lg.CodigoPedido) as Quantidade_Entregue from HauszMapa.Pedidos.LogPedidos lg
        JOIN (SELECT CodigoPedido
        ,MAX(IdLog) ultimaetapa
        FROM [HauszMapa].[Pedidos].[LogPedidos]
        WHERE IdUsuarioAlteracao = 'Aplicacao'
        GROUP BY CodigoPedido) maxlog
        ON maxlog.CodigoPedido = lg.CodigoPedido
        where ParaIdEtapaFlexy = 9 
		AND lg.IdLog = maxlog.ultimaetapa
        AND DataAtualizacao between '2022-06-01' and '2022-07-01'
		AND IdUsuarioAlteracao = 'Aplicacao'
        """))
        lista_entreguetotal = conn.execute(query_entregue).all()
        for lista in lista_entreguetotal:
            dict_filtro_hoje = {}
            for keys, values in lista.items():
                dict_filtro_hoje[keys] = values
            list_entregue.append(dict_filtro_hoje)

    return list_entregue

#consulta do BD em cima da tabela  select *  from HauszMapa.Pedidos.LogPedidos where ParaIdEtapaFlexy = 25
def Quant_avaria():
    engine = get_connection()
    list_avaria = []
    with engine.connect() as conn:
        query_avaria = (text(f"""
        select count(avarias.Avarias) QuantidadeAvaria from
        (select  DISTINCT lr.CodigoPedido Avarias
		from HauszMapa.Logistica.LogReversaOcorrencia lr
		join(select CodigoPedido, max(IdOcorrencia) ultimaetapa ,max(DataInserido) ultimadata
		from HauszMapa.Logistica.LogReversaOcorrencia 
		where IdCausaOcorrencia = 1
		GROUP BY CodigoPedido) maxlog on maxlog.CodigoPedido = lr.CodigoPedido
		--where lr.IdCausaOcorrencia = 1
		and DataInserido between '2022-06-01' and '2022-07-01') avarias
        """))
        lista_avaria = conn.execute(query_avaria).all()
        for lista in lista_avaria:
            dict_avaria = {}
            for keys, values in lista.items():
                dict_avaria[keys] = values
            list_avaria.append(dict_avaria)

    return list_avaria