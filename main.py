menu = """
---------------------------------------------
[d] depositar
[s] sacar
[e] extrato
[q] sair
---------------------------------------------

Digite a opção desejada: """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)    

    if opcao == 'd':
        valor = float(input('Digite o valor a ser depositado: '))
        if valor <= 0:
            print(f'\n--- Valor inválido')
            continue
        else:
            saldo += valor
            extrato.append(f'Depósito de R$ {valor:.2f}')

    elif opcao == 's':
        if numero_saques < LIMITE_SAQUES:
            valor = float(input('Digite o valor a ser sacado: '))
            if valor <= 0:
                print(f'\n--- Valor inválido')
                continue
            elif valor > 500:
                print(f'\n--- Valor máximo para saque é de R$ 500')
                continue
            elif valor > saldo:
                print(f'\n--- Saldo insuficiente')
                continue
            else:
                saldo -= valor
                extrato.append(f'Saque de R$ {valor:.2f}')
                numero_saques += 1
        else:
            print('Limite de saques atingido. seu limite é de 3 saques por dia')

    elif opcao == 'e':
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
        
    elif opcao == 'q':
        break

    else:
        print(f'\n--- Opção inválida')
