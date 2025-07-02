# Gerenciador-de-Vendas
Meu  primeiro projeto em PYthon
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
    win.geometry("380x400")
    win.resizable(False, False)

    # Frame para inputs com padding
    frame = ctk.CTkFrame(win, corner_radius=12)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    campos = {}
    labels = ["Nome", "CPF", "Email", "Telefone"]
    placeholders = [
        "Digite o nome completo",
        "000.000.000-00",
        "email@exemplo.com",
        "(00) 00000-0000"
    ]
    for i, label in enumerate(labels):
        ctk.CTkLabel(frame, text=label, font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(12 if i==0 else 8, 4))
        entry = ctk.CTkEntry(frame, font=("Helvetica", 14))
        entry.pack(fill="x")
        entry.insert(0, placeholders[i])
        def on_focus_in(e, ph=placeholders[i], ent=entry):
            if ent.get() == ph:
                ent.delete(0, "end")
        def on_focus_out(e, ph=placeholders[i], ent=entry):
            if ent.get().strip() == "":
                ent.insert(0, ph)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        campos[label.lower()] = entry

    def salvar_cliente():
        dados = {}
        for campo in campos:
            valor = campos[campo].get().strip()
            # Evita salvar o placeholder como valor
            if valor == placeholders[labels.index(campo.capitalize())]:
                valor = ""
            dados[campo] = valor
        if not all(dados.values()):
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return
        clientes.append(dados)
        salvar_dados()
        win.destroy()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

    btn_salvar = ctk.CTkButton(frame, text="Salvar Cliente", command=salvar_cliente, width=200, height=40, corner_radius=8)
    btn_salvar.pack(pady=25)

def janela_registrar_venda():
    win = ctk.CTkToplevel(janela)
    win.title("Registrar Venda")
    win.geometry("380x360")
    win.resizable(False, False)

    frame = ctk.CTkFrame(win, corner_radius=12)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    labels = ["CPF do Cliente", "Valor da Venda (R$)", "Data (DD/MM/AAAA)"]
    placeholders = ["000.000.000-00", "0.00", "01/01/2025"]
    entradas = []

    for i, label in enumerate(labels):
        ctk.CTkLabel(frame, text=label, font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(12 if i==0 else 8, 4))
        entry = ctk.CTkEntry(frame, font=("Helvetica", 14))
        entry.pack(fill="x")
        entry.insert(0, placeholders[i])

        def on_focus_in(e, ph=placeholders[i], ent=entry):
            if ent.get() == ph:
                ent.delete(0, "end")
        def on_focus_out(e, ph=placeholders[i], ent=entry):
            if ent.get().strip() == "":
                ent.insert(0, ph)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entradas.append(entry)

    def salvar_venda():
        cpf = entradas[0].get().strip()
        valor_str = entradas[1].get().strip()
        data = entradas[2].get().strip()

        # Verifica placeholders
        if cpf == placeholders[0] or valor_str == placeholders[1] or data == placeholders[2]:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        if not cpf or not valor_str or not data:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if not any(c["cpf"] == cpf for c in clientes):
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return

        try:
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return

        vendas.append({"cliente_cpf": cpf, "valor": valor, "data": data})
        salvar_dados()
        win.destroy()
        messagebox.showinfo("Sucesso", "Venda registrada!")

    btn_salvar = ctk.CTkButton(frame, text="Salvar Venda", command=salvar_venda, width=200, height=40, corner_radius=8)
    btn_salvar.pack(pady=25)

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
    win.geometry("380x250")
    win.resizable(False, False)

    frame = ctk.CTkFrame(win, corner_radius=12)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="CPF do Cliente", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(12, 4))
    cpf_entry = ctk.CTkEntry(frame, font=("Helvetica", 14))
    cpf_entry.pack(fill="x")
    cpf_entry.insert(0, "000.000.000-00")

    def on_focus_in(e):
        if cpf_entry.get() == "000.000.000-00":
            cpf_entry.delete(0, "end")
    def on_focus_out(e):
        if cpf_entry.get().strip() == "":
            cpf_entry.insert(0, "000.000.000-00")

    cpf_entry.bind("<FocusIn>", on_focus_in)
    cpf_entry.bind("<FocusOut>", on_focus_out)

    def consultar():
        cpf = cpf_entry.get().strip()
        if cpf == "000.000.000-00" or not cpf:
            messagebox.showerror("Erro", "Informe um CPF válido.")
            return
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

    btn_consultar = ctk.CTkButton(frame, text="Consultar", command=consultar, width=200, height=40, corner_radius=8)
    btn_consultar.pack(pady=25)

# ------------------------ Interface principal ------------------------
carregar_dados()

janela = ctk.CTk()
janela.title("Gerenciador de Clientes e Vendas")
janela.geometry("420x540")
janela.resizable(False, False)

titulo = ctk.CTkLabel(janela, text="Menu Principal", font=("Helvetica", 28, "bold"))
titulo.pack(pady=30)

botoes = [
    ("Cadastrar Cliente", janela_cadastro_cliente),
    ("Registrar Venda", janela_registrar_venda),
    ("Listar Clientes", listar_clientes),
    ("Listar Vendas", listar_vendas),
    ("Vendas por Cliente", vendas_por_cliente),
    ("Sair", janela.destroy)
]

for texto, comando in botoes:
    btn = ctk.CTkButton(
        janela, text=texto, width=300, height=50,
        command=comando, corner_radius=12,
        font=("Helvetica", 16, "bold")
    )
    btn.pack(pady=12)

janela.mainloop()
