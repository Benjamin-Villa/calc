import math

constanteMatematica = {"e", 'π', 'ans'}

operadorBinario = {'+': 1, '-': 1, '*': 3, '/': 3, '#': 2, '%': 2, '^': 4, 'log': 4}
funcionesUnitarias = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'exp', 'ln','°'}


def tokenizar(ecuacion):
    tokens = []
    numero = ""
    print("ECUACION A TOKENIZAR: " + ecuacion)
    for char in ecuacion:
        print("ANALIZANDO " + char)
        if char.isdigit() or char == '.':
            # Es o número entero o decimal
            if numero.isalnum() and not numero.isdigit() :
                # Si no se estaba construyendo número, añadir token y reiniciar num

                tokens.append(numero)
                print("NUEVO TOKEN: " + numero)

                if tokens:
                    if tokens[-1] == ')':
                        # en caso de multiplicacion implicita con parentesis
                        print("Multiplicación implícita detectada, agregando *")
                        tokens.append('*')
                        print("NUEVO TOKEN: *")


                numero = ""
            elif '.' in numero and char == '.':
                # se estaba construyendo numero, pero el numero ya contiene decimal
                tokens.append(numero)
                tokens.append('*')


                # hay dos números, uno al lado del otro, se trata de multiplicación
                print("NUEVO TOKEN: " + numero)
                print("Multiplicación implícita detectada, agregando *")
                print("NUEVO TOKEN: *")
                numero = "0"
            numero += char
        elif char in ['e','π']: # números especiales
            if numero:  # Si ya tenía un token, añadirlo y reiniciar
                tokens.append(numero)
                print("NUEVO TOKEN: " + numero)

                if numero not in funcionesUnitarias:
                    print("Multiplicación implícita detectada, agregando *")
                    print("NUEVO TOKEN: *")
                    tokens.append('*')

            numero = ""
            tokens.append(char)



        elif char in operadorBinario:
            # Operador binario
            if numero:  # Si ya tenía un token, añadirlo y reiniciar
                tokens.append(numero)
                print("NUEVO TOKEN: " + numero)
                numero = ""
            tokens.append(char)
            print("NUEVO TOKEN: " + char)
        elif char.isspace():
            # Espacio significa reiniciar
            if numero:
                tokens.append(numero)
                print("NUEVO TOKEN: " + numero)
                numero = ""
        elif char.isalpha():
            #Encuentro letra
            if numero.isdigit() or numero.count('.') == 1:
                # si estaba haciendo un número, añadir a token y reiniciar
                tokens.append(numero)
                print("NUEVO TOKEN: " + numero)
                print("Multiplicación implícita detectada, agregando *")
                tokens.append('*')
                numero = ""

            if tokens:
                if tokens[-1] == ')' or tokens[-1] :
                    #en caso de multiplicacion implicita con parentesis
                    tokens.append('*')
                    print("NUEVO TOKEN: *")


            numero += char
        elif char in {"(", ")"}:
            # Paréntesis
            if numero:  # Si estaba haciendo algo, guardarlo y reiniciar.
                tokens.append(numero)
                print("NUEVO TOKEN: " + numero)

                if (tokens[-1] not in operadorBinario  and tokens[-1] not in funcionesUnitarias
                        and tokens[-1] != '(' and char == '('):
                    #si el último token es un número adyacente al paréntesis, o se trata de una función compuesta.
                    #se trata de multiplicación implícita.
                    tokens.append('*')
                    print("NUEVO TOKEN: *")

                numero = ""
            tokens.append(char)
            print("NUEVO TOKEN: " + char)
        elif char == '°':
            #conversor rads a grados
            if numero:  # Si estaba haciendo algo, guardarlo y reiniciar.
                tokens.append(numero)
                print("NUEVO TOKEN: " + numero)
                numero = ""
            tokens.append('°')
            print("NUEVO TOKEN: °")

        else:
            # Ignorar otros caracteres.
            pass

    # Añadir token al final
    if numero:
        if tokens:
            if tokens[-1] == ')':
                tokens.append('*')
                print("NUEVO TOKEN: *")

        tokens.append(numero)
        print("NUEVO TOKEN: " + numero)
    print(f"TOKENS FINALES: {tokens}")
    return tokens


