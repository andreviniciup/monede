console.log('Script metas.js carregado');

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modalMeta');
    const uploadArea = document.querySelector('.upload-imagem');
    const inputImagem = document.getElementById('imagem');

    // Fecha o modal quando clica fora dele
    window.onclick = function(event) {
        if (event.target == modal) {
            fecharModalMeta();
        }
    }

    // Preview da imagem
    uploadArea.addEventListener('click', () => inputImagem.click());
    
    inputImagem.addEventListener('change', function(e) {
        const arquivo = e.target.files[0];
        if (arquivo) {
            const leitor = new FileReader();
            leitor.onload = function(e) {
                const placeholder = document.querySelector('.placeholder-upload');
                placeholder.innerHTML = `
                    <img src="${e.target.result}" 
                         style="max-width: 100%; max-height: 140px; border-radius: 4px;">
                `;
            }
            leitor.readAsDataURL(arquivo);
        }
    });

    // Formata o input de valor
    const inputValor = document.getElementById('valor_meta');
    inputValor.addEventListener('input', function(e) {
        let valor = e.target.value.replace(/\D/g, '');
        valor = (parseFloat(valor) / 100).toFixed(2);
        e.target.value = valor;
    });
});

function abrirModalMeta() {
    const modal = document.getElementById('modalMeta');
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function fecharModalMeta() {
    const modal = document.getElementById('modalMeta');
}

function toggleMenu(element) {
    const menu = element.nextElementSibling;
    menu.style.display = menu.style.display === "block" ? "none" : "block";
  }
  
  // Fechar o menu ao clicar fora dele
  document.addEventListener('click', function(event) {
    const menus = document.querySelectorAll('.menu');
    menus.forEach(menu => {
        if (!menu.contains(event.target) && !menu.previousElementSibling.contains(event.target)) {
            menu.style.display = 'none';
        }
    });
  });
  document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal-valor-meta');
    const form = document.getElementById('form-valor-meta');
    let metaId = null;

    // Abrir o modal ao clicar no botão
    window.abrirModalValorMeta = (button) => {
        metaId = button.dataset.metaId; // Pega o ID da meta do botão clicado
        modal.style.display = 'flex'; // Exibe o modal
    };

    // Fechar o modal
    window.fecharModalValorMeta = () => {
        modal.style.display = 'none'; // Esconde o modal
    };

    // Submeter o formulário
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Impede o envio padrão do formulário
        
        // Captura o valor do input e remove espaços extras
        const valorInput = document.getElementById('valor_meta');
        let valor = valorInput.value.trim();  // Remove espaços extras do valor inserido
    
        // Verifica se o valor está vazio ou se não é um número válido
        if (!valor || isNaN(parseFloat(valor))) {
            alert('Por favor, insira um valor válido.');
            return;
        }
    
        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
            // Faz a requisição POST ao backend com o valor corretamente convertido para float
            const response = await fetch(`/metas/atualizar-meta/${metaId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ valor_meta: parseFloat(valor) }) // Converte para número float
            });
    
            if (response.ok) {
                const result = await response.json();
                alert('Meta atualizada com sucesso!');
                // Atualize o DOM, se necessário
            } else {
                const errorData = await response.json();
                alert(`Erro ao atualizar a meta: ${errorData.message || 'Erro desconhecido.'}`);
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Ocorreu um erro inesperado.');
        }
    
        modal.style.display = 'none'; // Fecha o modal após o envio
    });
    
    
});
