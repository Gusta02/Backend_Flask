from .classes import Empresa, uhome, valor_pagar

# importa a classe
empresa = Empresa('app/Dash_Financeiro/planilhas/artse.xlsx')


artse = Empresa('app/Dash_Financeiro/planilhas/artse.xlsx')
easy = Empresa('app/Dash_Financeiro/planilhas/easy.xlsx')
Hausz = Empresa('app/Dash_Financeiro/planilhas/hausz.xlsx')
Logz = Empresa('app/Dash_Financeiro/planilhas/logz.xlsx')
Supply = Empresa('app/Dash_Financeiro/planilhas/supply.xlsx')
Uhome = Empresa('app/Dash_Financeiro/planilhas/uhome.xlsx')
Vns = Empresa('app/Dash_Financeiro/planilhas/VNS.xlsx')


# instancias a pagar da classe

artse_totalcontaspagar = artse.calcula_tipo('CONTAS A PAGAR')
easy_totalcontaspagar = easy.calcula_tipo('CONTAS A PAGAR')
Hausz_totalpagar = Hausz.calcula_tipo('CONTAS A PAGAR')
logz_totalpagar = Logz.calcula_tipo('CONTAS A PAGAR')
suplly_totalpagar = Supply.calcula_tipo('CONTAS A PAGAR')
uhome_totalpagar = Uhome.calcula_tipo('CONTAS A PAGAR')
Vns_totalpagar = Vns.calcula_tipo('CONTAS A PAGAR')

#Soma todas empresas na condição CONTAS A PAGAR

SOMA_TODASEMPRESAS_APAGAR = (artse_totalcontaspagar 
+ easy_totalcontaspagar + Hausz_totalpagar
+ logz_totalpagar + suplly_totalpagar
+ uhome_totalpagar + Vns_totalpagar)

# instancias da classe

valor_total = uhome.get_valor()

conta_pagar = valor_pagar

# instancias a receber da classe
artse_totalRECEBER = artse.calcula_tipo('CONTAS A RECEBER')
easy_totalRECEBER = easy.calcula_tipo('CONTAS A RECEBER')
Hausz_totalRECEBER = Hausz.calcula_tipo('CONTAS A RECEBER')
logz_totalRECEBER = Logz.calcula_tipo('CONTAS A RECEBER')
suplly_totalRECEBER = Supply.calcula_tipo('CONTAS A RECEBER')
uhome_totalRECEBER = Uhome.calcula_tipo('CONTAS A RECEBER')
Vns_totalRECEBER = Vns.calcula_tipo('CONTAS A RECEBER')

TODASEMPRESAS_CONTASARECEBER = (artse_totalRECEBER 
+ easy_totalRECEBER + Hausz_totalRECEBER
+ logz_totalRECEBER + suplly_totalRECEBER
+ uhome_totalRECEBER + Vns_totalRECEBER)

# Fluxo de caixa CP - CR
fluxoCaixa = SOMA_TODASEMPRESAS_APAGAR + TODASEMPRESAS_CONTASARECEBER