<script>
    import { Bar } from 'svelte-chartjs';
    import 'chart.js/auto';

    export let data = [];
    let chartData = {};

    let chartOptions = {
        indexAxis: 'y', 
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { display: false },
            tooltip: {
                backgroundColor: '#333',
                titleColor: '#fff',
                bodyColor: '#eee'
            }
        },
        scales: {
            x: { 
                ticks: { color: '#gray' }, 
                grid: { color: '#444' },
                title: {
                    display: true,
                    text: 'Nº de Pacientes',
                    color: '#aaa'
                }
            },
            y: { 
                ticks: { color: '#gray' }, 
                grid: { display: false } 
            }
        }
    };

    $: {
        const counts = data.reduce((acc, item) => {
            
            const city = item.cidade?.trim(); 

            if (city) { 
                const formattedCity = city.charAt(0).toUpperCase() + city.slice(1).toLowerCase();
                acc[formattedCity] = (acc[formattedCity] || 0) + 1;
            }
            return acc;
        }, {});

        const top10 = Object.entries(counts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 10);

    
        // const reversedTop10 = top10.reverse();

        const labels = top10.map(item => item[0]);
        const dataPoints = top10.map(item => item[1]);

        chartData = {
            labels,
            datasets: [{
                label: 'Pacientes',
                data: dataPoints,
                backgroundColor: '#76b7b2',
                borderRadius: 4
            }]
        };
    }
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
    <h3 class="text-center text-lg font-semibold mb-3 text-black">Incidência por Região de Origem</h3>
    <div class="relative flex-grow min-h-[300px]">
        {#if data.length > 0 && chartData.labels?.length > 0}
            <Bar data={chartData} options={chartOptions} />
        {:else}
            <p class="text-center text-gray-400 italic mt-10">Não há dados de cidade para exibir.</p>
        {/if}
    </div>
</div>