import PyPDF2
import re
import os


vet = []

colocar_banco = int(input(("Colocar Dados em Banco?: ")))

def Gerar_Dados():


    PDF = os.listdir("pdf")
    with open("Nomes.txt", "w") as arquivo:
        arquivo.write("")

    # print(PDF)

    for pdf in PDF:

        # Abre o arquivo pdf 
        # lembre-se que para o windows você deve usar essa barra -> / 
        # lembre-se também que você precisa colocar o caminho absoluto
        pdf_file = open(f"pdf/{pdf}", 'rb')

        #Faz a leitura usando a biblioteca
        read_pdf = PyPDF2.PdfFileReader(pdf_file)

        # pega o numero de páginas
        number_of_pages = read_pdf.getNumPages()

        #lê a primeira página completa
        page = read_pdf.getPage(0)

        #extrai apenas o texto
        page_content = page.extractText()

        # faz a junção das linhas 
        parsed = ''.join(page_content)

        # print(parsed)

        with open("Nomes.txt", "a") as arquivo:
            arquivo.write("\n")
            arquivo.write(f"Local: Pdfs/{pdf}")
            arquivo.write(parsed)




def cria_Banco():
    import sqlite3

    conn = sqlite3.connect('Arquivos_Presos.db')


    cursor = conn.cursor()



    # criando a tabela (schema)
    cursor.execute(""" CREATE TABLE Arquivos_Presos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            Sexo VARCHAR(9) NOT NULL,
            Nascimento DATE NOT NULL,
            UF VARCHAR(2) NOT NULL,
            Nacionalidade TEXT NOT NULL,
            Mãe TEXT NOT NULL,
            Pai TEXT NOT NULL,
            Data_de_Cadastro DATE NOT NULL,
            Local TEXT NOT NULL
    );
    """)

    print('Tabela criada com sucesso.')
    # desconectando...



def procurar():
    with open("Nomes.txt", "r") as arquivo:
        texto = arquivo.readlines()

    n = 0
    for nome in texto:
        chave = 0
        if "Local:" in nome:
            nome = nome.translate(str.maketrans("", "", "\n"))
            Local = nome[7::]
        if "Nome" in nome: 
            nome = nome.translate(str.maketrans("", "", "\n"))
            Nomec = nome[6::]
            n +=1
        elif "Sexo" in nome:
            nome = nome.translate(str.maketrans("", "", "\n"))
            Sexo = nome.split(" ")
            Nascimento = nome.split(" ")
            try:
                Sexo = Sexo[1]
                if Sexo == "Nascimento:":
                    Sexo = "Não Informado"
            except:
                Sexo = "Não Informado"
            try: 
                if Sexo == "Não Informado":
                    Nascimento = Nascimento[2]
                else:
                    Nascimento = Nascimento[3]
            except:
                Nascimento = "Não Informado"
        elif "UF" in nome:
            nome = nome.translate(str.maketrans("", "", "\n"))
            UF = nome.split(" ")
            try:
                Nacionalidade = UF[3]
            except:
                Nacionalidade = "Não Informado"
            if UF[1] == "Nacionalidade:":
                UF = "Não Informado"
            else:
                # print(UF[1])
                UF = UF[1]
        
        elif "Mãe" in nome:
            nome = nome.translate(str.maketrans("", "", "\n"))
            Mãe = nome[5::]
        elif "Pai" in nome:
            nome = nome.translate(str.maketrans("", "", "\n"))
            try:
                Pai = nome[5::]
            except:
                Pai = "Não Informado"        
        elif "Data de cadastro" in nome:
            nome = nome.translate(str.maketrans("", "", "\n"))
            Data_de_Cadastro = nome[18::]
            chave = 1
        if chave == 1:
            # print(Nomec, Sexo, Nascimento, UF, Nacionalidade, Mãe, Pai, Data_de_Cadastro)
            vet.append(f"{Nomec} - {Sexo} - {Nascimento} - {UF} - {Nacionalidade} - {Mãe} - {Pai} - {Data_de_Cadastro}")
            
            if colocar_banco == 1:
                
                import sqlite3
                conn = sqlite3.connect('Arquivos_Presos.db')
                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO Arquivos_Presos (nome, Sexo, Nascimento, UF, Nacionalidade, Mãe, Pai, Data_de_Cadastro, Local)
                VALUES (?,?,?,?,?,?,?,?,?)
                """, (Nomec, Sexo, Nascimento, UF, Nacionalidade, Mãe, Pai, Data_de_Cadastro, Local))

                conn.commit()

    #print('Dados inseridos com sucesso.')


    #conn.close()


def escreve_para_exel():
    for vetor in vet:
        
        elems = [vetor.split("-")[0], vetor.split("-")[1], vetor.split("-")[2], vetor.split("-")[3], vetor.split("-")[4], vetor.split("-")[5], vetor.split("-")[6], vetor.split("-")[7]]
        texto_a_ser_inserido = ("	".join(elems))
        with open("Dados_Tarauacá.txt", "a", encoding = "UTF-8") as arquivo:
            arquivo.write("\n")
            arquivo.write(texto_a_ser_inserido)





# Gerar_Dados()
# cria_Banco()
procurar()
# escreve_para_exel()
