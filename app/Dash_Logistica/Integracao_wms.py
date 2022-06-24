from flask import Blueprint, render_template, request
from ..controllers.controller_logistica import IntegracaoWms

wms = Blueprint('wms', __name__ , template_folder='templates', static_folder='static',  static_url_path='/app/Dash_Logistica/static/')

def card1():
        rejeicaohj = IntegracaoWms.card_hoje()
        rejeicaohj = rejeicaohj[0]['quantidade_de_rejeicao']
        return rejeicaohj

def card2():
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

        try:
                percentual_mes = mes_seguinte / mes_passado * 100
    
        except:
                percentual_mes = 0
        
        #ESTE CARD É O PERCENTUAL DE REJEICOES DO MES ANTERIOR
        mes_resultado = "{:.2f}".format((percentual_mes))

        return mes_resultado

def card4():
        ontem = IntegracaoWms.card_ontem()
        return ontem

def card5():
        rejeicoes_mes_anterior = IntegracaoWms.qtd_mes_passado()
        rejeicoes_mes_anterior = rejeicoes_mes_anterior[0]['quantidade_de_rejeicao']
        return rejeicoes_mes_anterior

def card6():

        possivel_rejeicao = IntegracaoWms.Pre_rejeicao()
        possivel_rejeicao = possivel_rejeicao[0]['Pre_rejeicoes']
        return possivel_rejeicao

@wms.route('/dashboard/logistica/integracao_wms/<int:page>', methods=["GET","POST"])
def index(page= 1):
        page = page
        tabela = IntegracaoWms.tabela_filtro1(page)

        card_1 = card1()
        card_2 = card2()
        card_3 = card3()
        card_4 = card4()
        card_5 = card5()
        card_6 = card6()
        
        return render_template("Integracao_wms.html", card1 = card_1, card2 = card_2 ,card3 = card_3, card4 = card_4, card5 = card_5, card6 = card_6, tabela = tabela, page = page)

@wms.route('/dashboard/logistica/itengracao_wms/filtro/<int:page>', methods=["POST"])
def filtro_tabela(codigoPedido = '', SKU = '', RejeicaoID = '', DataFim = '', DataIni = '', page = 1):
        page = page
        codigoPedido = codigoPedido
        SKU = SKU
        RejeicaoID=RejeicaoID
        DataFim = DataFim
        DataIni = DataIni

        if request.method == 'POST':
               
                codigoPedido = request.form['codigoPedido']

                if codigoPedido == '':
        
                        codigoPedido = "''"
                        print('Sem Codigo')
        
                SKU = request.form['SKU']

                if SKU == '':
        
                        SKU = "''"
                        print('Sem SKU')
                
                RejeicaoID = request.form['RejeicaoID']

                if RejeicaoID == '':
        
                        RejeicaoID = "''"
                        print('Sem RejeicaoID')
        
                DataFim = request.form['DataFim']
                

                if DataFim == '':
        
                        DataFim = "''"
                        print('Sem DataFim')
                else:
                        DataFim = f"'{DataFim}'"

                DataIni = request.form['DataIni']   

                if DataIni == '':
        
                        DataIni = "''"
                        print('Sem DataIni')
                else:
                        DataIni = f"'{DataIni}'"

                print(DataFim)
                print(DataIni)

                tabela = IntegracaoWms.tabela_filtro(page, codigoPedido, SKU, RejeicaoID, DataFim, DataIni)

        card_1 = card1()
        card_2 = card2()
        card_3 = card3()
        card_4 = card4()
        card_5 = card5()
        card_6 = card6()
        

        return render_template("Integracao_wms.html", card1 = card_1, card2 = card_2 ,card3 = card_3, card4 = card_4, card5 = card_5, card6 = card_6, tabela = tabela, page = page)