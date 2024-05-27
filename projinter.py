# Aluna: Nayane da Silva Costa;
# Aluna do 4° período de Análise e Desenvolvimento de Sistemas do Centro Universitário de
# João Pessoa - Unipê ;
# Projeto Interdisciplinar - Implementação de uma calculadora de despesas utilizando a linguagem
# de programação Python para o script e MySQL para conexão com o banco de dados
# Última modificação: 13/05/2024;

import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
from tkinter import simpledialog
import mysql.connector


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de despesas")

        self.label_boas_vindas = tk.Label(self.root, text="Seja bem-vindo à nossa calculadora de despesas!", padx=20, font=("Neue Helvetica", 15))
        self.label_boas_vindas.pack()

        self.espaco = tk.Label(self.root, text="")
        self.espaco.pack()

        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()

        self.login_button = tk.Button(self.frame_botoes, text="Login", command=self.abrir_janela_login,font=("Lucida Sans", 15), foreground="white", bg="green")
        self.login_button.pack(side=tk.LEFT, padx=5)

        self.cadastrar_button = tk.Button(self.frame_botoes, text="Cadastre-se", command=self.abrir_janela_cadastro, font=("Lucida Sans", 15), foreground="white", bg="green")
        self.cadastrar_button.pack(side=tk.LEFT, padx=5)

    def abrir_janela_login(self):
        self.root.withdraw()
        root = tk.Tk()
        login_window = LoginWindow(root)
        login_window.on_login_sucesso = self.abrir_janela_calculadora
        root.mainloop()

    def abrir_janela_cadastro(self):
        self.root.withdraw()
        root = tk.Tk()
        CriarUsuarioWindow(root)
        root.mainloop()

    @classmethod
    def abrir_janela_calculadora(cls, usuario):
        root = tk.Tk()
        CalculadoraDespesasWindow(root, usuario)
        root.mainloop()


class CriarUsuarioWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastre-se")

        tk.Label(self.root, text="Novo Usuário:", font=("Neue Helvetica", 13)).grid(row=0, column=0, padx=20, sticky="w")
        self.novo_usuario_entry = tk.Entry(self.root, width=40)
        self.novo_usuario_entry.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(self.root, text="Nova Senha:", font=("Neue Helvetica", 13)).grid(row=1, column=0, padx=20, sticky="w")
        self.nova_senha_entry = tk.Entry(self.root, show="*")
        self.nova_senha_entry.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(self.root, text="Salário:", font=("Neue Helvetica", 13)).grid(row=2, column=0, padx=20, sticky="w")
        self.salario_entry = tk.Entry(self.root)
        self.salario_entry.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        criar_usuario_button = tk.Button(self.root, text="Criar Usuário", command=self.criar_usuario, font=("Lucida Sans", 15), foreground="white", bg="green")
        criar_usuario_button.grid(row=3, column=0, columnspan=2, pady=10)

    def criar_usuario(self):
        novo_usuario = self.novo_usuario_entry.get()
        nova_senha = self.nova_senha_entry.get()
        salario = float(self.salario_entry.get())

        if novo_usuario and nova_senha and salario:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="usuarios_despesas"
                )
                cursor = connection.cursor()
                cursor.execute("INSERT INTO usuarios (usuario, senha, salario) VALUES (%s, %s, %s)",
                               (novo_usuario, nova_senha, salario))
                connection.commit()
                messagebox.showinfo("Novo Usuário Criado", "Novo usuário criado com sucesso!")
                self.novo_usuario_entry.delete(0, tk.END)
                self.nova_senha_entry.delete(0, tk.END)
                self.salario_entry.delete(0, tk.END)
                MainWindow.abrir_janela_calculadora(novo_usuario)
            except mysql.connector.Error as error:
                print("Falha ao inserir novo usuário:", error)
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            messagebox.showerror("Erro", "Por favor, insira um usuário, uma senha e um salário.")


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        tk.Label(self.root, text="Usuário:", font=("Neue Helvetica", 13)).grid(row=0, column=0)
        self.usuario_entry = tk.Entry(self.root, width=40)
        self.usuario_entry.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(self.root, text="Senha:", font=("Neue Helvetica", 13)).grid(row=1, column=0)
        self.senha_entry = tk.Entry(self.root, show="*")
        self.senha_entry.grid(row=1, column=1,  padx=20, pady=5, sticky="ew")

        autenticar_button = tk.Button(self.root, text="Autenticar", command=self.autenticar_usuario, font=("Lucida Sans", 15), foreground="white", bg="green")
        autenticar_button.grid(row=2, column=0, columnspan=2, pady=10)

        cadastrar_button = tk.Button(self.root, text="Cadastrar", command=self.ir_para_tela_cadastro, font=("Lucida Sans", 15), foreground="white", bg="green")
        cadastrar_button.grid(row=3, column=0, columnspan=2, pady=10)

        recuperar_senha_button = tk.Button(self.root, text="Esqueci minha senha", command=self.abrir_janela_recuperar_senha, font=("Lucida Sans", 15), foreground="white", bg="green")
        recuperar_senha_button.grid(row=4, column=0, columnspan=2, pady=10)

    def ir_para_tela_cadastro(self):
        self.root.withdraw()
        root = tk.Tk()
        CriarUsuarioWindow(root)
        root.mainloop()

    def abrir_janela_recuperar_senha(self):
        self.root.withdraw()
        root = tk.Tk()
        RecuperarSenhaWindow(root)
        root.mainloop()


    def autenticar_usuario(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usuarios_despesas"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
            user = cursor.fetchone()
            if user:
                messagebox.showinfo("Autenticação bem-sucedida", "Bem-vindo!")
                self.root.destroy()  # Fecha a janela de login
                MainWindow.abrir_janela_calculadora(usuario)  # Abre a janela da calculadora
            else:
                messagebox.showerror("Erro de Autenticação", "Usuário ou senha inválidos.")
        except mysql.connector.Error as error:
            print("Falha na autenticação:", error)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class RecuperarSenhaWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Recuperar Senha")

        tk.Label(self.root, text="Usuário:", font=("Neue Helvetica", 13)).grid(row=0, column=0)
        self.usuario_entry = tk.Entry(self.root, width=40)
        self.usuario_entry.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(self.root, text="Nova Senha:", font=("Neue Helvetica", 13)).grid(row=1, column=0)
        self.nova_senha_entry = tk.Entry(self.root, show="*")
        self.nova_senha_entry.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        recuperar_button = tk.Button(self.root, text="Recuperar Senha", command=self.recuperar_senha, font=("Lucida Sans", 15), foreground="white", bg="green")
        recuperar_button.grid(row=2, column=0, columnspan=2, pady=10)

    def recuperar_senha(self):
        nome_usuario = self.usuario_entry.get()
        nova_senha = self.nova_senha_entry.get()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usuarios-despesas"
            )

            cursor = connection.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (nome_usuario,))
            usuario = cursor.fetchone()

            if usuario:
                cursor.execute("UPDATE usuarios SET senha = %s WHERE usuario = %s", (nova_senha, nome_usuario))
                connection.commit()

                print("Senha redefinida com sucesso.")
            else:
                print("Nome de usuário não encontrado.")

        except mysql.connector.Error as error:
            print("Erro ao recuperar a senha:", error)

        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()
