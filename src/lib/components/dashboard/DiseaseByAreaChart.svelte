<script>
    import { Bar } from 'svelte-chartjs';
    import 'chart.js/auto';

    export let data = [];

    let chartData = {};

    const chartColors = [
        '#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc949',
        '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab', '#17becf', '#8c564b'
    ];

    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false 
            },
            tooltip: {
                backgroundColor: '#333',
                titleColor: '#fff',
                bodyColor: '#eee',
                padding: 10,
                cornerRadius: 4,
                callbacks: {
                    label: ctx => `${ctx.dataset.label}: ${ctx.raw} caso(s)`
                }
            }
        },
        scales: {
            x: {
                stacked: false,
                ticks: {
                    color: '#gray',
                    font: { family: 'Poppins', size: 12 }
                },
                grid: {
                    color: '#ccc'
                },
                title: {
                    display: true,
                    text: 'Número de Casos',
                    color: '#gray',
                    font: { size: 14 }
                }
            },
            y: {
                stacked: false,
                ticks: {
                    color: '#gray',
                    font: { family: 'Poppins', size: 12 }
                },
                grid: {
                    color: '#ccc'
                }
            }
        }
    };

    $: {

        const valoresIgnorados = [undefined, null, '', 'Sem dados', 'sem dados'];
        const allDiseases = [...new Set(data.map(d => d.DiagnosedDisease))].filter(disease => !valoresIgnorados.includes(disease));

        const dataByArea = data.reduce((acc, curr) => {
            const area = curr.HealthArea;
            if (area) { 
                if (!acc[area]) acc[area] = [];
                acc[area].push(curr);
            }
            return acc;
        }, {});

        const labels = Object.keys(dataByArea);

        const datasets = allDiseases.map((disease, index) => ({
            label: disease,
            data: labels.map(area =>
                dataByArea[area].filter(d => d.DiagnosedDisease === disease).length
            ),
            backgroundColor: chartColors[index % chartColors.length],
            borderRadius: 6,
            barPercentage: 0.7
        }));

        chartData = { labels, datasets };
    }
</script>

<!-- <h3 class="text-center text-lg font-semibold mb-3 text-white">
    Distribuição de Doenças por Área Médica
</h3>

{#if data.length > 0}
    <div class="rounded-xl bg-[#1e1e2f] p-4 shadow-md">
        <div class="max-h-[500px] overflow-y-auto min-h-[300px]" style="height: {chartData.labels.length * 50}px">
            <Bar data={chartData} options={chartOptions} />
        </div>
    </div>
{:else}
    <p class="text-center text-gray-400 italic">Sem dados para exibir nesta seleção.</p>
{/if} -->
<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
    <h3 class="text-center text-lg font-semibold mb-3 text-black">
        Diagnósticos / Procedimentos
    </h3>
    {#if data.length > 0}
        <div class="max-h-[500px] overflow-y-auto min-h-[300px]" style="height: {chartData.labels.length * 50}px">
            <Bar data={chartData} options={chartOptions} />
        </div>
    {:else}
        <p class="text-center text-gray-400 italic mt-10">Sem dados para exibir nesta seleção.</p>
    {/if}
</div>