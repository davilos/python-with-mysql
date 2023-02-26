import sys
from typing import Union

import MySQLdb
from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

CONEXAO: Connection
CONS = Console()
PROMPT = Prompt()


def menu():
    """
    Função para gerar o menu inicial
    """

    CONS.print()
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos')
    print('2 - Inserir produtos')
    print('3 - Atualizar produto')
    print('4 - Deletar produto')
    print('5 - Encerrar o programa')
    print('m/menu - Mostrar a tela de menu novamente')
    print('================================================')

    while True:
        try:
            opcao = input('\033[32m\n-> : \033[m')
            match opcao:
                case '1':
                    listar()
                case '2':
                    inserir()
                case '3':
                    atualizar()
                case '4':
                    deletar()
                case 'm' | 'menu' | 'M' | 'Menu':
                    menu()
                case '5':
                    sair = input('Para confirmar o encerramento digite "0": ')
                    match sair:
                        case '0':
                            desconectar()
                            sys.exit()
                        case _:
                            continue
                case _:
                    raise ValueError()
        except ValueError:
            print('\033[31m\nOpção inválida, tente novamente!\033[m')


def conectar() -> None:
    """
    Função para conectar ao servidor
    """
    global CONEXAO

    try:
        user: str = input('Digite o seu usuário: ')
        password: str = PROMPT.ask('Digite a senha do usuário', password=True)

        CONEXAO = MySQLdb.connect(
            db='pmysql',
            host='127.0.0.1',
            port=3306,
            user=user,
            passwd=password,
        )
    except MySQLdb.Error as error:
        print(
            f'\033[31mErro ao tentar se conectar no MySQL Server\n{error}\033[m'
        )
        sys.exit()
    else:
        menu()


def desconectar() -> None:
    """
    Função para desconectar do servidor.
    """
    try:
        CONEXAO.close()
    except MySQLdb.OperationalError:
        print(
            '\033[31mA conexão já foi fechada, ou não existe uma conexão!\033[m'
        )


def listar() -> None:
    """
    Função para listar os produtos
    """
    cursor: Cursor = CONEXAO.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos: tuple = cursor.fetchall()

    if len(produtos) > 0:
        table = Table(title='Produtos cadastrados')

        table.add_column('id', justify='right')
        table.add_column('Nome')
        table.add_column('Preço', justify='right')
        table.add_column('Estoque', justify='right')

        for produto in produtos:
            table.add_row(
                str(produto[0]),
                str(produto[1]),
                str(produto[2]),
                str(produto[3]),
            )

        CONS.print()
        CONS.print(table)
    else:
        print('Ainda não existem produtos cadastrados!')


def inserir() -> None:
    """
    Função para inserir um produto
    """
    cursor: Cursor = CONEXAO.cursor()

    try:
        CONS.print()
        nome: Union[str, ValueError] = get_name()
        preco: float = float(input('Informe o preço do produto: '))
        estoque: int = int(input('Informe a quantidade em estoque: '))
        CONS.print()

        cursor.execute(
            f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {estoque})"
        )
    except ValueError:
        print(
            '\033[31mErro ao inserir produto, digite os valores corretos!\033[m'
        )
    else:
        CONEXAO.commit()

        if cursor.rowcount == 1:
            print(f'O produto \033[1m{nome}\033[m foi inserido com sucesso!')
        else:
            print('\033[31mNão foi possível inserir o produto.\033[m')


def atualizar() -> None:
    """
    Função para atualizar um produto
    """
    cursor: Cursor = CONEXAO.cursor()

    try:
        CONS.print()
        codigo: int = int(input('Informe o código do produto: '))
        nome: Union[str, ValueError] = get_name()
        preco: float = float(input('Informe o novo preço do produto: '))
        estoque: int = int(input('Informe a nova quantidade em estoque: '))

        cursor.execute(
            f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id={codigo}"
        )
    except ValueError:
        print(
            '\033[31mErro ao atualizar produto, digite os valores corretos!\033[m'
        )
    else:
        CONEXAO.commit()

        if cursor.rowcount == 1:
            print(f'O produto \033[1m{nome}\033[m foi atualizado com sucesso!')
        else:
            print('\033[31mNão foi possível atualizar o produto.\033[m')


def deletar() -> None:
    """
    Função para deletar um produto
    """
    cursor: Cursor = CONEXAO.cursor()

    try:
        CONS.print()
        codigo: int = int(input('Informe o código do produto: '))

        cursor.execute(f'DELETE FROM produtos WHERE id={codigo}')
    except ValueError:
        print(
            '\033[31mErro ao deletar produto, digite os valores corretos!\033[m'
        )
    else:
        CONEXAO.commit()

        if cursor.rowcount == 1:
            print('O produto foi deletado com sucesso!')
        else:
            print('\033[31mNão foi possível deletar o produto.\033[m')


def get_name() -> str | ValueError:
    """
    Função para testar se o nome do produto que está sendo recebido não é uma string vazia.
    """
    nome: str = input('Informe o nome do produto: ').strip()

    if len(nome) > 0:
        return nome.title()

    raise ValueError()
