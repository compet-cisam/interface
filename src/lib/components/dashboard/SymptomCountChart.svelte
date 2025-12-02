<script>
    import { Bar } from 'svelte-chartjs';
    import { Chart, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

    Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

    export let data = [];

    let chartData = {};
    
    // Configuração do gráfico
    let chartOptions = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        layout: {
            padding: {
                top: 0,
                bottom: 0
            }
        },
        plugins: { 
            legend: { display: false },
            tooltip: {
                backgroundColor: '#333',
                titleColor: '#fff',
                bodyColor: '#eee',
                padding: 10,
                cornerRadius: 4
            }
        },
        scales: {
            x: {
                display: false, 
                grid: { display: false }
            },
            y: {
                display: false, 
                grid: { display: false }
            }
        },
        elements: {
            bar: {
                borderRadius: 4,
                barThickness: 28 
            }
        }
    };


    $: {
        const counts = {};
        data.forEach((item) => {
            if (item.motivo_solicitacao && typeof item.motivo_solicitacao === 'string') {
                const individualSymptoms = item.motivo_solicitacao.split('+');
                individualSymptoms.forEach(symptomStr => {
                    const cleanedSymptom = symptomStr.trim();
                    if (cleanedSymptom) {
                        counts[cleanedSymptom] = (counts[cleanedSymptom] || 0) + 1;
                    }
                });
            }
        });

        const symptomEntries = Object.entries(counts);
        const filteredSymptoms = symptomEntries.filter(([symptom, count]) => count >= 2);
        const sortedSymptoms = filteredSymptoms.sort(([, a], [, b]) => b - a);

        const labels = sortedSymptoms.map(item => item[0]); 
        const dataPoints = sortedSymptoms.map(item => item[1]);

        chartData = {
            labels,
            datasets: [
                {
                    label: 'Sintomas',
                    data: dataPoints,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }
            ]
        };
    }
</script>



<div class="rounded-xl bg-[#fcfeff] p-4 shadow-md h-full flex flex-col">
    <h3 class="text-center text-black text-lg font-semibold mb-3">Ocorrência por Motivação de Consulta</h3>
    
    <div class="relative flex-grow h-[450px] overflow-y-auto pr-2">

        {#if data.length > 0 && chartData.labels?.length > 0}
            <div class="flex flex-row" style="height: {Math.max(chartData.labels.length * 55, 450)}px">
                
                <div class="w-[40%] flex flex-col justify-around pr-2 border-r border-gray-100">
                    {#each chartData.labels as label}
                        <div class="h-[55px] flex items-center justify-end w-full marquee-container group cursor-default">
                            <span class="text-xs text-right text-gray-700 font-medium font-primary marquee-content px-1">
                                {label}
                            </span>
                            
                            {#if label.length > 25}
                                <div class="absolute left-0 top-0 bottom-0 w-4 bg-gradient-to-r from-[#fcfeff] to-transparent pointer-events-none"></div>
                            {/if}
                        </div>
                    {/each}
                </div>

                <div class="w-[60%] h-full relative">
                    <div class="absolute inset-0">
                        <Bar data={chartData} options={chartOptions} />
                    </div>
                </div>

            </div>
        {:else}
            <div class="flex items-center justify-center h-full">
                <p class="text-center text-gray-500 italic">Sem dados para exibir nesta seleção.</p>
            </div>
        {/if}
    </div>
</div>