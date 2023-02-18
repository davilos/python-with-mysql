import MySQLdb
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt

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
    CONS.print()

    while True:
        try:
            opcao = input(f'-> : ')
            match opcao:
                case '1':
                    listar()
                case '2':
                    inserir()
                case '3':
                    atualizar()
                case '4':
                    deletar()
                case 'm' | 'menu' | 'M':
                    menu()
                case '5':
                    sair = input('Para confirmar o encerramento digite "0": ')
                    match sair:
                        case '0':
                            desconectar()
                            exit()
                        case _:
                            continue
                case _:
                    raise ValueError()
        except ValueError:
            print('\033[31mOpção inválida, tente novamente!\033[m')


def conectar() -> None:
    """
    Função para conectar ao servidor
    """
    try:
        user: str = input('Digite o seu usuário: ')
        password: str = PROMPT.ask('Digite a senha do usuário', password=True)

        global CONEXAO
        CONEXAO = MySQLdb.connect(
            db='pmysql',
            host='127.0.0.1',
            port=3306,
            user=user,
            passwd=password,
        )
    except MySQLdb.Error as Error:
        print(
            f'\033[31mErro ao tentar se conectar no MySQL Server\n{Error}\033[m'
        )
        exit()
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
    cursor = CONEXAO.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

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
        CONS.print()
    else:
        print('Ainda não existem produtos cadastrados!\n')


def inserir() -> None:
    """
    Função para inserir um produto
    """
    cursor = CONEXAO.cursor()

    try:
        CONS.print()
        nome = get_name()
        preco = float(input('Informe o preço do produto: '))
        estoque = int(input('Informe a quantidade em estoque: '))
        CONS.print()

        cursor.execute(
            f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {estoque})"
        )
    except ValueError:
        print(
            '\033[31mErro ao inserir produto, digite os valores corretos!\033[m\n'
        )
    else:
        CONEXAO.commit()

        if cursor.rowcount == 1:
            print(f'O produto \033[1m{nome}\033[m foi inserido com sucesso!\n')
        else:
            print('\033[31mNão foi possível inserir o produto.\033[m\n')


def atualizar() -> None:
    """
    Função para atualizar um produto
    """
    cursor = CONEXAO.cursor()


def deletar() -> None:
    """
    Função para deletar um produto
    """
    cursor = CONEXAO.cursor()


def get_name() -> str | ValueError:
    nome: str = input('Informe o nome do produto: ')

    if len(nome) > 0:
        return nome.strip().title()
    else:
        raise ValueError()
