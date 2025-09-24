<script>
    import { Line } from 'svelte-chartjs';
    import { Chart, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js';

    Chart.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale);
    
    export let data = [];

    const monthsOfTheYear = [
        'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
    ];

    $: chartData = {
        labels: monthsOfTheYear,
        datasets: [{
            label: 'Consultas por Mês',
            data: monthsOfTheYear.map(month => {
                return data.filter(item => item.AppointmentMonth.trim() === month).length;
            }),
            fill: true,

            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderColor: 'rgba(59, 130, 246, 1)',
            pointBorderColor: 'rgba(59, 130, 246, 1)',
            pointBackgroundColor: '#fff',
            tension: 0.4
        }]
    };

    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
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
                grid: { 
                    display: true 
                }
            },
            y: {
                ticks: { color: '#9CA3AF', font: { family: 'Poppins', size: 12 } },
                grid: { 
                    display: true 
                },
                border: {
                    display: false
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

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
	<h3 class="text-center text-lg font-semibold mb-3 text-black">Tendência de Consultas por Mês</h3>
	<div class="max-h-[500px] overflow-y-auto min-h-[300px]" >
		<Line data={chartData} options={chartOptions} />
	</div>
</div>