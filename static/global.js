document.addEventListener('DOMContentLoaded',  function() {
    // si el contenido de la página ha cargado, podemos empezar
    // este archivo contiene la lógica del teclado.
    const expressionInput = document.getElementById('expression-input');
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



    // definir campos y botones

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
});
