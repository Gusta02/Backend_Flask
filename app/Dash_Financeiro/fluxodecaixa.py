from .kpis_michel.classes import dict_empresas,resumo_fc,resumo_cr,resumo_cp,lista_resumo_detalhado, rank
from flask import Blueprint, render_template, request, Response
import locale
import io
import pandas as pd

Contas_Pagar = Blueprint('Contas_Pagar', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

@Contas_Pagar.route("/dashboard/financeiro/ContasPagar", methods=["GET","POST"])
def Contas_a_Pagar():

    locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")  
    
    selecionar_empresa = 'Todas'
    periodicidade = 0

    if request.method == 'POST':
        selecionar_empresa =  request.form.get('empresa')
        periodicidade = int(request.form.get('periodicidade'))
        
    empresa_selecionada = dict_empresas[selecionar_empresa]
    empresa_selecionada.filtra_dias(periodicidade)

    filtro_empresas = list(dict_empresas.keys())

    #labels grafico

    primeiro = rank.index[0][0]
    valor_pri = rank.index[0][1]

    segundo = rank.index[2][0]
    valor_seg = rank.index[2][1]

    terceiro = rank.index[3][0]
    valor_ter = rank.index[3][1]

    quarto= rank.index[6][0]
    valor_quar = rank.index[6][1]

    quint= rank.index[7][0]
    valor_quin = rank.index[7][1]

    labels_empresa = [primeiro,segundo, terceiro, quarto, quint]
    values_empresa = [valor_pri,valor_seg, valor_ter, valor_quar, valor_quin]

    #fim grafico
    #renderizando no front
    fluxodecaixa = locale.currency(empresa_selecionada.get_valor(), grouping=True)
    card_total_pagar = locale.currency(empresa_selecionada.calcula_tipo('CONTAS A PAGAR'), grouping= True)
    card_total_receber = locale.currency(empresa_selecionada.calcula_tipo('CONTAS A RECEBER'), grouping= True)

    return render_template('contas_a_pagar.html', page = 1, card= fluxodecaixa, card1 = card_total_pagar, card2= card_total_receber, 
    filtro_empresa = filtro_empresas, selecionar_empresa = selecionar_empresa, labels_empresa = labels_empresa, values_empresa = values_empresa )

@Contas_Pagar.route("/dashboard/financeiro/downloadresumo", methods=["GET","POST"])
def PagarDownload_excel():
    
    resumo_fc.rename(columns={360:'12 meses'},inplace=True)
    resumo_cp.rename(columns={360:'12 meses'},inplace=True)
    resumo_cr.rename(columns={360:'12 meses'},inplace=True)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        resumo_fc.to_excel(writer, sheet_name = 'Fluxo de Caixa')
        resumo_cr.to_excel(writer, sheet_name = 'Contas a Receber')
        resumo_cp.to_excel(writer, sheet_name = 'Contas a Pagar')
    headers = {
    'Content-Disposition': 'attachment; filename=Fluxo_de_Caixa-Resumo.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)

@Contas_Pagar.route("/dashboard/financeiro/download_resumo_detalhado", methods=["GET","POST"])
def download_resumo_detalhado():
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        lista_resumo_detalhado[0].to_excel(writer, sheet_name = '15 dias')
        lista_resumo_detalhado[1].to_excel(writer, sheet_name = '30 dias')
        lista_resumo_detalhado[2].to_excel(writer, sheet_name = '60 dias')
        lista_resumo_detalhado[3].to_excel(writer, sheet_name = '90 dias')
        lista_resumo_detalhado[4].to_excel(writer, sheet_name = '12 meses')
    headers = {
    'Content-Disposition': 'attachment; filename=Fluxo_de_Caixa_Detalhado.xlsx',
    'Content-type': 'application/vnd.ms-excel'
    }
    return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)