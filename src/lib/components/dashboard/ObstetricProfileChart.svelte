<script>
    import { Bar } from 'svelte-chartjs';
    import 'chart.js/auto';

    export let data = [];
    let chartData = {};

    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: '#gray' } } },
        scales: {
            x: { ticks: { color: '#gray' }, grid: { color: '#444' } },
            y: { ticks: { color: '#gray' }, grid: { color: '#444' } }
        }
    };

    $: {
        const totals = data.reduce((acc, item) => {
            acc.gravidez += Number(item.gravidez) || 0;
            acc.parto += Number(item.parto) || 0;
            acc.aborto += Number(item.aborto) || 0;
            return acc;
        }, { gravidez: 0, parto: 0, aborto: 0 });

        chartData = {
            labels: ['Eventos Obstétricos Totais na Amostra'],
            datasets: [
                {
                    label: 'Gestações',
                    data: [totals.gravidez],
                    backgroundColor: '#4e79a7',
                    borderRadius: 4
                },
                {
                    label: 'Partos',
                    data: [totals.parto],
                    backgroundColor: '#59a14f',
                    borderRadius: 4
                },
                {
                    label: 'Abortos',
                    data: [totals.aborto],
                    backgroundColor: '#e15759',
                    borderRadius: 4
                }
            ]
        };
    }
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
    <h3 class="text-center text-lg font-semibold mb-3 text-black">Perfil Obstétrico (Soma Total)</h3>
    <div class="relative flex-grow min-h-[250px]">
        {#if data.length > 0}
            <Bar data={chartData} options={chartOptions} />
        {:else}
            <p class="text-center text-gray-400 italic mt-10">Carregando dados...</p>
        {/if}
    </div>
</div>