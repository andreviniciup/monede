document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

// Função que será chamada quando conectar ao backend
async function fetchDashboardData() {
    try {
        // Aqui você fará a chamada ao seu backend
        // const response = await fetch('/api/dashboard-data/');
        // const data = await response.json();
        // updateCharts(data);
        
        // Por enquanto, usando dados mockados
        return {
            expenses: {
                daily: [120, 150, 180, 140, 160, 190, 170],
                categories: {
                    'Alimentação': 2500,
                    'Transporte': 1200,
                    'Moradia': 3000,
                    'Lazer': 800,
                    'Saúde': 1500
                }
            },
            balance: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                income: [8000, 8200, 8400, 8300, 8600, 8500],
                expenses: [6000, 6400, 6200, 6800, 6500, 6700]
            }
        };
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
    }
}

let charts = {};

async function initializeCharts() {
    const data = await fetchDashboardData();
    
    // Gráfico de Gastos
    charts.expenses = new Chart(document.getElementById('expensesChart'), {
        type: 'line',
        data: {
            labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
            datasets: [{
                label: 'Gastos',
                data: data.expenses.daily,
                borderColor: '#10b981',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(16, 185, 129, 0.1)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

    // Gráfico de Categorias
    charts.categories = new Chart(document.getElementById('categoryChart'), {
        type: 'doughnut',
        data: {
            labels: Object.keys(data.expenses.categories),
            datasets: [{
                data: Object.values(data.expenses.categories),
                backgroundColor: [
                    '#10b981',
                    '#3b82f6',
                    '#f59e0b',
                    '#ef4444',
                    '#8b5cf6'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });

    // Gráfico de Balanço
    charts.balance = new Chart(document.getElementById('balanceChart'), {
        type: 'bar',
        data: {
            labels: data.balance.labels,
            datasets: [
                {
                    label: 'Receitas',
                    data: data.balance.income,
                    backgroundColor: '#10b981'
                },
                {
                    label: 'Despesas',
                    data: data.balance.expenses,
                    backgroundColor: '#ef4444'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Função para atualizar o período dos gráficos
function updateTimeRange(period) {
    // Aqui você implementará a lógica para buscar dados do período selecionado
    console.log(`Período selecionado: ${period}`);
    // Exemplo de como atualizar quando tiver o backend:
    // fetchDashboardData(period).then(data => updateCharts(data));
}