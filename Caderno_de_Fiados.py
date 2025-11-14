import json
clientes = {}

def registrar_cliente(nome_cliente):

    nome_chave = nome_cliente.lower()

    if nome_chave in clientes:
        print(f"Erro: Cliente '{nome_cliente}' já está cadastrado.")
    else:
        clientes[nome_chave] = {
            "nome_exibicao": nome_cliente,
            "saldo_devedor": 0.0,
            "transacoes": []
        }
        print(f"Cliente '{nome_cliente}' registrado com sucesso!")

    salvar_dados()

def registrar_compra(cliente,data,valor):

    nome_chave = cliente.lower()

    if nome_chave in clientes:

        nova_transacao = {"tipo":"compra","data":data,"valor":valor}

        clientes[nome_chave]['transacoes'].append(nova_transacao)
        clientes[nome_chave]["saldo_devedor"] += valor

        print(f"Compra de R$ {valor} registrada para {clientes[nome_chave]['nome_exibicao']}.")
        print(f"Novo saldo devedor: R$ {clientes[nome_chave]['saldo_devedor']:.2f}")

    else:
        print(f"Erro: '{cliente}' não encontrado!")

    salvar_dados()

def registrar_pagamento(cliente,data,valor):

    nome_chave = cliente.lower()

    if nome_chave in clientes:

        nova_transacao = {"tipo":"pagamento","data":data,"valor":valor}

        clientes[nome_chave]['transacoes'].append(nova_transacao)
        clientes[nome_chave]["saldo_devedor"] -= valor

        print(f"Pagamento de R$ {valor} registrado para {clientes[nome_chave]['nome_exibicao']}.")
        print(f"Novo saldo devedor: R$ {clientes[nome_chave]['saldo_devedor']:.2f}")

    else:
        print(f"Erro: '{cliente}' não encontrado!")

    salvar_dados()

def consultar_cliente(cliente):
    nome_chave = cliente.lower()

    if nome_chave in clientes:
        dados_cliente = clientes[nome_chave]

        print(f"--- Extrato do Cliente: {dados_cliente['nome_exibicao']} ---")
        print(f"Saldo Devedor Atual: R$ {dados_cliente['saldo_devedor']:.2f}")
        print("\n--- Histórico de Transações ---")

        if not dados_cliente['transacoes']:
            print("Nenhuma transação registrada.")
        else:
            for transacao in dados_cliente['transacoes']:
                valor_str = f"R$ {transacao['valor']:.2f}"
                tipo_str = transacao['tipo'].capitalize()

                print(f"  {transacao['data']} | {tipo_str:<10} | {valor_str}")

    else:
        print(f"Erro: Cliente '{cliente}' não encontrado!")

def apagar_cliente(cliente):
    nome_chave = cliente.lower()

    if nome_chave in clientes:
        del clientes[nome_chave]
        print(f"Cliente '{cliente}' apagado com sucesso!")
    else:
        print(f"Cliente '{cliente}' não encontrado!")

    salvar_dados()

def mostrar_saldo_total():
    total_devido = 0
    for cliente in clientes:
        total_devido += clientes[cliente]['saldo_devedor']
    print(f"Saldo total devido: {total_devido:.2f}")

def listar_clientes():

    if not clientes:
        print('Nenhum cliente registrado com sucesso!')
        return

    for dados_cliente in clientes.values():
        print(f"{dados_cliente['nome_exibicao']}: R$ {dados_cliente['saldo_devedor']:.2f}")

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

def main():
    while True:
        print("\n--- CADERNO DE FIADOS (MENU) ---")
        print("1. Registrar Novo Cliente")
        print("2. Registrar Compra")
        print("3. Registrar Pagamento")
        print("4. Consultar Cliente (Extrato)")
        print("5. Listar Clientes (Nome e Saldo)")
        print("6. Apagar Cliente")
        print("7. Ver Saldo Devedor Total")
        print("8. Sair do Programa")
        print("---------------------------------")
        escolha = (input("Escolha uma das opções: "))
        if escolha == '1':
            cliente = input("Informe o nome do cliente: ")
            registrar_cliente(cliente)

        elif escolha == '2':
            cliente = input("Informe o nome do cliente: ")
            data = input("Informe o data de compra: ")
            valor = input("Informe o valor do compra: ")
            try:
                valor = float(valor)
                registrar_compra(cliente, data, valor)
            except ValueError:
                print("Erro: Valor inválido. Deve ser um número (ex: 50.50).")

        elif escolha == '3':
            cliente = input("Informe o nome do cliente: ")
            data = input("Informe o data de pagamento: ")
            valor = input("Informe o valor do pagamento: ")

            try:
                valor = float(valor)
                registrar_pagamento(cliente, data, valor)
            except ValueError:
                print("Erro: Valor inválido. Deve ser um número (ex: 50.50).")

        elif escolha == '4':
            cliente = input("Informe o nome do cliente: ")
            consultar_cliente(cliente)

        elif escolha == '5':
            listar_clientes()

        elif escolha == '6':
            cliente = input("Informe o nome do cliente: ")
            apagar_cliente(cliente)

        elif escolha == '7':
            mostrar_saldo_total()

        elif escolha == '8':
            break

        else:
            print("Opção invalida. Tente novamente.")

main()