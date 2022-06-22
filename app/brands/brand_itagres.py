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

class Itagres:
    def __init__(self, path, datataual):
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        self.config= '--psm 4  -c preserve_interword_spaces=1 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.[]|,,.~â ÃÂç'
        self.tesseract_language = "por"
        self.lista_produtos = []
        self.imagem = 'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\'
        self.pdffile = path
        self.dataatual = datataual

    def converter_imgpdf(self) -> None:
        images = convert_from_path(self.pdffile, 200, poppler_path='C:\\Projetoshausz\\apphauszetlsbi\\poppler-21.10.0\\bin')
        for i in range(len(images)):
            images[i].save(self.imagem+'itagres'+ str(i) +'.jpg', 'JPEG')

    def filtrar_skus(self, skus):
        lista_dicts = []
        for sku in skus:
            valor = sku.split("\n")
            for val in valor:
                dict_items = {}
                try:
                    if re.search('[0-9]{1,3},[0-9]{1,2}', val, re.IGNORECASE):
                        valor = val.split(" ")
                        dict_items['CODIGO'] = valor[0]
                        dict_items['SALDO'] = valor[-1]
                        lista_dicts.append(dict_items)
                except:
                    dict_items['CODIGO'] = 'valornaoencontrado'
                    dict_items['SALDO'] = '0'
                    lista_dicts.append(dict_items)

        return lista_dicts

    def converte_float(self, digitos):
        lista_dicts = []
        for digito in digitos:
            sku = digito['CODIGO']
            saldo = digito['SALDO']
            if re.search('[0-9]{1,4},[0-9]{1,2}', saldo, re.IGNORECASE):
                dict_saldos = {}
                valor = str(saldo).replace(".","").replace(",",".").strip()
                dict_saldos["SALDO"] = valor
                dict_saldos["SKU"] = str(sku).strip()
                dict_saldos["PRAZO"] = 'Prazo do Fabricante'
                dict_saldos['DATA'] = self.dataatual
                lista_dicts.append(dict_saldos)
        return lista_dicts

    def ajuste_saldos(self, saldos):
        ajustados = []
        for saldo in saldos:
            try:
                if re.search('[0-9]{1,5}\.[0-9]{1,2}',saldo, re.IGNORECASE):
                    ajustados.append(float(saldo))
                else:
                    ajustados.append('naotem')
            except:
                ajustados.append('naotem')
        return ajustados

    def ajuste_skus(self, skus):
        lista_skus = []
        for sku in skus:
            try:
                valor = str(sku).strip()
                if re.search('[0-9]{1,5}[A]', valor, re.IGNORECASE):
                    lista_skus.append(valor)
                else:
                    lista_skus.append('naotem')
            except:
                lista_skus.append('naotem')
        return lista_skus

    def imagem_reader(self) -> None:
        tesseract_language = "por"
        config= '--psm 4  -c preserve_interword_spaces=1 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.[]|,,.~â ÃÂç'
        lista_dicts = []
        imgs = os.listdir('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\')
        for im in imgs:
            try:
                img = cv2.imread(f'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\{im}')

                imagemgray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Convertendo para rgb
                texto = pytesseract.image_to_string(imagemgray, config=config)
                texto = texto.split("\n")
                remov = [x for x in texto if x !='' if x !=' ']
                saldos = self.filtrar_skus(remov)
            
                digitos = self.converte_float(saldos)
                for digi in digitos:
                    lista_dicts.append(digi)
            
            except:
                print("Erro leitura imagem")

        data = pd.DataFrame(lista_dicts)

        data['SALDO'] = self.ajuste_saldos(data['SALDO'])
        data['SKU'] = self.ajuste_skus(data['SKU'])
        data.drop(data.loc[data['SALDO']=='naotem'].index, inplace=True)
        data = data.sort_values('SALDO', ascending=False).drop_duplicates('SKU').sort_index()
        data['MARCA'] = 'Itagres'
        data.to_excel('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\logs\\itagres.xlsx')
        jsons = data.to_dict('records')
        
      
        return jsons

