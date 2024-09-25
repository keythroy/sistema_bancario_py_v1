import textwrap
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from datetime import datetime



class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._agencia = '0001'
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def depositar(self, valor):
        if valor <= 0:
            return False, '\n!!! Valor inválido'
        
        self._saldo += valor
        self._historico.registrar(Deposito(valor))
        return True, '\nDepósito realizado com sucesso'

    
    def sacar(self, valor):
        saldo = self._saldo

        if valor <= 0:
            return False, '\n!!! Valor inválido'
        
        if valor > saldo:
            return False, '\n!!! Saldo insuficiente'
        
        self._saldo -= valor
        self._historico.registrar(Saque(valor))
        return True, '\nSaque realizado com sucesso'

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, numero_saques=3):
        super().__init__(numero, cliente)
        self._numero_saques = numero_saques
        self._limite_saques = limite

    def sacar(self, valor):
        
        numero_saques = len(
            [transacao for transacao in self._historico.transacoes if transacao['tipo'] == Saque.__name__]
        )

        if numero_saques > self._numero_saques:
            return False, f'\n!!! Limite de saques atingido. Seu limite é de {self._limite_saques} saques por dia'
        
        if valor > self._limite_saques:
            return False, f'\n!!! Valor máximo para saque é de R$ {self._limite_saques:.2f}'
        
        return super().sacar(valor)
    
    def __str__(self):
        return f"""\n
        -------------------------------------------------
        Agência: \t\t{self._agencia}
        Cliente: \t\t{self._cliente.nome}
        Número da conta: \t{self._numero}
        -------------------------------------------------
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def registrar(self, transacao):
        self._transacoes.append({
            'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @property
    @abstractmethod
    def tipo(self):
        pass    

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    @property
    def tipo(self):
        return self.__class__.__name__
    
    def registrar(self, conta):
        success, msg = conta.depositar(self._valor)

        if not success:
            print("\n!!! Erro ao realizar depósito")

        print(msg)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    @property
    def tipo(self):
        return self.__class__.__name__
    
    def registrar(self, conta):
        success, msg = conta.sacar(self._valor)

        if not success:
            print("\n!!! Erro ao realizar saque")

        print(msg)
        
def menu():
    menu = """
        ----------------- MENU ----------------------
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

def criar_cliente(clientes):
    cpf = input('Digite o CPF: ')
    cliente = filtrar_cliente_por_cpf(clientes, cpf)
    
    if cliente:
        print('\n!!! Cliente já cadastrado !!!')
        return
    
    nome = input('Digite o nome: ')
    data_nascimento = input('Digite a data de nascimento: ')
    endereco = input('Digite o endereço: ')

    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)

    print(f'\nCliente {cliente.nome} cadastrado com sucesso')

def filtrar_cliente_por_cpf(clientes, cpf):
    clientes = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes[0] if clientes else None

def criar_conta(numero, clientes, contas):
    cpf = input('Digite o CPF: ')
    cliente = filtrar_cliente_por_cpf(clientes, cpf)

    if not cliente:
        print('\n!!! Cliente não encontrado !!!')
        return

    conta = ContaCorrente.nova_conta(numero=numero,cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f'\nConta criada com sucesso. Número da conta: {conta.numero}')

def listar_contas(contas):
    if not contas:
        print('\n!!! Nenhuma conta encontrada !!!')
        return

    for conta in contas:
        print(textwrap.dedent(str(conta)))

    
def get_conta_cliente(cliente):
    if not cliente.contas:
        print('\n!!! Cliente não possui conta !!!')
        return 
    
    for conta in cliente.contas:
        print(f"Conta: {conta.numero}")

    numero_conta = input('Digite o número da conta: ')
    
    conta = [conta for conta in cliente.contas if conta.numero == int(numero_conta)]
    
    return conta[0]

def transacao(clientes, tipo):
    cpf = input('Digite o CPF: ')
    cliente = filtrar_cliente_por_cpf(clientes, cpf)

    if not cliente:
        print('\n!!! Cliente não encontrado !!!')
        return

    if tipo == 'd':
        valor = float(input('Digite o valor do depósito: '))
        transacao = Deposito(valor)
    elif tipo == 's':
        valor = float(input('Digite o valor do saque: '))
        transacao = Saque(valor)
    else:
        print('\n!!! Transação inválida !!!')
        return
        

    conta = get_conta_cliente(cliente)
    if not conta:
        print('\n!!! Conta não encontrada !!!')
        return
    
    cliente.realizar_transacao(conta, transacao)

def extrato(clientes):
    cpf = input('Digite o CPF: ')
    cliente = filtrar_cliente_por_cpf(clientes, cpf)

    if not cliente:
        print('\n!!! Cliente não encontrado !!!')
        return

    conta = get_conta_cliente(cliente)
    if not conta:
        print('\n!!! Conta não encontrada !!!')
        return
    
    print("\n---------------- EXTRATO --------------------")
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print('\n!!! Nenhuma transação realizada !!!')
    else:
        for transacao in transacoes:
            print(f"{transacao['data']} - {transacao['tipo']} - {transacao['valor']}")

    print("\n---------------------------------------------")
    print(f"Saldo: R$ {conta.saldo:.2f}") 
    print("\n---------------------------------------------")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            transacao(clientes,'d')

        elif opcao == 's':
            transacao(clientes,'s')
            
        elif opcao == 'e':
            extrato(clientes)
            
        elif opcao == 'nu':
            criar_cliente(clientes)

        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            break

        else:
            print(f'\n--- Opção inválida')


main()