from flask import Blueprint, render_template, request
from ..controllers.controller_logistica import IntegracaoWms
import pandas as pd


wms = Blueprint('wms', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

def card1():
        #rejeicaohj, sao as rejeicoes do dia atual -  CARD 1
        rejeicaohj = IntegracaoWms.card_hoje()
        rejeicaohj = rejeicaohj[0]['quantidade_de_rejeicao']
        return rejeicaohj

def card2():
        #dia_percentual é a porcentagem de rejeicao com base no dia anterior - CARD 2
        ontem = IntegracaoWms.card_ontem()

        try:
                percentual = card1 / ontem * 100
        except:
                percentual = 0
        dia_percentual = "{:.2f}".format(percentual)

        return dia_percentual

def card3():
        
        mes_passado = IntegracaoWms.card_mes_passado()
        mes_passado = mes_passado[0]['quantidade_de_rejeicao']

        #mes seguinte 
        mes_seguinte = IntegracaoWms.card_mes_seguinte()
        mes_seguinte = mes_seguinte[0]['quantidade_de_rejeicao']

        percentual_mes = ((mes_seguinte / mes_passado) * 100)-100

        mes_resultado =f'{percentual_mes:.2f}' 
        #/////////// CARD COM PERCENTUAL DAS REJEICOES DO MES ANTERIOR COM O MES ATUAL - CARD 3

        return mes_resultado 

def card4():
        #contem todas as rejeicoes do dia anterior   - CARD 4
        ontem = IntegracaoWms.card_ontem()
        return ontem

def card5():
        #total de rejeicoes que tivemos no mes anterior - card 5
        rejeicoes_mes_anterior = IntegracaoWms.card_mes_passado()
        rejeicoes_mes_anterior = rejeicoes_mes_anterior[0]['quantidade_de_rejeicao']
        return rejeicoes_mes_anterior

def card6():
        # /////////////////  STATUS VERIFICANDO ESTOQUE - CARD 6 
        possivel_rejeicao = IntegracaoWms.Verificando()
        possivel_rejeicao = possivel_rejeicao[0]['VerificandoEstoque']
        return possivel_rejeicao

def categoriza_status():
        lista_values = {'0':'Integrou','6':'SemEstoque','3':'Erro'}

        rejeicoes_wms = IntegracaoWms.select_wms_rejeicoes()
        rejeicoes = pd.DataFrame(rejeicoes_wms)


        rejeicoes['statusRejeicao'] = rejeicoes['RejeicaoId'].map(lista_values)
        rejeicoes[rejeicoes.loc[:,'statusRejeicao'].astype(str).str.contains('Integrou')]

def read_excel(tabela):

        planilhas = pd.read_excel(f'C:/Users/Gusta/Documents/Backend_Flask/app/Dash_Logistica/planilha/{tabela}.xlsx',skiprows=[0,1,2,3,4,5])
        dfwms2 = pd.read_excel('C:/Users/Gusta/Documents/Backend_Flask/app/Dash_Logistica/planilha/WD6part2.xlsx',skiprows=[0,1,2,3,4,5])
        dfwxd1 = pd.read_excel('C:/Users/Gusta/Documents/Backend_Flask/app/Dash_Logistica/planilha/WXDpart1.xlsx',skiprows=[0,1,2,3,4,5])
        dfwxd2 = pd.read_excel('C:/Users/Gusta/Documents/Backend_Flask/app/Dash_Logistica/planilha/WXDpart2.xlsx',skiprows=[0,1,2,3,4,5])
        dfwpj1 = pd.read_excel('C:/Users/Gusta/Documents/Backend_Flask/app/Dash_Logistica/planilha/WPJpart1.xlsx',skiprows=[0,1,2,3,4,5,6])
        dfwpj2 = pd.read_excel('C:/Users/Gusta/Documents/Backend_Flask/app/Dash_Logistica/planilha/WPJpart2.xlsx',skiprows=[0,1,2,3,4,5,6])
        return planilhas
 
#Unifica tabelas wms, renomeia colunas e concatena
def uni_tabela_wms():
        dfwxd1 = read_excel('WXDpart1')
        dfwxd1['UNIDADE_CD'] = 'Hausz-SP'
        dfwxd1[['Dt. Inclusão','Dt. Mov.','Dt. Reserva','Dt. Conf. Sep.'
        ,'Dt. Embarque','No. D.P.','No. Cli.','Obs. Resumida','No. Ped. Cli.'
        ,'No. N.F.','Sit. Fase','Transp. (Ped.)','Destinatário','Doca','Vols.', 'UNIDADE_CD']]
        
        dfwxd2 = read_excel('WXDpart2')
        dfwxd2['UNIDADE_CD'] = 'Hausz-SC'
        dfwxd2[['Dt. Inclusão','Dt. Mov.','Dt. Reserva','Dt. Conf. Sep.'
        ,'Dt. Embarque','No. D.P.','No. Cli.','Obs. Resumida','No. Ped. Cli.'
        ,'No. N.F.','Sit. Fase','Transp. (Ped.)','Destinatário','Doca','Vols.', 'UNIDADE_CD']]

        unificalocwms = pd.concat([dfwxd1, dfwxd2])

        unificalocwms.rename(columns={'Dt. Inclusão':'DATA_INCLUSAO_PEDIDO','Dt. Mov.':'DATA_MOVIMENTO'
                ,'Dt. Reserva':'DATA_RESERVA','Dt. Conf. Sep.':'DATA_CONFERENCIA_SEPARACAO'
                ,'Dt. N.F.':'DATA_NOTA_FISCAL','Dt. Embarque':'DATA_EMBARQUE'
                ,'No. D.P.':'NUMERO_DP','No. Cli.':'NUMERO_CLI','Obs. Resumida':'REFERENCIA_PEDIDO_WMS'
                ,'No. Ped. Cli.':'REFERENCIA_PEDIDO_CLI','No. N.F.':'NUMERO_PEDIDO_NF'
                ,'Sit. Fase':'FASE_PEDIDO_WMS','Prior.':'PRIORIDADE','Transp. (Ped.)':'TRANSPORTADORA_PEDIDO'
                ,'Destinatário':'DESTINATARIO','Doca':'DOCA','Vols.':'VOLUMES'}, inplace=True)


        unificalocwms.loc[:,['DATA_INCLUSAO_PEDIDO','DATA_MOVIMENTO','DATA_RESERVA','DATA_CONFERENCIA_SEPARACAO'
                ,'DATA_NOTA_FISCAL','DATA_EMBARQUE']] = unificalocwms.loc[:,['DATA_INCLUSAO_PEDIDO','DATA_MOVIMENTO','DATA_RESERVA'
                ,'DATA_CONFERENCIA_SEPARACAO','DATA_NOTA_FISCAL','DATA_EMBARQUE']].apply(pd.to_datetime, errors='coerce',dayfirst=True)

        dfwms1 = read_excel('WD6part1')
        dfwms1['UNIDADE_CD'] = 'Hausz-SP'
        dfwms1[['Dt. Mov.', 'No. D.P.', 'Situação', 'M', 'Observação Resumida',
        'N.F.(s) Cliente', 'Ped(s). Cliente', 'N.F.(s) Retorno', 'Tipo Retorno',
        'Vols.', 'Rep.', 'No. Emb.', 'Razão Social Transp.', 'SKU', 'Qt. Total',
        'T.I.', 'T.I. Pend.']]

        dfwms2 = read_excel('WD6part2')
        dfwms2['UNIDADE_CD'] = 'Hausz-SC'
        dfwms2[['Dt. Mov.', 'No. D.P.', 'Situação', 'M', 'Observação Resumida',
        'N.F.(s) Cliente', 'Ped(s). Cliente', 'N.F.(s) Retorno', 'Tipo Retorno',
        'Vols.', 'Rep.', 'No. Emb.', 'Razão Social Transp.', 'SKU', 'Qt. Total',
        'T.I.', 'T.I. Pend.']]

        unifica_pedidos_wms = pd.concat([dfwms1, dfwms2])
        unifica_pedidos_wms.rename(columns={'Dt. Mov.':'DATAMOVIMENTO','Observação Resumida':'REFERENCIA_PEDIDOHAUSZ'
        ,'N.F.(s) Cliente':'NUMERO_NOTA_CLIENTE','N.F.(s) Retorno':'NUMERO_NOTA_RETORNO'
        ,'Vols.':'VOLUMES','Qt. Total':'QUANTIDADETOTAL'}, inplace=True)
        unifica_pedidos_wms['REFERENCIA_PEDIDOHAUSZ'].fillna('valornaoencontrado', inplace=True)
        unifica_pedidos_wms['Situação'].fillna('valornaoencontrado', inplace=True)

        dfwpj1 = read_excel('WPJpart1')
        dfwpj1['UNIDADE_CD'] = 'Hausz-SP'
        dfwpj2 = read_excel('WPJpart2')
        dfwpj2['UNIDADE_CD'] = 'Hausz-SC'

        unificawpj = pd.concat([dfwpj1, dfwpj2])

        #unificawpj.rename(columns={'':''})

        unificawpj.rename(columns={'No. N.F.':'NUMERO_NOTAFISCAL','Dt. Mov.':'DATA_MOVIMENTACAO'
        ,'Cód. Merc.':'REFERENCIA_MERCADORIA','Vl. Unit. (R$)':'VALOR_UNITARIO','Vl. Total (R$)':'VALOR_TOTAL'},inplace=True)

        return unifica_pedidos_wms

#filtra seleciona datas pedidos, ordena do maior para o menor e deleta os duplicados mantendo o maior
def filtraSelecionaPedidos():
        logsgeral = IntegracaoWms.select_log_wms_pedidos()
        logpedidowms = pd.DataFrame(logsgeral)

        logpedidowms.loc[:,'ParaIdEtapaFlexy'] = logpedidowms.loc[:,'ParaIdEtapaFlexy'].astype(int)

        logpedidowms = logpedidowms[(logpedidowms.loc[:,'ParaIdEtapaFlexy'] == 6) & (logpedidowms.loc[:,'dataatualizacao'].astype(str).str.contains(f'{IntegracaoWms.retorna_dataatual()}'))]
        #logpedidowms = logpedidowms.sort_values('dataatualizacao', ascending=False)
        logpedidowms = logpedidowms.sort_values('dataatualizacao', ascending=False).drop_duplicates('CodigoPedido').sort_index()
        return logpedidowms

def quantidade_pedidos_rejeicao():
        rejeicoes = rejeicoes[(rejeicoes['Data'].astype(str).str.contains(f'{IntegracaoWms.retorna_dataatual()}'))]

        unificavalores = pd.merge(filtraSelecionaPedidos(),rejeicoes, on='CodigoPedido', how='left')
        unificavalores.loc[:,['CodigoPedido','StatusPedido','NomeEtapa','RejeicaoId','statusRejeicao']]


        freq_rejeicoes = unificavalores.loc[:,'statusRejeicao'].value_counts()

        freq_rejeicoes_porc = unificavalores.loc[:,'statusRejeicao'].value_counts(normalize=True) * 100

        freq_rejeicoes_porc = freq_rejeicoes_porc.reset_index(name='frequencia')
        freq_rejeicoes_porc.columns = ['Status','Frequencia']
        return unificavalores

def status_pedido():
        logsgeral = IntegracaoWms.select_log_wms_pedidos()
        dfstatus = pd.DataFrame(logsgeral)

        dfstatus = dfstatus[dfstatus.loc[:,'dataatualizacao'].astype(str).str.contains(f'{IntegracaoWms.retorna_dataatual()}')]


        etapas = dfstatus['NomeEtapa'].value_counts(normalize=True) * 100
        etapas = etapas.reset_index(name='frequencia').round(2)
        etapas.columns=['Etapas','Frequencia']

def total_status_pedidos():
        unifica_pedidos_wms = uni_tabela_wms()
        total =  unifica_pedidos_wms.loc[:,'REFERENCIA_PEDIDOHAUSZ'] = unifica_pedidos_wms.loc[:,'REFERENCIA_PEDIDOHAUSZ'].apply(lambda k: str(k).replace('Ped.:','').split('-')[0].strip())

def FrequenciaSituacaoPedidos():
        unifica_pedidos_wms = uni_tabela_wms()
        frequencia_status_nota = unifica_pedidos_wms.loc[:,'Situação'].value_counts()
        frequencia_status_nota_porc = unifica_pedidos_wms.loc[:,'Situação'].value_counts(normalize=True) * 100

@wms.route('/dashboard/logistica/integracao_wms/<int:page>', methods=["GET","POST"])
def index(page= 1):
        page = page
        tabela = IntegracaoWms.tabela_filtro1(page)
        # print(tabela)
        pag = 1

        card_1 = card1()
        card_2 = card2()
        card_3 = card3()
        card_4 = card4()
        card_5 = card5()
        card_6 = card6()
        
        return render_template("Integracao_wms.html", card1 = card_1, card2 = card_2 ,card3 = card_3, card4 = card_4, card5 = card_5, card6 = card_6, tabela = tabela, page = page, pag = pag)

@wms.route('/dashboard/logistica/itengracao_wms/filtro', methods=["POST"])
def filtro_tabela(codigoPedido = '', SKU = '', RejeicaoID = '', DataFim = '', DataIni = ''):
        pag = 0
        codigoPedido = codigoPedido
        SKU = SKU
        RejeicaoID=RejeicaoID
        DataFim = DataFim
        DataIni = DataIni

        if request.method == 'POST':
               
                codigoPedido = request.form['codigoPedido']

                if codigoPedido == '':
        
                        codigoPedido = "''"
                        # print('Sem Codigo')
        
                SKU = request.form['SKU']

                if SKU == '':
        
                        SKU = "''"
                        # print('Sem SKU')
                
                RejeicaoID = request.form['RejeicaoID']

                if RejeicaoID == '':
        
                        RejeicaoID = "''"
                        # print('Sem RejeicaoID')
        
                DataFim = request.form['DataFim']
                

                if DataFim == '':
        
                        DataFim = "''"
                        # print('Sem DataFim')
                else:
                        DataFim = f"'{DataFim}'"

                DataIni = request.form['DataIni']   

                if DataIni == '':
        
                        DataIni = "''"
                        # print('Sem DataIni')
                else:
                        DataIni = f"'{DataIni}'"

                # print(DataFim)
                # print(DataIni)

                tabela = IntegracaoWms.tabela_filtro(codigoPedido, SKU, RejeicaoID, DataFim, DataIni)

        card_1 = card1()
        card_2 = card2()
        card_3 = card3()
        card_4 = card4()
        card_5 = card5()
        card_6 = card6()
        

        return render_template("Integracao_wms.html", card1 = card_1, card2 = card_2 ,card3 = card_3, card4 = card_4, card5 = card_5, card6 = card_6, tabela = tabela, page = pag)