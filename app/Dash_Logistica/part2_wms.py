from flask import Blueprint, render_template, request
from ..controllers.controller_logistica import IntegracaoWms
import pandas as pd


def rejeicaoes():
    lista_values = {'0':'Integrou','6':'SemEstoque','3':'Erro'}

    rejeicoes_wms = IntegracaoWms.select_wms_rejeicoes()
    rejeicoes = pd.DataFrame(rejeicoes_wms)


    rejeicoes['statusRejeicao'] = rejeicoes['RejeicaoId'].map(lista_values)
    rejeicoes[rejeicoes.loc[:,'statusRejeicao'].astype(str).str.contains('Integrou')]
    return rejeicoes

def nfentrada():
    nfentrada = IntegracaoWms.select_pedido_compra_nota_entrada()
    return nfentrada

def data_atual():
    data_atual =  IntegracaoWms.retorna_dataatual()
    return data_atual

def excel():
    dfwms1 = pd.read_excel('../planilha/WD6part1.xlsx',skiprows=[0,1,2,3,4,5])
    dfwms2 = pd.read_excel('../planilha/WD6part2.xlsx',skiprows=[0,1,2,3,4,5])
    dfwxd1 =  pd.read_excel('../planilha/WXDpart1.xlsx',skiprows=[0,1,2,3,4,5])
    dfwxd2 =  pd.read_excel('../planilha/WXDpart2.xlsx',skiprows=[0,1,2,3,4,5])
    dfwpj1 = pd.read_excel('../planilha/WPJpart1.xlsx',skiprows=[0,1,2,3,4,5,6])
    dfwpj2 = pd.read_excel('../planilha/WPJpart2.xlsx',skiprows=[0,1,2,3,4,5,6])


    dfwxd1['UNIDADE_CD'] = 'Hausz-SP'
    dfwxd1[['Dt. Inclusão','Dt. Mov.','Dt. Reserva','Dt. Conf. Sep.'
        ,'Dt. Embarque','No. D.P.','No. Cli.','Obs. Resumida','No. Ped. Cli.'
        ,'No. N.F.','Sit. Fase','Transp. (Ped.)','Destinatário','Doca','Vols.', 'UNIDADE_CD']]

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


    dfwms1['UNIDADE_CD'] = 'Hausz-SP'
    dfwms1[['Dt. Mov.', 'No. D.P.', 'Situação', 'M', 'Observação Resumida',
        'N.F.(s) Cliente', 'Ped(s). Cliente', 'N.F.(s) Retorno', 'Tipo Retorno',
        'Vols.', 'Rep.', 'No. Emb.', 'Razão Social Transp.', 'SKU', 'Qt. Total',
        'T.I.', 'T.I. Pend.']]

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


    dfwpj1['UNIDADE_CD'] = 'Hausz-SP'
    dfwpj2['UNIDADE_CD'] = 'Hausz-SC'

    unificawpj = pd.concat([dfwpj1, dfwpj2])

    #unificawpj.rename(columns={'':''})

    unificawpj.rename(columns={'No. N.F.':'NUMERO_NOTAFISCAL','Dt. Mov.':'DATA_MOVIMENTACAO'
        ,'Cód. Merc.':'REFERENCIA_MERCADORIA','Vl. Unit. (R$)':'VALOR_UNITARIO','Vl. Total (R$)':'VALOR_TOTAL'},inplace=True)

    return 

def logpedidowms():
    logsgeral = IntegracaoWms.select_log_wms_pedidos()
    logpedidowms = pd.DataFrame(logsgeral)

    logpedidowms.loc[:,'ParaIdEtapaFlexy'] = logpedidowms.loc[:,'ParaIdEtapaFlexy'].astype(int)


    logpedidowms = logpedidowms[(logpedidowms.loc[:,'ParaIdEtapaFlexy'] == 6) & (logpedidowms.loc[:,'dataatualizacao'].astype(str).str.contains(f'{data_atual}'))]
    #logpedidowms = logpedidowms.sort_values('dataatualizacao', ascending=False)
    logpedidowms = logpedidowms.sort_values('dataatualizacao', ascending=False).drop_duplicates('CodigoPedido').sort_index()
    return logsgeral

def grafico1():
    rejeicoes = rejeicoes[(rejeicoes['Data'].astype(str).str.contains(f'{data_atual}'))]


    unificavalores = pd.merge(logpedidowms,rejeicoes, on='CodigoPedido', how='left')
    unificavalores.loc[:,['CodigoPedido','StatusPedido','NomeEtapa','RejeicaoId','statusRejeicao']]


    freq_rejeicoes = unificavalores.loc[:,'statusRejeicao'].value_counts()

    freq_rejeicoes_porc = unificavalores.loc[:,'statusRejeicao'].value_counts(normalize=True) * 100

    freq_rejeicoes_porc = freq_rejeicoes_porc.reset_index(name='frequencia')
    freq_rejeicoes_porc.columns = ['Status','Frequencia']

def grafico2():
    dfstatus = pd.DataFrame(logpedidowms())

    dfstatus = dfstatus[dfstatus.loc[:,'dataatualizacao'].astype(str).str.contains(f'{data_atual}')]


    etapas = dfstatus['NomeEtapa'].value_counts(normalize=True) * 100
    etapas = etapas.reset_index(name='frequencia').round(2)
    etapas.columns=['Etapas','Frequencia']