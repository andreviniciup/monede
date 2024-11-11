document.addEventListener('DOMContentLoaded', () => {
    const inputBox = document.querySelector('.input-box');
    const calendarElement = document.querySelector('.calendar-element');
    const prevMonthBtn = document.querySelector('.prev-month');
    const nextMonthBtn = document.querySelector('.next-month');
    const currentMonthYear = document.querySelector('.current-month-year');
    const calendarGrid = document.querySelector('.calendar-grid');
    const applyBtn = document.querySelector('.apply-btn');
  
    let currentDate = new Date();
    let selectedStartDate = null;
    let selectedEndDate = null;
    let isRangeSelection = true;
  
    function renderCalendar() {
      const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
      const daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
  
      calendarGrid.innerHTML = '';
  
      // Render empty cells for days before the first day of the month
      for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement('div');
        calendarGrid.appendChild(cell);
      }
  
      // Render calendar days
      for (let i = 1; i <= daysInMonth; i++) {
        const cell = document.createElement('div');
        cell.textContent = i;
        cell.addEventListener('click', () => handleDayClick(i));
        if (selectedStartDate && selectedEndDate) {
          if (new Date(currentDate.getFullYear(), currentDate.getMonth(), i) >= selectedStartDate && new Date(currentDate.getFullYear(), currentDate.getMonth(), i) <= selectedEndDate) {
            cell.classList.add('selected');
          }
        }
        calendarGrid.appendChild(cell);
      }
  
      currentMonthYear.textContent = `${currentDate.toLocaleString('default', { month: 'long' })} ${currentDate.getFullYear()}`;
    }
  
    function handleDayClick(day) {
      const clickedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
      if (!selectedStartDate) {
        selectedStartDate = clickedDate;
      } else if (!selectedEndDate) {
        selectedEndDate = clickedDate;
        if (selectedEndDate < selectedStartDate) {
          [selectedStartDate, selectedEndDate] = [selectedEndDate, selectedStartDate];
        }
      } else {
        selectedStartDate = clickedDate;
        selectedEndDate = null;
      }
      renderCalendar();
    }
  
    prevMonthBtn.addEventListener('click', () => {
      currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
      renderCalendar();
    });
  
    nextMonthBtn.addEventListener('click', () => {
      currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
      renderCalendar();
    });
  
    inputBox.addEventListener('click', () => {
      calendarElement.style.display = 'block';
    });
  
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.calendar-wrapper')) {
        calendarElement.style.display = 'none';
      }
    });
  
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        calendarElement.style.display = 'none';
      }
    });
  
    applyBtn.addEventListener('click', () => {
      if (selectedStartDate && selectedEndDate) {
        inputBox.value = `${format(selectedStartDate, 'MM/dd/yyyy')} - ${format(selectedEndDate, 'MM/dd/yyyy')}`;
      }
      calendarElement.style.display = 'none';
    });
  
    function format(date, format) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return format.replace('yyyy', year).replace('MM', month).replace('dd', day);
    }

    function toggleDatePicker() {
    const dateTextInicial = document.getElementById("dataInicialText");
    const dateInputInicial = document.getElementById("data-inicial");
    dateTextInicial.style.display = "none";
    dateInputInicial.style.display = "inline";
    dateInputInicial.focus();
  }

  function updateDateText() {
    const dateTextInicial = document.getElementById("dataInicialText");
    const dateInputInicial = document.getElementById("data-inicial");
    if (dateInputInicial.value) {
      const selectedDate = new Date(dateInputInicial.value);
      const formattedDate = selectedDate.toLocaleDateString("pt-BR", {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
      dateTextInicial.textContent = formattedDate;
      dateInputInicial.style.display = "none";
      dateTextInicial.style.display = "inline";
    }
  }

  function toggleDatePickerFinal() {
    const dateTextFinal = document.getElementById("dataFinalText");
    const dateInputFinal = document.getElementById("data-final");
    dateTextFinal.style.display = "none";
    dateInputFinal.style.display = "inline";
    dateInputFinal.focus();
  }

  function updateDateFinalText() {
    const dateTextFinal = document.getElementById("dataFinalText");
    const dateInputFinal = document.getElementById("data-final");
    if (dateInputFinal.value) {
      const selectedDate = new Date(dateInputFinal.value);
      const formattedDate = selectedDate.toLocaleDateString("pt-BR", {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
      dateTextFinal.textContent = formattedDate;
      dateInputFinal.style.display = "none";
      dateTextFinal.style.display = "inline";
    }
  }

  function toggleDropdown() {
    const dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
  }

  // Expor funções necessárias globalmente
  window.toggleDatePicker = toggleDatePicker;
  window.updateDateText = updateDateText;
  window.toggleDatePickerFinal = toggleDatePickerFinal;
  window.updateDateFinalText = updateDateFinalText;
  window.toggleDropdown = toggleDropdown;
  
    renderCalendar();
  });