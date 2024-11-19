function abrirModalConta() {
    document.getElementById('modalConta').style.display = 'flex';
}

function fecharModalConta() {
    document.getElementById('modalConta').style.display = 'none';
}

// Fechar o modal ao clicar fora do conteúdo
window.onclick = function(event) {
    const modal = document.getElementById('modalConta');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

  function abrirModalBanco() {
    document.getElementById('modalCriarBanco').style.display = 'flex';
  }
  
  function fecharModalBanco() {
    document.getElementById('modalCriarBanco').style.display = 'none';
  }
  
  // Fechar o modal se o usuário clicar fora do conteúdo do modal
  window.onclick = function(event) {
    const modalBanco = document.getElementById('modalCriarBanco');
    if (event.target === modalBanco) {
      modalBanco.style.display = 'none';
    }
  };
  
  document.addEventListener('DOMContentLoaded', function () {
    // Exemplo simples: Alerta ao criar uma conta
    const form = document.querySelector('form');
    if (form) {
      form.addEventListener('submit', function () {
        alert('Conta criada com sucesso!');
      });
    }
  });
    