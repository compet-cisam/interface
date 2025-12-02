<script>
    import { Doughnut } from 'svelte-chartjs';
    import 'chart.js/auto';

    export let data = []; 
    let chartData = {};


    const chartColors = ['#e15759', '#76b7b2', '#008000', '#bab0ab']; // Vermelho, Verde-água, Azul, Cinza

    let chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { 
                    color: '#gray', 
                    font: { family: 'Poppins', size: 12 },
                    padding: 15
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
        
        const histeroscopiaData = data.filter(item => item.especialidade === 'Histeroscopia Diagnóstica');

        const counts = {
            'Sangramento Ativo': 0,
            'Menopausa': 0,
            'Ciclo Menstrual Ativo': 0,
            'Indeterminado': 0
        };

        const longLabels = {
            sangramento: 'Estou com sangramento ativo (não é fluxo menstrual)',
            menopausa: 'Estou na Menopausa (não menstruo mais)',
            cicloAtivo: 'Ainda tenho ciclo menstrual ativo (ainda menstruo regularmente)'
        };

        histeroscopiaData.forEach(item => {
            const condicao = item.condicao_saude?.trim();
            
            if (condicao === longLabels.sangramento) {
                counts['Sangramento Ativo']++;
            } else if (condicao === longLabels.menopausa) {
                counts['Menopausa']++;
            } else if (condicao === longLabels.cicloAtivo) {
                counts['Ciclo Menstrual Ativo']++;
            } else {
                counts['Indeterminado']++; 
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
                borderColor: 'white',
                borderWidth: 2
            }]
        };
    }
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
    <h3 class="text-center text-lg font-semibold mb-3 text-black">Condição Menstrual</h3>
    <div class="relative flex-grow min-h-[250px]">
        {#if data.length > 0}
            <Doughnut data={chartData} options={chartOptions} />
        {:else}
            <p class="text-center text-black italic mt-10">Sem dados para exibir.</p>
        {/if}
    </div>
</div>