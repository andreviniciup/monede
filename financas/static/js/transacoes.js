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

  document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#search-transactions');
    const tableBody = document.querySelector('#transactions-table tbody');
    let timeoutId;
  
    if (searchInput) {
      searchInput.addEventListener('input', function(e) {
        clearTimeout(timeoutId);
        
        timeoutId = setTimeout(() => {
          const searchTerm = e.target.value.trim();
          
          fetch(`/buscar-transacoes/?q=${encodeURIComponent(searchTerm)}`)
            .then(response => response.json())
            .then(data => {
              if (data.error) {
                console.error('Erro:', data.error);
                tableBody.innerHTML = `<tr><td colspan="8">Erro ao buscar transações</td></tr>`;
              } else {
                tableBody.innerHTML = '';
                data.transacoes.forEach(transacao => {
                  const row = document.createElement('tr');
                  row.classList.add('transacao-row'); // Adiciona uma classe CSS à linha
                  row.innerHTML = `
                    <td>
                      ${transacao.logo_url ? `<img src="${transacao.logo_url}" alt="Logo" class="transacao-logo">` : ''}
                    </td>
                    <td class="transacao-titulo">${transacao.titulo}</td>
                    <td class="transacao-data">${transacao.data}</td>
                    <td class="transacao-valor">${transacao.valor.toFixed(2)}</td>
                    <td class="transacao-tipo">${transacao.tipo}</td>
                    <td class="transacao-forma-pagamento">${transacao.forma_pagamento}</td>
                    <td class="transacao-categoria">${transacao.categoria}</td>
                    <td class="transacao-acoes">
                      <a href="/editar-transacao/${transacao.id}" class="btn-editar">Editar</a>
                      <a href="/excluir-transacao/${transacao.id}" class="btn-excluir">Excluir</a>
                    </td>
                  `;
                  tableBody.appendChild(row);
                });
  
                // Opcional: Atualizar contador de resultados se houver
                const counter = document.querySelector('#results-counter');
                if (counter) {
                  counter.textContent = `${data.quantidade} resultado(s) encontrado(s)`;
                }
              }
            })
            .catch(error => {
              console.error('Erro:', error);
              tableBody.innerHTML = `<tr><td colspan="8">Erro ao buscar transações</td></tr>`;
            });
        }, 300); // Delay de 300ms para evitar muitas requisições
      });
    } else {
      console.error('Elemento #search-transactions não encontrado.');
    }
  });