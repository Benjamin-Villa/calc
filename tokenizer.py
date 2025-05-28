import math

constanteMatematica = {"e", 'π', 'ans','x'}

operadorBinario = {'+': 1, '-': 1, '*': 3, '/': 3, '#': 2, '%': 2, '^': 4, 'log': 4}
funcionesUnitarias = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan','sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh', 'exp','log', 'ln','°'}


def tokenizar(ecuacion):
    tokens = []
    nuevoToken = ""
    print("ECUACION A TOKENIZAR: " + ecuacion)
    for char in ecuacion:
        print("ANALIZANDO " + char)
        if char.isdigit() or char == '.':
            # Es o número entero o decimal
            if nuevoToken.isalnum() and not nuevoToken.isdigit() and nuevoToken not in constanteMatematica: # no incluye parentesis
                # Si nuevo token no se trata de letras, añadir el token a la pila y reiniciar
                # nuevo token se trata definitivamente de una funcion o operador binario.

                if tokens:
                    if tokens[-1] == ')':
                        # en caso de multiplicacion implicita con parentesis
                        print("Multiplicación implícita detectada, agregando *")
                        tokens.append('*')
                        print("NUEVO TOKEN: *")
                # ejemplo: (5)tan1 = (5)*tan1

                tokens.append(nuevoToken)
                print("NUEVO TOKEN: " + nuevoToken)
                nuevoToken = ""

            elif '.' in nuevoToken and char == '.':
                # se estaba construyendo numero, pero el numero ya contiene decimal
                tokens.append(nuevoToken)
                tokens.append('*')


                # hay dos números, uno al lado del otro, se trata de multiplicación
                #ejemplo 5.2.3 = 5.2*0.3
                print("NUEVO TOKEN: " + nuevoToken)
                print("Multiplicación implícita detectada, agregando *")
                print("NUEVO TOKEN: *")
                nuevoToken = "0"
            nuevoToken += char
        elif char in ['e','π']: # números especiales
            if nuevoToken:  # Si ya tenía un token, añadirlo y reiniciar
                tokens.append(nuevoToken)
                print("NUEVO TOKEN: " + nuevoToken)

                if nuevoToken not in funcionesUnitarias or nuevoToken != '(':
                    print("Multiplicación implícita detectada, agregando *")
                    print("NUEVO TOKEN: *")
                    tokens.append('*')

            nuevoToken = ""
            tokens.append(char)



        elif char in operadorBinario:
            # Operador binario
            if nuevoToken:  # Si ya tenía un token, añadirlo y reiniciar
                tokens.append(nuevoToken)
                print("NUEVO TOKEN: " + nuevoToken)
                nuevoToken = ""
            tokens.append(char)
            print("NUEVO TOKEN: " + char)
        elif char.isspace():
            # Espacio significa reiniciar
            if nuevoToken:
                tokens.append(nuevoToken)
                print("NUEVO TOKEN: " + nuevoToken)
                nuevoToken = ""
        elif char.isalpha() and not char.isdigit() or char == '.':
            #Encuentro letra, definitivamente ningun numero
            if nuevoToken.isdigit() or nuevoToken.count('.') == 1:
                # si estaba haciendo un número, añadir a token y reiniciar
                tokens.append(nuevoToken)
                print("NUEVO TOKEN: " + nuevoToken)
                print("Multiplicación implícita detectada, agregando *")
                tokens.append('*')
                nuevoToken = ""

            if tokens:
                if tokens[-1] == ')':
                    #en caso de multiplicacion implicita con parentesis
                    tokens.append('*')
                    print("NUEVO TOKEN: *")


            nuevoToken += char
        elif char in {"(", ")"}:
            # Paréntesis
            if nuevoToken:  # Si estaba haciendo algo, guardarlo y reiniciar.
                tokens.append(nuevoToken)
                print("NUEVO TOKEN: " + nuevoToken)

                if (tokens[-1] not in operadorBinario  and tokens[-1] not in funcionesUnitarias
                        and tokens[-1] != '(' and char == '('):
                    #si el último token es un número adyacente al paréntesis, o se trata de una función compuesta.
                    #se trata de multiplicación implícita.
                    tokens.append('*')
                    print("NUEVO TOKEN: *")

                nuevoToken = ""
            tokens.append(char)
            print("NUEVO TOKEN: " + char)
        elif char == '°':
            #conversor rads a grados
            if nuevoToken:  # Si estaba haciendo algo, guardarlo y reiniciar.
                tokens.append(nuevoToken)
                print("NUEVO TOKEN: " + nuevoToken)
                nuevoToken = ""
            tokens.append('°')
            print("NUEVO TOKEN: °")
        else:
            return "ES"
            pass

    # Añadir token al final
    if nuevoToken:
        if tokens:
            if tokens[-1] == ')':
                tokens.append('*')
                print("NUEVO TOKEN: *")

        tokens.append(nuevoToken)
        print("NUEVO TOKEN: " + nuevoToken)
    print(f"TOKENS FINALES: {tokens}")
    return tokens


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
        return operadorBinario.get(op, 0) # Prioridad de operaciones, 0 por defecto

    print(F"CONSTRUCCION NPI DE: {tokens}")

    for token in tokens:
        if token.replace('.', '', -1).isdigit() or token in constanteMatematica:
            # Si es un número, sin importar si es decimal
            salida.append(token)
            print("NUEVO VALOR: " + token)
        elif token in funcionesUnitarias:
            # Si es función, añadir a la pila
            operadores.append(token)
            print("NUEVA FUNCION: " + token)
        elif token in operadorBinario:
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
            if operadores and operadores[-1] in funcionesUnitarias:
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


