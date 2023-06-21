import tkinter as tk
from tkinter import ttk
import sqlite3
import os

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Nomes")
        self.janela.geometry("1280x720")

        self.lbl_nome = tk.Label(self.janela, text="Nome:")
        self.lbl_nome.grid(column=0, row=0, sticky=tk.W)

        self.entry_nome = tk.Entry(self.janela)
        self.entry_nome.grid(column=0, row=1, sticky=tk.W, pady=10, padx=5)

        self.bnt = tk.Button(self.janela, text="Confirmar", command=self.Confirmar)
        self.bnt.grid(row=2, column=0, sticky=tk.W, pady=10)



        colunas = ["Nome", "Sexo", "Nascimento", "UF", "Nacionalidade", "Mãe", "Pai", "Data de Cadastro"]

        self.tvw = ttk.Treeview(self.janela, columns=colunas, show="headings", height=25)
        self.tvw.grid(column=0, row=3, padx=20)

        for coluna in colunas:
            self.tvw.heading(coluna, text=coluna)

        for cont in range(1, 7):
            if cont != 5 and cont != 6:
                self.tvw.column(colunas[cont], minwidth=0, width=100)
            else:
                self.tvw.column(colunas[cont], minwidth=0, width=200)
  
        self.scr = ttk.Scrollbar(self.janela, command=self.tvw.yview)
        
        self.tvw.configure(yscroll=self.scr.set)
        self.scr.grid(row=3, column=0, sticky=tk.E, padx=21, ipady=236)


        

    # def Banco_insere(self):
        conn = sqlite3.connect('Arquivos_Presos.db')

        self.cursor = conn.cursor()

        comando = f'SELECT Nome, Sexo, Nascimento, UF, Nacionalidade, Mãe, Pai, Data_de_Cadastro FROM Arquivos_Presos'

        self.cursor.execute(comando)

        resultado = self.cursor.fetchall() # ler o banco de dados

        for i in resultado:
            self.tvw.insert('', tk.END, values= (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])) 

        

        self.bnt_Selecionar = tk.Button(self.janela, width=10, height=1, text="Selecionar", command=self.Selecionar)
        self.bnt_Selecionar.grid(column=0, row=4, sticky=tk.E, padx=20, pady=20)

    def Selecionar(self):
        selecionado = self.tvw.selection()
        selec = self.tvw.item(selecionado, 'values')[0]
        print(str(selec))
        selec = f"'{(str(selec))}'"

        comando = f'SELECT Local FROM Arquivos_Presos WHERE Nome == {selec}'

        self.cursor.execute(comando)

        resultado = self.cursor.fetchall() # ler o banco de dados

        resultado = resultado[0][0]

        resultado = str(resultado).replace("/", "\\")

        os.startfile(resultado)

        print(resultado)

    def Confirmar(self):
        Nome = self.entry_nome.get()
        comando = f'SELECT Nome, Sexo, Nascimento, UF, Nacionalidade, Mãe, Pai, Data_de_Cadastro FROM Arquivos_Presos WHERE Nome LIKE "%{Nome}%"'

        self.cursor.execute(comando)

        resultado = self.cursor.fetchall() # ler o banco de dados

        print(resultado)

        for i in self.tvw.get_children():
            self.tvw.delete(i)

        for i in resultado:
            self.tvw.insert('', tk.END, values= (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])) 

janela = tk.Tk()
Tela(janela)
janela.mainloop()




