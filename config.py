import urllib
import pyodbc
import os
from urllib.parse import quote_plus
from urllib import parse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from os import environ as env

load_dotenv()

driver = env['driver']
server = env['server']
database = env['database']
usuario = env['usuario']
password = env['password']

patharquivos = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv','xlsx'}

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET = '292e8ca15d171e358a8b473c66c35e6ad859dca78c30c0749d90bc7f813e9fc2'
TEMPLATE_FOLDER = os.path.abspath(os.path.dirname(__file__)) #serve para unir caminhos e diretorios
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection() -> URL:
    connection_string = """{};SERVER={};DATABASE={};UID={};PWD={}""".format(driver,server,database,usuario,password)
    url_db = quote_plus(connection_string)
    connection_url = f'mssql+pyodbc:///?odbc_connect=+{url_db}'
    return create_engine(connection_url,fast_executemany=True)





