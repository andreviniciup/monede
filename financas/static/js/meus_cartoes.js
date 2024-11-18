function abrirModalCartao() {
    document.getElementById('modalCartao').style.display = 'block';
}

function fecharModalCartao() {
    document.getElementById('modalCartao').style.display = 'none';
}

async function pagarFatura(cartaoId) {
    try {
        const response = await fetch(`/cartoes/${cartaoId}/pagar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        if (response.ok) {
            location.reload();
        }
    } catch (error) {
        console.error('Erro ao pagar fatura:', error);
    }
}

function filtrarTransacoes() {
    const dataInicial = document.getElementById('dataInicial').value;
    const dataFinal = document.getElementById('dataFinal').value;
    
    const url = new URL(window.location);
    url.searchParams.set('data_inicial', dataInicial);
    url.searchParams.set('data_final', dataFinal);
}