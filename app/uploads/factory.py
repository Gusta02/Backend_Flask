import re
from datetime import datetime

from ..brands.brand_deca import Deca
from ..brands.brand_gaudi import Gaudi
from ..brands.brand_level import Level
from ..brands.brand_portoferreira import PortoFerreira
from ..brands.brand_gaudi import Gaudi
from ..brands.brand_itagres import Itagres
from ..brands.brand_elizabeth import Elizabeth
from ..brands.brand_lexxa import Lexxa
from ..brands.brand_sense import Sense


class Produto:
    def __init__(self, path):
        self.path = path
        self.data_atual = str(datetime.today().strftime('%Y-%m-%d %H:%M'))

    def retorna_marca(self):
        if re.search('deca.?',self.path, re.IGNORECASE):
            deca = Deca(self.path)
            jsons = deca.read_excel(self.path,self.data_atual)
            return jsons

        if re.search('level.?|leve.?',self.path, re.IGNORECASE): 
            level = Level(self.path,self.data_atual)
            jsons = level.excel_reader()
            return jsons

        if re.search('porto|porto ferreira', self.path, re.IGNORECASE):
            porto = PortoFerreira(self.path,self.data_atual)
            jsons = porto.reader_excel()
            return jsons

        if re.search('gaudi.?', self.path, re.IGNORECASE):
            gaudi = Gaudi(self.path, self.data_atual)
            gaudi.converter_imgpdf()
            jsons =  gaudi.create_dataframe()
            return jsons

        if re.search('itagres.?', self.path, re.IGNORECASE):
            itagres = Itagres(self.path, self.data_atual)
            itagres.converter_imgpdf()
            jsons =  itagres.imagem_reader()
            return jsons

        if re.search('elizabeth.?', self.path, re.IGNORECASE):
            elizabeth = Elizabeth(self.path, self.data_atual)
            print(elizabeth)
            elizabeth.converter_imgpdf()
            jsons = elizabeth.create_dataframe()
            return jsons

        if re.search('lexxa.?',self.path, re.IGNORECASE):
            lexxa = Lexxa(self.path, self.data_atual)
            lexxa.converter_imgpdf()
            jsons = lexxa.create_dataframe()
        
            return jsons

        if re.search('sense.?',self.path, re.IGNORECASE):

            sense = Sense(self.path, self.data_atual)
            sense.converter_imgpdf()
            jsons = sense.create_dataframe()
            
            return jsons




        
      



