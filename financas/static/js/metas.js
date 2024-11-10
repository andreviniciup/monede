// static/financas/js/metas.js

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