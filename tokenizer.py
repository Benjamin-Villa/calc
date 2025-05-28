math_const = {"e", 'π', 'ans', 'x'}

bin_op = {'+': 1, '-': 1, '*': 3, '/': 3, '#': 2, '%': 2, '^': 4, 'log': 4}
fun = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh', 'exp', 'log', 'ln', '°'}

def tokenizar(input):
    tokens = []
    new = ''
    for char in input:
        if diferente_tipo(new,char) == 0:
            #caso 0: omitir el nuevo y añadir
            tokens.append(new)
            print("NUEVO TOKEN: " + new)
        if diferente_tipo(new, char) == 1:
            #caso 1: añadir la cadena y el nuevo
            tokens.append(new)
            print("NUEVO TOKEN: ", new)
            tokens.append(new)
            print("NUEVO TOKEN: ", char)
            new = ''
        if diferente_tipo(new, char) == 2:
            #caso 2: concatenar nuevo con cadena
            new += char

    tokens.append(new)
    return tokens

def diferente_tipo(cadena,comp):
    #Explicación de output
    if comp in bin_op :
        return 1
    if comp in {'(',')'}:
        return 1
    if comp.isspace():
        return 0
    if cadena in math_const:
        return 1
    if comp == '°':
        return 1
    if cadena.isalpha():
        if not comp.isalpha():
            return 2
    if cadena.isdigit():
        if comp == '.':
            return 2
        if comp.isdigit():
            return 2
    if cadena.isdecimal():
        if comp.isdigit():
            return 2
    return False



def es_numero(input):
     if input in math_const:
         return True
     if input.replace('.','').isdigit():
         return True
     return False


def polaca_inversa(input):

    if not input:
        return "EV"
    tokens = tokenizar(input)
    if tokens == "ES":
        return "ES"
    print(f"TOKENS DETECTADOS: {tokens}")
    salida = []
    operadores = []  # pila

    def precedencia(op):
        return bin_op.get(op, 0) # Prioridad de operaciones, 0 por defecto

    print(F"CONSTRUCCION NPI DE: {tokens}")

    for token in tokens:
        if token.replace('.', '', -1).isdigit() or token in math_const:
            # Si es un número, sin importar si es decimal
            salida.append(token)
            print("NUEVO VALOR: " + token)
        elif token in fun:
            # Si es función, añadir a la pila
            operadores.append(token)
            print("NUEVA FUNCION: " + token)
        elif token in bin_op:
            # Si tenemos operador
            while (operadores and
                   operadores[-1] != '(' and
                   (precedencia(operadores[-1]) > precedencia(token) or
                    (precedencia(operadores[-1]) == precedencia(
                        token) and token != '^'))):  # Asociatividad, exceptuando potencia
                salida.append(operadores.pop())
            operadores.append(token)
            print('NUEVO OPERADOR: ' + token)
        elif token == '(':
            operadores.append(token)
        elif token == ')':
            while operadores and operadores[-1] != '(':
                salida.append(operadores.pop())
            if operadores and operadores[-1] == '(':
                operadores.pop()
            if operadores and operadores[-1] in fun:
                salida.append(operadores.pop())
            #llevar cuenta de los paréntesis

    # Carrear operadores a la cola
    while operadores:
        # Si quedan paréntesis, está mal la entrada.
        if operadores[-1] == '(':
            return "EP"
        salida.append(operadores.pop())
    print(f"NPI FINAL: {salida}")
    return salida


