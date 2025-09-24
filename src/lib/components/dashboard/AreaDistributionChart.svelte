<script>
    import { Doughnut } from 'svelte-chartjs';
    import 'chart.js/auto';

    export let data = [];
    let chartData = {};
    const chartColors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f'];

    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: { color: 'gray', font: { family: 'Poppins', size: 12 } }
            }
        }
    };

    $: {
    const counts = data.reduce((acc, item) => {
        const area = item.HealthArea;

        if (area) {
            acc[area] = (acc[area] || 0) + 1;
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
            hoverOffset: 4
        }]
    };
    }
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
    <h3 class="text-center text-lg font-semibold mb-3 text-black">Atendimentos por Área</h3>
    <div class="relative flex-grow min-h-[250px]">
        <!-- {#if data.length > 0}
            <Doughnut {chartData} {chartOptions} />
        {:else}
            <p class="text-center text-gray-400 italic mt-10">Sem dados para exibir.</p>
        {/if} -->
        <Doughnut data={chartData} options={chartOptions} />
    </div>
</div>