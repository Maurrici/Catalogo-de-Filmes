import socket
import json
import pymysql


def catalogo():
    # with open("catalogo.json", "r") as f:
    #   catalogo = json.load(f)
    #   f.close()

    # Obtendo filmes
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM filmes")

    filmes = cursor.fetchall()

    serversocket.sendto(json.dumps(filmes).encode(), address)


def buscar():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo Busca
    # with open("catalogo.json", "r") as f:
    #   catalogo = json.load(f)
    #   f.close()
    nome, address = serversocket.recvfrom(1024)
    nome = nome.decode()

    # Realizando Busca
    # for movie in catalogo:
    #    if nome.lower() in movie["name"].lower():
    #        listbusca.append(movie)
    cursor.execute("SELECT * FROM filmes WHERE nome LIKE '%{}%'".format(nome))

    listbusca = json.dumps(cursor.fetchall())
    print(listbusca)

    serversocket.sendto(listbusca.encode(), address)


def inserir():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo Filme
    new_movie, address = serversocket.recvfrom(2048)
    new_movie = json.loads(new_movie.decode())
    # with open("catalogo.json", "r") as f:
    #    catalogo = json.load(f)
    #    f.close()
    new_movie["link"] = "images/default.png"
    cursor.execute("SELECT MAX(idFilmes) FROM filmes")
    last_id = cursor.fetchone()
    new_movie["id"] = str(last_id[0] + 1)
    # catalogo.append(new_movie)

    # Inserindo Filme

    cursor.execute("INSERT INTO filmes VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(new_movie["id"],
            new_movie["name"], new_movie["year"], new_movie["genre"], new_movie["duration"], new_movie["resume"],
            new_movie["director"], new_movie["link"]))

    conexao.commit()
    conexao.close()


def excluir():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo id
    id_delete, address = serversocket.recvfrom(4000)
    id_delete = id_delete.decode()
    # with open("catalogo.json", "r") as f:
    #    catalogo = json.load(f)
    #    f.close()

    # for movie in catalogo:
    #    if movie["id"] == id_delete:
    #        catalogo.remove(movie)
    #        break
    # with open("catalogo.json", "w") as f:
    #    json.dump(catalogo, f)
    #    f.close()
    cursor.execute("DELETE FROM filmes WHERE idFilmes = '{}'".format(id_delete))
    conexao.commit()
    conexao.close()


def login():
    # Conexão com Banco de Dados
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Dados do Usuário
    data, address = serversocket.recvfrom(1024)
    data = json.loads(data.decode())

    # Busca SQL
    cursor.execute("SELECT * FROM usuarios WHERE nickName = '{}' AND senha = '{}'".format(data["name"], data["senha"]))
    dados = cursor.fetchone()
    print(dados)
    # Enviando dados
    serversocket.sendto(json.dumps(dados).encode(), address)

    # Fechando conexão com Banco de Dados
    conexao.close()


def registro():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo Novo Usuario
    new_user, address = serversocket.recvfrom(2048)
    new_user = json.loads(new_user.decode())

    # Criando id
    cursor.execute("SELECT MAX(idFilmes) FROM filmes")
    last_id = cursor.fetchone()
    new_user["id"] = str(last_id[0] + 1)

    # Inserindo Usuario
    cursor.execute("INSERT INTO usuarios VALUES ('{}', '{}', '{}', '{}')".format(new_user["id"], new_user["name"],
                                                                                new_user["email"],new_user["senha"]))

    conexao.commit()
    conexao.close()


# Criando Socket para conexão
port = 8000
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.bind(('127.0.0.1',port))
print("Server Status: Running...")
while True:
    data, address = serversocket.recvfrom(1024)
    print("Server connected by {}".format(address))
    op = int(data.decode())
    # 0 -> Login
    # 1 -> Catalogo
    # 2 -> Buscar
    # 3 -> Inserir Novo filme
    # 4 -> Inserir na lista de favoritos
    # 5 -> Excluir
    # 6 -> Excluir da lista de favoritos
    # 7 -> Verificar se existe na lista favoritos
    # 9 -> Registro
    if op == 1: # Mostrar todos os Filmes
        catalogo()

    elif op == 2: # Buscar por um filme
        buscar()

    elif op == 3:
        inserir()

    elif op == 5:
        excluir()

    elif op == 0:
        login()