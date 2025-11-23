import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry

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
    
def on_imprimir_extrato():
    nome = simpledialog.askstring("Imprimir Extrato", "Digite o nome do cliente:", parent=root)
    
    if not nome:
        return

    texto_extrato = consultar_cliente(nome)

    if texto_extrato is None:
        messagebox.showerror("Erro", f"Cliente '{nome}' não encontrado.")
    else:
        nome_arquivo = f"extrato_{nome}.txt"
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(texto_extrato)
            
            messagebox.showinfo("Sucesso", f"Arquivo '{nome_arquivo}' salvo com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}")

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

def on_registrar_cliente():
    nome = nome_entry.get()
    
    if not nome:
        messagebox.showerror("Erro", "O campo 'Nome' não pode estar vazio.")
        return
    
    if registrar_cliente(nome):
        messagebox.showinfo("Sucesso", f"Cliente '{nome}' registrado!")
        limpar_campos()
    else:
        messagebox.showwarning("Aviso", f"Cliente '{nome}' já está cadastrado.")

def on_registrar_compra():
    nome = nome_entry.get()
    data = data_entry.get()
    valor_str = valor_entry.get()
    
    if not nome or not data or not valor_str:
        messagebox.showerror("Erro", "Preencha todos os campos (Nome, Data, Valor).")
        return

    try:
        valor = float(valor_str)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido! Deve ser um número (ex: 50.50).")
        return
        
    if registrar_compra(nome, data, valor):
        messagebox.showinfo("Sucesso", f"Compra de R$ {valor:.2f} registrada para {nome}!")
        limpar_campos()
    else:
        messagebox.showerror("Erro", f"Cliente '{nome}' não foi encontrado.")

def on_registrar_pagamento():
    nome = nome_entry.get()
    data = data_entry.get()
    valor_str = valor_entry.get()
    
    if not nome or not data or not valor_str:
        messagebox.showerror("Erro", "Preencha todos os campos (Nome, Data, Valor).")
        return
    try:
        valor = float(valor_str)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido! Use números (ex: 50.50).")
        return
        
    if registrar_pagamento(nome, data, valor):
        messagebox.showinfo("Sucesso", f"Pagamento de R$ {valor:.2f} registrado para {nome}!")
        limpar_campos()
    else:
        messagebox.showerror("Erro", f"Cliente '{nome}' não foi encontrado.")

def on_consultar_cliente():
    nome = simpledialog.askstring("Consultar Cliente", "Digite o nome do cliente:", parent=root)
    
    if not nome:
        return
    
    extrato_texto = consultar_cliente(nome)

    if extrato_texto:
        messagebox.showinfo(f"Extrato de {nome}", extrato_texto)
    else:
        messagebox.showerror("Erro", f"Cliente '{nome}' não encontrado.")

def on_mostrar_saldo_total():
    total = mostrar_saldo_total()
    messagebox.showinfo("Saldo Total", f"O saldo devedor total é: R$ {total:.2f}")

def on_apagar_cliente():
    nome = simpledialog.askstring("Apagar Cliente", "Digite o nome do cliente a apagar:", parent=root)
    if not nome:
        return
        
    if messagebox.askyesno("Confirmar", f"Tem certeza que deseja apagar '{nome}'? Esta ação não pode ser desfeita."):
        if apagar_cliente(nome):
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' apagado.")
        else:
            messagebox.showerror("Erro", f"Cliente '{nome}' não encontrado.")

def on_listar_clientes():
    janela_lista = tk.Toplevel()
    janela_lista.title("Gerenciamento de Clientes")
    janela_lista.geometry("400x350")

    frame_lista = ttk.Frame(janela_lista)
    frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

    colunas = ("nome", "saldo")
    tabela = ttk.Treeview(frame_lista, columns=colunas, show="headings")
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tabela.yview)

    tabela.configure(yscrollcommand=scrollbar.set)

    tabela.heading("nome", text="Nome do Cliente")
    tabela.heading("saldo", text="Saldo Devedor")
    tabela.column("nome", minwidth=0, width=200)
    tabela.column("saldo", minwidth=0, width=100)

    scrollbar.pack(side="right", fill="y")
    tabela.pack(side="left", fill="both", expand=True)

    if not clientes:
        tabela.insert("", "end", values=("Nenhum registro", ""))
    else:
        for dados_cliente in clientes.values():
            nome = dados_cliente['nome_exibicao']
            saldo = f"R$ {dados_cliente['saldo_devedor']:.2f}"
            tabela.insert("", "end", values=(nome, saldo))

def limpar_campos():
    nome_entry.delete(0, 'end')
    data_entry.delete(0, 'end')
    valor_entry.delete(0, 'end')
    nome_entry.focus()
root = tk.Tk()
root.title("Caderno de Fiados V1.0")

frame = ttk.Frame(root, padding="10")

nome_label = ttk.Label(frame, text="Nome do Cliente:")
nome_entry = ttk.Entry(frame, width=40)

data_label = ttk.Label(frame, text="Data:")
data_entry = DateEntry(frame, width=37, background='gray', 
                       foreground='white', borderwidth=2, 
                       locale='pt_BR', date_pattern='dd-mm-yyyy')

valor_label = ttk.Label(frame, text="Valor (R$):")
valor_entry = ttk.Entry(frame, width=40)

btn_comprar = ttk.Button(frame, text="Registrar Compra", command=on_registrar_compra)
btn_pagar = ttk.Button(frame, text="Registrar Pagamento", command=on_registrar_pagamento)
btn_registrar = ttk.Button(frame, text="Novo Cliente", command=on_registrar_cliente)
btn_consultar = ttk.Button(frame, text="Extrato", command=on_consultar_cliente)
btn_imprimir = ttk.Button(frame, text="Exportar Extrato", command=on_imprimir_extrato)
btn_listar = ttk.Button(frame, text="Clientes", command=on_listar_clientes)
btn_total = ttk.Button(frame, text="Saldo Total", command=on_mostrar_saldo_total)
btn_apagar = ttk.Button(frame, text="Excluir Cliente", command=on_apagar_cliente)

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
btn_imprimir.grid(row=6, column=2, sticky=(tk.W, tk.E), padx=5, pady=5)

root.mainloop()