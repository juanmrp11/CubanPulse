const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let currentDate = new Date();
let startDate = null; // Fecha de inicio de la selección
let endDate = null; // Fecha de fin de la selección
let clickCount = 0; // Contador de clics

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
        datesHTML += `<div class="date ${activeClass}" data-date="${i}">${i}</div>`;
    }

    // Días del mes siguiente (inactivos)
    for (let i = 1; i <= 7 - lastDayIndex; i++) {
        datesHTML += `<div class="date inactive">${new Date(currentYear, currentMonth + 1, i).getDate()}</div>`;
    }

    datesElement.innerHTML = datesHTML;

// Agregar evento de clic a cada fecha
const dateElements = document.querySelectorAll('.date');
dateElements.forEach(dateElement => {
    dateElement.addEventListener('click', function() {
        // Verificar si el día es inactivo antes de proceder
        if (!this.classList.contains('inactive')) {
            const selectedDate = new Date(currentYear, currentMonth, this.textContent);
            // Verificar si la fecha seleccionada es hoy o futura
            if (selectedDate >= new Date()) {
                clickCount++; // Incrementar contador de clics
                if (clickCount === 1) {
                    startDate = selectedDate; // Establecer fecha de inicio
                    endDate = null; // Reiniciar fecha de fin
                } else if (clickCount === 2) {
                    endDate = selectedDate; // Establecer fecha de fin
                } else if (clickCount === 3) {
                    // Reiniciar selección
                    startDate = null;
                    endDate = null;
                    clickCount = 0; // Reiniciar contador
                }
                updateSelection(); // Actualizar selección
            }
        }
    });
});
};

// Función para actualizar la selección visual
function updateSelection() {
    const dateElements = document.querySelectorAll('.date');
    dateElements.forEach(dateElement => {
        // Crear un objeto Date solo si el texto no es inactivo
        const dayText = dateElement.textContent;
        const isInactive = dateElement.classList.contains('inactive');

        // Limpiar selección anterior
        dateElement.classList.remove('selected');

        // Solo proceder si el día no es inactivo
        if (!isInactive) {
            const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayText);

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
}

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

prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
    keepSelection(); // Mantener la selección
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
    keepSelection(); // Mantener la selección
});

// Botón "Hoy"
document.getElementById('todayBtn').addEventListener('click', () => {
    currentDate = new Date(); // Establece la fecha actual
    updateCalendar(); // Actualiza el calendario
    clickCount = 0; // Reinicia el contador de clics
    startDate = null; // Reinicia la selección
    endDate = null; // Reinicia la selección
});

updateCalendar();

    const totalPriceElement = document.getElementById('totalPrice');

// Función para calcular el precio total
const calculateTotalPrice = () => {
    let total = 0;

    // Sumar el precio de los alojamientos seleccionados
    const selectedAccommodation = document.querySelectorAll('.l.selected');
    selectedAccommodation.forEach(button => {
        const priceText = button.nextElementSibling.textContent; // Asumiendo que el precio está justo después del botón
        const price = parseFloat(priceText.replace('$ ', '').replace('/nigth', '').trim());
        total += price;
    });

    // Sumar el precio de los servicios seleccionados
    const selectedServices = document.querySelectorAll('input[name="servicios"]:checked');
    selectedServices.forEach(service => {
        const servicePrice = parseFloat(service.dataset.price);
        total += servicePrice;
    });

    // Actualizar el precio total en el HTML
    totalPriceElement.textContent = `$ ${total.toFixed(2)}`;
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
        const parentContainer = this.closest('.tar'); // Encuentra el contenedor padre
        parentContainer.classList.toggle('selected-background');
        this.classList.toggle('selected'); // Alternar la clase 'selected'
        
        // Cambiar el texto y el color del botón
        if (this.classList.contains('selected')) {
            this.textContent = 'DESELECT'; // Cambiar texto a 'DESELECT'
            this.style.backgroundColor = '#ff6347'; // Cambiar color de fondo (puedes personalizar este color)
        } else {
            this.textContent = 'SELECT'; // Cambiar texto de vuelta a 'SELECT'
            this.style.backgroundColor = ''; // Resetear color de fondo (vuelve al color por defecto)
        }

        calculateTotalPrice(); // Recalcular el total
    });
});

// Llamar a la función para calcular el total al cargar la página
calculateTotalPrice();
