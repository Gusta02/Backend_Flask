import pandas as pd
import re
import os

class Level:
    def __init__(self, path, dataatualizacao) -> None:
        self.lista_produtos = []
        self.sheets = []
        self.path = path
        self.dataatualizacao = dataatualizacao

    def ajuste_data_producao(self, datas: str) -> str:
        if re.search('NaT',str(datas), re.IGNORECASE):
            return 'Produto Disponivel'
        else:
            return datas

    def converte_float(self, saldos: float) -> float:
        lista_saldos = []
        for saldo in saldos:
            try:
                valor = str(saldo).replace(",",".")
                lista_saldos.append(float(valor))
            except:
                lista_saldos.append(float(0))
        return lista_saldos

    def ajuste_referencia(self, skus: str) -> str:
        lista_skus = []
        for sku in skus:
            try:
                valor = str(sku).strip() + 'L'
                lista_skus.append(valor)
            except:
                lista_skus.append('valornaoencontrado')
        return lista_skus

    def excel_reader(self) -> dict:
    
        level = pd.ExcelFile(self.path)
        for sheet in level.sheet_names:
            if re.search('ESTOQUE', sheet, re.IGNORECASE):
                try:
                    data = pd.read_excel(self.path, sheet_name=f'{sheet}')
                    data = data[['Código','Estoque']]
                    self.sheets.append(data)
                except:
                    print("error")

            if re.search('previ.?', sheet, re.IGNORECASE):
                try:
                    data = pd.read_excel(self.path, sheet_name=f'{sheet}')
                    data['Estoque'] = 0
                    data = data[['Código','Estoque','Previsão*']]
                    self.sheets.append(data)
                except:
                    print("Error")
    
        unificalevel = pd.concat(self.sheets, axis=0)
        unificalevel.reset_index()
        
        unificalevel['Previsão*'] = unificalevel['Previsão*'].apply(lambda x: self.ajuste_data_producao(x))
        
        unificalevel['Código'] = self.ajuste_referencia(unificalevel['Código'])
        unificalevel['Estoque'] = self.converte_float(unificalevel['Estoque'])
        unificalevel['Previsão*'].fillna(0, inplace=True)
        unificalevel.rename(columns={'Código':'SKU','Estoque':'SALDO'},inplace = True)
        unificalevel['PRAZO'] = 'Prazo do fabricante'
        unificalevel['MARCA'] = 'Level'
        unificalevel['DATA'] = self.dataatualizacao


        unificalevel
        unificalevel.to_excel("C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\logs\\level.xlsx")
        #unificalevel.to_excel("D:\\productsbrandshausz\\files\\save_files\\level.xlsx")
        level_dict = unificalevel.to_dict('records')

        return level_dict
        
    
