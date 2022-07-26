import os

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_frete_recebido.sql')) as f:
	query_frete_recebido= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_prazo_na_separacao.sql')) as f:
	query_prazo_na_separacao= f.read()


with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_entregaxprazo.sql')) as f:
	query_entregaxprazo= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_sem_etapas.sql')) as f:
	query_sem_etapas= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_pedido_perfeito.sql')) as f:
	query_pedido_perfeito= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_total_de_pedidos.sql')) as f:
	query_total_de_pedidos= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_pedidos_ja_atrasados.sql')) as f:
	query_pedidos_ja_atrasados= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_pedidos_ja_atrasados.sql')) as f:
	query_pedidos_ja_atrasados= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_fator_multiplicador_prod.sql')) as f:
	query_fator_multiplicador_prod= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_fator_multiplicador_show_room.sql')) as f:
	query_fator_multiplicador_show_room= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_quantidade_do_sistema.sql')) as f:
	query_quantidade_do_sistema= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_entregas_por_estado.sql')) as f:
	query_entregas_por_estado= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_produtos_por_pedido.sql')) as f:
	query_produtos_por_pedido= f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_preco_produtos_estoque.sql')) as f:
	query_preco_produtos_estoque = f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_venda_por_marca.sql')) as f:
	query_vendas_ano_atual = f.read()

with open(os.path.abspath('app/Dash_Logistica/kpis_luiz/queries/financeiro/query_venda_por_SKU_por_mes.sql')) as f:
	query_venda_SKU_mensal = f.read()