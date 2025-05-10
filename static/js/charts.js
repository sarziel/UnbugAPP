document.addEventListener('DOMContentLoaded', function() {
    // Dashboard charts initialization
    initDashboardCharts();
    
    // Initialize charts on finance page if present
    if (document.getElementById('incomeExpenseChart')) {
        initFinanceCharts();
    }
    
    // Initialize charts on inventory page if present
    if (document.getElementById('inventoryStatusChart')) {
        initInventoryCharts();
    }
});

function initDashboardCharts() {
    const serviceOrderStatusChart = document.getElementById('serviceOrderStatusChart');
    const projectStatusChart = document.getElementById('projectStatusChart');
    const monthlyFinanceChart = document.getElementById('monthlyFinanceChart');
    
    if (serviceOrderStatusChart) {
        // Service Order Status Chart
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
                                position: 'bottom'
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching service order stats:', error);
            });
    }
    
    if (projectStatusChart) {
        // Project Status Chart
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
                                position: 'bottom'
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching project stats:', error);
            });
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
}

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
        fetch('/inventory/stats')
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
        fetch('/inventory/top-items')
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
