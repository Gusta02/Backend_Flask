from itertools import zip_longest
import os
import sys
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
import cv2
import numpy as np
import re
import pandas as pd


class Sense:
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    def __init__(self,path, datataual):
        self.config= '--psm 4  -c preserve_interword_spaces=1 tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.[]|,,.~â ÃÂç'
        self.tesseract_language = "por"
        self.lista_produtos = []
        self.imagem = 'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\'
        self.pdffile = path
        self.dataatual = datataual

    def converter_imgpdf(self):
        imagens_files = 'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\'
        images = convert_from_path(self.pdffile, 200, poppler_path='C:\\Projetoshausz\\apphauszetlsbi\\poppler-21.10.0\\bin')
        for i in range(len(images)):
            images[i].save(imagens_files+'sense'+ str(i) +'.jpg', 'JPEG')

    def separa_valores(self, listas):
        lista_dicts = []
        for lista in listas:
            valores = lista.split(" ")
            remov_espacos = list(filter(lambda k: len(k.strip()) > 0, valores))
            cont = len(remov_espacos)
            if cont > 4:
                sku = remov_espacos[-2]
                saldo = remov_espacos[-1]
                
                dict_saldo = {}
                dict_saldo['SKU'] = str(sku).strip()
                dict_saldo['MARCA'] = str('Sense')
                try:
                    saldos = saldo.strip().replace(".","").replace(",",".")
                    dict_saldo['SALDO'] = float(saldos)
                except:
                    dict_saldo['SALDO'] = float(0)

                dict_saldo['DATA'] = self.dataatual

            
                dict_saldo['PRAZO'] = 'Prazo Definido pelo fabricante'
               
                
                lista_dicts.append(dict_saldo)

        return lista_dicts

    def reader_imagem(self):
       
        lista_dicts_saldos = []
        imgs = os.listdir('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\')

        for im in imgs:
            if 'sense' in im:
                img = cv2.imread(f'C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\imagens\\{im}')
                #imagemgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #Convertendo para rgb
                imagemgray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Convertendo para rgb
                texto = pytesseract.image_to_string(imagemgray, lang= self.tesseract_language,config=self.config)
                valor = texto.split("\n")
                dicts = self.separa_valores(valor)
                for dict in dicts:
                    lista_dicts_saldos.append(dict)
            
        return lista_dicts_saldos

    def create_dataframe(self):
        listas = self.reader_imagem()
        data = pd.DataFrame(listas)
        data['SKU'].fillna(0, inplace=True)

        data['SALDO'].fillna(0, inplace=True)
        data['SALDO'] = data['SALDO'].astype(float)
        data.drop(data.loc[data['SALDO']=='valornaoencontrado'].index, inplace=True)
        data = data.sort_values('SALDO', ascending=False).drop_duplicates('SKU').sort_index()
        data.to_excel('C:\\Projetoshausz\\apphauszetlsbi\\uploadarquivos\\logs\\sense0606.xlsx')
        jsons = data.to_dict('records')
        return jsons


    
