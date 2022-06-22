from sqlalchemy import DateTime
from sqlalchemy import Column, Float, Integer, Numeric, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class ProdutoBasico(Base):
    __tablename__='ProdutoBasico'
    __table_args__ = {"schema": "Produtos"}
    IdProduto = Column(Integer, primary_key=True, nullable=False)

    SKU = Column(String(100), nullable=True)
    CodOmie = Column(Integer, nullable=False)
    NomeProduto = Column(String(250), nullable=True)
    NomeEtiqueta = Column(String(200), nullable=True)
    NomeTotem = Column(String(200), nullable=True)
    EAN = Column(String(50), nullable=True)
    NCM = Column(String(12), nullable=True)
    CEST = Column(String(10), nullable=True)
    DataInserido = Column(DateTime, nullable=True)
    IdMarca = Column(Integer, nullable=False)
    ValorMinimo = Column(Numeric(18,2), nullable=False)
    bitLinha = Column(Boolean, nullable=True)
    BitAtivo = Column(Boolean, nullable=True)
    IdSubCat = Column(Integer, nullable=False)
    bitOmie = Column(Boolean, nullable=True)
    EstoqueAtual = Column(Integer, nullable=True)
    SaldoAtual = Column(Numeric(16,4), nullable=False)
    InseridoPor = Column(String(50), nullable=True)
    DataAlteracao = Column(DateTime, nullable=True)
    bitPromocao = Column(Boolean, nullable=True)
    bitOutlet = Column(Boolean, nullable=True)
    bitAmostra = Column(Boolean, nullable=True)
    bitPrecoAtualizado = Column(Boolean, nullable=True)
    PesoCubado = Column(Numeric(9,6), nullable=False)
    Peso = Column(Numeric(9,6), nullable=False)
    IdDept = Column(Integer, nullable=True)
    EstoqueLocal = Column(Integer, nullable=True)
    bitEasy = Column(Boolean, nullable=True)
  
   
    def __repr__(self):
        return f"<Produto : {self.IdProduto} >"


class ProdutoDetalhe(Base):
    __tablename__ = 'ProdutoDetalhe'
    IdProduto = Column(Integer, primary_key=True, unique=True)
    SKU = Column(String(100), nullable=True, unique=False)
    IdMarca = Column(Integer, nullable=True, unique=False)
    IdSubCat =  Column(Integer, nullable=True, unique=False)
    Descricao = Column(String(), nullable=True, unique=False)
    QuantidadeMinima = Column(Integer, nullable=True, unique=False)
    TamanhoBarra = Column(String(), nullable=True, unique=False)
    Unidade = Column(Integer, nullable=True, unique=False)
    FatorVenda = Column(Integer, nullable=True, unique=False)
    FatorMultiplicador = Column(Integer, nullable=True, unique=False)
    FatorUnitario = Column(String(), nullable=True, unique=False)
    UrlImagem = Column(String(), nullable=True, unique=False)
    Garantia = Column(String(), nullable=True, unique=False)
    Nimagem = Column(Integer, nullable=True, unique=False)
    Comprimento = Column(Integer, nullable=True, unique=False)
    Largura = Column(Integer, nullable=True, unique=False)
    Altura = Column(Integer, nullable=True, unique=False)
    ValorMinimo = Column(Integer, nullable=True, unique=False)
    bitVerificadoFoto = Column(Boolean, nullable=True, unique=False)
    Peso = Column(Integer, nullable=True, unique=False)
    bitAtivo = Column(Boolean, nullable=True, unique=False)
    UsuarioAlteracao = Column(String(), nullable=True, unique=False)
    DataInserido = Column(DateTime)
    IdProdutoNaoUsaMais = Column(Integer, nullable=True, unique=False)
    


class MarcaProduto(Base):
    __tablename__ = 'Marca'
    IdMarca = Column(Integer, primary_key=True, unique=True)
    Marca = Column(String(), nullable=True, unique=False)
    PrazoFabricacao = Column(Integer, nullable=True, unique=False)
    PedidoMinimo = Column(Integer, nullable=True, unique=False)
    Sobre = Column(String(), nullable=True, unique=False)
    Video = Column(String(), nullable=True, unique=False)
    DataCadastro = Column(DateTime)
    DataAtualizacao = Column(DateTime)
    IncluidoPor = Column(String(), nullable=True, unique=False)
    AlteradoPor = Column(String(), nullable=True, unique=False)
    BitAtivo = Column(Boolean, nullable=True, unique=False)
    IdMarca2 = Column(Integer, nullable=True, unique=False)
    ImgNome = Column(String(), nullable=True, unique=False)
    bitShowRoom = Column(Boolean, nullable=True, unique=False)


