import customtkinter as ctk
from tkinter import messagebox
import json
import os

# Ativa tema escuro ou claro
ctk.set_appearance_mode("dark")  # "light" ou "dark"
ctk.set_default_color_theme("blue")

clientes = []
vendas = []

def salvar_dados():
    with open("clientes.json", "w") as f:
        json.dump(clientes, f, indent=4)
    with open("vendas.json", "w") as f:
        json.dump(vendas, f, indent=4)

def carregar_dados():
    global clientes, vendas
    if os.path.exists("clientes.json"):
        with open("clientes.json", "r") as f:
            clientes[:] = json.load(f)
    if os.path.exists("vendas.json"):
        with open("vendas.json", "r") as f:
            vendas[:] = json.load(f)

def janela_cadastro_cliente():
    win = ctk.CTkToplevel(janela)
    win.title("Cadastrar Cliente")
    win.geometry("300x350")

    campos = {}
    labels = ["Nome", "CPF", "Email", "Telefone"]
    for i, label in enumerate(labels):
        ctk.CTkLabel(win, text=label).pack(pady=(10 if i == 0 else 5, 2))
        entry = ctk.CTkEntry(win)
        entry.pack()
        campos[label.lower()] = entry

    def salvar_cliente():
        dados = {campo: campos[campo].get().strip() for campo in campos}
        if not all(dados.values()):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        clientes.append(dados)
        salvar_dados()
        win.destroy()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

    ctk.CTkButton(win, text="Salvar", command=salvar_cliente).pack(pady=20)

def janela_registrar_venda():
    win = ctk.CTkToplevel(janela)
    win.title("Registrar Venda")
    win.geometry("300x300")

    ctk.CTkLabel(win, text="CPF do Cliente").pack(pady=5)
    cpf_entry = ctk.CTkEntry(win)
    cpf_entry.pack()

    ctk.CTkLabel(win, text="Valor da Venda (R$)").pack(pady=5)
    valor_entry = ctk.CTkEntry(win)
    valor_entry.pack()

    ctk.CTkLabel(win, text="Data (DD/MM/AAAA)").pack(pady=5)
    data_entry = ctk.CTkEntry(win)
    data_entry.pack()

    def salvar_venda():
        cpf = cpf_entry.get().strip()
        valor_str = valor_entry.get().strip()
        data = data_entry.get().strip()

        if not cpf or not valor_str or not data:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if not any(c["cpf"] == cpf for c in clientes):
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return

        try:
            valor = float(valor_str)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        vendas.append({"cliente_cpf": cpf, "valor": valor, "data": data})
        salvar_dados()
        win.destroy()
        messagebox.showinfo("Sucesso", "Venda registrada!")

    ctk.CTkButton(win, text="Salvar", command=salvar_venda).pack(pady=20)

def listar_clientes():
    if not clientes:
        messagebox.showinfo("Clientes", "Nenhum cliente cadastrado.")
        return
    texto = ""
    for c in clientes:
        texto += f"Nome: {c['nome']}\nCPF: {c['cpf']}\nEmail: {c['email']}\nTelefone: {c['telefone']}\n\n"
    messagebox.showinfo("Clientes Cadastrados", texto)

def listar_vendas():
    if not vendas:
        messagebox.showinfo("Vendas", "Nenhuma venda registrada.")
        return
    texto = ""
    for v in vendas:
        texto += f"CPF Cliente: {v['cliente_cpf']}\nValor: R$ {v['valor']:.2f}\nData: {v['data']}\n\n"
    messagebox.showinfo("Vendas Registradas", texto)

def vendas_por_cliente():
    win = ctk.CTkToplevel(janela)
    win.title("Vendas por Cliente")
    win.geometry("300x200")

    ctk.CTkLabel(win, text="CPF do Cliente").pack(pady=5)
    cpf_entry = ctk.CTkEntry(win)
    cpf_entry.pack()

    def consultar():
        cpf = cpf_entry.get().strip()
        vendas_cliente = [v for v in vendas if v["cliente_cpf"] == cpf]
        if not vendas_cliente:
            messagebox.showinfo("Vendas", "Nenhuma venda para este CPF.")
            return

        texto = ""
        total = 0
        for v in vendas_cliente:
            texto += f"Valor: R$ {v['valor']:.2f} | Data: {v['data']}\n"
            total += v['valor']
        texto += f"\nTotal: R$ {total:.2f}"
        messagebox.showinfo(f"Vendas de {cpf}", texto)
        win.destroy()

    ctk.CTkButton(win, text="Consultar", command=consultar).pack(pady=20)

# ------------------------ Interface principal ------------------------
carregar_dados()

janela = ctk.CTk()
janela.title("Gerenciador de Clientes e Vendas")
janela.geometry("400x500")

ctk.CTkLabel(janela, text="Menu Principal", font=("Helvetica", 22, "bold")).pack(pady=20)

botoes = [
    ("Cadastrar Cliente", janela_cadastro_cliente),
    ("Registrar Venda", janela_registrar_venda),
    ("Listar Clientes", listar_clientes),
    ("Listar Vendas", listar_vendas),
    ("Vendas por Cliente", vendas_por_cliente),
    ("Sair", janela.destroy)
]

for texto, comando in botoes:
    ctk.CTkButton(janela, text=texto, width=250, height=40, command=comando).pack(pady=10)

janela.mainloop()
