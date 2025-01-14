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
                    selectedDates = [startDate]; // Reiniciar el array de fechas seleccionadas
                    console.log("Fecha de inicio seleccionada:", startDate);
                    console.log("Fechas seleccionadas:", selectedDates);
                } else if (!endDate) {
                    if (selectedDate >= startDate) {
                        endDate = selectedDate; // Establecer fecha de fin
                        // Agregar el rango de fechas seleccionadas
                        for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
                            selectedDates.push(new Date(d)); // Agregar cada fecha en el rango
                        }
                        console.log("Fecha de fin seleccionada:", endDate);
                        console.log("Fechas seleccionadas después de agregar rango:", selectedDates);
                    } else {
                        // Si se selecciona una fecha anterior a la fecha de inicio, reiniciar la selección
                        startDate = selectedDate;
                        endDate = null;
                        selectedDates = [startDate]; // Reiniciar el array de fechas seleccionadas
                        console.log("Reiniciando selección. Nueva fecha de inicio:", startDate);
                        console.log("Fechas seleccionadas:", selectedDates)
                    }
                } else {
                    // Reiniciar selección si ya hay una fecha de inicio y fin
                    startDate = selectedDate;
                    endDate = null;
                    selectedDates = [startDate]; // Reiniciar el array de fechas seleccionadas
                    console.log("Reiniciando selección. Nueva fecha de inicio:", startDate);
                    console.log("Fechas seleccionadas:", selectedDates);
                }
                updateSelection(); // Actualizar selección visual
            }
        }
    });
});
};

const checkAvailability = (alojamientoId) => {
    return reservas.every(reserva => {
        // Convertir las fechas de la reserva a objetos Date para la comparación
        const reservaInicio = new Date(reserva.fecha_inicio);
        const reservaFin = new Date(reserva.fecha_fin);
        
        // Comprobar la superposición
        return (
            (startDate < reservaInicio || startDate > reservaFin) && // La fecha de inicio está fuera de la reserva
            (endDate < reservaInicio || endDate > reservaFin) // La fecha de fin está fuera de la reserva
        );
    });
};

// Al cargar los alojamientos
const loadAccommodations = () => {
    const accommodationElements = document.querySelectorAll('.tar'); // Suponiendo que '.tar' son tus alojamientos
    accommodationElements.forEach(element => {
        const alojamientoId = parseInt(element.dataset.alojamientoId); // Obteniendo el ID del alojamiento
        if (!checkAvailability(alojamientoId)) {
            element.style.display = 'none'; // Ocultar si está reservado
        } else {
            element.style.display = 'block'; // Mostrar si está disponible
        }
    });
};

// Función para actualizar la selección visual
function updateSelection() {
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
    loadAccommodations(); // Llama a la función para cargar alojamientos disponibles
    countSelectedDays(); // Contar días seleccionados después de actualizar la selección
    console.log("Fechas seleccionadas al actualizar la selección:", selectedDates);
    console.log("Fecha de inicio:", startDate);
    console.log("Fecha de fin:", endDate);
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
    updateSelection()
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
    keepSelection(); // Mantener la selección
    updateSelection()
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
    const selectedAccommodation = document.querySelector('.tar.selected-background'); // Solo un alojamiento seleccionado
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
        const parentContainer = this.closest('.tar');

        // Verificar si el alojamiento ya está seleccionado
        const isSelected = parentContainer.classList.contains('selected-background');

        // Si no está seleccionado, ocultar todos los demás
        if (!isSelected) {
            accommodationButtons.forEach(btn => {
                const btnParent = btn.closest('.tar');
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
                const btnParent = btn.closest('.tar');
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

// Llamar a la función para calcular el total al cargar la página
updateCalendar();
calculateTotalPrice();