const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let currentDate = new Date();
let startDate = null; // Fecha de inicio de la selección
let endDate = null; // Fecha de fin de la selección
let clickCount = 0; // Contador de clics
let selectedDaysCount = 0; // Contador de días seleccionados
let selectedDates = []; // Array para almacenar las fechas seleccionadas
let reservas = []; // Declara reservas globalmente
let dateRangeCount = 0;

const updateCalendar = () => {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay();
    const lastDayIndex = lastDay.getDay();
    const monthYearString = currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
    monthYearElement.textContent = monthYearString;
    let datesHTML = '';

    // Días del mes anterior (inactivos)
    for (let i = firstDayIndex; i > 0; i--) {
        datesHTML += `<div class="date inactive">${new Date(currentYear, currentMonth, 0 - i + 1).getDate()}</div>`;
    }

    // Días del mes actual
    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const activeClass = date.toDateString() === new Date().toDateString() ? 'active' : '';
        const selectedClass = (startDate && endDate) && date >= startDate && date <= endDate ? 'selected' : '';
        datesHTML += `<div class="date ${activeClass}" data-date="${i}">${i}</div>`;
    }

    // Días del mes siguiente (inactivos)
    for (let i = 1; i <= 7 - lastDayIndex; i++) {
        datesHTML += `<div class="date inactive">${new Date(currentYear, currentMonth + 1, i).getDate()}</div>`;
    }
    datesElement.innerHTML = datesHTML;

    // Evento de clic en cada fecha
    const dateElements = document.querySelectorAll('.date');
    dateElements.forEach(dateElement => {
        dateElement.addEventListener('click', function() {
            // Verificar si el día es inactivo antes de proceder
            if (!this.classList.contains('inactive')) {
                const selectedDate = new Date(currentYear, currentMonth, this.textContent);
                // Verificar si la fecha seleccionada es hoy o futura
                if (selectedDate >= new Date()) {
                    if (!startDate) {
                        startDate = selectedDate; // Establecer fecha de inicio
                        selectedDates = [startDate];
                    } else if (!endDate) {
                        if (selectedDate >= startDate) {
                            endDate = selectedDate; // Establecer fecha de fin
                            // Agregar el rango de fechas seleccionadas
                            for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
                                selectedDates.push(new Date(d)); // Agregar cada fecha en el rango
                            }
                        } else {
                            // Si se selecciona una fecha anterior a la fecha de inicio, reiniciar la selección
                            startDate = selectedDate;
                            endDate = null;
                            selectedDates = [startDate]; // Reiniciar el array de fechas seleccionadas
                        }
                    } else {
                        // Reiniciar selección si ya hay una fecha de inicio y fin
                        startDate = selectedDate;
                        endDate = null;
                        selectedDates = [startDate]; // Reiniciar el array de fechas seleccionadas
                    }
                    updateSelection(); // Actualizar selección visual
                }
            }
        });
    });
};

function checkAvailability() {
    const alojamientos = document.querySelectorAll('.tar-a');
    
    alojamientos.forEach(alojamiento => {
        // Get the availability dates for this accommodation
        const disponibilidades = JSON.parse(alojamiento.dataset.disponibilidades || '[]');
        
        // Check if selected dates overlap with any unavailable dates
        const isUnavailable = disponibilidades.some(disponibilidad => {
            const startDate = new Date(disponibilidad.fecha_inicio);
            const endDate = new Date(disponibilidad.fecha_fin);
            
            return selectedDates.some(date => 
                date >= startDate && date <= endDate && !disponibilidad.disponible
            );
        });
        
        // Hide accommodation if dates overlap with unavailable dates
        if (isUnavailable) {
            alojamiento.classList.add('hidden');
        } else {
            alojamiento.classList.remove('hidden');
        }
    });
}

