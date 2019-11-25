import tkinter as tk
import socket
import json


class Application:
    def create():
        window = tk.Tk()
        width_value = window.winfo_screenwidth()
        height_value = window.winfo_screenheight()
        window.geometry("%dx%d+0+0" % (width_value, height_value))
        window["bg"] = "gray15"
        window.title("Atlas Cinéfilo")
        window.iconbitmap("images/icone.ico")
        Application(window)
        window.mainloop()

    def __init__(self, master=None):
        # Variáveis Help
        self.width_value = master.winfo_screenwidth()
        self.height_value = master.winfo_screenheight()
        self.menu_state = 0
        self.catalogo_state = 0
        self.limite = 10
        self.user = {}

        # A1 : Frame que compreende toda a tela
        self.a1 = tk.Frame(master)
        self.a1["width"] = self.width_value
        self.a1["height"] = self.height_value
        self.a1.grid(row=0, column=0)

        # Login
        self.tela_login = tk.Frame(self.a1, width=self.width_value, height=self.height_value, bg="gray15")
        self.tela_login.place(x=0, y=0)

        nick_entry = tk.Entry(self.tela_login, highlightthickness=2, highlightbackground="black", width=20, bg="gray25",
        fg="snow", font=("Small Fonts", "15", "bold"))
        nick_entry.place(x=100, y=100)

        senha_entry = tk.Entry(self.tela_login, highlightthickness=2, highlightbackground="black", width=20, bg="gray25",
        fg="snow", font=("Small Fonts", "15", "bold"))
        senha_entry.place(x=100, y=200)

        login_button = tk.Button(self.tela_login, text="Logar")
        login_button["command"] = lambda: self.autenticar(nick_entry.get(), senha_entry.get())
        login_button.place(x=150, y=300)


        # A2 : Frame que conterá o MENU da Interface
        self.a2 = tk.Frame(self.a1, highlightthickness=2, highlightbackground="black")

        # menu_button : Botão responsável por fazer menu aparecer e desaparecer
        self.menu_button = tk.Button(self.a1, text="MENU  | v |", padx=78, pady=10, fg="snow")

        # Logo do programa
        photo1 = tk.PhotoImage(file="images/logo.png")
        photo1 = photo1.subsample(2, 2)
        self.label_image = tk.Label(self.a2, image=photo1, bg="gray15", highlightbackground="black")
        self.label_image.image = photo1

        # back_button : Buttun que volta ao MENU (Não está inserido na tela cada função deve inseri - lo)
        self.back_button = tk.Button(self.a2, text="<<  Voltar", padx=50, pady=10, fg="snow")

        # A3 : Frame que conterá o título da OPÇÃO
        self.a3 = tk.Frame(self.a1, highlightthickness=2, highlightbackground="black")

        # titulo_label : Label que conterá o titulo da OPÇÃO
        self.titulo_label = tk.Label(self.a3, text="Atlas Cinéfilo", fg="snow", bg="gray15")

        # A4 : Frame que conterá as informações
        self.a4 = tk.Frame(self.a1, highlightthickness=2, highlightbackground="black")

        # Frames Pré Configurados
        self.barra_menu = tk.Frame(self.a2, highlightthickness=2, highlightbackground="black")
        self.filmes_place = tk.Frame(self.a4, highlightthickness=2, highlightbackground="black")

        # Buttons Pré configurados
        self.filme = tk.Button(self.filmes_place)
        self.next_button = tk.Button(self.filmes_place)
        self.back_movie = tk.Button(self.filmes_place)
        self.favorito_button = tk.Button(self.filmes_place)

    def autenticar(self, name, senha):
        # Dicionario Usuario
        user = {}
        user["name"] = name
        user["senha"] = senha

        # Enviando requisição
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        op = 0
        port = 8000
        client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
        client_socket.sendto(json.dumps(user).encode(), ("127.0.0.1", port))

        data, address = client_socket.recvfrom(1024)
        data = json.loads(data.decode())
        if (data == None):
            tk.Label(self.tela_login, text="NickName ou Senha incorretos").place(x=100,y=400)
        else:
            # Dicionário User
            user["id"] = data[0]
            user["name"] = data[1]
            user["email"] = data[2]
            self.user = user
            self.tela_login.destroy()
            self.iniciar()

    def iniciar(self):
        # Elementos de Tela

        # A2 : Frame que conterá o MENU da Interface
        self.a2["width"] = (self.width_value / 5)
        self.a2["height"] = self.height_value
        self.a2["bg"] = "gray15"
        self.a2.place(x=0, y=0)

        # menu_button : Botão responsável por fazer menu aparecer e desaparecer
        self.menu_button["font"] = ("Small Fonts", "13", "bold")
        self.menu_button["command"] = self.menu
        self.menu_button["bg"] = "DodgerBlue2"
        self.menu_button["activebackground"] = "darkred"
        self.menu_button.place(x=5, y=10)

        # Logo do Programa
        self.label_image.place(x=60, y=250)

        # A3 : Frame que conterá o título da OPÇÃO
        self.a3["width"] = self.width_value - (self.width_value / 5)
        self.a3["height"] = (self.height_value / 8)
        self.a3["bg"] = "gray15"
        self.a3.place(x=(self.width_value / 5), y=0)

        # titulo_label : Label que conterá o titulo da OPÇÃO
        self.titulo_label["font"] = ("Small Fonts", "25", "bold")
        self.titulo_label.place(x=10, y=10)

        # A4 : Frame que conterá as informações
        self.a4["width"] = self.width_value - (self.width_value / 5)
        self.a4["height"] = self.height_value - (self.height_value / 8)
        self.a4["bg"] = "gray15"
        self.a4.place(x=(self.width_value / 5), y=(self.height_value / 8))

    # Métodos referentes ao geral
    def menu(self):
        if self.menu_state == 0:
            # Tela MENU
            self.menu_button["text"] = "MENU  | ^ |"
            self.menu_state = 1 # Avisando que o Frame passará a existir
            self.barra_menu = tk.Frame(self.a2, highlightthickness=2, highlightbackground="black")
            self.barra_menu["bg"] = "gray25"
            self.barra_menu["width"] = ((self.width_value/5) - 12)
            self.barra_menu["height"] = (self.height_value - 200)
            self.barra_menu.place(x=5, y=40)

            # Opções MENU
            # filme_button : Botão que levará ao catalogo de filmes
            filme_button = tk.Button(self.barra_menu, text="FILMES", padx=86, pady=5, fg="snow")
            filme_button["font"] = ("Small Fonts", "12", "bold")
            filme_button["command"] = self.catalogo
            filme_button["bg"] = "DodgerBlue2"
            filme_button["activebackground"] = "darkred"
            filme_button.place(x=3, y=30)

            # buscar_button : Botão que levará ao catalogo de filmes
            buscar_button = tk.Button(self.barra_menu, text="BUSCAR UM FILME", padx=34, pady=5, fg="snow")
            buscar_button["font"] = ("Small Fonts", "12", "bold")
            buscar_button["bg"] = "DodgerBlue2"
            buscar_button["command"] = self.buscar
            buscar_button["activebackground"] = "darkred"
            buscar_button.place(x=3, y=80)

            # inserir_button : Botão que levará ao catalogo de filmes
            inserir_button = tk.Button(self.barra_menu, text="INSERIR NOVO FILME", padx=25, pady=5, fg="snow")
            inserir_button["font"] = ("Small Fonts", "12", "bold")
            inserir_button["command"] = self.inserir
            inserir_button["bg"] = "DodgerBlue2"
            inserir_button["activebackground"] = "darkred"
            inserir_button.place(x=3, y=130)

        else:
            self.menu_button["text"] = "MENU  | v |"
            self.menu_state = 0 # Avisando que o Frame passará a não aparecer
            self.barra_menu.destroy()

    def back_menu(self):
        self.titulo_label["text"] = "Atlas Cinéfilo"
        self.filmes_place.destroy()
        self.back_button.destroy()
        self.catalogo_state = 0
        self.limite = 10

    def create_backButton(self):
        self.back_button.destroy()
        self.back_button = tk.Button(self.a2, text="<<  Voltar", padx=50, pady=10, fg="snow")
        self.back_button["font"] = ("Small Fonts", "15", "bold")
        self.back_button["command"] = self.back_menu
        self.back_button["bg"] = "darkred"
        self.back_button["activebackground"] = "DodgerBlue2"
        self.back_button.place(x=5, y=self.height_value - 100)  # Oferecendo opção de voltar

    def create_filmesPlace(self):
        self.filmes_place.destroy()
        self.filmes_place = tk.Frame(self.a4)
        self.filmes_place["width"] = self.width_value - (self.width_value / 5)
        self.filmes_place["height"] = self.height_value - (self.height_value / 8)
        self.filmes_place["bg"] = "gray15"
        self.filmes_place.place(x=0, y=0)

    # Métodos referentes as opções
    def catalogo(self):
        self.titulo_label["text"] = "Filmes"
        # back_button : Buttun que volta ao MENU (Não está inserido na tela cada função deve inseri - lo)
        self.create_backButton()

        # Obtendo catálogo do Servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        op = 1
        port = 8000
        client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
        filmes, address = client_socket.recvfrom(40000)
        filmes = json.loads(filmes.decode())
        # Chamando função que irá criar os botoes
        self.create_button_movie(filmes, self.catalogo_state)

    def create_button_movie(self, lista, state):
        # filmes_place : Frame que contem os filmes
        self.create_filmesPlace()

        # Variáveis Auxiliadoras
        indice = state * 10
        linha_image = 0
        linha_label = 1
        coluna = 0
        filme_label = {}
        lista_exhibition = lista[indice:indice+10]
        for movie in lista_exhibition:
            filme = {}
            filme["id"] = movie[0]
            filme["name"] = movie[1]
            filme["year"] = movie[2]
            filme["genre"] = movie[3]
            filme["duration"] = movie[4]
            filme["resume"] = movie[5]
            filme["director"] = movie[6]
            filme["link"] = movie[7]

            # Imagem do Filme
            photo1 = tk.PhotoImage(file=filme["link"])
            photo1 = photo1.subsample(3, 3)

            self.filme = tk.Button(self.filmes_place, compound=tk.TOP, image=photo1,bg='gray25', fg="snow",
            font=("Small Fonts", "15", "bold"))
            self.filme["command"] = lambda view = filme : self.show_movie(view)
            #self.filme["width"] = 200
            self.filme.grid(row=linha_image, column=coluna)
            self.filme.image = photo1

            # Título do Filme
            filme_label[filme["name"]] = tk.Label(self.filmes_place, text=filme["name"], wraplength=160, bg='gray15',
            font=("Small Fonts", "14", "bold"), fg="snow")
            filme_label[filme["name"]].grid(row=linha_label, column=coluna, sticky=tk.N)

            # Posicionamento dos filmes
            coluna += 1
            if coluna > 4:
                linha_image += 2
                linha_label += 2
                coluna = 0
        # Botões de Paginação
        if len(lista) - self.limite > 0:
            self.next_button.destroy()
            self.next_button = tk.Button(self.filmes_place, text=">>", font=("Small Fonts", "14", "bold"), fg="snow",
            bg="DodgerBlue2")
            self.next_button["command"] = lambda: self.next(lista)
            self.next_button.grid(row=3, column=6)
        else:
            self.next_button.destroy()

        if self.catalogo_state > 0:
            self.back_movie.destroy()
            self.back_movie = tk.Button(self.filmes_place, text="<<", font=("Small Fonts", "14", "bold"), fg="snow",
            bg="DodgerBlue2")
            self.back_movie["command"] = lambda: self.back(lista)
            self.back_movie.grid(row=3, column=5)
        else:
            self.back_movie.destroy()

    def next(self, lista):
        self.catalogo_state += 1
        self.limite += 10
        self.create_button_movie(lista, self.catalogo_state)

    def back(self, lista):
        self.catalogo_state -= 1
        self.limite -= 10
        self.create_button_movie(lista, self.catalogo_state)

    def show_movie(self, filme):
        self.create_filmesPlace()

        # Icone Favoritos
        photo = tk.PhotoImage(file="images/favoritos_false.png")
        self.favorito_button = tk.Button(self.filmes_place, image=photo, bg="gray25")
        self.favorito_button.image = photo
        self.favorito_button["command"] = lambda: self.favoritos(photo["file"], filme["id"])
        self.favorito_button.place(x=1000, y=10)

        #self.verificacao(filme["id"])

        # Imagem do filme
        photo1 = tk.PhotoImage(file=filme["link"])
        photo1 = photo1.subsample(2, 2)
        self.filme = tk.Button(self.filmes_place, compound=tk.TOP, image=photo1, bg='gray25', fg="snow",
        font=("Small Fonts", "15", "bold"))
        self.filme.place(x=20, y=20)
        self.filme.image = photo1

        # Nome do filme
        name_label = tk.Label(self.filmes_place, text="NOME: "+filme["name"], font=("Small Fonts", "14", "bold"),
        bg='gray15', fg="snow")
        name_label.place(x=300, y=50)

        # Ano do filme
        ano_label = tk.Label(self.filmes_place, text="ANO: " + str(filme["year"]), bg='gray15', fg="snow",
        font=("Small Fonts", "14", "bold"))
        ano_label.place(x=300, y=90)

        # Genêro do filme
        genero_label = tk.Label(self.filmes_place, text="GÊNERO: " + filme["genre"],
        font=("Small Fonts", "14", "bold"), bg='gray15', fg="snow")
        genero_label.place(x=300, y=130)

        # Duração do filme
        duration_label = tk.Label(self.filmes_place, text="DURAÇÃO: " + filme["duration"],
        font=("Small Fonts", "14", "bold"), bg='gray15', fg="snow")
        duration_label.place(x=300, y=170)

        #Diretor do filme
        director_label = tk.Label(self.filmes_place, text="DIRETOR: " + filme["director"],
        font=("Small Fonts", "14", "bold"), bg='gray15', fg="snow")
        director_label.place(x=300, y=210)

        # Sinopse do filme
        resume_label = tk.Label(self.filmes_place, text="SINOPSE: " + filme["resume"], wraplength=700, bg='gray15',
        fg="snow", font=("Small Fonts", "14", "bold"))
        resume_label.place(x=20, y=400)

        # Botao de excluir
        excluir_button = tk.Button(self.filmes_place, text="Excluir", padx=50, pady=10, fg="snow")
        excluir_button["font"] = ("Small Fonts", "15", "bold")
        excluir_button["command"] = lambda: self.excluir(filme["id"])
        excluir_button["bg"] = "darkred"
        excluir_button["activebackground"] = "DodgerBlue2"
        excluir_button.place(x=self.width_value - 500, y=self.height_value - 200)

    def verificacao(self, id):
        # Verificar se existe na lista favoritos do usuário
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = 8000
        # Requisição
        op = 7
        client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
        # Enviar Dados
        data = {}
        data["idFilme"] = id
        data["idUser"] = self.user["id"]
        client_socket.sendto(json.dumps(data).encode(), ("127.0.0.1", port))
        resp, address = client_socket.recvfrom(1024)
        if int(resp.decode()) == 1:
            # Alterar aparência do Botão
            photo = tk.PhotoImage(file="images/favoritos_true.png")
            self.favorito_button(self.filmes_place, image=photo)
            self.favorito_button.image = photo

    def favoritos(self, link, id):
        if link == "images/favoritos_false.png":
            # Alterar aparência do Botão
            photo = tk.PhotoImage(file="images/favoritos_true.png")
            self.favorito_button(self.filmes_place, image=photo)
            self.favorito_button.image = photo

            # Adicionar a lista favoritos do usuário
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            port = 8000
            # Requisição
            op = 4
            client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
            # Enviar Dados
            data = {}
            data["idFilme"] = id
            data["idUser"] = self.user["id"]
            client_socket.sendto(json.dumps(data).encode(), ("127.0.0.1", port))
        else:
            # Alterar aparência do Botão
            photo = tk.PhotoImage(file="images/favoritos_false.png")
            self.favorito_button(self.filmes_place, image=photo)
            self.favorito_button.image = photo

            # Remover da lista favoritos do usuário
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            port = 8000
            # Requisição
            op = 6
            client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
            # Enviar Dados
            data = {}
            data["idFilme"] = id
            data["idUser"] = self.user["id"]
            client_socket.sendto(json.dumps(data).encode(), ("127.0.0.1", port))

    def inserir(self):
        self.back_menu()
        self.titulo_label["text"] = "Inserir Filmes"
        # back_button : Buttun que volta ao MENU (Não está inserido na tela cada função deve inseri - lo)
        self.create_backButton()
        # filmes_place : Frame que contem os filmes
        self.create_filmesPlace()
        # Criando caixas de inserção de informações

        # Nome
        nome_label = tk.Label(self.filmes_place, text="Nome do Filme:", font=("Small Fonts", "15", "bold"),
        bg="gray15", fg="snow")
        nome_label.place(x=70, y=100)
        nome_entry = tk.Entry(self.filmes_place, bg="gray25", fg="snow", font=("Small Fonts", "15", "bold"), width=30)
        nome_entry.place(x=265, y=103)

        # Ano
        ano_label = tk.Label(self.filmes_place, text="Ano do Filme:", font=("Small Fonts", "15", "bold"),
        bg="gray15", fg="snow")
        ano_label.place(x=70, y=135)
        ano_entry = tk.Entry(self.filmes_place, bg="gray25", fg="snow", font=("Small Fonts", "15", "bold"), width=30)
        ano_entry.place(x=265, y=138)

        # Genero
        genero_label = tk.Label(self.filmes_place, text="Gênero do Filme:", font=("Small Fonts", "15", "bold"),
        bg="gray15", fg="snow")
        genero_label.place(x=70, y=170)
        genero_entry = tk.Entry(self.filmes_place, bg="gray25", fg="snow", font=("Small Fonts", "15", "bold"), width=30)
        genero_entry.place(x=265, y=173)

        # Duração
        duracao_label = tk.Label(self.filmes_place, text="Duração do Filme:", font=("Small Fonts", "15", "bold"),
        bg="gray15", fg="snow")
        duracao_label.place(x=70, y=205)
        duracao_entry = tk.Entry(self.filmes_place, bg="gray25", fg="snow", font=("Small Fonts", "15", "bold"), width=30)
        duracao_entry.place(x=265, y=208)

        # Diretor
        director_label = tk.Label(self.filmes_place, text="Diretor do Filme:", font=("Small Fonts", "15", "bold"),
        bg="gray15", fg="snow")
        director_label.place(x=70, y=240)
        director_entry = tk.Entry(self.filmes_place, bg="gray25", fg="snow", font=("Small Fonts", "15", "bold"), width=30)
        director_entry.place(x=265, y=243)

        # Resume
        resume_label = tk.Label(self.filmes_place, text="Sinopse do Filme:", font=("Small Fonts", "15", "bold"),
        bg="gray15", fg="snow")
        resume_label.place(x=70, y=275)
        resume_entry = tk.Entry(self.filmes_place, bg="gray25", fg="snow", font=("Small Fonts", "15", "bold"), width=30)
        resume_entry.place(x=265, y=278)

        # Botao de inserir
        inserir_button = tk.Button(self.filmes_place, text="Inserir", padx=50, pady=10, fg="snow")
        inserir_button["font"] = ("Small Fonts", "15", "bold")
        inserir_button["command"] = lambda : self.enviar_filme(nome_entry.get(), ano_entry.get(), genero_entry.get(),
        duracao_entry.get(), resume_entry.get(), director_entry.get())
        inserir_button["bg"] = "DodgerBlue2"
        inserir_button["activebackground"] = "darkred"
        inserir_button.place(x=self.width_value - 500, y=self.height_value - 200)

    def enviar_filme(self, nome, ano, genero, duracao, resume, director):
        if((nome == "") or (ano == "") or (genero == "") or (duracao == "") or (resume == "")):
            # ALERTA
            alerta_label = tk.Label(self.filmes_place, text="Preencha todos os campos e tente novamente",
                                            font=("Small Fonts", "15", "bold"), bg="gray15", fg="darkred")
            alerta_label.place(x=100, y=self.height_value - 400)
        else:
            self.back_menu()
            # Enviando novo filme para o servidor
            movie = {}
            movie["name"] = nome
            movie["year"] = ano
            movie["genre"] = genero
            movie["duration"] = duracao
            movie["resume"] = resume
            movie["director"] = director
            # Obtendo catálogo do Servidor
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            op = 3
            port = 8000
            client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
            movie = json.dumps(movie)
            client_socket.sendto(movie.encode(), ("127.0.0.1", port))

    def buscar(self):
        self.back_menu()
        self.titulo_label["text"] = "Pesquisa"
        # back_button : Buttun que volta ao MENU (Não está inserido na tela cada função deve inseri - lo)
        self.create_backButton()

        # filmes_place : Frame que contem os filmes
        self.create_filmesPlace()

        please = tk.Label(self.filmes_place, text="Digite sua busca: ", fg="snow", bg="gray15")
        please["font"] = ("Small Fonts", "25", "bold")
        please.place(x=10, y=10)

        busca = tk.Entry(self.filmes_place, highlightthickness=2, highlightbackground="black", width=55, bg="gray25",
        fg="snow", font=("Small Fonts", "15", "bold"))
        busca.place(x=210, y=140)

        botão_busca = tk.Button(self.filmes_place, text="Pesquisar", padx=102, pady=10, fg="snow",
        font=("Small Fonts", "15", "bold"))
        botão_busca.place(x=400, y=200)
        botão_busca["bg"] = "DodgerBlue2"
        botão_busca["activebackground"] = "DarkSlateGray4"
        botão_busca["command"] = lambda : self.busca_conexao(busca.get())

    def busca_conexao(self, conteudo):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        op = 2
        port = 8000
        client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
        client_socket.sendto(conteudo.encode(), ("127.0.0.1", port))
        filmes, address = client_socket.recvfrom(40000)
        filmes = json.loads(filmes.decode())
        if filmes == []:
            # filmes_place : Frame que contem os filmes
            self.create_filmesPlace()

            please = tk.Label(self.filmes_place, text="Nenhum filme encontrado no catálogo ", fg="snow", bg="gray15")
            please["font"] = ("Small Fonts", "25", "bold")
            please.place(x=270, y=260)
        else:
            for movie in filmes:
                self.create_button_movie(filmes, self.catalogo_state)

    def excluir(self, id):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        op = 5
        port = 8000
        print(id)
        client_socket.sendto(str(op).encode(), ("127.0.0.1", port))
        client_socket.sendto(str(id).encode(), ("127.0.0.1", port))

        # filmes_place : Frame que contem os filmes
        self.create_filmesPlace()

        info = tk.Label(self.filmes_place, text="Filme deletado do catálogo.", fg="snow", bg="gray15")
        info["font"] = ("Small Fonts", "25", "bold")
        info.place(x=290, y=400)

        # Logo do programa
        photo1 = tk.PhotoImage(file="images/logo.png")
        #photo1 = photo1.subsample(2, 2)
        label_image = tk.Label(self.filmes_place, image=photo1, bg="gray15", highlightbackground="black")
        label_image.image = photo1
        label_image.place(x=370, y=0)
