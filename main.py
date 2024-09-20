import textwrap

def menu():
    menu = """
        -----------------MENU------------------------
        [d]\tdepositar
        [s]\tsacar
        [e]\textrato
        [nc]\tnovo conta
        [lc]\tlistar contas
        [nu]\tnovo usuario
        [q]\tsair
        ---------------------------------------------

        Digite a opção desejada: """
    
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    
    if valor <= 0:
        print(f'\n--- Valor inválido')
    else:
        saldo += valor
        extrato.append(f'Depósito:\t\t R$ {valor:.2f}')
        print(f'\n--- Depósito realizado com sucesso')
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    if numero_saques > LIMITE_SAQUES:
        print('--- Limite de saques atingido. seu limite é de 3 saques por dia')

    elif valor <= 0:
        print(f'\n--- Valor inválido')
    
    elif valor > limite:
        print(f'\n--- Valor máximo para saque é de R$ {limite:.2f}')
    
    elif valor > saldo:
        print(f'\n--- Saldo insuficiente')
    
    else:
        saldo -= valor
        extrato.append(f'Saque:\t\tR$ {valor:.2f}')
        numero_saques += 1
        print(f'\n--- Saque realizado com sucesso')
        

    return saldo, extrato

def extrato(saldo, /, *, extrato):
    print(f'\n---------------------------------------------')
    print('Extrato')
    print('---------------------------------------------')
    if len(extrato) == 0:
        print('Nenhuma transação realizada')
    else:
        for item in extrato:
            print(item)
    print('---------------------------------------------')
    print(f'Saldo: R$ {saldo:.2f}')
    print(f'---------------------------------------------\n')
    
def criar_usuario(usuarios):
    cpf = input('Digite o CPF do usuário (somente números): ')
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print('--- Usuário já cadastrado')
        return
    
    nome = input('Digite o nome do usuário: ')
    data_nascimento = input('Digite a data de nascimento do usuário (dd/mm/aaaa): ')
    endereco = input('Digite o endereço do usuário (logradouro, nº - bairro - cidade/sigla estado): ')
    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})

    print('--- Usuário cadastrado com sucesso')

def filtrar_usuarios(cpf, usuarios):
    usuario = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario[0] if usuario else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Digite o CPF do usuário (somente números): ')
    usuario = filtrar_usuarios(cpf, usuarios)

    if not usuario:
        print('--- Usuário não encontrado')
        return
    
    print('--- Conta criada com sucesso')
    return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

def listar_contas(contas):
    for conta in contas:
        linha = f'''
            -------------------------------------------------
            Agência: \t\t{conta["agencia"]}
            Número da conta: \t{conta["numero_conta"]}
            Nome do usuário: \t{conta["usuario"]["nome"]}
        '''
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input('Digite o valor a ser depositado: '))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':
            valor = float(input('Digite o valor a ser sacado: '))

            saldo, extrato = sacar(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                numero_saques=numero_saques, 
                LIMITE_SAQUES=LIMITE_SAQUES
            )
            
        elif opcao == 'e':
            extrato(saldo, extrato=extrato)
            
        elif opcao == 'nu':
            criar_usuario(usuarios)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            break

        else:
            print(f'\n--- Opção inválida')


main()