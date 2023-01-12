import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine
from tkinter import *
from tkinter import ttk
root = Tk()

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser


try:
    conn = pg.connect(dbname="NomeBanco", user="UsuarioBanco", password="SenhaBanco",port="portaBanco",host="localhost")
    cur = conn.cursor()
    print("Conectado com sucesso")
except:
    print("Erro ao conectar")
records = 0
class Relatorios():

    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c =  canvas.Canvas("cliente.pdf")

        self.codigoRel = self.CodigoEntry.get()
        self.nomeRel = self.NomeEntry.get()
        self.foneRel = self.TelefoneEntry.get()
        self.cidadeRel = self.CidadeEntry.get()

        self.c.setFont("Helvetica-Bold",24)
        self.c.drawString(200, 790, ' Ficha do Cliente')

        self.c.setFont("Helvetica-Bold",18)
        self.c.drawString(50, 700,'Codigo:' + self.codigoRel)
        self.c.drawString(50, 670,'Nome:' + self.nomeRel)
        self.c.drawString(50, 630,'Cidade:' + self.cidadeRel)
        self.c.drawString(50, 600,'Telefone:' + self.foneRel)

        self.c.rect(20, 550,550,5, fill=True, stroke = False)

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Func():
    def Limpar(self):
        self.CodigoEntry.delete(0,END)
        self.NomeEntry.delete(0,END)
        self.CidadeEntry.delete(0,END)
        self.TelefoneEntry.delete(0,END)
    def cadastro2(self):
        try:
            conn = pg.connect(dbname="Datpy", user="postgres", password="32212020",port="5432",host="localhost")
            cur = conn.cursor()
            print("Conectado com sucesso")
        except:
            print("Erro ao conectar")
            records = 0
        cod = self.CodigoEntry.get()
        Nome = self.NomeEntry.get()
        cidade = self.CidadeEntry.get()
        telefone = self.TelefoneEntry.get()
        sql_insert = 'INSERT INTO autenticador(cod,nome,cidade,telefone) values (\'{}\',\'{}\',\'{}\',\'{}\')'.format(cod,Nome,cidade,telefone)
        try:
            cur.execute(sql_insert)
            print("Usuario cadastro com sucesso")
        except:
            print("Usuario já cadastrado")
        conn.commit()
        self.select_lista()
    def excluir(self):
        try:
            codigo = self.CodigoEntry.get()
            sql = 'delete from autenticador where cod = \'{}\''.format(codigo)
            cur.execute(sql)
            conn.commit()
            print("Apagado com sucesso")
        except:
            print("Usuario inexistente")
        self.Limpar()
        self.select_lista()
    def select_lista(self):
        conn = pg.connect(dbname="Datpy", user="postgres", password="32212020",port="5432",host="localhost")
        self.lista_Cli.delete(*self.lista_Cli.get_children())
        lista = cur.execute('''SELECT cod, nome, cidade, telefone FROM autenticador ORDER BY nome ASC;''')
        results = cur.fetchall()
        for i in results:
            self.lista_Cli.insert('',END,values=i)
        conn.commit()
    def Duplo_click(self,event):
        self.Limpar()
        self.lista_Cli.selection()
        for n in self.lista_Cli.selection():
            col1,col2,col3,col4 = self.lista_Cli.item(n, 'values')
            self.CodigoEntry.insert(END, col1)
            self.NomeEntry.insert(END, col2)
            self.CidadeEntry.insert(END, col3)
            self.TelefoneEntry.insert(END, col4) 
    def altera_cli(self):
        codigo = self.CodigoEntry.get()
        Nome = self.NomeEntry.get()
        cidade = self.CidadeEntry.get()
        telefone = self.TelefoneEntry.get()
        sql = cur.execute('''UPDATE autenticador SET nome=\'{}\', cidade=\'{}\', telefone=\'{}\' WHERE cod = \'{}\''''.format(Nome,cidade,telefone,codigo))
        self.select_lista()
    conn.commit()
    def busc_cli(self):
        self.lista_Cli.delete(*self.lista_Cli.get_children())
        self.NomeEntry.insert(END, '%')
        nome = self.NomeEntry.get()
        sql = cur.execute('''SELECT cod,nome,cidade,telefone FROM autenticador WHERE nome LIKE '%s' ORDER BY nome ASC;'''% nome)
        buscanomecli = cur.fetchall()
        for i in buscanomecli:
            self.lista_Cli.insert('',END, values=i)
        self.Limpar()
    conn.commit()

