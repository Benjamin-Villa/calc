import math
import tokenizer


def evaluar(tokens, previo):
    print(f"EVALUANDO: {tokens}")
    if not tokens:  # si no sale nada de los tokens
        return "Expresión no debe ser nula"

    if tokens == "EP":
        return "Error de paréntesis"
    elif tokens == "ES":
        return "Error de sintaxis"
    elif tokens == "EV":
        return "Expresión no debe ser vacía"

    pila = []  # pila para evaluar notacion polaca

    for token in tokens:
        if token.replace('.', '', 1).isdigit() or token in tokenizer.math_const:
            if token == 'π':
                token = math.pi
            elif token == 'e':
                token = math.e
            elif token == 'ans':
                if not previo:
                    return "Error: No hay resultado Previo"
                else:
                    token = previo
            # Se obtiene valor, empilar como float
            print("NUEVO VALOR: " + str(token))
            pila.append(float(token))
        elif token in tokenizer.fun:
            if not pila:
                return "Error de sintaxis"
            arg = pila.pop()
            if arg == "e":
                arg = math.e
            elif arg == "pi":
                arg = math.pi
            arg = float(arg)
            try:
                if token == 'sin':                                  #sin
                    pila.append(math.sin(arg))
                elif token == 'cos':                                #cos
                    pila.append(math.cos(arg))
                elif token == 'tan':                                #tan
                    pila.append(math.tan(arg))
                elif token == 'asin':                               #asin
                    if arg > 1 or arg < -1:
                        return "error de dominio para ArcSin"
                    pila.append(math.asin(arg))
                elif token == 'acos':                               #acos
                    if arg > 1 or arg < -1:
                        return "error de dominio para ArcCos"
                    pila.append(math.acos(arg))
                elif token == 'atan':                               #atan
                    pila.append(math.atan(arg))
                elif token == 'tanh':                               #tanh
                    pila.append(math.tanh(arg))
                elif token == 'sinh':                               #sinh
                    pila.append(math.sinh(arg))
                elif token == 'cosh':                               #cosh
                    pila.append(math.cosh(arg))
                elif token == 'exp':                                #exp
                    pila.append(math.exp(arg))
                elif token == 'ln':                                 #ln
                    if arg <= 0:
                        return "Error de dominio para ln"
                    pila.append(math.log(arg))
                elif token == '°':                                  #rad
                    #convertir grados a rads
                    pila.append(arg*math.pi/180)
                elif token == 'log':                              #log10
                    if arg <= 0:
                        return "Error de dominio para log"
                    pila.append(math.log10(arg))
                elif token == 'asinh':                              #asinh
                    pila.append(math.asinh(arg))
                elif token == 'acosh':                              #acosh
                    if arg < 1:
                        return "Error de dominio para ArcCosH"
                    pila.append(math.acosh(arg))
                elif token == 'atanh':                              #atanh
                    if arg >= 1 or arg <= -1:
                        return "error de dominio para ArcTanH"
                    pila.append(math.atanh(arg))
                else:
                    return "Error, función no reconocida: " + str(arg)
            except ValueError as e:
                print(f"Error evaluando función {token} con argumento {str(arg)}: {e}")
                return None

        elif token in tokenizer.bin_op:
            if len(pila) < 2 and token in {'+', '-'}:
                arg = float(pila.pop())
                if token == '-':
                    arg = arg * -1
                pila.append(arg)
            elif len(pila) < 2 and token not in {'+', '-'}:
                return "Error de sintaxis"
            else:
                arg2 = float(pila.pop())
                arg1 = float(pila.pop())
                try:
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
                    elif token == '#':
                        if arg2 == 0:
                            return "Error, división entera por cero"
                        pila.append(math.floor(arg1 / arg2))
                except ValueError as e:
                    return "Error evaluando operador " + token + " con argumentos " + str(arg1) + " op " + str(
                        arg2) + "e"

    # Si el proceso es correcto, debería haber un solo elemento en la pila
    if len(pila) == 1:
        print("RESULTADO = " + str(pila[0]))
        return str(pila[0])
    else:
        return "Error: Expresión inválida"

def integrar(tokens,start,end,numero):
    print(f"INTEGRAR: {tokens}" )
    result = float(0.0)
    dx = (float(end)-float(start))/int(numero)
    print('RESOLUCION DX = ' + str(dx))
    for i in range(numero):
        punto_x = float(start) + dx * i
        print(f"||I = {i}")
        print(f"|||PUNTO X = {punto_x}")

        tokens_con_valor = replaceX_devuelve_nueva(tokens, punto_x)

        resultadoDx = float(evaluar(tokens_con_valor,''))*dx
        print("|||RESULTADO PARA = "  + str(resultadoDx))
        result += resultadoDx
    print(f"RESULTADO INTEGRAL: {result}")
    return result


def replaceX_devuelve_nueva(tokens_originales, value):
    nueva_lista = []
    for token in tokens_originales:
        if token == 'x':
            nueva_lista.append(str(value)) # Guardar como string
        else:
            nueva_lista.append(token)
    return nueva_lista

