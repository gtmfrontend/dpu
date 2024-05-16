from random import randrange

def gerar_numero(tamanho):
    numero = ''
    for digito in range(tamanho):
        algarismo = randrange(10)
        numero = numero + str(algarismo)
    print('numero: ' + numero)
    return numero

def soma_algarismos(numero):
    soma = 0
    for algarismo in numero:
        soma += int(algarismo)
    print('soma: ' + str(soma))
    if soma % 3 == 0 and soma > 9:
        soma_algarismos(str(soma))



tamanho = randrange(40000000)

num = gerar_numero(tamanho)
soma = soma_algarismos(num)


