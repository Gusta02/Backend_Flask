from dataclasses import fields
from flask_marshmallow import Marshmallow, Schema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models.produtos import ProdutoBasico, ProdutoDetalhe, MarcaProduto



class Basicoschema(Schema):
    class Meta:
        model = ProdutoBasico
        load_instance = True

    IdProduto = auto_field()
    SKU = auto_field()
    CodOmie = auto_field()
    NomeProduto = auto_field()
    NomeEtiqueta = auto_field()
    NomeTotem = auto_field()
    EAN = auto_field()
    NCM = auto_field()
    CEST = auto_field()
    DataInserido = auto_field()
    IdMarca = auto_field()
    ValorMinimo = auto_field()
    bitLinha = auto_field()
    BitAtivo = auto_field()
    IdSubCat = auto_field()
    bitOmie = auto_field()
    EstoqueAtual = auto_field()
    SaldoAtual = auto_field()
    InseridoPor = auto_field()
    DataAlteracao = auto_field()
    bitPromocao = auto_field()
    bitOutlet = auto_field()
    bitAmostra = auto_field()
    bitPrecoAtualizado = auto_field()
    PesoCubado = auto_field()
    Peso = auto_field()
    IdDept = auto_field()
    EstoqueLocal = auto_field()
    bitEasy = auto_field()

   
class DetalheSchema(Schema):
    class Meta:
        model = ProdutoDetalhe
        load_instance = True
    IdProduto = auto_field()
    SKU = auto_field()
    IdMarca = auto_field()
    IdSubCat =  auto_field()
    Descricao = auto_field()
    QuantidadeMinima = auto_field()
    TamanhoBarra = auto_field()
    Unidade = auto_field()
    FatorVenda = auto_field()
    FatorMultiplicador = auto_field()
    FatorUnitario = auto_field()
    UrlImagem = auto_field()
    Garantia = auto_field()
    Nimagem = auto_field()
    Comprimento = auto_field()
    Largura = auto_field()
    Altura = auto_field()
    ValorMinimo = auto_field()
    bitVerificadoFoto = auto_field()
    Peso = auto_field()
    bitAtivo = auto_field()
    UsuarioAlteracao = auto_field()
    DataInserido = auto_field()
    IdProdutoNaoUsaMais = auto_field()


class MarcaSchema(Schema):
    class Meta:
        model = MarcaProduto
        load_instance = True
        detalhe = Nested(DetalheSchema)
    IdMarca = auto_field()
    Marca = auto_field()
    PrazoFabricacao = auto_field()
    PedidoMinimo = auto_field()
    Sobre = auto_field()
    Video = auto_field()
    DataCadastro = auto_field()
    DataAtualizacao = auto_field()
    IncluidoPor = auto_field()
    AlteradoPor = auto_field()
    BitAtivo = auto_field()
    IdMarca2 = auto_field()
    ImgNome = auto_field()
    bitShowRoom = auto_field()
