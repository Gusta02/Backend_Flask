
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime


db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db

  
class InformacoesSellers(db.Model):
    __tablename__='InformacoesSellers'
    IdSeller = db.Column(db.Integer, primary_key=True, nullable=False)
    SkuSeller = db.Column(db.String(100), nullable=True)
    UrlSeller = db.Column(db.String(2000), nullable=True)
    PrecoProdutoSeller =  db.Column(db.Float, nullable=True)
    PrecoMetroSeller = db.Column(db.Float, nullable=True)
    PrecoFreteSeller = db.Column(db.Float, nullable=True)
    PrazoSeller = db.Column(db.Integer, nullable=True)
    CepHausz = db.Column(db.String(30), nullable=True)
    ImagemProduto =  db.Column(db.String(2000), nullable=True)
    EanReferencia = db.Column(db.String(15), nullable=True)
    Marca = db.Column(db.String(50), nullable=True)
    NomeSeller = db.Column(db.String(200), nullable=True)
    SiteSeller = db.Column(db.String(150), nullable=True)
    CategoriaSeller = db.Column(db.String(50), nullable=True)
    Metro = db.Column(db.Float, nullable=True)
    SkuHausz = db.Column(db.String(2000), nullable=True)
    DataAtualizado = db.Column(DateTime, nullable=True)
    NomeProdutoSeller = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f"<Seller : {self.IdSeller} >"
