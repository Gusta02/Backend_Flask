from flask import Blueprint, render_template, request,  Response
from ..Dash_Logistica.kpis_luiz.main import estoque
#import locale
import io

financeiro = Blueprint('financeiro', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')


@financeiro.route("/dashboard/financeiro/", methods=["GET","POST"])
def home_financeiro():

    ################## Back dos Cards de inventário, vendas 2022 e gráfico #########################


    ########################## Inicialização ######################################

    
    marca_selecionada = request.args.get('marca')
    if marca_selecionada is None:
        marca_selecionada = ''

    try:
        ano_selecionado = int(request.args.get('ano'))
    except:
        ano_selecionado = 2022

    if ano_selecionado>2022:
        ano_previsao = ano_selecionado
        ano_selecionado = 0
    elif ano_selecionado==2022:
        ano_previsao = ano_selecionado
    else:
        ano_previsao = 0

    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    #locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  # Seleção da moeda brasileira
    #ano = date.today().year
    
    ########################## Cards de Venda e Inventário Total ######################################

    venda_total_showroom = 'R$ ' + str(estoque.calcula_venda_total(df=estoque.df_vendas_por_mes_por_marca,ano=ano_selecionado,marca=marca_selecionada,tipo='showroom')) #locale.currency(estoque.calcula_venda_total(df=estoque.df_vendas_por_mes_por_marca,ano=ano_selecionado,marca=marca_selecionada,tipo='showroom'), grouping=True)
    venda_total = 'R$ ' + str(estoque.calcula_venda_total(df=estoque.df_vendas_por_mes_por_marca,ano=ano_selecionado,marca=marca_selecionada)) #locale.currency(estoque.calcula_venda_total(df=estoque.df_vendas_por_mes_por_marca,ano=ano_selecionado,marca=marca_selecionada), grouping=True)
    inventario_total = 'R$ ' + str(estoque.inventario(marca=marca_selecionada).Inventário.sum()) #locale.currency(estoque.inventario(marca=marca_selecionada).Inventário.sum(), grouping=True)

    ########################## Gráfico de Vendas Por Mês Por Marca ######################################

    if ano_selecionado:
        labels_vendas = meses[estoque.filtra(df=estoque.df_vendas_por_mes_por_marca,ano=ano_selecionado).columns.get_level_values('Mes').min()-1:estoque.filtra(df=estoque.df_vendas_por_mes_por_marca,ano=ano_selecionado).columns.get_level_values('Mes').max()]
    else:
        labels_vendas = ['2020','2021','2022']
    
    values_vendas = estoque.calcula_venda_mensal(df=estoque.df_vendas_por_mes_por_marca,marca=marca_selecionada,ano=ano_selecionado).tolist()
    values_vendas_cliente = estoque.calcula_venda_mensal(df=estoque.df_vendas_por_mes_por_marca,marca= marca_selecionada,ano=ano_selecionado,tipo='cliente').tolist()
    values_vendas_showroom = estoque.calcula_venda_mensal(df=estoque.df_vendas_por_mes_por_marca,marca= marca_selecionada,ano=ano_selecionado,tipo='showroom').tolist()
    values_vendas_pct = estoque.calcula_pct(df=estoque.df_vendas_por_mes_por_marca,ano = ano_selecionado, marca = marca_selecionada)
    marcas = estoque.marcas

    ########################## Gráfico Top 3 SKUs Mais Vendidos ######################################    

    df_top3 = estoque.calcula_top_3(ano=ano_selecionado,marca=marca_selecionada)
    labels_top3 = df_top3.index.get_level_values('SKU').to_list()
    top3_sku_vendas = df_top3['valorTotal'].to_list()
    nomes_top3 = df_top3.index.get_level_values('NomeProduto').to_list()
    marcas_top3 = df_top3.index.get_level_values('Marca').to_list()
    try:
        values_top3 = [
            {'x':0, 'y':top3_sku_vendas[0], 'Produto': nomes_top3[0], 'Marca': marcas_top3[0]}, 
            {'x':1, 'y':top3_sku_vendas[1], 'Produto': nomes_top3[1], 'Marca': marcas_top3[1]}, 
            {'x':2, 'y':top3_sku_vendas[2], 'Produto': nomes_top3[2], 'Marca': marcas_top3[2]}
            ]
    except:
        try:
            values_top3 = [
                {'x':0, 'y':top3_sku_vendas[0], 'Produto': nomes_top3[0], 'Marca': marcas_top3[0]}, 
                {'x':1, 'y':top3_sku_vendas[1], 'Produto': nomes_top3[1], 'Marca': marcas_top3[1]}, 
                ]
        except:
            values_top3 = [
            {'x':0, 'y':top3_sku_vendas[0], 'Produto': nomes_top3[0], 'Marca': marcas_top3[0]}, 
            ]
    
    ########################## Gráfico SKUs Únicos ######################################   

    df_SKUs_unicos = estoque.calcula_SKUs_unicos(ano=ano_selecionado,marca=marca_selecionada)

    if ano_selecionado:
        try:
            labels_SKUs_unicos = meses[df_SKUs_unicos.index.get_level_values('Mes').min()-1:df_SKUs_unicos.index.get_level_values('Mes').max()]
        except:
            labels_SKUs_unicos = meses
    else:
        labels_SKUs_unicos = list(range(df_SKUs_unicos.index.get_level_values('Ano').min(),df_SKUs_unicos.index.get_level_values('Ano').max()+1))
    
    values_SKUs_unicos = df_SKUs_unicos.tolist()

    ########################## Projeção de Vendas ######################################

    if ano_previsao==2022:
        labels_projecao = meses[6:12]
        titulo_projecao = 'Projeção de Vendas X Unidade 2022 ' + marca_selecionada
        values_projecao,qt_unidades = estoque.calcula_projecao(ano = ano_previsao, marca = marca_selecionada)
    elif ano_previsao:
        labels_projecao = meses
        titulo_projecao = 'Projeção de Vendas X Unidades ' + str(ano_previsao) + ' ' + marca_selecionada
        values_projecao,qt_unidades = estoque.calcula_projecao(ano = ano_previsao, marca = marca_selecionada)
    else:
        labels_projecao = ['2022','2023','2024']
        titulo_projecao = 'Projeção de Vendas X Unidades ' + marca_selecionada
        values_projecao2022,qt_unidades = estoque.calcula_projecao(ano = 2022, marca = marca_selecionada)
        values_projecao2023,qt_unidades = estoque.calcula_projecao(ano = 2023, marca = marca_selecionada)
        values_projecao2024,qt_unidades = estoque.calcula_projecao(ano = 2024, marca = marca_selecionada)
        values_projecao,qt_unidades = estoque.calcula_projecao(ano = ano_previsao, marca = marca_selecionada)
        values_projecao = [sum(values_projecao2022), sum(values_projecao2023),sum(values_projecao2024)]

    ################# Dicionário de Variáveis ######################

    dict_variaveis = dict(
    inventario_total = inventario_total
    ,venda_total = venda_total
    ,labels_vendas = labels_vendas
    ,values_vendas = values_vendas
    ,marcas = marcas
    ,marca_selecionada = marca_selecionada
    ,values_vendas_pct = values_vendas_pct
    ,venda_total_showroom=venda_total_showroom
    ,values_vendas_cliente=values_vendas_cliente
    ,values_vendas_showroom=values_vendas_showroom
    ,ano_selecionado=ano_selecionado
    ,labels_top3=labels_top3
    ,values_top3=values_top3
    ,labels_SKUs_unicos=labels_SKUs_unicos
    ,values_SKUs_unicos = values_SKUs_unicos
    ,labels_projecao = labels_projecao
    ,values_projecao = values_projecao
    ,title_projecao = 'Projeção de Vendas' + str(ano_previsao)
    ,qt_unidades = qt_unidades
    ,titulo_projecao = titulo_projecao
    )
    
    return render_template('home_financeiro.html',**dict_variaveis)

@financeiro.route('/download/<df>/<filename>',methods=['GET']) # Gera Arquivos em Excel para Download
def download_excel(df,filename):

    tabela = getattr(estoque, df)
    buffer = io.BytesIO()
    tabela.to_excel(buffer,engine='openpyxl')
    headers = {
    'Content-Disposition': 'attachment; filename={}.xlsx'.format(filename),
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)