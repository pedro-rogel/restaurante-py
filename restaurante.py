from sqlalchemy import Column,Integer,String,Float

class Restaurante:
    def __init__(self, nome,end,telefone,ramo) -> None:
        self.nome = nome
        self.end = end
        self.telefone = telefone
        self.ramo = ramo
        
class Cliente:
    def __init__(self,nome,telefone,email) -> None:
        self.nome = nome
        self.telefone = telefone
        self.email = email
        
class Dono(Restaurante):
    def __init__(self, nome,telefone,email) -> None:
        self.email = email
        super().__init__(nome, end, telefone, ramo)
    

class Funcionario:
    def __init__(self,nome,cargo,salario) -> None:
        self.nome = nome
        self.cargo = cargo
        self._salario = salario
    
    
class Cardapio:
    def __init__(self,itens,descricao) -> None:
        self.itens = itens
        self.descricao = descricao
        
class ItemCardapio:
    def __init__(self,nomePedido,descricao,preco,categoria,disponibilidade) -> None:
        self.nome = nomePedido
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria
        self.disponibilidade = disponibilidade
        
class Pedido:
    def __init__(self,cliente,itens,status,dataPedido) -> None:
        self.cliente = cliente
        self.itens = itens
        self.status = status
        self.dataPedido = dataPedido
        
class Cliente:
    def __init__(self,nome,telefone,email) -> None:
        self.nome = nome
        self.telefone = telefone
        self.email = email
        
    
