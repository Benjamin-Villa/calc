math_const = {"e", 'π', 'ans', 'x'}

bin_op = {'+': 1, '-': 1, '*': 3, '/': 3, '#': 2, '%': 2, '^': 4, 'log': 4}
fun = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh', 'exp', 'log', 'ln', '°'}

def tokenizar(input):

    clean = input.lower().replace(' ', '')
    print("ECUACION: ", clean)
    tokens = []
    new = ''
    for char in clean:
        print("check: ",char)
        if diferente_tipo(new, char) == 1:
            #caso 1: añadir la cadena y el nuevo
            if new:
                tokens.append(new)
                print("NUEVO TOKEN: ", new)
            if char:
                tokens.append(char)
                print("NUEVO TOKEN: ", char)
            new = ''
        elif diferente_tipo(new, char) == 2:
            #caso 2: concatenar nuevo con cadena
            new += char
        elif diferente_tipo(new, char) == 3:
            #caso 3: multiplicación implícita
            tokens.append(new)
            tokens.append('*')
            tokens.append(char)
            print("NUEVO TOKEN: multiplicacion entre: ", new, " * ",char)
        elif diferente_tipo(new, char) == 4:
            tokens.append(new)
            print("NUEVO TOKEN: ", new)
            new = char

    tokens.append(new)
    print("NUEVO TOKEN: ", new)

    return tokens

def diferente_tipo(cadena,comp):
    #Explicación de output
    # retornar 1 implica añadir la cadena creada y añadir el nuevo char.
    # retornar 2 concatena el nuevo caracter a la cadena
    # retornar 3 implica que existe multiplicación implicita entre el token creado y el nuevo caracter
    # retornar 4 significa añadir el nuevo token, y empezar a construir otro a base del char
    if comp in bin_op :
        return 1
    if cadena == '':
        return 2


    if comp == ')':
        return 1
    if comp =='(':
        if cadena.isdecimal() or cadena in math_const or cadena == ')':
            return 3
        return 1
    if comp.isspace():
        return 0
    if cadena in math_const:
        return 1
    if comp == '°':
        return 1
    if cadena.isalpha():
        if comp.isalpha():
            return 2
        return 1
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


