from flask import Flask, render_template, request,jsonify
import logic

app = Flask(__name__)
@app.route("/")
def deploy():
    return render_template('home.html')
@app.route("/evaluate", methods=['POST'])
def eval():
    try:
        # 1. Obtener los datos JSON de la solicitud POST
        data = request.get_json()
        if not data or 'expression' not in data:
            # Si los datos no son JSON válidos o no contienen 'expression'
            return jsonify({"error": "Formato de solicitud inválido. Se espera JSON con 'expression'."}), 400

        expression = data.get('expression')

        if not expression:
            # Si el campo 'expression' está vacío
            return jsonify({"error": "No se proporcionó ninguna expresión para evaluar."}), 400

        # 2. Llamar a tu función de evaluación
        # Asegúrate de que evaluarEcuación maneja sus propios errores internos
        # y devuelve un valor (ej. float) si es exitoso, o None si hay un error
        result = logic.evaluar(expression)

        # 3. Manejar el resultado de la evaluación
        if not (str(result).replace('.','',-1)
                .replace('-','',-1)
                .replace('e','',-1).isdigit()):
            #números en formato matemático pueden contener . - o e. Eliminar todos.
            # Si evaluarEcuación devolvió un texto
            # Devolver el error entregado por el backend
            return jsonify(
                {"result":result}), 400  # Usar 400 Bad Request

        else:
            # Si la evaluación fue exitosa, devolver el resultado como JSON
            return jsonify({"result": result})

    except Exception as e:
        # Capturar cualquier otra excepción inesperada durante el manejo de la solicitud
        print(f"Error inesperado en /evaluate: {e}")  # Log the error on the server side
        return jsonify(
            {"error": f"Ocurrió un error interno del servidor: {str(e)}"}), 500  # Usar 500 Internal Server Error