def polaca_inversa(input):

    if not input:
        return "EV"
    tokens = tokenizar(input)
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


def evaluar(input, previo):
    print("EVALUANDO: " + input)
    tokens = polaca_inversa(input)
    if not tokens:  # si no sale nada de los tokens
        return "Expresión no debe ser nula"

    if tokens == "EP":
        return "Error de paréntesis"
    elif tokens == "EV":
        return "Expresión no debe ser vacía"

    pila = []  # Stack for evaluation

    for token in tokens:  # Iterate through RPN tokens, NOT the original input string
        if token.replace('.', '', 1).isdigit() or token in constanteMatematica:
            if token == 'π':
                token = math.pi
            elif token == 'e':
                token = math.e
            elif token == 'ans':
                if not previo:
                    return "Error: No hay resultado Previo"
                else:
                    token = previo
            # If the token is a number, push it as a float onto the evaluation stack
            print("NUEVO VALOR: " + str(token))
            pila.append(float(token))  # Corrected: Convert to float
        elif token in funcionesUnitarias:
            # If the token is a unary function
            if not pila:
                return "Error de sintaxis"
            arg = pila.pop()
            if arg == "e":
                arg = math.e
            elif arg == "pi":
                arg = math.pi
            arg = float(arg)
            try:
                # Ensure argument is a float before passing to math functions
                if token == 'sin':
                    pila.append(math.sin(arg))
                elif token == 'cos':
                    pila.append(math.cos(arg))
                elif token == 'tan':
                    pila.append(math.tan(arg))
                elif token == 'asin':
                    if arg > 1 or arg < -1:
                        return "error de dominio para asin"
                    pila.append(math.asin(arg))
                elif token == 'acos':
                    if arg > 1 or arg < -1:
                        return "error de dominio para acos"
                    pila.append(math.acos(arg))
                elif token == 'atan':
                    pila.append(math.atan(arg))
                elif token == 'exp':
                    pila.append(math.exp(arg))
                elif token == 'ln':
                    if arg <= 0:
                        return "Error de dominio para ln"
                    pila.append(math.log(arg))
                elif token == '°':
                    #convertir grados a rads
                    pila.append(arg*math.pi/180)
                else:
                    return "Error, función no reconocida: " + str(arg)
            except ValueError as e:
                print(f"Error evaluando función {token} con argumento {str(arg)}: {e}")
                return None

        elif token in operadorBinario:
            # If the token is a binary operator
            if len(pila) < 2 and token in {'+', '-'}:
                arg = float(pila.pop())
                if token == '-':
                    arg = arg * -1
                pila.append(arg)
            elif len(pila) < 2 and token not in {'+', '-'}:
                return "Error de sintaxis"
            else:

                # Pop the two top elements (order matters for subtraction and division)
                arg2 = float(pila.pop())
                arg1 = float(pila.pop())
                try:
                    # Ensure arguments are floats before performing operations
                    if token == '+':
                        pila.append(arg1 + arg2)
                    elif token == '-':
                        pila.append(arg1 - arg2)
                    elif token == '*':
                        pila.append(arg1 * arg2)
                    elif token == '/':
                        if arg2 == 0:
                            return "Error, división por cero"
                        pila.append(arg1 / arg2)
                    elif token == '^':
                        if (arg2 ** -1) % 2 == 0 and arg1 < 0:  # si la potencia se trata de una raíz par
                            return "Error, raíz par de un número negativo."

                        pila.append(arg1 ** arg2)
                    elif token == '%':
                        if arg2 == 0:
                            return "Error, Módulo por cero"
                        pila.append(arg1 % arg2)
                    elif token == '#':  # Integer division
                        if arg2 == 0:
                            return "Error, división entera por cero"
                        pila.append(math.floor(arg1 / arg2))
                except ValueError as e:
                    return "Error evaluando operador " + token + " con argumentos " + str(arg1) + " op " + str(
                        arg2) + "e"

    # After processing all RPN tokens, the result should be the only element left on the stack
    # Moved this check OUTSIDE the for loop
    if len(pila) == 1:
        print("RESULTADO = " + str(pila[0]))
        return str(pila[0])
    else:
        # This indicates an issue with the RPN conversion or input
        return "Error: Expresión inválida"
