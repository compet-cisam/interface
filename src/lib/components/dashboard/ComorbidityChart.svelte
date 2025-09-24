<script>
    import { Doughnut } from 'svelte-chartjs';
    import 'chart.js/auto';

    export let data = [];
    let chartData = {};
    const chartColors = ['#e15759', '#76b7b2', '#59a14f', '#edc949', '#af7aa1', '#ff9da7', '#9c755f'];

    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: { color: '#ccc', font: { family: 'Poppins', size: 12 } }
            }
        }
    };

    $: {
        // Lógica para separar comorbidades unidas por "+"
        const counts = data.reduce((acc, item) => {
            if (item.Comorbidade && item.Comorbidade.toLowerCase() !== 'none') {
                const comorbidities = item.Comorbidade.split('+').map(c => c.trim());
                comorbidities.forEach(c => {
                    acc[c] = (acc[c] || 0) + 1;
                });
            } else {
                acc['Nenhuma'] = (acc['Nenhuma'] || 0) + 1;
            }
            return acc;
        }, {});

        const labels = Object.keys(counts);
        const dataPoints = Object.values(counts);

        chartData = {
            labels,
            datasets: [{
                data: dataPoints,
                backgroundColor: chartColors,
                hoverOffset: 4,
                borderColor: '#1e1e2f'
            }]
        };
    }
</script>

<div class="bg-[#1e1e2f] p-4 rounded-xl shadow-lg h-full flex flex-col">
    <h3 class="text-center text-lg font-semibold mb-3 text-white">Prevalência de Comorbidades</h3>
    <div class="relative flex-grow min-h-[250px]">
        {#if data.length === 0}
            <Doughnut data={chartData} {chartOptions} />
        {:else}
            <p class="text-center text-gray-400 italic mt-10">Carregando dados...</p>
        {/if}
        <!-- <Doughnut data={chartData} options={chartOptions} /> -->
    </div>
</div>