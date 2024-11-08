from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from time import sleep
import os

# Exceções personalizadas
class EntradaInteiroInvalidaError(Exception):
    pass

class EntradaFloatInvalidaError(Exception):
    pass

class EntradaNotaInvalidaError(Exception):
    pass

class EntradaOpcaoInvalidaError(Exception):
    pass

# Classes de entrada com validação e raise
class EntradaInteiro:
    def __init__(self, mensagem="Digite um número inteiro: "):
        self.mensagem = mensagem

    def obter(self):
        try:
            valor = int(input(self.mensagem))
            os.system('cls')
            return valor
        except ValueError:
            raise EntradaInteiroInvalidaError("Erro: Entrada inválida! Digite um número inteiro.")

class EntradaFloat:
    def __init__(self, mensagem="Digite um número decimal: "):
        self.mensagem = mensagem

    def obter(self):
        try:
            valor = float(input(self.mensagem))
            os.system('cls')
            return valor
        except ValueError:
            raise EntradaFloatInvalidaError("Erro: Entrada inválida! Digite um número decimal.")

def layout():
    print('-' * 30)

# Configuração do banco de dados e sessão
engine = create_engine('sqlite:///restaurante.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definição das classes
class Restaurante(Base):
    __tablename__ = "restaurante"
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    endereco = Column(String(50))
    telefone = Column(String(20))
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
    telefone = Column(String(20))
    email = Column(String(50))
    
    pedidos = relationship('Pedido', back_populates='cliente', cascade='all, delete-orphan')
    avaliacoes = relationship("Avaliacao", back_populates="cliente", cascade="all, delete-orphan")
    
    def __init__(self, cpf, nome, telefone, email) -> None:
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.email = email

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    cpf = Column(String, primary_key=True)
    nome = Column(String(50))
    cargo = Column(String(50))
    salario = Column(Float)
    
    def __init__(self, cpf, nome, cargo, salario) -> None:
        self.cpf = cpf
        self.nome = nome
        self.cargo = cargo
        self.salario = salario

class Cardapio(Base):
    __tablename__ = 'itens_cardapio'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    descricao = Column(String(50))
    preco = Column(Float)
    categoria = Column(String(50))
    disponibilidade = Column(Boolean)
    
    def __init__(self, nome, descricao, preco, categoria, disponibilidade) -> None:
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
        self.disponibilidade = disponibilidade
        
    def getter(self):
        return '✔️' if self.disponibilidade else '✖️'
    
    def alternar_disponibilidade(self):
        self.disponibilidade = not self.disponibilidade

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    
    id = Column(Integer, primary_key=True)
    restaurante_id = Column(Integer, ForeignKey('restaurante.id'))
    cliente_id = Column(String, ForeignKey('clientes.cpf'))
    nota = Column(Float)  # Nota da avaliação, por exemplo, entre 0 e 5
    comentario = Column(String(250))  # Comentário opcional
    
    restaurante = relationship("Restaurante", back_populates="avaliacoes")
    cliente = relationship("Cliente", back_populates="avaliacoes")
    
    def __init__(self, restaurante_id, cliente_id, nota, comentario=None):
        self.restaurante_id = restaurante_id
        self.cliente_id = cliente_id
        self.nota = nota
        self.comentario = comentario

# Funções principais com tratamento de exceções
def cadastrarRestaurante():
    nome = input('Digite o nome do Restaurante: ').strip()
    endereco = input('Digite o endereço do restaurante: ').strip()
    telefone = input('Digite o telefone do restaurante: ').strip()
    ramo = input('Digite o ramo: ').strip()
    
    restaurante = Restaurante(nome=nome, endereco=endereco, telefone=telefone, ramo=ramo)
    session.add(restaurante)
    session.commit()
    os.system('cls')
    print('Restaurante cadastrado com sucesso!')

def desligarRestaurante():
    restaurante_nome = input("Digite o nome do restaurante que você deseja desligar: ").strip()
    restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
    if restaurante:
        session.delete(restaurante)
        session.commit()
        os.system('cls')
        print("Restaurante deletado com sucesso!")
    else:
        os.system('cls')
        print('Restaurante não encontrado')

def alterarInformacoes():
    restaurante_nome = input("Digite o nome do restaurante para atualizar: ").strip()
    restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
    
    if not restaurante:
        os.system('cls')
        print("Restaurante não encontrado.")
        return

    entrada_inteiro = EntradaInteiro("Digite a opção desejada: ")

    while True:
        print("1. Alterar Nome")
        print("2. Alterar Endereço")
        print("3. Alterar Telefone")
        print("4. Alterar Ramo")
        print("5. Sair")
        
        try:
            opcao = entrada_inteiro.obter()
            
            if opcao == 1:
                restaurante.nome = input("Digite o novo nome do restaurante: ").strip()
            elif opcao == 2:
                restaurante.endereco = input("Digite o novo endereço: ").strip()
            elif opcao == 3:
                restaurante.telefone = input("Digite o novo telefone: ").strip()
            elif opcao == 4:
                restaurante.ramo = input("Digite o novo ramo: ").strip()
            elif opcao == 5:
                break
            else:
                raise EntradaOpcaoInvalidaError("Opção inválida.")
            
            session.commit()
            os.system('cls')
            print("Informação alterada com sucesso!")
        except (EntradaInteiroInvalidaError, EntradaOpcaoInvalidaError) as e:
            os.system('cls')
            print(e)

def cadastarFuncionario():
    entrada_inteiro = EntradaInteiro("Digite a opção: ")
    entrada_float = EntradaFloat("Digite o salário: ")

    while True:
        print("1. Desligar Funcionario")
        print("2. Cadastrar Funcionario")
        print("3. Sair")
        
        try:
            opcao = entrada_inteiro.obter()
            
            if opcao == 1:
                funcionario_cpf = input("Digite o CPF do funcionario: ").strip()
                funcionario = session.query(Funcionario).filter_by(cpf=funcionario_cpf).first()
                if funcionario:
                    session.delete(funcionario)
                    session.commit()
                    os.system('cls')
                    print("Funcionario desligado com sucesso!")
                else:
                    os.system('cls')
                    print("Funcionario não encontrado.")
            elif opcao == 2:
                cpf = input('Digite o CPF do funcionario: ').strip()
                nome = input('Digite o nome: ').strip()
                cargo = input('Digite o cargo: ').strip()
                
                try:
                    salario = entrada_float.obter()
                    funcionario = Funcionario(cpf=cpf, nome=nome, cargo=cargo, salario=salario)
                    session.add(funcionario)
                    session.commit()
                    os.system('cls')
                    print('Funcionario cadastrado com sucesso!')
                except EntradaFloatInvalidaError as e:
                    os.system('cls')
                    print(e)
            elif opcao == 3:
                os.system('cls')
                break
            else:
                raise EntradaOpcaoInvalidaError("Opção inválida.")
        except (EntradaInteiroInvalidaError, EntradaOpcaoInvalidaError) as e:
            os.system('cls')
            print(e)
    
def cadastrarCardapio():
    entrada_float = EntradaFloat("Digite o preço do prato: ")
    while True:
        print('1. Cadastrar Prato no Cardápio')
        print('2. Ver Status do Prato')
        print('3. Voltar')
        try:
            entrada_inteiro = EntradaInteiro("Digite a opção: ")
            opcao = entrada_inteiro.obter()
            os.system('cls')

            if opcao == 1:
                nome_item = input("Digite o nome do prato: ").strip()
                descricao = input("Digite os ingredientes: ").strip()
                preco = entrada_float.obter()
                categoria = input("Digite a categoria: ").strip()
                status = False  # Prato inicialmente indisponível

                # Cria e adiciona o novo prato ao banco de dados
                cardapio = Cardapio(nome=nome_item, descricao=descricao, preco=preco, categoria=categoria, disponibilidade=status)
                session.add(cardapio)
                session.commit()
                print("Prato cadastrado com sucesso no cardápio!")
                os.system('cls')

            elif opcao == 2:
                nome_item = input("Digite o nome do prato para ver o status: ").strip()
                item = session.query(Cardapio).filter_by(nome=nome_item).first()

                # Verifica se o item foi encontrado
                if item:
                    print(f"Status de disponibilidade do prato '{item.nome}': {item.getter()}")
                else:
                    print("Prato não encontrado no cardápio.")
                input("Pressione Enter para continuar...")
                os.system('cls')

            elif opcao == 3:
                os.system('cls')
                break
            else:
                raise EntradaOpcaoInvalidaError("Opção inválida.")
        except (EntradaInteiroInvalidaError, EntradaOpcaoInvalidaError) as e:
            os.system('cls')
            print(e)

def avaliarRestaurante():
    try:
        cliente_cpf = input("Digite o CPF do cliente avaliador: ").strip()
        cliente = session.query(Cliente).filter_by(cpf=cliente_cpf).first()
        if not cliente:
            print("Cliente não encontrado. Por favor, cadastre o cliente primeiro.")
            return
        
        restaurante_nome = input("Digite o nome do restaurante que deseja avaliar: ").strip()
        restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
        if not restaurante:
            print("Restaurante não encontrado.")
            return

        entrada_float = EntradaFloat("Digite a nota de avaliação (0 a 5): ")
        nota = entrada_float.obter()
        if nota < 0 or nota > 5:
            raise EntradaNotaInvalidaError("Erro: A nota deve ser entre 0 e 5.")

        comentario = input("Digite um comentário (opcional): ").strip()    
        avaliacao = Avaliacao(restaurante_id=restaurante.id, cliente_id=cliente.cpf, nota=nota, comentario=comentario)
        session.add(avaliacao)
        session.commit()
        print("Avaliação cadastrada com sucesso!")
        os.system('cls')
    except EntradaFloatInvalidaError as e:
        os.system('cls')
        print(e)
    except EntradaNotaInvalidaError as e:
        os.system('cls')
        print(e)

def alternarEstadoCardapio():
    nome_item = input("Digite o nome do prato que deseja alterar a disponibilidade: ").strip()
    item = session.query(Cardapio).filter_by(nome=nome_item).first()

    if item:
        print(f"Disponibilidade atual de '{item.nome}': {item.getter()}")
        alterar = input("Deseja alterar a disponibilidade? (s/n): ").strip().lower()
        if alterar == 's':
            item.alternar_disponibilidade()
            session.commit()
            print(f"Disponibilidade do item '{item.nome}' alterada para: {item.getter()}")
        else:
            print("Nenhuma alteração feita.")
    else:
        print("Item não encontrado no cardápio.")
    input("Pressione Enter para continuar...")
    os.system('cls')

def mostrarInformacoesRestaurante():
    restaurante_nome = input("Digite o nome do restaurante para ver as informações: ").strip()
    restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
    
    if restaurante:
        print("\nInformações do Restaurante:")
        print(f"Nome: {restaurante.nome}")
        print(f"Endereço: {restaurante.endereco}")
        print(f"Telefone: {restaurante.telefone}")
        print(f"Ramo: {restaurante.ramo}")
        print("-" * 30)
    else:
        print("Restaurante não encontrado.")
    input("Pressione Enter para continuar...")
    os.system('cls')

# Menu principal
def projeto():
    entrada_inteiro = EntradaInteiro("Digite a opção: ")
    while True:
        print("Bem Vindo ao nosso Projeto!")
        layout()
        print("Escolha sua opção: ")
        print("1. Cadastrar Restaurante")
        print("2. Desligar Restaurante")
        print("3. Alterar Informações")
        print("4. Cadastrar Funcionarios")
        print("5. Cadastrar Cardápio")
        print("6. Avaliar Restaurante")
        print("7. Alternar Estado (status ou disponibilidade)")
        print("8. Mostrar Informações do Restaurante")
        print("9. Sair")
        
        try:
            opcao = entrada_inteiro.obter()
            
            if opcao == 1:
                cadastrarRestaurante()
            elif opcao == 2:
                desligarRestaurante()
            elif opcao == 3:
                alterarInformacoes()
            elif opcao == 4:
                cadastarFuncionario()
            elif opcao == 5:
                cadastrarCardapio()
            elif opcao == 6:
                avaliarRestaurante()
            elif opcao == 7:
                alternarEstadoCardapio()
            elif opcao == 8:
                mostrarInformacoesRestaurante()
            elif opcao == 9:
                print("Saindo...")
                sleep(1)
                os.system('cls')
                break
            else:
                raise EntradaOpcaoInvalidaError("Opção inválida.")
        except (EntradaInteiroInvalidaError, EntradaOpcaoInvalidaError) as e:
            os.system('cls')
            print(e)

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

# Executando a função
projeto()
