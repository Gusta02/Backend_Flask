import pandas as pd
import os
import re

from datetime import datetime

class Brands:
    def __init__(self):
        self.path = 'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\coletados\\'
        self.data_atual = str(datetime.today().strftime('%Y-%m-%d %H:%M'))
    def ajuste_referencia_tarkett(self, referencias):
        lista_referencias = []
        for ref in referencias:
            try:
                sku = str(ref).split("(")[0].strip()
                lista_referencias.append(sku)
            except:
                lista_referencias.append('naoencontrado')

        return lista_referencias
    
    def ajuste_nome_produto_tarkett(self, nomes):
        lista_nomeproduto = []
        for nome in nomes:
            try:
                valor = str(nome).strip()
                lista_nomeproduto.append(valor)
            except:
                lista_nomeproduto.append("valornaoencontrado")

        return lista_nomeproduto


    def ajuste_saldos_tarkett(self, saldos):
        lista_saldos = []
        for saldo in saldos:
            try:
                sald = str(saldo).strip().replace(",",".")
                lista_saldos.append(float(sald))
            except:
                lista_saldos.append(float(0))
        return lista_saldos

    def ajuste_saldo_incepa(self,saldos):
        lista_saldos = []
        for saldo in saldos:
            try:
                valor = str(saldo).replace("Armazem"
                            ,"").split("\n")[-1].strip().replace(",",".")
                lista_saldos.append(valor)
            except:
                lista_saldos.append(valor)
        return lista_saldos


    def ajuste_referencias_gruporoca(self, referencias):
        lista_referencias = []
        for referencia in referencias:
            try:
                valor = str(referencia).strip()
                lista_referencias.append(valor)
            except:
                lista_referencias.append("valornaoencontrado")

        return lista_referencias

    def ajuste_nomes_grupo_roca(self, nomes):
        lista_nomes = []
        for nome in nomes:
            try:
                valor = str(nome).strip().replace("nÃ£o","não")
                lista_nomes.append(valor)
            except:
                lista_nomes.append("valornaoencontrado")
            
        return lista_nomes

    def read_file(self):
        lista_jsons = []
        files = os.listdir(self.path)
        for file in files:
            if re.search('tarkett.?', file, re.IGNORECASE):
                data = pd.read_excel(self.path+file)
                data['Codigos'] = self.ajuste_referencia_tarkett(data['Codigos'])
                data['Saldos'] = self.ajuste_saldos_tarkett(data['Saldos'])
                data['Nomes'] = self.ajuste_nome_produto_tarkett(data['Nomes'])
                data = data[['Codigos','Saldos','Nomes']]
                data["DATAATUAL"] = self.data_atual
                data["MARCA"] = 'Tarkett'
                data["PRAZO"] = 'Prazo do Fabricante'
                data.rename(columns={'Codigos':'SKU','Saldos':'SALDO','Nomes':'NomeProduto'},inplace = True)
                data = data[['SKU','SALDO','NomeProduto','DATAATUAL','MARCA','PRAZO']]
                jsons_tarkett = data.to_dict('records')
                data.to_excel('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\logs\\tarkett.xlsx')
                lista_jsons.append(jsons_tarkett)
               
        
            if re.search('incepa.?',file, re.IGNORECASE):
                data = pd.read_csv(self.path+file,sep=";")
                data.fillna(0, inplace=True)
                data["Nome"].fillna("naotem", inplace=True)
                data["Nome"].fillna("naoencontrado", inplace=True)
                data['Saldo0'] = self.ajuste_saldo_incepa(data['Saldo0'])
                data['Referencia'] = self.ajuste_referencias_gruporoca(data['Referencia'])
                data['Nome'] = self.ajuste_nomes_grupo_roca(data['Nome'])
                data["DATAATUAL"] = self.data_atual
                data["MARCA"] = 'Incepa'
                data["PRAZO"] = 'Prazo do Fabricante'
                data.rename(columns={'Referencia':'SKU','Saldo0':'SALDO','Nome':'NomeProduto'},inplace = True)
                data = data[['SKU','SALDO','NomeProduto','MARCA','DATAATUAL','PRAZO']]
                jsons_incepa = data.to_dict('records')
                data.to_excel('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\logs\\incepa.xlsx')
                lista_jsons.append(jsons_incepa)
                
            if re.search('roca.?',file, re.IGNORECASE):
                data = pd.read_csv(self.path+file, sep=";")
                data.fillna(0, inplace=True)
                data["Nome"].fillna("naotem", inplace=True)
                data['Saldo0'] = self.ajuste_saldo_incepa(data['Saldo0'])
                data['Referencias'] = self.ajuste_referencias_gruporoca(data['Referencias'])
                data['Nome'] = self.ajuste_nomes_grupo_roca(data['Nome'])
              
                data["DATAATUAL"] = self.data_atual
                data["MARCA"] = 'Roca'
                data["PRAZO"] = 'Prazo do Fabricante'
                data.rename(columns={'Referencias':'SKU','Saldo0':'SALDO','Nome':'NomeProduto'},inplace = True)
                data = data[['SKU','SALDO','NomeProduto','DATAATUAL','MARCA','PRAZO']]
                jsons_roca = data.to_dict('records')
                data.to_excel('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\logs\\roca.xlsx')
                lista_jsons.append(jsons_roca)
        
        return lista_jsons