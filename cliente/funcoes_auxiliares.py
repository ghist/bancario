def v_int(valor):
    try:
        valor = int(valor)
    except ValueError:
        return None

    else:
        if valor > -1:
            return valor
        else:
            return None


def v_float(valor):
    try:
        valor = float(valor)
    except ValueError:
        return None

    else:
        if valor > -1:
            return valor
        else:
            return None


def trata_data(data):
    data = data.split('/')
    data = f"{data[2]}/{data[1]}/{data[0]}"

    return data

def valida_cpf(cpf):
    if cpf.isdigit() == True and len(cpf) == 11:
        return True

    elif len(cpf) == 14:

        if cpf[3] == '.' and cpf[7] == '.' and cpf[11] == '-':
            aux = cpf.replace('.', '')
            aux = aux.replace('-', '')
            if aux.isdigit():
                return True

    return False


def trata_mensagen(operacao):
    transacao = operacao.split(',')

    return transacao

def concatenar_operacao(operacao):
    trasacao = ''

    for i in operacao:
        trasacao+= str(i) + ','

    return trasacao






