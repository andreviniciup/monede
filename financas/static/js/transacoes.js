// Function to open the modal
function abrirModalNovaTransacao() {
    var modal = document.getElementById("modalTransacao");
    modal.style.display = "block";
  }
  
  // Function to close the modal
  function fecharModalTransacao() {
    var modal = document.getElementById("modalTransacao");
    modal.style.display = "none";
  }
  
  // Add event listener to close the modal when clicking outside of it
  window.onclick = function(event) {
    var modal = document.getElementById("modalTransacao");
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }