from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///restaurante.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Restaurante(Base):
    __tablename__ = "restaurante"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    endereco = Column(String(50))
    telefone = Column(String(13))
    ramo = Column(String(20))
    
    avaliacoes = relationship("Avaliacao", back_populates="restaurante", cascade="all, delete-orphan")
    
    def __init__(self, nome, endereco, telefone, ramo) -> None:
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.ramo = ramo


class Cliente(Base):
    __tablename__ = "clientes"
    cpf = Column(String, primary_key=True)
    nome = Column(String(50))
    telefone = Column(String(13))
    email = Column(String(50))
    
    pedidos = relationship('Pedido', back_populates='cliente', cascade='all, delete-orphan')
    
    def __init__(self, nome, telefone, email) -> None:
        self.nome = nome
        self.telefone = telefone
        self.email = email


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    cpf = Column(String, primary_key=True)
    nome = Column(String(50))
    cargo = Column(String(50))
    salario = Column(Float)
    
    def __init__(self, nome, cargo, salario) -> None:
        self.nome = nome
        self.cargo = cargo
        self.salario = salario


class Dono(Funcionario):
    __tablename__ = 'donos'
    id = Column(Integer, primary_key=True)
    telefone = Column(String(13))
    email = Column(String(50))
    
    def __init__(self, nome, cargo, salario, telefone, email) -> None:
        super().__init__(nome, cargo, salario)
        self.telefone = telefone
        self.email = email


class Cardapio(Base):
    __tablename__ = 'cardapios'
    id = Column(Integer, primary_key=True)
    descricao = Column(String(50))
    
    
    itens = relationship("ItemCardapio", back_populates="cardapio")

    def __init__(self, descricao) -> None:
        self.descricao = descricao


class ItemCardapio(Base):
    __tablename__ = 'itens_cardapio'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    descricao = Column(String(50))
    preco = Column(Float)
    categoria = Column(String(50))
    disponibilidade = Column(Boolean)
    cardapio_id = Column(Integer, ForeignKey('cardapios.id'))
    
    # Relacionamento com Cardapio
    cardapio = relationship("Cardapio", back_populates="itens")

    def __init__(self, nome, descricao, preco, categoria, disponibilidade) -> None:
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
        self.disponibilidade = disponibilidade


class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(String, ForeignKey('clientes.cpf'))
    status = Column(String(50))
    data_pedido = Column(Date)
    
    # Relacionamento com Cliente
    cliente = relationship("Cliente", back_populates="pedidos")
    
    def __init__(self, cliente_id, status, data_pedido) -> None:
        self.cliente_id = cliente_id
        self.status = status
        self.data_pedido = data_pedido


class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    
    id = Column(Integer, primary_key=True)
    restaurante_id = Column(Integer, ForeignKey('restaurante.id'))  # Chave estrangeira para o restaurante
    cliente_id = Column(String, ForeignKey('clientes.cpf'))
    nota = Column(Float)  # Nota da avaliação, por exemplo, entre 0 e 5
    comentario = Column(String(250))  # Comentário opcional
    
    # Relacionamento com Restaurante
    restaurante = relationship("Restaurante", back_populates="avaliacoes")
    cliente = relationship("Cliente", back_populates="avaliacoes")
    
    def __init__(self, restaurante_id, nota, comentario=None):
        self.restaurante_id = restaurante_id
        self.nota = nota
        self.comentario = comentario