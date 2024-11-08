from sqlalchemy import Column,Table, Integer, String, Float, Boolean, Date, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from time import sleep
import os

class EntradaInteiroInvalidaError(Exception):
    pass

class EntradaFloatInvalidaError(Exception):
    pass

class EntradaNotaInvalidaError(Exception):
    pass

class EntradaOpcaoInvalidaError(Exception):
    pass

class CPFInvalidoError(Exception):
    pass

def layout():
    print('-' * 30)
    
engine = create_engine('sqlite:///restaurante.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

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
    nota = Column(Float)  
    comentario = Column(String(250)) 
    
    restaurante = relationship("Restaurante", back_populates="avaliacoes")
    cliente = relationship("Cliente", back_populates="avaliacoes")
    
    def __init__(self, restaurante_id, cliente_id, nota, comentario=None):
        self.restaurante_id = restaurante_id
        self.cliente_id = cliente_id
        self.nota = nota
        self.comentario = comentario


def cadastrarRestaurante():
    nome = input('Digite o nome do Restaurante: ').strip().title()
    endereco = input('Digite o endereço do restaurante: ').strip().title()
    telefone = input('Digite o telefone do restaurante: ').strip().title()
    ramo = input('Digite o ramo: ').strip().title()
    
    restaurante = Restaurante(nome=nome, endereco=endereco, telefone=telefone, ramo=ramo)
    session.add(restaurante)
    session.commit()
    os.system('cls')
    print('Restaurante cadastrado com sucesso!')
    input("Digite Enter para voltar")
    os.system('cls')

def desligarRestaurante():
    while True:
        restaurante_nome = input("Digite o nome do restaurante que você deseja desligar: ").strip()
        restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
        if restaurante:
            session.delete(restaurante)
            session.commit()
            os.system('cls')
            print("Restaurante deletado com sucesso!")
            input("Digite Enter para Limpar")
            os.system('cls')
            break
        else:
            os.system('cls')
            print('Restaurante não encontrado')
            continue

def alterarInformacoes():
    while True:
        restaurante_nome = input("Digite o nome do restaurante para atualizar: ").strip().title()
        restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
        
        if not restaurante:
            os.system('cls')
            print("Restaurante não encontrado.")
            input("Digite Enter para voltar")
            os.system('cls')
            continue

        while True:
            print("1. Alterar Nome")
            print("2. Alterar Endereço")
            print("3. Alterar Telefone")
            print("4. Alterar Ramo")
            print("5. Sair")
            opcao = int(input("Digite a opção desejada: "))
            try:
                if opcao == 1:
                    restaurante.nome = input("Digite o novo nome do restaurante: ").strip().title()
                elif opcao == 2:
                    restaurante.endereco = input("Digite o novo endereço: ").strip().title()
                elif opcao == 3:
                    restaurante.telefone = input("Digite o novo telefone: ").strip().title()
                elif opcao == 4:
                    restaurante.ramo = input("Digite o novo ramo: ").strip().title()
                elif opcao == 5:
                    break
                else:
                    raise EntradaOpcaoInvalidaError("Opção inválida.") 
                session.commit()
                os.system('cls')
                print("Informação alterada com sucesso!")
                input("Pressione Enter para voltar")
                os.system('cls')
            except (EntradaOpcaoInvalidaError) as e:
                os.system('cls')
                print(e)
                input("Digite Enter para Voltar")
                os.system('cls')
                continue
        break

def cadastarFuncionario():
    while True:
        print("1. Desligar Funcionario")
        print("2. Cadastrar Funcionario")
        print("3. Sair")
        try:
            opcao = int(input("Digite a opção desejada: "))
            if opcao == 1:
                funcionario_cpf = input("Digite o CPF do funcionario: ").strip().title()
                funcionario = session.query(Funcionario).filter_by(cpf=funcionario_cpf).first()
                if funcionario:
                    session.delete(funcionario)
                    session.commit()
                    os.system('cls')
                    print("Funcionario desligado com sucesso!")
                    input("Digite Enter para voltar")
                    os.system('cls')
                    break
                else:
                    os.system('cls')
                    print("Funcionario não encontrado.")
                    input("Digite Enter para voltar")
                    os.system('cls')
                    continue
            elif opcao == 2:
                nome = input('Digite o nome: ').strip().title()
                cargo = input('Digite o cargo: ').strip().title()
                while True:
                    try:
                        cpf = input('Digite o CPF do funcionario: ').strip().title()
                        if len(cpf) != 11 or not cpf.isdigit():
                            raise CPFInvalidoError("CPF inválido! Digite um CPF válido.")
                    except CPFInvalidoError as e:
                        os.system('cls')
                        print(e)
                        input("Digite Enter para voltar")
                        os.system('cls')
                        continue
                    while True:
                        try:
                            salario = float(input("Digite o salário do funcionario: "))
                            if salario >= 1:
                                funcionario = Funcionario(cpf=cpf, nome=nome, cargo=cargo, salario=salario)
                                session.add(funcionario)
                                session.commit()
                                os.system('cls')
                                print('Funcionario cadastrado com sucesso!')
                                input("Digite Enter para voltar")
                                os.system('cls')
                                break
                            else:
                                raise EntradaFloatInvalidaError("Erro, Digite um valor maior do que zero (0)")
                        except EntradaFloatInvalidaError as e:
                            os.system('cls')
                            print(e)
                            input("Digite Enter para voltar")
                            os.system('cls')
                        except ValueError:
                            print("Erro: entrada inválida. Digite um salário válido.")
                    break
            elif opcao == 3:
                os.system('cls')
                break
            else:
                raise EntradaOpcaoInvalidaError("Opção inválida.")
        except (EntradaInteiroInvalidaError, EntradaOpcaoInvalidaError) as e:
            os.system('cls')
            print(e)
            break
        
        
def deletarPrato():
    while True:
        nomePrato = input("Digite o nome do Prato: ")
        prato = session.query(Cardapio).filter_by(nome=nomePrato).first()
        if prato:
            delet = input("Deseja mesmo excluir esse prato (s/n):  ").lower()
            if delet =='s':
                session.delete(prato)
                session.commit()
                os.system('cls')
                print("Prato deletado com sucesso")
                input("Pressione Enter para voltar")
                os.system('cls')
                break
            else:
                input("Pressione Enter para voltar")
                os.system('cls')
                break
        else:
            os.system('cls')
            print("Prato não encontrado")
            input("Pressione Enter para voltar")
            os.system('cls')
            break

def cadastrarCardapio():
    while True:
        print('1. Cadastrar Prato')
        print('2. Ver Status do Prato')
        print('4. Deletar Prato')
        print('3. Voltar')
        try:
            opcao = int(input("Digite a opção desejada: "))
            os.system('cls')
            if opcao == 1:
                nome_item = input("Digite o nome do prato: ").strip().title()
                descricao = input("Digite os ingredientes: ").strip().title()
                preco = float(input("Digite um preço para o prato: "))
                categoria = input("Digite a categoria: ").strip().title()
                status = False  
                cardapio = Cardapio(nome=nome_item, descricao=descricao, preco=preco, categoria=categoria, disponibilidade=status)
                session.add(cardapio)
                session.commit()
                print("Prato cadastrado com sucesso no cardápio!")
                input("Digite Enter para voltar")
                os.system('cls')

            elif opcao == 2:
                nome_item = input("Digite o nome do prato para ver o status: ").strip().title()
                item = session.query(Cardapio).filter_by(nome=nome_item).first()
                if item:
                    print(f"Status de disponibilidade do prato '{item.nome}': {item.getter()}")
                else:
                    print("Prato não encontrado no cardápio.")
                input("Pressione Enter para continuar...")
                os.system('cls')
                
            elif opcao == 3:
                os.system('cls')
                break
            elif opcao == 4:
                deletarPrato()
            else:
                raise EntradaOpcaoInvalidaError("Opção inválida.")
        except (EntradaOpcaoInvalidaError) as e:
            os.system('cls')
            print(e)
            input("Digite Enter para voltar")
            os.system('cls')

def avaliarRestaurante():
    while True:
        cliente_cpf = input("Digite o CPF do cliente avaliador: ").strip().title()
        try:
            if len(cliente_cpf) != 11 or not cliente_cpf.isdigit():
                raise CPFInvalidoError("Erro: Insira um CPF válido")
        except CPFInvalidoError as e:
            os.system('cls')
            print(e)
            input("Digite Enter para voltar")
            os.system('cls')
        cliente = session.query(Cliente).filter_by(cpf=cliente_cpf).first()
        if not cliente:
                print("Cliente não encontrado. Por favor, cadastre o cliente primeiro.")
                input("Digite Enter para voltar")
                os.system('cls')
                break
            
        restaurante_nome = input("Digite o nome do restaurante que deseja avaliar: ").strip().title()
        restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
        if not restaurante:
                print("Restaurante não encontrado.")
                input("Digite Enter para voltar")
                os.system('cls')
                continue
        try:
            nota = float(input("Digite a nota de avaliação (0 a 5): "))
            if nota > 0 or nota < 5:
                comentario = input("Digite um comentário (opcional): ").strip().title()    
                avaliacao = Avaliacao(restaurante_id=restaurante.id, cliente_id=cliente.cpf, nota=nota, comentario=comentario)
                session.add(avaliacao)
                session.commit()
                print("Avaliação cadastrada com sucesso!")
                input("Digite Enter para voltar")
                os.system('cls')
                break
            else:
                raise EntradaNotaInvalidaError("Erro: A nota deve ser entre 0 e 5.")
        except EntradaFloatInvalidaError as e:
                print(e)
                input("Digite Enter para voltar")
                os.system('cls')
                
def cadastrarCliente():
    while True:
        nome = input("Digite o nome do cliente: ").strip().title()
        try:
            cpf = input("Digite o cpf do cliente: ").strip().title()
            if len(cpf) != 11 or not cpf.isdigit():
                raise CPFInvalidoError("CPF iválido!")
            tele = input("Digite o telefone do cliente: ").strip().title()
            email = input("Digite o email do cliente: ").strip().title()
            cliente_adcionado = session.query(Cliente).filter_by(cpf=cpf).first()
            if cliente_adcionado:
                os.system('cls')
                print("Cliente já cadastrado")
                input("Digite Enter para voltar")
                os.system('cls')
                return cliente_adcionado
            cliente = Cliente(cpf=cpf, nome=nome, telefone=tele, email=email)
            session.add(cliente)
            session.commit()
            os.system('cls')
            print("Cliente Cadastrado com Sucesso!")
            input("Digite Enter para voltar")
            os.system('cls')
            break
            
        except CPFInvalidoError as e:
            os.system('cls')
            print(e)
            continue
        
def alternarEstadoCardapio():
    while True:
        nome_item = input("Digite o nome do prato que deseja alterar a disponibilidade: ").strip().title()
        item = session.query(Cardapio).filter_by(nome=nome_item).first()
        if item:
            print(f"Disponibilidade atual de '{item.nome}': {item.getter()}")
            alterar = input("Deseja alterar a disponibilidade? (s/n): ").strip().lower()
            if alterar == 's':
                item.alternar_disponibilidade()
                session.commit()
                print(f"Disponibilidade do item '{item.nome}' alterada para: {item.getter()}")
                print("Alternado com Sucesso")
                os.system('cls')
                break
            else:
                print("Nenhuma alteração feita.")
                break
        else:
            print("Item não encontrado no cardápio.")
        input("Pressione Enter para voltar")
        os.system('cls')
        continue

def mostrarInformacoesRestaurante():
    restaurante_nome = input("Digite o nome do restaurante para ver as informações: ").strip().title()
    restaurante = session.query(Restaurante).filter_by(nome=restaurante_nome).first()
    
    if restaurante:
        os.system('cls')
        print("\nInformações do Restaurante:")
        print(f"Nome: {restaurante.nome}")
        print(f"Endereço: {restaurante.endereco}")
        print(f"Telefone: {restaurante.telefone}")
        print(f"Ramo: {restaurante.ramo}")
        print("-" * 30)
        
        if restaurante.avaliacoes:
            print("\nAvaliações:")
            for avaliacao in restaurante.avaliacoes:
                cliente = session.query(Cliente).filter_by(cpf=avaliacao.cliente_id).first()
                nome_cliente = cliente.nome if cliente else "Cliente não encontrado"
                print(f"Cliente: {nome_cliente}")
                print(f"Nota: {avaliacao.nota}")
                print(f"Comentário: {avaliacao.comentario if avaliacao.comentario else 'Sem comentário'}")
                print("-" * 30)
        else:
            print("Este restaurante ainda não possui avaliações.")
            
    else:
        print("Restaurante não encontrado.")
    
    input("Pressione Enter para Voltar")
    os.system('cls')
    

                

def projeto():
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
        print("9. Cadastrar Cliente")
        print("10. Sair")
        layout()
        
        try:
            opcao = int(input("Digite a opção desejada: "))
            
            if opcao == 1:
                os.system('cls')
                cadastrarRestaurante()
            elif opcao == 2:
                os.system('cls')
                desligarRestaurante()
            elif opcao == 3:
                os.system('cls')
                alterarInformacoes() 
            elif opcao == 4:
                os.system('cls')
                cadastarFuncionario()
            elif opcao == 5:
                os.system('cls')
                cadastrarCardapio()
            elif opcao == 6:
                os.system('cls')
                avaliarRestaurante()
            elif opcao == 7:
                os.system('cls')
                alternarEstadoCardapio()
            elif opcao == 8:
                os.system('cls')
                mostrarInformacoesRestaurante()
            elif opcao == 9:
                cadastrarCliente()
            elif opcao == 10:
                print("Saindo...")
                for i in range(3,0,-1):
                    print(i)
                    sleep(0.5)
                break
            else:
                raise EntradaOpcaoInvalidaError("Opção inválida.")
        except (EntradaOpcaoInvalidaError) as e:
            os.system('cls')
            print(e)


Base.metadata.create_all(engine)
projeto()
