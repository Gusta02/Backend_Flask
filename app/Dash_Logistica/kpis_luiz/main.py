import package_luiz.sql_queries as sql
from package_luiz.data_extractor import sql_to_pd
from package_luiz.kpi import Entregas,SemEtapas,PedidoPerfeito,IndicadorPerformance

entregas = Entregas()
sem_etapas = SemEtapas()
pedido_perfeito = PedidoPerfeito()


kpi_entregues_no_prazo = round(entregas.indice.loc[True],2)
entregas_sem_etapa_19 = round(sem_etapas.calcula_sem_19().loc[True],2)
entrega_sem_etapa_7 = round(sem_etapas.calcula_sem_7().loc[True],2)
kpi_pedido_perfeito = pedido_perfeito.calcula_indice()
kpi_pedidos_ja_atrasados = sql_to_pd(sql.query_pedidos_ja_atrasados).iloc[0,0]

localizacaoLR = IndicadorPerformance(7,4,5)
print(localizacaoLR.fatornota7)
