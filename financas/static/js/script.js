document.addEventListener("DOMContentLoaded", function() {
  console.log("JavaScript carregado!");

  // Função para alternar a exibição do date picker "Data Inicial"
  function toggleDatePicker() {
    const dateInput = document.getElementById("data-inicial");
    const dateText = document.getElementById("dataInicialText");
    dateText.style.display = "none";
    dateInput.style.display = "inline";
    dateInput.focus();
  }

  // Função para atualizar o texto com a data selecionada "Data Inicial"
  function updateDateText() {
    const dateInput = document.getElementById("data-inicial");
    const dateText = document.getElementById("dataInicialText");
    
    if (dateInput.value) {
      const selectedDate = new Date(dateInput.value);
      const formattedDate = selectedDate.toLocaleDateString("pt-BR", {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
      dateText.textContent = formattedDate;
      dateInput.style.display = "none";
      dateText.style.display = "inline";
    }
  }

  // Função para alternar a exibição do date picker "Data Final"
  function toggleDatePickerFinal() {
    const dateInput = document.getElementById("data-final");
    const dateText = document.getElementById("dataFinalText");
    dateText.style.display = "none";
    dateInput.style.display = "inline";
    dateInput.focus();
  }

  // Função para atualizar o texto com a data selecionada "Data Final"
  function updateDateFinalText() {
    const dateInput = document.getElementById("data-final");
    const dateText = document.getElementById("dataFinalText");
    
    if (dateInput.value) {
      const selectedDate = new Date(dateInput.value);
      const formattedDate = selectedDate.toLocaleDateString("pt-BR", {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
      dateText.textContent = formattedDate;
      dateInput.style.display = "none";
      dateText.style.display = "inline";
    }


      function toggleDropdown() {
        const dropdownContent = document.getElementById("dropdownContent");
        dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
      }

    // Fecha o dropdown se clicar fora dele
    window.onclick = function(event) {
        if (!event.target.closest('.dropdown')) {
            const dropdownContent = document.getElementById("dropdownContent");
            dropdownContent.style.display = "none";
        }
  }
}

  // Expor as funções para o HTML
  window.toggleDatePicker = toggleDatePicker;
  window.updateDateText = updateDateText;
  window.toggleDatePickerFinal = toggleDatePickerFinal;
  window.updateDateFinalText = updateDateFinalText;

  // Adicionar ouvintes para os campos de data
  const dateInputInicial = document.getElementById("data-inicial");
  const dateInputFinal = document.getElementById("data-final");

  if (dateInputInicial) {
    dateInputInicial.addEventListener("change", updateDateText);
  }

  if (dateInputFinal) {
    dateInputFinal.addEventListener("change", updateDateFinalText);
  }
});
