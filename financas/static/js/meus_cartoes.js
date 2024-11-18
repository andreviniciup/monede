function abrirModalCartao() {
    document.getElementById('modalCartao').style.display = 'block';
}

function fecharModalCartao() {
    document.getElementById('modalCartao').style.display = 'none';
}

function abrirModalTransacao() {
    document.getElementById('modalTransacao').style.display = 'block';
}

function fecharModalTransacao() {
    document.getElementById('modalTransacao').style.display = 'none';
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
    const url = new URL(window.location.href);
    url.searchParams.set('data_inicial', dataInicial);
    url.searchParams.set('data_final', dataFinal);
    window.location.href = url.toString();
}