class Funcs1():
    def limpa_tela(self):
        self.CodigoEntry.delete(0,END)
        self.NomeEntry.delete(0,END)
        self.CidadeEntry.delete(0,END)
        self.TelefoneEntry.delete(0,END)
    def Autenticador(self):
        i=1
        conn = pg.connect(dbname="Datpy", user="postgres", password="32212020",port="5432",host="localhost")
        sql = " select * from cad"
        cur.execute(sql)
        records = cur.fetchall()
        usuario = self.UsuarioEntry.get()
        senha = self.SenhaEntry.get()
        for row in records:
            if usuario == row[0] and senha == row[1]: 
                i=0
        if(i==0):
            self.janela2()
        else:
            print("Erro na autenticação")
        conn.commit()
    def cadastro(self):
        usuario = self.UsuarioEntry.get()
        senha = self.SenhaEntry.get()
        sql_insert = 'INSERT INTO cad(usuario,senha) values (\'{}\',\'{}\')'.format(usuario,senha)
        try:
            cur.execute(sql_insert)
            print("Usuario cadastro com sucesso")
        except:
            print("Usuario já cadastrado")
        conn.commit()
class Application(Funcs1,Func,Relatorios):
    def __init__(self):
        self.root = root
        self.janela()
        self.frames_da_tela()
        self.criando_labels()
        self.criando_Entry()
        self.criando_botoes()
        root.mainloop()
    def janela(self):
        self.root.title("Cadastro de Produtos") # titulo da Janela
        self.root.configure(background = 'lightBlue') # Cror de Fundo da janela
        self.root.geometry("388x388") # tamanho da tela inicial
        self.root.resizable(False,False) # responsidade da janela
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd =4, bg='Gray',highlightbackground='white',highlightthickness=3) # criando um frame da tela (Exisem tres formas de chamar os componentes do Tkinter palce pack grid)
        self.frame_1.place(relx=0.02,rely=0.02, relwidth =0.96, relheight = 0.96)
    def criando_labels(self):
        #Criando labek Código
        self.LoginLabel = Label(self.frame_1,text="Login",background="Gray",font=("Arial",25))
        self.LoginLabel.place(relx=0.38,rely=0.05)
        self.NomeLabel = Label(self.frame_1,text="Usuario:",background="Gray",font=("Arial"))
        self.NomeLabel.place(relx=0.08,rely=0.35)
        self.senhaLabel = Label(self.frame_1,text="Senha:",background="Gray",font=("Arial"))
        self.senhaLabel.place(relx=0.08,rely=0.45)
    def criando_Entry(self):
        #Criando entry código
        self.UsuarioEntry = Entry(self.frame_1)
        self.UsuarioEntry.place(relx=0.27,rely=0.35,relwidth=0.55)
        self.SenhaEntry = Entry(self.frame_1,show="*")
        self.SenhaEntry.place(relx=0.27,rely=0.45,relwidth=0.55)
    def criando_botoes(self):
        #Criação do botão LIMPAR 
        self.bt_limpar = Button(self.frame_1,text="Entrar",border=2,bg='white',fg='black',font=('verdana',8,'bold'),command=self.Autenticador)
        self.bt_limpar.place(relx=0.27,rely=0.65,relwidth=0.2,relheight=0.10)
    def janela2(self):
            self.root1 = Toplevel()
            self.root1.transient(self.root)
            self.root1.focus_force()
            self.root1.grab_set()
            self.tela2()
            self.frames_da_tela2()
            self.criando_botoes2()
            self.criando_Entry2()
            self.criando_labels2()
            self.lista_frame22()
            self.select_lista()
            self.Menus()
            self.root1.mainloop()
    def tela2(self):
            self.root1.title("Cadastro de Produtos") # titulo da Janela
            self.root1.configure(background = 'lightBlue') # Cror de Fundo da janela
            self.root1.geometry("788x588") # tamanho da tela inicial
            self.root1.resizable(True,True) # responsidade da janela
            self.root1.wm_maxsize(width = 900, height=700) # limite maximo do tamanho da tela
            self.root1.wm_minsize(width = 500, height=400) #limite minimo
    def frames_da_tela2(self):
            self.frame_1 = Frame(self.root1, bd =4, bg='Gray',highlightbackground='white',highlightthickness=3) # criando um frame da tela (Exisem tres formas de chamar os componentes do Tkinter palce pack grid)
            self.frame_1.place(relx=0.02,rely=0.02, relwidth =0.96, relheight = 0.46)
            self.frame_2 = Frame(self.root1, bd =4, bg='Gray',highlightbackground='white',highlightthickness=3) # criando um frame da tela (Exisem tres formas de chamar os componentes do Tkinter palce pack grid)
            self.frame_2.place(relx=0.02,rely=0.5, relwidth =0.96, relheight = 0.46)
    def criando_botoes2(self):
            #Criação do botão LIMPAR 
            self.bt_limpar = Button(self.frame_1,text="Limpar",border=2,bg='white',fg='black',font=('verdana',8,'bold'),command=self.Limpar)
            self.bt_limpar.place(relx=0.2,rely=0.1,relwidth=0.1,relheight=0.15)
            #Criação do botão BUSCAR
            self.bt_buscar = Button(self.frame_1,text="Buscar",border=2,bg='white',fg='black',font=('verdana',8,'bold'),command=self.busc_cli)
            self.bt_buscar.place(relx=0.3,rely=0.1,relwidth=0.1,relheight=0.15)
            #Criação do botão NOVO
            self.bt_buscar = Button(self.frame_1,text="Novo",border=2,bg='white',fg='black',font=('verdana',8,'bold'),command=self.cadastro2)
            self.bt_buscar.place(relx=0.6,rely=0.1,relwidth=0.1,relheight=0.15)
            #Criação do botão ALTERAR
            self.bt_buscar = Button(self.frame_1,text="Alterar",border=2,bg='white',fg='black',font=('verdana',8,'bold'),command=self.altera_cli)
            self.bt_buscar.place(relx=0.7,rely=0.1,relwidth=0.1,relheight=0.15)
            #Criação do botão APAGAR
            self.bt_buscar = Button(self.frame_1,text="Apagar",border=2,bg='white',fg='black',font=('verdana',8,'bold'),command=self.excluir)
            self.bt_buscar.place(relx=0.8,rely=0.1,relwidth=0.1,relheight=0.15)
    def criando_Entry2(self):
            #Criando entry código
            self.CodigoEntry = Entry(self.frame_1)
            self.CodigoEntry.place(relx=0.05,rely=0.15,relwidth=0.08)
            #Criando entry nome
            self.NomeEntry = Entry(self.frame_1)
            self.NomeEntry.place(relx=0.05,rely=0.45,relwidth=0.85)
            #Criando entry Cidade
            self.TelefoneEntry = Entry(self.frame_1)
            self.TelefoneEntry.place(relx=0.5,rely=0.7,relwidth=0.4)
            #Criando entry Telefone
            self.CidadeEntry = Entry(self.frame_1)
            self.CidadeEntry.place(relx=0.05,rely=0.7,relwidth=0.4)
    def criando_labels2(self):
            #Criando labek Código
            self.CodigoLabel = Label(self.frame_1,text="Código",background="Gray")
            self.CodigoLabel.place(relx=0.05,rely=0.05)
            #Criando label Nome
            self.NomeLabel = Label(self.frame_1,text="Nome",background="Gray")
            self.NomeLabel.place(relx=0.05,rely=0.35)
            #Criando label Telefone
            self.TelefoneLabel = Label(self.frame_1,text="Telefone",background="Gray")
            self.TelefoneLabel.place(relx=0.5,rely=0.6)
            #Criando label cidade
            self.CidadeLabel = Label(self.frame_1,text="Cidade",background="Gray")
            self.CidadeLabel.place(relx=0.05,rely=0.6)
    def lista_frame22(self):
            self.lista_Cli = ttk.Treeview(self.frame_2,height=3,column=("col1","col2","col3","col4")) #Criação da visualização dos dados
            #Criando o Cabeçalho da visualização
            self.lista_Cli.heading("#0",text="")
            self.lista_Cli.heading("#1",text="Código")
            self.lista_Cli.heading("#2",text="Nome")
            self.lista_Cli.heading("#3",text="Cidade")
            self.lista_Cli.heading("#4",text="Telefone")

            self.lista_Cli.column("#0",width=1)
            self.lista_Cli.column("#1",width=50)
            self.lista_Cli.column("#2",width=200)
            self.lista_Cli.column("#3",width=125)
            self.lista_Cli.column("#4",width=125)

            self.lista_Cli.place(relx=0.01,rely=0.08, relwidth=0.95, relheight=0.9)

            self.scroolLista = Scrollbar(self.frame_2,orient = 'vertical')
            self.lista_Cli.configure(yscrollcommand= self.scroolLista.set)
            self.scroolLista.place(relx=0.96,rely=0.08,relwidth=0.04,relheight=0.9)
            self.lista_Cli.bind('<Double-1>',self.Duplo_click)
    def Menus(self):
            menubar = Menu(self.root1)
            self.root1.config(menu=menubar)
            filemenu = Menu(menubar)
            filemenu2 = Menu(menubar)

            def Quit(): 
                self.root1.destroy()
                self.UsuarioEntry.delete(0,END)
                self.SenhaEntry.delete(0,END)

            menubar.add_cascade(label = "Opções",menu= filemenu)
            menubar.add_cascade(label="Relatorios",menu = filemenu2)

            filemenu.add_command(label="Voltar", command= Quit)
            filemenu.add_command(label="Cadastrar", command= self.janela3)
            filemenu.add_command(label="Limpa Cliente",command= self.Limpar())
            filemenu2.add_command(label="Ficha do cliente",command= self.geraRelatCliente)
    def janela3(self):
        self.root2 = Toplevel()
        self.root2.transient(self.root1)
        self.root2.focus_force()
        self.root2.grab_set()
        self.tela3()
        self.frames_da_tela3()
        self.criando_labels3()
        self.criando_Entry3()
        self.criando_botoes3()
        self.root2.mainloop()
    def tela3(self):
        self.root2.title("Cadastro de Usuarios") # titulo da Janela
        self.root2.configure(background = 'lightBlue') # Cror de Fundo da janela
        self.root2.geometry("388x388") # tamanho da tela inicial
        self.root2.resizable(False,False) # responsidade da janela
    def frames_da_tela3(self):
        self.frame_1 = Frame(self.root2, bd =4, bg='Gray',highlightbackground='white',highlightthickness=3) # criando um frame da tela (Exisem tres formas de chamar os componentes do Tkinter palce pack grid)
        self.frame_1.place(relx=0.02,rely=0.02, relwidth =0.96, relheight = 0.96)
    def criando_labels3(self):
        #Criando labek Código
        self.LoginLabel = Label(self.frame_1,text="Login",background="Gray",font=("Arial",25))
        self.LoginLabel.place(relx=0.38,rely=0.05)
        self.NomeLabel = Label(self.frame_1,text="Usuario:",background="Gray",font=("Arial"))
        self.NomeLabel.place(relx=0.08,rely=0.35)
        self.senhaLabel = Label(self.frame_1,text="Senha:",background="Gray",font=("Arial"))
        self.senhaLabel.place(relx=0.08,rely=0.45)
    def criando_Entry3(self):
        #Criando entry código
        self.UsuarioEntry = Entry(self.frame_1)
        self.UsuarioEntry.place(relx=0.27,rely=0.35,relwidth=0.55)
        self.SenhaEntry = Entry(self.frame_1,show="*")
        self.SenhaEntry.place(relx=0.27,rely=0.45,relwidth=0.55)
    def criando_botoes3(self):
        #Criação do botão LIMPAR 
        self.bt_limpar = Button(self.frame_1,text="Cadastrar",border=2,bg='white',fg='black',font=('verdana',8,'bold'),command=self.cadastro)
        self.bt_limpar.place(relx=0.27,rely=0.65,relwidth=0.2,relheight=0.10) 
        conn = pg.connect(dbname="Datpy", user="postgres", password="32212020",port="5432",host="localhost")
        conn.commit()      
Application()
