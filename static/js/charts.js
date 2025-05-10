document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts on finance page if present
    if (document.getElementById('incomeExpenseChart')) {
        initFinanceCharts();
    }

    // Initialize charts on inventory page if present
    if (document.getElementById('inventoryStatusChart')) {
        initInventoryCharts();
    }

    const serviceOrderStatusChart = document.getElementById('serviceOrderStatusChart');
    const projectStatusChart = document.getElementById('projectStatusChart');
    const monthlyFinanceChart = document.getElementById('monthlyFinanceChart');

    if (serviceOrderStatusChart) {
        fetch('/dashboard/service-order-stats')
            .then(response => response.json())
            .then(data => {
                new Chart(serviceOrderStatusChart, {
                    type: 'doughnut',
                    data: {
                        labels: ['Abertas', 'Em Andamento', 'Concluídas', 'Canceladas'],
                        datasets: [{
                            data: [
                                data.open || 0,
                                data.in_progress || 0,
                                data.completed || 0,
                                data.cancelled || 0
                            ],
                            backgroundColor: [
                                '#17a2b8',
                                '#0a6ebd', 
                                '#28a745',
                                '#dc3545'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    boxWidth: 12,
                                    font: {
                                        size: 12
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error:', error));
    }

    if (projectStatusChart) {
        fetch('/dashboard/project-stats')
            .then(response => response.json())
            .then(data => {
                new Chart(projectStatusChart, {
                    type: 'doughnut',
                    data: {
                        labels: ['Planejamento', 'Em Andamento', 'Em Espera', 'Concluídos', 'Cancelados'],
                        datasets: [{
                            data: [
                                data.planning || 0,
                                data.in_progress || 0,
                                data.on_hold || 0,
                                data.completed || 0,
                                data.cancelled || 0
                            ],
                            backgroundColor: [
                                '#17a2b8',
                                '#0a6ebd',
                                '#ffc107',
                                '#28a745',
                                '#dc3545'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    boxWidth: 12,
                                    font: {
                                        size: 12
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error:', error));
    }

    if (monthlyFinanceChart) {
        // Monthly Finance Chart
        fetch('/dashboard/finance-stats')
            .then(response => response.json())
            .then(data => {
                new Chart(monthlyFinanceChart, {
                    type: 'bar',
                    data: {
                        labels: data.months,
                        datasets: [
                            {
                                label: 'Receitas',
                                data: data.income,
                                backgroundColor: '#28a745',
                                borderColor: '#28a745',
                                borderWidth: 1
                            },
                            {
                                label: 'Despesas',
                                data: data.expenses,
                                backgroundColor: '#dc3545',
                                borderColor: '#dc3545',
                                borderWidth: 1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value) {
                                        return 'R$ ' + value.toLocaleString('pt-BR');
                                    }
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return context.dataset.label + ': R$ ' + context.parsed.y.toLocaleString('pt-BR');
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching finance stats:', error);
            });
    }
});

function initFinanceCharts() {
    const incomeExpenseChart = document.getElementById('incomeExpenseChart');
    const categoriesChart = document.getElementById('categoriesChart');

    if (incomeExpenseChart) {
        // Income vs Expense Chart
        fetch('/finance/stats')
            .then(response => response.json())
            .then(data => {
                new Chart(incomeExpenseChart, {
                    type: 'pie',
                    data: {
                        labels: ['Receitas', 'Despesas'],
                        datasets: [{
                            data: [data.total_income || 0, data.total_expenses || 0],
                            backgroundColor: ['#28a745', '#dc3545'],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return context.label + ': R$ ' + context.raw.toLocaleString('pt-BR');
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching finance stats:', error);
            });
    }

    if (categoriesChart) {
        // Categories Chart
        fetch('/finance/category-stats')
            .then(response => response.json())
            .then(data => {
                new Chart(categoriesChart, {
                    type: 'bar',
                    data: {
                        labels: data.categories,
                        datasets: [
                            {
                                label: 'Valores',
                                data: data.amounts,
                                backgroundColor: function(context) {
                                    const index = context.dataIndex;
                                    return data.types[index] === 'income' ? '#28a745' : '#dc3545';
                                },
                                borderWidth: 1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value) {
                                        return 'R$ ' + value.toLocaleString('pt-BR');
                                    }
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const type = data.types[context.dataIndex];
                                        const typeLabel = type === 'income' ? 'Receita' : 'Despesa';
                                        return typeLabel + ': R$ ' + context.parsed.y.toLocaleString('pt-BR');
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching category stats:', error);
            });
    }
}

function initInventoryCharts() {
    const inventoryStatusChart = document.getElementById('inventoryStatusChart');
    const topItemsChart = document.getElementById('topItemsChart');

    if (inventoryStatusChart) {
        // Inventory Status Chart
        fetch('/stock/stats')
            .then(response => response.json())
            .then(data => {
                new Chart(inventoryStatusChart, {
                    type: 'doughnut',
                    data: {
                        labels: ['Estoque Normal', 'Estoque Baixo', 'Sem Estoque'],
                        datasets: [{
                            data: [
                                data.normal || 0,
                                data.low || 0,
                                data.out || 0
                            ],
                            backgroundColor: [
                                '#28a745',
                                '#ffc107',
                                '#dc3545'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching inventory stats:', error);
            });
    }

    if (topItemsChart) {
        // Top Items Chart
        fetch('/stock/top-items')
            .then(response => response.json())
            .then(data => {
                new Chart(topItemsChart, {
                    type: 'bar',
                    data: {
                        labels: data.items,
                        datasets: [{
                            label: 'Quantidade em Estoque',
                            data: data.quantities,
                            backgroundColor: '#0a6ebd',
                            borderColor: '#0a6ebd',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching top items:', error);
            });
    }
}
// Inicialização dos gráficos do dashboard

function initDashboardCharts() {
    // Inicializa os gráficos quando o DOM estiver pronto
    console.log("Iniciando gráficos do dashboard");

    // Gráfico de Status das Ordens de Serviço
    initServiceOrderChart();

    // Gráfico de Status dos Projetos
    initProjectStatusChart();

    // Gráfico de Finanças Mensais (se o usuário tiver acesso)
    if (document.getElementById('monthlyFinanceChart')) {
        initMonthlyFinanceChart();
    }
}

function initServiceOrderChart() {
    const ctx = document.getElementById('serviceOrderStatusChart');
    if (!ctx) return;

    // Buscar dados da API
    fetch('/dashboard/service-order-stats')
        .then(response => response.json())
        .then(data => {
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Abertas', 'Em Progresso', 'Concluídas', 'Canceladas'],
                    datasets: [{
                        data: [data.open, data.in_progress, data.completed, data.cancelled],
                        backgroundColor: ['#17a2b8', '#007bff', '#28a745', '#dc3545']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar dados de ordens:', error));
}

function initProjectStatusChart() {
    const ctx = document.getElementById('projectStatusChart');
    if (!ctx) return;

    // Buscar dados da API
    fetch('/dashboard/project-stats')
        .then(response => response.json())
        .then(data => {
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Planejamento', 'Em Progresso', 'Em Espera', 'Concluídos', 'Cancelados'],
                    datasets: [{
                        data: [data.planning, data.in_progress, data.on_hold, data.completed, data.cancelled],
                        backgroundColor: ['#17a2b8', '#007bff', '#ffc107', '#28a745', '#dc3545']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar dados de projetos:', error));
}

function initMonthlyFinanceChart() {
    const ctx = document.getElementById('monthlyFinanceChart');
    if (!ctx) return;

    // Buscar dados da API
    fetch('/dashboard/finance-stats')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Erro de permissão:', data.error);
                return;
            }

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.months,
                    datasets: [
                        {
                            label: 'Receitas',
                            data: data.income,
                            borderColor: '#28a745',
                            backgroundColor: 'rgba(40, 167, 69, 0.1)',
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Despesas',
                            data: data.expenses,
                            borderColor: '#dc3545',
                            backgroundColor: 'rgba(220, 53, 69, 0.1)',
                            fill: true,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed.y !== null) {
                                        label += new Intl.NumberFormat('pt-BR', { 
                                            style: 'currency', 
                                            currency: 'BRL' 
                                        }).format(context.parsed.y);
                                    }
                                    return label;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return 'R$ ' + value.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao carregar dados financeiros:', error));
}