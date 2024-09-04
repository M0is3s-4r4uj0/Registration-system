import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
import customtkinter as ctk

class Registro:
    def __init__(self):
        self.conn = sql.connect("Registro_doacao.db")
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS sistema_doacao(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT(100) NOT NULL,
        contato TEXT(20) NOT NULL,
        data TEXT(10) NOT NULL,
        doar TEXT(20) NOT NULL,
        observacao TEXT(200) )''')

    def register(self, nome, contato, data, doar, observacao):
        self.c.execute("INSERT INTO sistema_doacao (nome, contato, data, doar, observacao) VALUES (?,?,?,?,?)", (nome, contato, data, doar, observacao))
        self.conn.commit()

    def visualizacao(self):
        self.c.execute("SELECT * FROM sistema_doacao")
        return self.c.fetchall()

    def buscar(self, id):
        self.c.execute("SELECT * FROM sistema_doacao WHERE id=?", (id,))
        return self.c.fetchone()

    def atualizacao(self, id, nome, contato, data, doar, observacao):
        consulta = ("UPDATE sistema_doacao SET nome=?, contato=?, data=?, doar=?, observacao=? WHERE id=?")
        self.c.execute(consulta, (nome, contato, data, doar, observacao, id))
        self.conn.commit()

    def deleta(self, id):
        self.c.execute("DELETE FROM sistema_doacao WHERE id=?", (id,))
        self.conn.commit()

    def exportar_para_excel(self, arquivo):
        dados = self.visualizacao()
        colunas = ['ID', 'Nome', 'Contato', 'Data', 'Doar', 'Observacao']
        df = pd.DataFrame(dados, columns=colunas)
        df.to_excel(arquivo, index=False)
        print(f'Dados exportados para {arquivo}')

    def gerar_relatorio(self):
        dados = self.visualizacao()
        colunas = ['ID', 'Nome', 'Contato', 'Data', 'Doar', 'Observacao']
        df = pd.DataFrame(dados, columns=colunas)
        relatorio = df.describe(include='all')
        print(relatorio)
        return relatorio

    def gerar_graficos(self):
        dados = self.visualizacao()
        colunas = ['ID', 'Nome', 'Contato', 'Data', 'Doar', 'Observacao']
        df = pd.DataFrame(dados, columns=colunas)
        doacao_count = df['Doar'].value_counts()

        plt.figure(figsize=(10, 6))
        plt.bar(doacao_count.index, doacao_count.values)
        plt.xlabel('Tipo de Doação')
        plt.ylabel('Quantidade')
        plt.title('Quantidade de Doações por Tipo')
        plt.show()


class Interface(Registro):
    def __init__(self):
        super().__init__()
        self.janela = Tk()
        self.layoute()

    def layoute(self):
        # Layout
        self.janela.title('Sistema de Registro')
        self.janela.geometry("800x600")
        self.janela.resizable(width=False, height=False)
        self.janela.configure(bg='#151824')

        # Elementos
        janela1 = Frame(self.janela, height=50, width=800, bg='#abf7ff')
        janela1_lb = Label(janela1, text="Sistema de Gerenciamento de Cadastro", font=('Candara', 15), fg='black', bg='#abf7ff')

        # Labels
        avis = Label(self.janela, text='Por favor, preencha todos os campos', bg='#151824', fg='#82160c')
        lb_nome = Label(self.janela, text='Nome do Doador', font=('Century Gothic', 10), fg='white', bg='#151824')
        lb_data = Label(self.janela, text='Data da Doação', font=('Century Gothic', 10), fg='white', bg='#151824')
        lb_contato = Label(self.janela, text='Contato do Doador', font=('Century Gothic', 10), fg='white', bg='#151824')
        lb_doacao = Label(self.janela, text='Doação', font=('Century Gothic', 10), fg='white', bg='#151824')
        lb_obs = Label(self.janela, text='Observação', font=('Century Gothic', 10), fg='white', bg='#151824')

        avis.place(x=120, y=60)
        janela1.grid(row=0, column=0)
        janela1_lb.place(x=90, y=7)

        lb_nome.place(x=10, y=100)
        lb_data.place(x=10, y=130)
        lb_contato.place(x=10, y=160)
        lb_doacao.place(x=10, y=190)
        lb_obs.place(x=10, y=220)

        # Entradas
        self.et_nome = Entry(self.janela, font=('Century Gothic', 10), bg='#9cf6ff', width=50)
        self.et_data = Entry(self.janela, font=('Century Gothic', 10), bg='#9cf6ff', width=50)
        self.et_contato = Entry(self.janela, font=('Century Gothic', 10), bg='#9cf6ff', width=50)
        self.et_doacao = ctk.CTkComboBox(self.janela, values=['Alimento', 'Roupa', 'Higiene', 'Dinheiro', 'Eletrônico'], font=('Century Gothic', 13), button_hover_color='green', button_color='#9cf6ff', width=100, height=20)
        self.et_obs = ctk.CTkTextbox(self.janela, width=355, height=70, font=("Century Gothic", 13), bg_color='#abf7ff')

        self.et_nome.place(x=120, y=100)
        self.et_data.place(x=120, y=130)
        self.et_contato.place(x=120, y=160)
        self.et_doacao.place(x=120, y=190)
        self.et_obs.place(x=120, y=220)

        # Botões
        bt_cadastra = Button(self.janela, text='Cadastrar', fg='black', bg='#abf7ff', activebackground='#044012', command=self.cadastrar)
        bt_expo_excel = Button(self.janela, text='Exportar para excel', fg='black', bg='#abf7ff', activebackground='#044012', command=self.exportar_excel)
        bt_relatorio = Button(self.janela, text='Gerar relatório', fg='black', bg='#abf7ff', activebackground='#044012', command=self.gerar_relatorio)
        bt_visualizar = Button(self.janela, text='Visualizar', fg='black', bg='#abf7ff', activebackground='#044012', command=self.visualizar_dados)
        bt_buscar = Button(self.janela, text='Buscar', fg='black', bg='#abf7ff', activebackground='#044012', command=self.buscar_registro)
        bt_deleta = Button(self.janela, text='Deletar', fg='black', bg='#abf7ff', activebackground='#044012', command=self.deletar_registro)
        bt_atualizacao = Button(self.janela, text='Atualizar', fg='black', bg='#abf7ff', activebackground='#044012', command=self.atualizar_registro)
        bt_grafico = Button(self.janela, text='Gerar Gráfico', fg='black', bg='#abf7ff', activebackground='#044012', command=self.gerar_grafico)

        bt_cadastra.place(x=60, y=300)
        bt_expo_excel.place(x=150, y=300)
        bt_relatorio.place(x=290, y=300)
        bt_buscar.place(x=60, y=350)
        bt_deleta.place(x=150, y=350)
        bt_visualizar.place(x=250, y=350)
        bt_atualizacao.place(x=350, y=350)
        bt_grafico.place(x=450, y=350)

        # Frame para visualização de dados
        self.frame_dados = Frame(self.janela, bg='#151824')
        self.frame_dados.place(x=10, y=400, width=780, height=180)
        self.text_dados = Text(self.frame_dados, bg='#9cf6ff', fg='black', font=('Century Gothic', 10))
        self.text_dados.pack(expand=True, fill=BOTH)

        self.janela.mainloop()

    def limpar_campos(self):
        self.et_nome.delete(0, END)
        self.et_data.delete(0, END)
        self.et_contato.delete(0, END)
        self.et_doacao.set('')
        self.et_obs.delete("1.0", END)

    def cadastrar(self):
        nome = self.et_nome.get()
        contato = self.et_contato.get()
        data = self.et_data.get()
        doar = self.et_doacao.get()
        observacao = self.et_obs.get("1.0", "end-1c")
        self.register(nome, contato, data, doar, observacao)
        self.limpar_campos()
        self.visualizar_dados()

    def buscar_registro(self):
        id = int(self.et_nome.get())
        dados = self.buscar(id)
        if dados:
            self.text_dados.delete("1.0", END)
            self.text_dados.insert(END, f'ID: {dados[0]}, Nome: {dados[1]}, Contato: {dados[2]}, Data: {dados[3]}, Doar: {dados[4]}, Observacao: {dados[5]}\n')
        else:
            self.text_dados.delete("1.0", END)
            self.text_dados.insert(END, "Registro não encontrado\n")

    def atualizar_registro(self):
        id = int(self.et_nome.get())
        nome = self.et_nome.get()
        contato = self.et_contato.get()
        data = self.et_data.get()
        doar = self.et_doacao.get()
        observacao = self.et_obs.get("1.0", "end-1c")
        self.atualizacao(id, nome, contato, data, doar, observacao)
        self.limpar_campos()
        self.visualizar_dados()

    def deletar_registro(self):
        id = int(self.et_nome.get())
        self.deleta(id)
        self.limpar_campos()
        self.visualizar_dados()

    def visualizar_dados(self):
        dados = self.visualizacao()
        self.text_dados.delete("1.0", END)
        for dado in dados:
            self.text_dados.insert(END, f'ID: {dado[0]}, Nome: {dado[1]}, Contato: {dado[2]}, Data: {dado[3]}, Doar: {dado[4]}, Observacao: {dado[5]}\n')

    def exportar_excel(self):
        self.exportar_para_excel('registro_doacao.xlsx')

    def gerar_relatorio(self):
        relatorio = super().gerar_relatorio()
        self.text_dados.delete("1.0", END)
        self.text_dados.insert(END, str(relatorio))

    def gerar_grafico(self):
        self.gerar_graficos()


if __name__ == "__main__":
    Interface()