// Función para actualizar la selección visual
function updateSelection () {
    const dateElements = document.querySelectorAll('.date');
    dateElements.forEach(dateElement => {
        const dayText = dateElement.textContent;
        const isInactive = dateElement.classList.contains('inactive');
        const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayText);
        dateElement.classList.remove('selected');
        // Solo proceder si el día no es inactivo
        if (!isInactive) {
            // Comprobar si hay una fecha de inicio y fin, y resaltar el rango
            if (startDate && endDate) {
                checkAvailability();
                if (date >= startDate && date <= endDate) {
                    dateElement.classList.add('selected');
                }
            } else if (startDate) {
                // Resaltar solo la fecha de inicio si no hay fin
                if (date.toDateString() === startDate.toDateString()) {
                    dateElement.classList.add('selected');
                }
            }
        }
    });
    updateSelectedDates();
    countSelectedDays(); // Contar días seleccionados después de actualizar la selección
}

// Contar días seleccionados
function countSelectedDays() {
    const selectedDateElements = document.querySelectorAll('.date.selected');
    selectedDaysCount = selectedDateElements.length; // Contar los días seleccionados
    calculateTotalPrice(); // Recalcular el total
}

function updateSelectedDates() {
    const startDateInput = document.getElementById('fecha_inicio');
    const endDateInput = document.getElementById('fecha_fin');
    console.log("fecha inicio",startDateInput);
    console.log("fecha fin",endDateInput);
    if (startDate && endDate) {
        startDateInput.value = startDate.toISOString().split('T')[0]; // Formato YYYY-MM-DD
        endDateInput.value = endDate.toISOString().split('T')[0]; // Formato YYYY-MM-DD
    } else {
        startDateInput.value = ''; // Limpiar si no hay selección
        endDateInput.value = ''; // Limpiar si no hay selección
    }
}


prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
    keepSelection(); // Mantener la selección
    updateSelection();
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
    keepSelection(); // Mantener la selección
    updateSelection();
});

// Mantener la selección al navegar entre meses
const keepSelection = () => {
    const dateElements = document.querySelectorAll('.date');
    dateElements.forEach(dateElement => {
        const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), dateElement.textContent);
        if (startDate && endDate) {
            if (date >= startDate && date <= endDate) {
                dateElement.classList.add('selected');
            }
        }
    });
};

// Botón "Hoy"
document.getElementById('todayBtn').addEventListener('click', () => {
    currentDate = new Date(); // Establece la fecha actual
    updateCalendar(); // Actualiza el calendario
    clickCount = 0; // Reinicia el contador de clics
    startDate = null; // Reinicia la selección
    endDate = null; // Reinicia la selección
});

// Calcular el precio total
const totalPriceElement = document.getElementById('totalPrice');
const precioTotalInput = document.getElementById('precio_total');

const calculateTotalPrice = () => {
    let total = 0;
    // Sumar el precio del alojamiento seleccionado
    const selectedAccommodation = document.querySelector('.tar-a.selected-background'); // Solo un alojamiento seleccionado
    if (selectedAccommodation) {
        const priceText = selectedAccommodation.querySelector('.r').textContent; // Obtener el precio
        const price = parseFloat(priceText.replace('$ ', '').replace('/nigth', '').trim());
        total += price;
    }
    // Sumar el precio de los servicios seleccionados
    const selectedServices = document.querySelectorAll('input[name="servicios"]:checked');
    selectedServices.forEach(service => {
        const servicePrice = parseFloat(service.dataset.price);
        total += servicePrice;
    });
    // Multiplicar por la cantidad de días seleccionados
    const selectedDaysCount = selectedDates.length - 1; // Usar la longitud del arreglo de fechas seleccionadas
    const finalTotal = selectedDaysCount > 0 ? total * selectedDaysCount : 0; // Calcular el total final
    totalPriceElement.textContent = `$ ${finalTotal.toFixed(2)}`;
    precioTotalInput.value = finalTotal.toFixed(2); // Actualizar el campo oculto con el precio total
};

// Agregar evento de cambio a los checkboxes de servicios
const serviceCheckboxes = document.querySelectorAll('input[name="servicios"]');
serviceCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', calculateTotalPrice);
});

