<script>
    import { Doughnut } from 'svelte-chartjs';
    import 'chart.js/auto';

    export let data = [];
    let chartData = {};

    
    const chartColors = ['#4e79a7', '#e15759', '#bab0ab']; 

    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom', 
                labels: { 
                    color: 'black', 
                    font: { family: 'Poppins', size: 12 },
                    padding: 20
                }
            },
            tooltip: {
                callbacks: {
                
                    label: (context) => {
                        const label = context.label || '';
                        const value = context.raw || 0;
                        const total = context.chart.getDatasetMeta(0).total || 1;
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${label}: ${value} (${percentage}%)`;
                    }
                }
            }
        }
    };

    $: {
        const counts = {
            'Agendada': 0,
            'Não foi indicada': 0,
            'Não informado': 0
        };

        const histeroscopiaData = data.filter(item => item.especialidade_extenso === 'Histeroscopia Diagnóstica');

        histeroscopiaData.forEach(item => {
            const indicacao = item.status_HD?.trim();
            if (indicacao === 'Agendado') {
                counts['Agendada']++;
            } else if (indicacao === 'Não foi indicada') {
                counts['Não foi indicada']++;
            } else {
                counts['Não informado']++; 
            }
        });

        const labels = Object.keys(counts);
        const dataPoints = Object.values(counts);

        chartData = {
            labels,
            datasets: [{
                data: dataPoints,
                backgroundColor: chartColors,
                hoverOffset: 4,
                borderColor: '#fcfeff',
                borderWidth: 2
            }]
        };
    }
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
    <h3 class="text-center text-lg font-semibold mb-3 text-black">Proporção de Indicação para HD</h3>
    <div class="relative flex-grow min-h-[250px]">
        {#if data.length > 0}
            <Doughnut data={chartData} options={chartOptions} />
        {:else}
            <p class="text-center text-gray-400 italic mt-10">Carregando dados...</p>
        {/if}
    </div>
</div>