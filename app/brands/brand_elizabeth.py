from itertools import zip_longest
import os
import sys
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
import cv2
import numpy as np
import re
import pandas as pd

files = os.listdir('D:\\productsbrandshausz\\files\\pdffile\\')


class Elizabeth:
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    def __init__(self,path, datataual):
        self.config= '--psm 4  -c preserve_interword_spaces=1 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.[]|,,.~â ÃÂç'
        self.tesseract_language = "por"
        self.pdffile = path
        self.dataatual = datataual

    def converter_imgpdf(self):
     
        imagens_files = 'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\'
        images = convert_from_path(self.pdffile, 200, poppler_path='C:\\Projetoshausz\\apphauszetlsbi\\poppler-21.10.0\\bin')
        for i in range(len(images)):
            images[i].save(imagens_files+'elizabeth'+ str(i) +'.jpg', 'JPEG')

    def separa_valores(self, strings):
        lista_dicts = []
        for string in strings:
            valor = string.split(" ")
          
            remov_espaco = list(filter(lambda x: len(x.strip()) >0, valor ))
            cont = len(remov_espaco)
            if cont > 10:
                values = remov_espaco[2:]
                saldos = remov_espaco[-1]
                skus = str(values[1:-7])
                contref = len(skus)
                dict_values = {}
                dict_values['SKU'] = skus
                dict_values['SALDO'] = saldos
                lista_dicts.append(dict_values)

        return lista_dicts

    def filtrar_skus(self, skus):
        lista_skus = []
        for sku in skus:
            try:
                if re.search('[0-9]{1,5}',sku, re.IGNORECASE):
                    ref = str(sku).replace("120X120","").strip()
                    lista_skus.append(ref)
            except:
                lista_skus.append('valornaoencontrado')
        
        return lista_skus

    def ajuste_floats(self, saldos):
        try:
            valor = str(saldos).replace(".","").replace(",",".").strip()
            return float(valor)
        except:
            return float(0)

    def reader_imagem(self):
        lista_dicts_saldos = []
        imgs = os.listdir('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\')
        for im in imgs:
            if 'elizabeth' in im:
                img = cv2.imread(f'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\{im}')
                #imagemgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #Convertendo para rgb
                imagemgray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Convertendo para rgb
                texto = pytesseract.image_to_string(imagemgray, lang= self.tesseract_language,config=self.config)
                valor = texto.split("\n")
                dicts = self.separa_valores(valor)
                for dict in dicts:
                    refs = dict['SKU']
                    saldos = dict['SALDO']
                    sku_produto = self.filtrar_skus(refs)
                    saldo_produto = self.ajuste_floats(saldos)
                    dict_saldos = {}
                    try:
                        dict_saldos['SKU'] = sku_produto
                        dict_saldos['SALDO'] = saldo_produto
                        dict_saldos['MARCA'] = 'Elizabeth'
                        dict_saldos['DATA'] = self.dataatual
                        dict_saldos['PRAZO'] = 'Prazo definido pelo Fabricante'
                        
                        lista_dicts_saldos.append(dict_saldos)

                    except:
                        dict_saldos['SKU'] = 'valornaoencontrado'
                        dict_saldos['SALDO'] = float(0)
                        dict_saldos['MARCA'] = 'Elizabeth'
                        dict_saldos['DATA'] = self.dataatual
                        dict_saldos['PRAZO'] = 'Prazo definido pelo Fabricante'

                        lista_dicts_saldos.append(dict_saldos)
        
  
        return lista_dicts_saldos

    def ajuste_referencia_sku(self, skus):
        lista_skus = []
        for sku in skus:
            try:
                valor = ''.join(sku).replace('0101','101').replace('0104','104').strip()
                lista_skus.append(valor)
            except:
                lista_skus.append('valornaoencontrado')

        return lista_skus

    def create_dataframe(self):
        listas = self.reader_imagem()
     
        data = pd.DataFrame(listas)
        data['SKU'].fillna(0, inplace=True)
        data['SKU'] = self.ajuste_referencia_sku(data['SKU'])
      
        data['SALDO'].fillna(0, inplace=True)
        data['SALDO'] = data['SALDO'].astype(float)
        data.drop(data.loc[data['SALDO']=='valornaoencontrado'].index, inplace=True)
        data = data.sort_values('SALDO', ascending=False).drop_duplicates('SKU').sort_index()

        data.to_excel("C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\logs\\elizabeth0606.xlsx")
        
        jsons = data.to_dict('records')
        print(jsons)
        return jsons
     