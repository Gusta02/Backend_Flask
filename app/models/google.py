
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime


db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db

  
class ProdutoPrecoGoogle(db.Model):
    __tablename__='ProdutoPrecoGoogle'
    IdProdutoGoogle = db.Column(db.Integer, primary_key=True, nullable=False)
    SKU = db.Column(db.String(255), nullable=True)
    IdMarca = db.Column(db.Integer, nullable=False)
    SellerMenor = db.Column(db.String(250), nullable=True)
    EanProduto = db.Column(db.String(20), nullable=True)
    MenorPReco = db.Column(db.Numeric(16,2), nullable=False)
    SellerMaior = db.Column(db.String(250), nullable=True)
    MaiorPreco = db.Column(db.Numeric(16,2), nullable=False)
    UrlGoogle = db.Column(db.String(1000), nullable=True)
    DataAtualizado = db.Column(DateTime, nullable=True)

    def __repr__(self):
            return f"<User : {self.IdProdutoGoogle} >"
