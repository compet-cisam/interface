<script>
    import { Line } from 'svelte-chartjs';
    import { Chart, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js';

    Chart.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale);
    
    export let data = [];

    const monthsOfTheYear = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];

    $: chartData = {
        labels: monthsOfTheYear,
        datasets: [{
            label: 'Consultas por Mês',
            data: monthsOfTheYear.map(month => {
                return data.filter(item => item.AppointmentMonth.trim() === month).length;
            }),
            fill: true,

            backgroundColor: 'rgba(59, 130, 246, 0.2)', // Azul suave
            borderColor: 'rgba(59, 130, 246, 1)',
            pointBorderColor: 'rgba(59, 130, 246, 1)',
            pointBackgroundColor: '#fff',
            // CORRIGIDO: Curvas mais suaves na linha.
            tension: 0.4
        }]
    };

    // CORRIGIDO: Opções de estilo para um visual mais limpo.
    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false, // Permite que o gráfico se ajuste melhor ao container.
        plugins: {
            legend: {
                display: false // Legenda removida para um visual mais limpo, o título já é suficiente.
            },
            tooltip: {
                backgroundColor: '#1e1e2f',
                titleColor: '#fff',
                bodyColor: '#ccc',
                padding: 10,
                cornerRadius: 4,
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 1
            }
        },
        scales: {
            x: {
                ticks: { color: '#9CA3AF', font: { family: 'Poppins', size: 12 } },
                // CORRIGIDO: Removida a linha de grade do eixo X.
                grid: { 
                    display: false 
                }
            },
            y: {
                ticks: { color: '#9CA3AF', font: { family: 'Poppins', size: 12 } },
                // CORRIGIDO: Removida a linha de grade do eixo Y para um look minimalista.
                grid: { 
                    display: false 
                },
                border: {
                    display: false // Remove a linha do eixo Y
                }
            }
        }
    };
</script>

<!-- <div class="h-64 rounded-xl bg-[#1e1e2f] p-4 shadow-lg"> -->
<!-- <h3 class="text-center text-gray-200 text-lg font-semibold mb-4">Tendência de Consultas por Mês</h3>

<div class="h-64 rounded-xl bg-[#1e1e2f] p-4 shadow-lg">
    <Line data={chartData} options={chartOptions} />
</div> -->

<div class="bg-[#1e1e2f] p-4 rounded-xl shadow-lg h-full flex flex-col">
	<h3 class="text-center text-lg font-semibold mb-3 text-white">Tendência de Consultas por Mês</h3>
	<div class="max-h-[500px] overflow-y-auto min-h-[300px]" >
		<Line data={chartData} options={chartOptions} />
	</div>
</div>