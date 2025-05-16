document.addEventListener('DOMContentLoaded', function() {
    // si el contenido de la página ha cargado, podemos empezar
    const expressionInput = document.getElementById('expression-input');
    const evaluateButton = document.getElementById('evaluate-button');
    const resultArea = document.getElementById('result-area');
    let prevRes = String;

    // definir campos y botones

    // Función para evaluar la expresión (la lógica que se repite)
    function evaluateExpression() {
        const expression = expressionInput.value;

        // mostrar que se está calculando
        resultArea.textContent = 'Calculando...';
        resultArea.style.color = 'black';

        // fetch envía la expresión al backend python
        fetch('/evaluate', { // /evaluate tiene que estar definido en la app.py
            method: 'POST', // flask usa POST.
            headers: {
                'Content-Type': 'application/json' // avisar que se envía un json
            },

            body: JSON.stringify({ expression: expression , previo: prevRes}) // Convertir el objeto JavaScript a una cadena JSON
        })
        .then(response => {
            // Respuesta cruda del servidor, es necesario revisar, en caso de que hubiera errores en la comunicación.

            if (!response.ok) {
                // si hay error, averiguar cual fue.
                return response.json().then(errorData => {
                    // Contiene el error del backend, o un error genérico.
                    throw new Error(errorData.result);
                });
            }
            // Si la respuesta fue OK, parsear el cuerpo de la respuesta como JSON
            return response.json();
        })
        .then(data => {
            // Manejar los datos recibidos del backend
            if (data.result !== undefined) {
                // Si hay un resultado, mostrarlo
                resultArea.textContent = 'Resultado: ' + data.result;
                prevRes = data.result;
                resultArea.style.color = 'green'; // Opcional: color verde para éxito
            } else if (data.error) {
                 // Si el backend devolvió un error, mostrarlo
                 resultArea.textContent = 'Error: ' + data.error;
                 resultArea.style.color = 'red'; // Opcional: color rojo para errores
            } else {
                 // Manejar un formato de respuesta inesperado
                 resultArea.textContent = 'Error: Formato de respuesta inesperado.';
                 resultArea.style.color = 'red';
            }
        })
        .catch(error => {
            // Capturar y manejar cualquier error durante el proceso fetch (ej. error de red)
            resultArea.textContent = 'Error de comunicación: ' + error.message;
            resultArea.style.color = 'red';
            console.error('Error en fetch:', error); // Registrar el error en la consola para depuración
        });
    }

    // Añadir un 'event listener' al botón de evaluar
    evaluateButton.addEventListener('click', evaluateExpression);

    // Añadir un 'event listener' al campo de entrada para la tecla 'keypress'
    expressionInput.addEventListener('keypress', function(event) {
        // Verificar si la tecla presionada es 'Enter' (código 13)
        if (event.key === 'Enter') {
            // Prevenir el comportamiento por defecto (ej. enviar un formulario si estuviera dentro de uno)
            event.preventDefault();
            // Llamar a la función para evaluar la expresión
            evaluateExpression();
        }
    });
});
