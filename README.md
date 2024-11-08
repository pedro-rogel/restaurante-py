<<<<<<< HEAD
# Gerenciamento de Restaurante com SQLAlchemy

Este projeto é uma aplicação de linha de comando para gerenciar um restaurante, utilizando Python e SQLAlchemy para manipulação de banco de dados. A aplicação permite o cadastro de restaurantes, funcionários, pratos de cardápio, avaliações e oferece funcionalidades avançadas de gerenciamento, como alteração de disponibilidade de pratos e consulta de informações de restaurante.

## Sumário
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Funcionalidades](#funcionalidades)
- [Uso](#uso)
- [Estrutura de Tratamento de Erros](#estrutura-de-tratamento-de-erros)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - SQLAlchemy
  - OS (nativa do Python)
  - Time (nativa do Python)

## Instalação

1. Clone o repositório para sua máquina local:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Instale as dependências:
   ```bash
   pip install sqlalchemy
   ```

3. Execute o arquivo principal para iniciar a aplicação:
   ```bash
   python nome_do_arquivo.py
   ```

## Funcionalidades

A aplicação oferece as seguintes funcionalidades principais:

1. **Cadastro de Restaurante**: Permite inserir informações do restaurante, como nome, endereço, telefone e ramo.

2. **Desligamento de Restaurante**: Exclui um restaurante do sistema.

3. **Alteração de Informações do Restaurante**: Edita informações do restaurante, como nome, endereço, telefone e ramo.

4. **Cadastro e Desligamento de Funcionários**: Adiciona ou remove funcionários, com controle sobre CPF, nome, cargo e salário.

5. **Cadastro de Pratos no Cardápio**: Permite adicionar pratos ao cardápio, incluindo nome, descrição, preço, categoria e disponibilidade.

6. **Avaliação do Restaurante**: Clientes podem avaliar restaurantes com notas e comentários.

7. **Alterar Estado de Disponibilidade dos Pratos**: Alterna entre "disponível" e "indisponível" para cada prato do cardápio.

8. **Exibir Informações do Restaurante**: Exibe informações detalhadas de um restaurante específico.

## Uso

### Menu Principal
Quando o programa é executado, o menu principal é exibido com opções numéricas para cada funcionalidade:

```
Bem Vindo ao nosso Projeto!
------------------------------
Escolha sua opção:
1. Cadastrar Restaurante
2. Desligar Restaurante
3. Alterar Informações
4. Cadastrar Funcionários
5. Cadastrar Cardápio
6. Avaliar Restaurante
7. Alternar Estado (status ou disponibilidade)
8. Mostrar Informações do Restaurante
9. Sair
```

O usuário deve inserir o número correspondente à funcionalidade desejada. Se uma entrada inválida for fornecida, uma mensagem de erro personalizada será exibida.

### Exemplo de Cadastro de Restaurante
1. Selecione a opção `1` para cadastrar um restaurante.
2. Siga as instruções na tela para inserir o nome, endereço, telefone e ramo do restaurante.
3. O sistema confirmará o cadastro e limpará a tela para retornar ao menu principal.

### Exemplo de Avaliação do Restaurante
1. Selecione a opção `6` para avaliar um restaurante.
2. Insira o CPF do cliente e o nome do restaurante que deseja avaliar.
3. Informe uma nota entre 0 e 5 e um comentário opcional.
4. A avaliação será salva e o sistema confirmará a operação.

## Estrutura de Tratamento de Erros

A aplicação inclui uma estrutura de tratamento de erros avançada com exceções personalizadas para entrada de dados:

- `EntradaInteiroInvalidaError`: Lançada quando o usuário insere um valor não-inteiro em uma entrada que exige números inteiros.
- `EntradaFloatInvalidaError`: Lançada quando o usuário insere um valor não-decimal em uma entrada que exige números decimais.
- `EntradaNotaInvalidaError`: Lançada ao inserir uma nota fora do intervalo permitido (0 a 5) para a avaliação do restaurante.
- `EntradaOpcaoInvalidaError`: Lançada quando o usuário insere uma opção fora do menu.

Essas exceções são tratadas em tempo de execução e garantem que o programa continue funcionando de maneira estável.

## Estrutura do Projeto

O projeto está organizado em uma estrutura simples, com classes representando as entidades principais:

- `Restaurante`: Representa os dados do restaurante.
- `Cliente`: Representa os dados dos clientes do restaurante.
- `Funcionario`: Representa os dados dos funcionários do restaurante.
- `Cardapio`: Representa o cardápio do restaurante com pratos e disponibilidade.
- `Avaliacao`: Permite que clientes façam avaliações do restaurante com notas e comentários.

## Contribuição

Se deseja contribuir com melhorias para o projeto, por favor, faça um fork do repositório, crie uma nova branch para a sua modificação, e envie um pull request. Sugestões para novas funcionalidades ou aprimoramento da estrutura de código são bem-vindas!

---



<h1>Para Usuários: </h1>

Este programa é uma aplicação de linha de comando criada para facilitar o gerenciamento de um restaurante. Com ela, você pode controlar desde o cadastro de informações básicas do restaurante até a avaliação de serviços pelos clientes, utilizando uma interface simples e intuitiva. Abaixo estão as principais funcionalidades e seu propósito:

1. **Cadastro de Restaurante**: Permite registrar novos restaurantes com informações como nome, endereço, telefone e ramo. Essa função facilita o gerenciamento de múltiplas unidades ou restaurantes cadastrados no sistema.

2. **Desligamento de Restaurante**: Esta opção remove um restaurante do sistema. Ideal para manter os dados atualizados e evitar informações desnecessárias.

3. **Alteração de Informações do Restaurante**: Caso precise atualizar dados, como um número de telefone ou endereço, essa função permite modificar as informações do restaurante de maneira rápida.

4. **Cadastro e Desligamento de Funcionários**: Permite registrar novos funcionários ou desligar os que não fazem mais parte da equipe, mantendo um controle atualizado sobre o quadro de colaboradores, com informações como CPF, cargo e salário.

5. **Cadastro de Pratos no Cardápio**: Nesta função, você pode adicionar novos pratos ao cardápio com detalhes sobre o prato, como ingredientes, categoria, preço e disponibilidade. É útil para gerenciar o menu e deixar claro quais pratos estão disponíveis.

6. **Avaliação do Restaurante**: Clientes cadastrados podem avaliar o restaurante com uma nota de 0 a 5 e um comentário opcional. Esse feedback ajuda a obter uma visão geral sobre a satisfação do cliente.

7. **Alterar Estado de Disponibilidade dos Pratos**: Caso algum prato precise ser temporariamente retirado ou colocado novamente no cardápio, essa opção permite alternar a disponibilidade do prato, facilitando o gerenciamento em tempo real do cardápio.

8. **Exibir Informações do Restaurante**: Fornece uma visão geral das informações do restaurante, como nome, categoria, endereço, telefone e ramo. É útil para consultas rápidas e para confirmar dados importantes.

O objetivo deste programa é oferecer uma solução prática e acessível para o gerenciamento de um restaurante, centralizando as operações diárias e permitindo que os administradores acompanhem facilmente as informações sobre a equipe, cardápio, avaliações e dados gerais do estabelecimento. A interface simples facilita o uso e torna a aplicação acessível para todos os níveis de experiência com tecnologia. 

Com esses recursos, o programa oferece uma base sólida para o controle e aprimoramento da experiência do cliente e da eficiência operacional do restaurante.
=======
>>>>>>> dev-pedro
