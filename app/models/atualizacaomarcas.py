
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime


db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db

  
class SaldosAtualizacaoMarcas(db.Model):
    __tablename__='SaldosAtualizacaoMarcas'
    IdMarcaSaldo = db.Column(db.Integer, primary_key=True, nullable=False)
    SKUMARCA = db.Column(db.String(255), nullable=True)
    SKUHAUSZ = db.Column(db.String(255), nullable=True)
    MARCA = db.Column(db.String(50), nullable=True)
    EAN = db.Column(db.String(50), nullable=True)
    IdMarca = db.Column(db.Integer, nullable=False)
    Saldo = db.Column(db.Numeric(18,2), nullable=True)
    DataAtualizado = db.Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Saldos : {self.IdMarcaSaldo} >"
