function abrirModalCartao() {
    const modal = document.getElementById('modalCartao');
    modal.style.display = 'block';
}

function fecharModalCartao() {
    const modal = document.getElementById('modalCartao');
    modal.style.display = 'none';
}

function fecharFatura(cartaoId) {
    // Implementar a lógica de fechar fatura
    console.log('Fechando fatura do cartão:', cartaoId);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('modalCartao');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}