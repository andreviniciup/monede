
function abrirModalNovoPagamento() {
    document.getElementById('modalNovoPagamento').style.display = 'block';
}

function fecharModalNovoPagamento() {
    document.getElementById('modalNovoPagamento').style.display = 'none';
}

async function salvarNovoPagamento(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch("{% url 'financas:adicionar_pagamento' %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        });

        const data = await response.json();
        if (data.status === 'success') {
            fecharModalNovoPagamento();
            location.reload();
        } else {
            alert('Erro ao salvar pagamento. Verifique os dados.');
        }
    } catch (error) {
        alert('Erro ao processar a requisição.');
    }
}

async function processarPagamento(pagamentoId) {
    try {
        const response = await fetch(`/financas/pagamentos/${pagamentoId}/processar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        });

        const data = await response.json();
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Erro ao processar pagamento.');
        }
    } catch (error) {
        alert('Erro ao processar a requisição.');
    }
}

