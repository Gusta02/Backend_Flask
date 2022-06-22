import pandas as pd
import re



class Deca:
    def __init__(self, path):
        self.path = path

    def converte_float(self, saldo):
        try:
            valor = str(saldo).replace(",","").replace(".",".").strip()
            num = float(valor)
            return num
        except:
            return float(0)

    def ajuste_referencias(self, ref):
        try:
            valor = str(ref).strip()
            return valor
        except:
            return 'valornaoencontrado'
    
    def verifica_prazo(self, prazos):
        lista_prazos_sajustados = []
        for prazo in prazos:
            if type(prazo) == float:
                lista_prazos_sajustados.append(prazo)
            elif re.search('nan', prazo, re.IGNORECASE):
                lista_prazos_sajustados.append(float(299))
            else:
                lista_prazos_sajustados.append(float(299))
        return lista_prazos_sajustados

    def read_excel(self, path,dataatual):
        data = pd.ExcelFile(path)
        for sheet in data.sheet_names:
            #decadf = pd.read_excel(self.path,sheet_name=)
            if re.search('geral.?', sheet, re.IGNORECASE):
                decadf = pd.read_excel(path,sheet_name=sheet)
                #filtrando linhas com regex
                filtrado = decadf[decadf['Cen.'].str.contains('(Jundiaí|Jundiai)', flags=re.IGNORECASE,regex=True)]
                filtrado['EST DISP'] = filtrado['EST DISP'].apply(lambda x: self.converte_float(x))
                filtrado = filtrado.sort_values('EST DISP', ascending=False).drop_duplicates('Nº do material').sort_index()
                filtrado['Nº do material'] = filtrado['Nº do material'].apply(lambda x: self.ajuste_referencias(x))
                filtrado['PRAZO_FINAL'] = self.verifica_prazo(filtrado['PRAZO_FINAL'])
                filtrado['MARCA'] = 'Deca'
                filtrado['DATA'] = dataatual
                filtrado = filtrado[['Nº do material','EST DISP','PRAZO_FINAL','DATA','MARCA']]

                filtrado.rename(columns={'Nº do material':'SKU','EST DISP':'SALDO','PRAZO_FINAL':'PRAZO'},inplace = True)
                decadict = filtrado.to_dict('records')
         
                return decadict
        