class CalculadoraDespesasWindow:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("Calculadora de Despesas")

        tk.Label(self.root, text="Valor:", font=("Neue Helvetica", 13)).grid(row=0, column=0)
        self.valor_entry = tk.Entry(self.root, width=40)
        self.valor_entry.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(self.root, text="Categoria:", font=("Neue Helvetica", 13)).grid(row=1, column=0)
        self.categorias = ["Alimentação", "Transporte", "Moradia", "Entretenimento"]
        self.categoria_var = tk.StringVar(self.root)
        self.categoria_dropdown = tk.OptionMenu(self.root, self.categoria_var, *self.categorias)
        self.categoria_dropdown.config(font=("Neue Helvetica", 10))
        self.categoria_dropdown.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        tk.Label(self.root, text="Data:", font=("Neue Helvetica", 13)).grid(row=2, column=0)
        self.data_entry = tk.Entry(self.root, width=40)
        self.data_entry.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        adicionar_button = tk.Button(self.root, text="Adicionar Despesa", command=self.adicionar_despesa, font=("Lucida Sans", 10), foreground="white", bg="green")
        adicionar_button.grid(row=3, column=0, columnspan=2, pady=10)

        calcular_button = tk.Button(self.root, text="Calcular Total de Despesas", command=self.calcular_total_despesas, font=("Lucida Sans", 10), foreground="white", bg="green")
        calcular_button.grid(row=4, column=0, columnspan=2, pady=10)

        alterar_salario_button = tk.Button(self.root, text="Alterar Salário", command=self.alterar_salario, font=("Lucida Sans", 10), foreground="white", bg="green")
        alterar_salario_button.grid(row=7, column=0, columnspan=2, pady=10)

        exportar_button = tk.Button(self.root, text="Exportar Despesas para CSV", command=self.exportar_despesas, font=("Lucida Sans", 10), foreground="white", bg="green")
        exportar_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.lista_despesas = tk.Listbox(self.root, width=50, height=10)
        self.lista_despesas.grid(row=6, column=0, columnspan=2)

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usuarios_despesas"
        )
        self.cursor = self.connection.cursor()

    def obter_usuario_id(self, usuario):
        try:
            query = "SELECT id FROM usuarios WHERE usuario = %s"
            self.cursor.execute(query, (usuario,))
            usuario_id = self.cursor.fetchone()[0]
            return usuario_id
        except mysql.connector.Error as error:
            print("Falha ao obter ID do usuário:", error)
            return None

    def adicionar_despesa(self):
        valor = float(self.valor_entry.get())
        categoria = self.categoria_var.get()
        data = self.data_entry.get()
        usuario_id = self.obter_usuario_id(self.usuario)

        if usuario_id is not None:
            self.lista_despesas.insert(tk.END, f"Valor: {valor} | Categoria: {categoria} | Data: {data}")
            self.salvar_despesa(valor, categoria, data, usuario_id)

            self.valor_entry.delete(0, tk.END)
            self.categoria_var.set("")
            self.data_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Falha ao obter ID do usuário.")

    def salvar_despesa(self, valor, categoria, data, usuario_id):
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        try:
            query = "INSERT INTO despesas (valor, categoria, data_compra, usuario_id) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (valor, categoria, data_formatada, usuario_id))
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Falha ao salvar despesa:", error)

    def alterar_salario(self):
        novo_salario = float(tk.simpledialog.askstring("Alterar Salário", "Digite o novo salário:"))

        try:
            query = "UPDATE usuarios SET salario = %s WHERE usuario = %s"
            self.cursor.execute(query, (novo_salario, self.usuario))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Salário alterado com sucesso!")

        except mysql.connector.Error as error:
            print("Erro ao alterar o salário:", error)
            messagebox.showerror("Erro", "Ocorreu um erro ao alterar o salário.")
    def calcular_total_despesas(self):
        usuario = self.usuario
        try:
            self.cursor.execute("SELECT salario FROM usuarios WHERE usuario = %s", (usuario,))
            salario = float(self.cursor.fetchone()[0])
            total_despesas = sum(
                float(despesa.split("Valor: ")[1].split(" |")[0]) for despesa in self.lista_despesas.get(0, tk.END))
            mensagem = f"Total de Despesas: R${total_despesas:.2f}\n"
            if total_despesas <= 0.8 * salario:
                mensagem += "Parabéns! Você economizou 20% do seu salário."
            else:
                mensagem += "Cuidado! Você precisa economizar mais."
            messagebox.showinfo("Total de Despesas", mensagem)
        except mysql.connector.Error as error:
            print("Falha ao calcular despesas:", error)

    def exportar_despesas(self):
        despesas = self.lista_despesas.get(0, tk.END)
        filename = f"despesas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Valor", "Categoria", "Data"])
            for despesa in despesas:
                valor = despesa.split("Valor: ")[1].split(" |")[0]
                categoria = despesa.split("Categoria: ")[1].split(" |")[0]
                data = despesa.split("Data: ")[1]
                writer.writerow([valor, categoria, data])
        messagebox.showinfo("Exportação de Dados", f"As despesas foram exportadas para o arquivo: {filename}")


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()