# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:30:23 2022

@author: Hausz
"""
#from asyncio import exceptions
from app.Dash_Logistica.kpis_luiz.config import get_connection
from sqlalchemy import text
import pandas as pd


def get_table(query):
    engine = get_connection()
    lista_dicts = []
    with engine.connect() as conn:
        query_unidade = text(query)
        lista_unidade = conn.execute(query_unidade).all()
        for unidade in lista_unidade:
            dict_Unidade = {}
            for keys, values in unidade.items():
                dict_Unidade[keys] = values
            lista_dicts.append(dict_Unidade)

    return lista_dicts

def sql_to_pd(query):
    return pd.DataFrame(get_table(query))
