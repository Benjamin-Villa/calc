document.addEventListener('DOMContentLoaded', function() {
    // si el contenido de la página ha cargado, podemos empezar
    const expressionInput = document.getElementById('expression-input');
    const evaluateButton = document.getElementById('evaluate-button');
    const resultArea = document.getElementById('result-area');
    const myCheckbox = document.getElementById('shift');


    const botonSin = document.getElementById('sin');
    const botonCos = document.getElementById('cos');
    const botonTan = document.getElementById('tan');
    const botonSinh = document.getElementById('sinh');
    const botonCosh = document.getElementById('cosh');
    const botonTanh = document.getElementById('tanh');
    const labelCheck = document.getElementById('checkLabel');
    const botonLn = document.getElementById('loge');

    const botonDot = document.getElementById('DOT');
    const botonExp = document.getElementById('EXP');

    const botonDel = document.getElementById('DEL');
    const botonAc = document.getElementById('AC');
    const botonesShift = [botonSin,botonTanh,botonSinh,botonCosh,botonTan,botonCos,botonExp,botonDot,botonLn]
    const nombresArc = {'sin':'ArcSin', 'cos':'ArcCos', 'tan':'ArcTan','sinh':'ArcSinH','cosh':'ArcCosH','tanh':'ArcTanH','EXP':'π','DOT':'e','loge':'log10'}
    const altVal = {'sin':'asin()', 'cos':'acos()', 'tan':'atan()','sinh':'asinh()','cosh':'acosh()','tanh':'atanh()','EXP':'π','DOT':'e','loge':'log()'}

    let prevRes = String;

    // definir campos y botones

    expressionInput.
    document.querySelectorAll(".add-text").forEach(button => {
        button.addEventListener("click", () => {
            const text = button.value; // Obtiene el valor del botón
            expressionInput.value += text; // Agrega el texto al campo de texto
            });
        });

    botonAc.addEventListener('click',function (){
        expressionInput.value = '';
    })

    botonDel.addEventListener('click',function (){
        expressionInput.value = expressionInput.value.substring(0,expressionInput.value.length-1)
    })

    myCheckbox.addEventListener('change', function() {
            if (this.checked) {

                console.log('Checkbox marcado');
                labelCheck.style.backgroundColor = '#ff5050';
                labelCheck.style.color = 'white';
                botonesShift.forEach(function(boton) {
                    const botonId = boton.id;
                    boton.style.backgroundColor = '#ff5050';
                    boton.style.color = 'white';
                    if (nombresArc[botonId]) {
                            // Almacenar el texto original en un atributo de datos (data attribute)
                            // para poder restaurarlo fácilmente después
                            if (!boton.dataset.originalText) {
                                boton.dataset.originalText = boton.textContent;
                            }
                            if (!boton.dataset.originalValue) {
                                boton.dataset.originalValue = boton.value;
                            }
                            boton.value = altVal[botonId]
                            boton.textContent = nombresArc[botonId];
                        }
                });
            }else{
                labelCheck.style.backgroundColor = '';
                labelCheck.style.color = '';
                labelCheck.style.border = ''; // Volver a valores por defecto
                botonesShift.forEach(function(boton) {
                                        // Checkbox desmarcado: Restaura los estilos originales
                                        boton.style.backgroundColor = ''; // Restaura al estilo CSS o por defecto
                                        boton.style.color = '';
                                        boton.style.border = '';
                    if (boton.dataset.originalText) {
                            boton.textContent = boton.dataset.originalText;
                    }
                    if (boton.dataset.originalValue) {
                            boton.value = boton.dataset.originalValue;
                    }
                }
            );
    }});

    // Función para evaluar la expresión
    function evaluateExpression() {
        const expression = expressionInput.value;

        resultArea.textContent = 'Calculando...';
        resultArea.style.color = 'black';

        // fetch envía la expresión al backend python
        fetch('/evaluate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // avisar que se envía un json
            },

            body: JSON.stringify({ expression: expression , previo: prevRes}) // Convertir el objeto JavaScript a una cadena JSON
        })
        .then(response => {
            // Respuesta bruta del servidor, es necesario revisar, en caso de que hubiera errores en la comunicación.

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
