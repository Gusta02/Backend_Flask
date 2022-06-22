
from urllib import response
from flask import Blueprint, current_app, jsonify, request
from app.models.produtos import ProdutoBasico,ProdutoDetalhe,MarcaProduto
from app.models.serializer import Basicoschema, DetalheSchema,  MarcaSchema


bp_teste = Blueprint("teste",__name__)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


@bp_teste.route("/teste", methods=["GET","POST"])
def teste():
    bs = Basicoschema(many=True)

    basico = ProdutoBasico.query.filter_by(IdMarca=1).all()
    bs.jsonify(basico)
  
    return bs.jsonify(basico), 200
    
    
