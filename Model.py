import math # Import math for function evaluation (optional, but good practice if you were to evaluate)

# Define precedence for binary operators
# Higher number means higher precedence
operadorBinario = {'+': 1, '-': 1, '*': 3, '/': 3, '#': 2, '%':2, '^': 4}
# Set of unary function names
funcionesUnitarias = {'sin','cos','tan','asin','acos','atan','exp','ln'}

def tokenizar(ecuacion):
    tokens = []
    numero = ""
    i = 0
    for char in ecuacion:
        if char.isdigit() or char == '.':
            # Es o número entero o decimal
            if numero.isalnum() and not numero.isdigit():
                 # Si no se estaba construyendo número, añadir token y reiniciar num
                 tokens.append(numero)
                 numero = ""
            numero += char
        elif char in operadorBinario:
            # Operador binario
            if numero: # Si ya tenía un token, añadirlo y reiniciar
                tokens.append(numero)
                numero = ""
            tokens.append(char)
        elif char.isspace():
            # Espacio significa reiniciar
            if numero:
                tokens.append(numero)
                numero = ""
        elif char.isalpha():
            #Encuentro letra
            if numero.isdigit() or numero.count('.') == 1:
                 # si estaba haciendo un número, añadir a token y reiniciar
                 tokens.append(numero)
                 numero = ""
            numero += char
        elif char in {"(", ")"}:
            # Paréntesis
            if numero: # Si estaba haciendo algo, guardarlo y reiniciar.
                tokens.append(numero)
                numero = ""
            tokens.append(char)
        else:
            # Ignorar otros caracteres.
            pass

    # Añadir token al final
    if numero:
        tokens.append(numero)

    return tokens


def polaca_inversa(input):
    tokens = tokenizar(input)
    salida = []
    operadores = [] # pila

    def precedencia(op):
        return operadorBinario.get(op, 0) # Get precedence, default to 0 for non-binary ops

    for token in tokens:
        if token.replace('.', '', -1).isdigit():
            # Si es un número, sin importar si es decimal
            salida.append(token)
        elif token in funcionesUnitarias:
            # Si es función, añadir a la pila
            operadores.append(token)
        elif token in operadorBinario:
            # Si tenemos operador
            while (operadores and
                   operadores[-1] != '(' and
                   (precedencia(operadores[-1]) > precedencia(token) or
                    (precedencia(operadores[-1]) == precedencia(token) and token != '^'))): # Left-associativity except for power
                salida.append(operadores.pop())
            operadores.append(token)
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
            print("Error: Paréntesis")
            return []
        salida.append(operadores.pop())

    return salida

def evaluarEcuación(input):
    tokens = polaca_inversa(input) # Get RPN tokens
    if not tokens: # Handle error from polaca_inversa
        return None

    pila = [] # Stack for evaluation

    for token in tokens: # Iterate through RPN tokens, NOT the original input string
        if token.replace('.', '', 1).isdigit():
            # If the token is a number, push it as a float onto the evaluation stack
            pila.append(float(token)) # Corrected: Convert to float
        elif token in funcionesUnitarias:
            # If the token is a unary function
            if not pila:
                print(f"Error: No hay suficientes argumentos para la función {token}")
                return None
            arg = pila.pop()
            try:
                # Ensure argument is a float before passing to math functions
                if token == 'sin':
                    pila.append(math.sin(float(arg)))
                elif token == 'cos':
                    pila.append(math.cos(float(arg)))
                elif token == 'tan':
                    pila.append(math.tan(float(arg)))
                elif token == 'asin':
                    pila.append(math.asin(float(arg)))
                elif token == 'acos':
                    pila.append(math.acos(float(arg)))
                elif token == 'atan':
                    pila.append(math.atan(float(arg)))
                elif token == 'exp':
                    pila.append(math.exp(float(arg)))
                elif token == 'ln':
                    if float(arg) <= 0:
                         print("Error: Dominio inválido para ln (el argumento debe ser > 0)")
                         return None
                    pila.append(math.log(float(arg)))
                else:
                    print(f"Error: Función no soportada: {token}")
                    return None
            except ValueError as e:
                 print(f"Error evaluando función {token} con argumento {arg}: {e}")
                 return None

        elif token in operadorBinario:
            # If the token is a binary operator
            if len(pila) < 2:
                print(f"Error: No hay suficientes argumentos para el operador {token}")
                return None
            # Pop the two top elements (order matters for subtraction and division)
            arg2 = pila.pop()
            arg1 = pila.pop()

            try:
                # Ensure arguments are floats before performing operations
                if token == '+':
                    pila.append(float(arg1) + float(arg2))
                elif token == '-':
                        pila.append(float(arg1) - float(arg2))
                elif token == '*':
                        pila.append(float(arg1) * float(arg2))
                elif token == '/':
                    if float(arg2) == 0:
                        print("Error: División por cero")
                        return None
                    pila.append(float(arg1) / float(arg2))
                elif token == '^':
                    pila.append(float(arg1) ** float(arg2))
                elif token == '%':
                    if float(arg2) == 0:
                        print("Error: Módulo por cero")
                        return None
                    pila.append(float(arg1) % float(arg2))
                elif token == '#':  # Integer division
                    if float(arg2) == 0:
                        print("Error: División entera por cero")
                        return None
                    pila.append(math.floor(float(arg1) / float(arg2)))
            except ValueError as e:
                print(f"Error evaluando operador {token} con argumentos {arg1}, {arg2}: {e}")
                return None


    # After processing all RPN tokens, the result should be the only element left on the stack
    # Moved this check OUTSIDE the for loop
    if len(pila) == 1:
        return pila[0]
    else:
        # This indicates an issue with the RPN conversion or input
        print("Error: Expresión inválida o problema de conversión RPN")
        return None