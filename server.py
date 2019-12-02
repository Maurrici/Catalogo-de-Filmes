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

    conexao.close()


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

    serversocket.sendto(listbusca.encode(), address)

    conexao.close()


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


def inserir_favorito():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo Filme
    ids, address = serversocket.recvfrom(2048)
    ids = json.loads(ids.decode())

    # Inserindo Filme aos favoritos
    print(type(ids["idFilme"]), type(ids["idUser"]))
    cursor.execute("INSERT INTO listafavoritos VALUES ('{}', '{}')".format(ids["idUser"], ids["idFilme"]))

    conexao.commit()
    conexao.close()


def excluir_favorito():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo id
    ids, address = serversocket.recvfrom(4000)
    ids = json.loads(ids.decode())

    cursor.execute("DELETE FROM listafavoritos WHERE Filmes_idFilmes = '{}' AND Usuarios_idUsuarios = '{}'".format(
                                                                                        ids["idFilme"], ids["idUser"]))
    conexao.commit()
    conexao.close()


def verificar_favorito():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo ids
    ids, address = serversocket.recvfrom(4000)
    ids = json.loads(ids.decode())

    # Buscando valores
    cursor.execute("SELECT * FROM listafavoritos WHERE Filmes_idFilmes = '{}' AND Usuarios_idUsuarios = '{}'".format(
        ids["idFilme"], ids["idUser"]))

    favorito = cursor.fetchone()
    print(favorito)
    # Enviando resposta
    if None == favorito:
        serversocket.sendto(str(0).encode(), address)
    else:
        serversocket.sendto(str(1).encode(), address)

    conexao.close()


def pegar_comentarios():
    # Estabelecendo conexao com o BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Obtendo id do filme
    idFilme, address = serversocket.recvfrom(1024)
    idFilme = int(idFilme.decode())

    cursor.execute("SELECT * FROM comentarios WHERE Filmes_idFilmes = '{}'".format(idFilme))

    comentarios = cursor.fetchall()

    serversocket.sendto(json.dumps(comentarios).encode(), address)

    conexao.close()


def encontrar_usuario():
    # Estabelecendo conexão com BD
    conexao = pymysql.connect(db="filmesbd", user="root", passwd="")
    cursor = conexao.cursor()

    # Recebendo Busca
    idUser, address = serversocket.recvfrom(1024)
    idUser = int(idUser.decode())

    cursor.execute("SELECT nickName FROM usuarios WHERE idUsuarios = '{}'".format(idUser))

    name = json.dumps(cursor.fetchone())

    serversocket.sendto(name.encode(), address)

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
    # 0 -> Login x
    # 1 -> Catalogo x
    # 2 -> Buscar x
    # 3 -> Inserir Novo filme x
    # 4 -> Inserir na lista de favoritos x
    # 5 -> Inserir Comentário
    # 6 -> Excluir da lista de favoritos x
    # 7 -> Verificar se existe na lista favoritos x
    # 8 -> Encontrar Usúario
    # 9 -> Registro x
    # 10 -> Comentarios
    if op == 0:
        login()

    elif op == 1: # Mostrar todos os Filmes
        catalogo()

    elif op == 2: # Buscar por um filme
        buscar()

    elif op == 3:
        inserir()

    elif op == 4:
        inserir_favorito()

    elif op == 5:
        pass

    elif op == 6:
        excluir_favorito()

    elif op == 7:
        verificar_favorito()

    elif op == 8:
        encontrar_usuario()

    elif op == 9:
        registro()

    elif op == 10:
        pegar_comentarios()