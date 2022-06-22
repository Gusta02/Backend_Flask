from flask import Blueprint, render_template, jsonify

from ..models.produtos import ProdutoBasico, ProdutoDetalhe, MarcaProduto
from ..models.serializer import Basicoschema,MarcaSchema,DetalheSchema

from config import TEMPLATE_FOLDER,get_connection
from ..controllers.consultascontroller import (retorna_all_produtos
,retorna_cadastros_novos, select_prazos_fabricantes,select_sku_coletado_especificacao
,select_sku_unitario_referencia, select_resumo_marcas,retorna_produtos_estoques)

from ..coletores.estoques_fabricas import Brands

import os
import pandas as pd


relatorios = Blueprint("relatorios",__name__, 
        template_folder=os.path.join(TEMPLATE_FOLDER, "resources", "templates"), 
        static_folder=os.path.join(TEMPLATE_FOLDER, "resources", "static"),static_url_path='/static/')



@relatorios.route("/googleshopping", methods=["GET","POST"])
def precos_google():
    data = pd.read_excel("D:\\ARQUIVOS GERAIS 0606\\google\\googlehausz0506.xlsx")
    jsons = data.to_dict('records')
 
    return render_template("googleshopping.html", produtos=jsons)

@relatorios.route("/produtos/", methods=["GET","POST"])
@relatorios.route("/produtos/<int:page>", methods=["GET","POST"])
def retorna_produtos(page=1):
    produtos = retorna_all_produtos(page)
    print(produtos)
    return render_template("produtos.html",page=page, produtos=produtos)


@relatorios.route("/freteconcorrente", methods=["GET","POST"])
def frete_concorrete():
    return render_template("freteconcorrente.html")

@relatorios.route("/prazosmarcas/", methods=["GET","POST"])
@relatorios.route("/prazosmarcas/<int:page>", methods=["GET","POST"])
def prazos_marca(page=1):
    produtos = select_prazos_fabricantes(page)
    return render_template("prazosmarcas.html", page=page, produtos = produtos)

@relatorios.route("/marcas", methods=["GET","POST"])
def retorna_marcas():
    marcas = select_resumo_marcas()
    print(marcas)
 
    return render_template("marcas.html", produtos = marcas)


@relatorios.route("/cadastrosnovos/", methods=["GET","POST"])
@relatorios.route("/cadastrosnovos/<int:page>", methods=["GET","POST"])
def retorna_produtos_coletas(page=1):
    jsons = retorna_cadastros_novos(page)

    return render_template("produtoscoletados.html",page=page, produtos=jsons)

@relatorios.route("/codigoproduto/<int:idproduto>", methods=["GET","POST"])
def retorna_sku_coletado(idproduto):

    skus = select_sku_unitario_referencia(idproduto)
    jsons = select_sku_coletado_especificacao(idproduto)
 
    return render_template("cadastro.html", produtos=jsons,skus=skus)

@relatorios.route("/marcasdinamicas", methods=["GET","POST"])
def marcas_dinamicas():
    lista_jsons = []
    brands = Brands()
    jsons = brands.read_file()
    for js in jsons:
        for brand in js:
            lista_jsons.append(brand)
    print(lista_jsons)
    return render_template("informacoesestoque.html", produtos = lista_jsons)


@relatorios.route("/startcoletores", methods=["GET","POST"])
def coletores():
    return "coletor"


@relatorios.route("/concorrentes", methods=["GET","POST"])
def preco_concorrente():
    return "teste"

'''
@relatorios.route("/testes", methods=["GET","POST"])
def testedash():
    return render_template('charts.html')
'''