// Agregar evento de clic a los botones de reserva de alojamiento
const accommodationButtons = document.querySelectorAll('.l');
accommodationButtons.forEach(button => {
    button.addEventListener('click', function () {
        const parentContainer = this.closest('.tar-a');
        // Verificar si el alojamiento ya está seleccionado
        const isSelected = parentContainer.classList.contains('selected-background');
        // Si no está seleccionado, ocultar todos los demás
        if (!isSelected) {
            accommodationButtons.forEach(btn => {
                const btnParent = btn.closest('.tar-a');
                btnParent.classList.add('hidden'); // Ocultar el alojamiento
            });
            // Mostrar solo el alojamiento seleccionado
            parentContainer.classList.remove('hidden'); // Mostrar el alojamiento seleccionado
            this.classList.add('selected');
            this.textContent = 'DESELECT'; // Cambiar texto a 'DESELECT'
            this.style.backgroundColor = '#bf1414'; // Cambiar color de fondo
            parentContainer.classList.add('selected-background');
            // Obtener el ID del alojamiento y asignarlo al campo oculto
            const alojamientoId = parentContainer.dataset.alojamientoId;
            document.getElementById('alojamiento_id').value = alojamientoId; // Asignar el ID al campo oculto
        } else {
            // Si ya estaba seleccionado, deseleccionarlo y mostrar todos los alojamientos
            accommodationButtons.forEach(btn => {
                const btnParent = btn.closest('.tar-a');
                btnParent.classList.remove('hidden'); // Mostrar todos los alojamientos
            });
            this.classList.remove('selected');
            this.textContent = 'SELECT'; // Resetear texto a 'SELECT'
            this.style.backgroundColor = ''; // Resetear color de fondo
            parentContainer.classList.remove('selected-background');
            // Limpiar el campo oculto
            document.getElementById('alojamiento_id').value = ''; // Limpiar el ID del alojamiento
        }
        calculateTotalPrice(); // Recalcular el total
    });
});

let selectedFiles = [];


        // Función para agregar un nuevo rango de fechas
        function addDateRange() {
            const container = document.getElementById('dateRangesContainer');
            const div = document.createElement('div');
            div.classList.add('col-lg-4');
            div.innerHTML = `
                <div class="mb-6 mt-3 col-lg-12" id="dateRange_${dateRangeCount}">
                    <label class="block text-white text-sm font-bold mb-2">Rango de Fechas ${dateRangeCount + 1}</label>
                    <div class="flex space-x-4">
                        <div class="w-full mb-2">
                            <label for="fecha_desde_${dateRangeCount}" class="block text-white text-sm font-bold mb-2">Desde</label>
                            <input type="date" id="fecha_desde_${dateRangeCount}" name="fecha_inicio_${dateRangeCount}" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200" required>
                        </div>
                        <div class="w-full mb-2">
                            <label for="fecha_hasta_${dateRangeCount}" class="block text-white text-sm font-bold mb-2">Hasta</label>
                            <input type="date" id="fecha_hasta_${dateRangeCount}" name="fecha_fin_${dateRangeCount}" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200" required>
                        </div>
                    </div>
                    <button type="button" onclick="removeDateRange(${dateRangeCount})" class="btn-solid-lg-1 mb-6">Eliminar</button>
                </div>
            `;
            container.appendChild(div);
            dateRangeCount++;
        }

        // Función para eliminar un rango de fechas
        function removeDateRange(index) {
            const dateRange = document.getElementById(`dateRange_${index}`);
            if (dateRange) {
                dateRange.remove();
            }
        }

        function enviarFormulario() {
            const formData = new FormData(document.getElementById('casaForm'));
            const disponibilidad = [];
        
            for (let i = 0; i < dateRangeCount; i++) {
                const fechaDesde = document.getElementById(`fecha_desde_${i}`)?.value;
                const fechaHasta = document.getElementById(`fecha_hasta_${i}`)?.value;
        
                if (fechaDesde && fechaHasta) {
                    disponibilidad.push({ "desde": fechaDesde, "hasta": fechaHasta });
                }
            }
        
            formData.set('disponibilidad', JSON.stringify(disponibilidad));  // Convertir a JSON
        
            fetch(document.getElementById('casaForm').action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': 'Ev7ZTldYYvrqhQdojNpIv82WLNxTwkWy7A0MUQwxcZlX6oldfd21bt4DET6yJHDI'
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = 'alojamiento';
                } else {
                    alert('Error al guardar el alojamiento.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al enviar el formulario.');
            });
        }

// Llamar a la función para calcular el total al cargar la página
updateCalendar();
calculateTotalPrice();