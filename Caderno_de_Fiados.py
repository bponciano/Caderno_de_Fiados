import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
clientes = {}

def registrar_cliente(nome_cliente):
    nome_chave = nome_cliente.lower()
    if nome_chave in clientes:
        return False
    else:
        clientes[nome_chave] = {
            "nome_exibicao": nome_cliente,
            "saldo_devedor": 0.0,
            "transacoes": []
        }
        salvar_dados()
        return True

def registrar_compra(cliente, data, valor):
    nome_chave = cliente.lower()
    if nome_chave in clientes:
        nova_transacao = {"tipo": "compra", "data": data, "valor": valor}
        clientes[nome_chave]['transacoes'].append(nova_transacao)
        clientes[nome_chave]["saldo_devedor"] += valor
        salvar_dados()
        return True
    else:
        return False


def registrar_pagamento(cliente, data, valor):
    nome_chave = cliente.lower()
    if nome_chave in clientes:
        nova_transacao = {"tipo": "pagamento", "data": data, "valor": valor}
        clientes[nome_chave]['transacoes'].append(nova_transacao)
        clientes[nome_chave]["saldo_devedor"] -= valor
        salvar_dados()
        return True
    else:
        return False

def consultar_cliente(cliente):
    nome_chave = cliente.lower()
    if nome_chave in clientes:
        dados_cliente = clientes[nome_chave]
        
        extrato = f"--- Extrato do Cliente: {dados_cliente['nome_exibicao']} ---\n"
        extrato += f"Saldo Devedor Atual: R$ {dados_cliente['saldo_devedor']:.2f}\n"
        extrato += "\n--- Histórico de Transações ---\n"

        if not dados_cliente['transacoes']:
            extrato += "Nenhuma transação registrada."
        else:
            for transacao in dados_cliente['transacoes']:
                valor_str = f"R$ {transacao['valor']:.2f}"
                tipo_str = transacao['tipo'].capitalize()
                extrato += f"  {transacao['data']} | {tipo_str:<10} | {valor_str}\n"
        
        return extrato
    else:
        return None

def apagar_cliente(cliente):
    nome_chave = cliente.lower()
    if nome_chave in clientes:
        del clientes[nome_chave]
        salvar_dados()
        return True
    else:
        return False

def mostrar_saldo_total():
    total_devido = 0
    for dados in clientes.values():
        total_devido += dados['saldo_devedor']
    return total_devido

def listar_clientes():
    if not clientes:
        return "Nenhum cliente registrado."
    
    lista_texto = "--- Lista de Clientes e Saldos ---\n"
    for dados_cliente in clientes.values():
        lista_texto += f"{dados_cliente['nome_exibicao']}: R$ {dados_cliente['saldo_devedor']:.2f}\n"
    return lista_texto

def carregar_dados():
    try:
        with open('dados.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Criando um novo.")
        return {}

def salvar_dados():

    with open('dados.json', 'w', encoding='utf-8') as f:
        json.dump(clientes, f, indent=2, ensure_ascii=False)

clientes = carregar_dados()

root = tk.Tk()
root.title("Caderno de Fiados v1.0")
root.title("Caderno de Fiados v1.0")

frame = ttk.Frame(root, padding="10")

nome_label = ttk.Label(frame, text="Nome do Cliente:")
nome_entry = ttk.Entry(frame, width=40)

data_label = ttk.Label(frame, text="Data (DD-MM-AAAA):")
data_entry = ttk.Entry(frame, width=40)

valor_label = ttk.Label(frame, text="Valor (R$):")
valor_entry = ttk.Entry(frame, width=40)

btn_comprar = ttk.Button(frame, text="Registrar Compra")
btn_pagar = ttk.Button(frame, text="Registrar Pagamento")
btn_registrar = ttk.Button(frame, text="Registrar Novo Cliente")
btn_consultar = ttk.Button(frame, text="Consultar Extrato")
btn_listar = ttk.Button(frame, text="Listar Clientes")
btn_total = ttk.Button(frame, text="Ver Saldo Total")
btn_apagar = ttk.Button(frame, text="Apagar Cliente")

frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

nome_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
nome_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

data_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
data_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

valor_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
valor_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

btn_comprar.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=10)
btn_pagar.grid(row=3, column=2, sticky=(tk.W, tk.E), padx=5, pady=10)

ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, columnspan=3, sticky='ew', pady=10)

btn_registrar.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
btn_consultar.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
btn_listar.grid(row=5, column=2, sticky=(tk.W, tk.E), padx=5, pady=5)

btn_apagar.grid(row=6, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
btn_total.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

root.mainloop()