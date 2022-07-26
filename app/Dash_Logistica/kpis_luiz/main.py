from app.Dash_Logistica.kpis_luiz import sql_queries as sql
from app.Dash_Logistica.kpis_luiz.data_extractor import sql_to_pd
from app.Dash_Logistica.kpis_luiz.kpi import Entregas, LeadTime, SemEtapas,PedidoPerfeito,IndicadorPerformance,DockStockTime,Estoque


##################### Instâncias de Objetos que Calculam KPIs ##########################

entregas = Entregas()
sem_etapas = SemEtapas()
pedido_perfeito = PedidoPerfeito()
dockstocktime = DockStockTime()
estoque = Estoque()
leadtime = LeadTime()

####################### KPIs resultates dos Objetos ##############################

kpi_entregues_no_prazo = entregas.indice.loc[True]
pct_entregas_sem_etapa_19 = sem_etapas.calcula_sem_19().loc[True]
pct_entregas_sem_etapa_7 = sem_etapas.calcula_sem_7().loc[True]
kpi_pedido_perfeito = pedido_perfeito.calcula_indice()
kpi_pedidos_ja_atrasados = sql_to_pd(sql.query_pedidos_ja_atrasados).iloc[0,0]
kpi_dock_stock_time = dockstocktime.calcula_indice()
kpi_leadtime_nacional = leadtime.indice
#kpi_excesso_de_estoque = estoque.count_estoque()['excesso']
#kpi_falta_de_estoque = estoque.count_estoque()['falta']
#kpi_acuracidade_do_sistema = estoque.indice
#estoque.rejeicoes_futuras()

# ##################### Instâncias de Objetos Performance do Time Logística ##########################

# dict_performance_time_logistica = dict(
# ind_localizacaoLR = IndicadorPerformance(7,4,5,6)
# ,ind_tempocicloLR = IndicadorPerformance(25,20,5,23)
# ,ind_pedidoperfeito = IndicadorPerformance(80,90,5,kpi_pedido_perfeito*100)
# ,ind_separacao = IndicadorPerformance(24,18,5,20)
# ,ind_dockstocktime = IndicadorPerformance(3,1.5,4,kpi_dock_stock_time*100)
# )

# ##################### Instâncias de Objetos Performance do Time Transporte ##########################
# dict_performance_time_transporte = dict(
# ind_leadtime = IndicadorPerformance(15,10,5)
# ,ind_coletasnoprazo = IndicadorPerformance(85,95,5)
# ,ind_entregasnoprazo = IndicadorPerformance(85,95,5,kpi_entregues_no_prazo*100)
# ,ind_avarias = IndicadorPerformance(5,2.5,5)
# #,ind_nps = IndicadorPerformance(7,8,4)
# )

# ####################### KPIs dos times ##############################

# kpi_time_logistica = IndicadorPerformance.calcula_kpi_time(dict_performance_time_logistica)
# kpi_time_transporte = IndicadorPerformance.calcula_kpi_time(dict_performance_time_transporte)
