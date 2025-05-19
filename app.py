from flask import Flask, render_template, request,jsonify
import logic

app = Flask(__name__)
@app.route("/")
def deploy():
    return render_template('home.html')
@app.route("/evaluate", methods=['POST'])
def calcular():
    try:
        # 1. Obtener JSON del Frontend
        data = request.get_json()

        if not data or 'expression' not in data:
            # Si hay error
            return jsonify({"error": "Formato de solicitud inválido. Se espera JSON con 'expression'."}), 400

        expression = data.get('expression')
        previo = data.get('previo')

        if not expression:
            # Si el campo 'expression' está vacío
            return jsonify({"error": "No se proporcionó ninguna expresión para evaluar."}), 400

        result = logic.evaluar(expression,previo)

        # 3. Manejar el resultado de la evaluación
        if not (str(result).replace('.','',-1)
                .replace('-','',-1)
                .replace('+', '', -1)
                .replace('e','',-1).isdigit()):
            #números en formato matemático pueden contener ., -, + o e. Eliminar todos.
            # Si evaluarEcuación devolvió un texto
            # Devolver el error entregado por el backend
            return jsonify(
                {"result":result}), 400  # Usar 400 Bad Request

        else:
            # Si la evaluación fue exitosa, devolver el resultado como JSON
            return jsonify({"result": result})

    except Exception as e:
        # Capturar cualquier otra excepción inesperada durante el manejo de la solicitud
        print(f"Error inesperado en /evaluate: {e}")  # manejar error de backend
        return jsonify(
            {"error": f"Ocurrió un error interno del servidor: {str(e)}"}), 500  # Usar 500 Internal Server Error

