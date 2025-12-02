<script>
	import { Line } from 'svelte-chartjs';
	import 'chart.js/auto';

	export let data = [];
	export let selectedYears = [];

	const lineColors = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc949'];
	const monthsOfTheYear = [
		'janeiro',
		'fevereiro',
		'março',
		'abril',
		'maio',
		'junho',
		'julho',
		'agosto',
		'setembro',
		'outubro',
		'novembro',
		'dezembro'
	];

	let chartData = {};
	let chartOptions = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			legend: {
				display: true,
				position: 'right',
				labels: { color: 'rgba(99, 99, 99, 1)', padding: 15 }
			},
			tooltip: {
				backgroundColor: '#1e1e2f',
				titleColor: '#fff',
				bodyColor: '#ccc',
				padding: 10,
				cornerRadius: 4,
				borderColor: 'rgba(59, 130, 246, 1)',
				borderWidth: 1,
				mode: 'index',
				intersect: false
			}
		},
		scales: {
			x: { ticks: { color: '#9CA3AF' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
			y: {
				ticks: { color: '#9CA3AF', precision: 0 },
				grid: { color: 'rgba(99, 99, 99, 0.25)' },
				beginAtZero: true
			}
		},
		interaction: {
			mode: 'index',
			intersect: false
		}
	};

	$: {
    const dataByYear = data.reduce((acc, item) => {
        const year = item.marcacao_ano;
        if (year) {
            if (!acc[year]) acc[year] = [];
            acc[year].push(item);
        }
        return acc;
    }, {});

    const allYearsInData = Object.keys(dataByYear).sort();
    const yearsToDisplay = selectedYears.length > 0 ? selectedYears : allYearsInData;

    const yearDatasets = yearsToDisplay.map((year, index) => {
        const yearData = dataByYear[year] || [];
        
        const monthlyCounts = monthsOfTheYear.map((monthName, i) => {
            const monthNumber = String(i + 1); 
            return yearData.filter((item) => item.marcacao_mes === monthNumber).length;
        });

        return {
            label: year,
            data: monthlyCounts,
            borderColor: lineColors[index % lineColors.length],
            backgroundColor: lineColors[index % lineColors.length] + '33',
            tension: 0.3,
            fill: false,
            borderWidth: 2,
            pointRadius: 3
        };
    });

    let finalDatasets = [...yearDatasets];
    if (selectedYears.length >= 0 && allYearsInData.length > 1) {
        
        const totalCountsPerMonth = monthsOfTheYear.map((monthName, i) => {
            const monthNumber = String(i + 1); 
            return allYearsInData.reduce((sum, year) => {
                return (
                    sum + (dataByYear[year]?.filter((item) => item.marcacao_mes === monthNumber).length || 0)
                );
            }, 0);
        });

        const averageData = totalCountsPerMonth.map((total) => Math.round(total / allYearsInData.length));

        finalDatasets.push({
            label: 'Média Geral',
            data: averageData,
            borderColor: '#4A5568',
            backgroundColor: '#4A5568',
            tension: 0.1,
            fill: false,
            borderWidth: 2,
            pointRadius: 1,
            borderDash: [5, 5]
        });
    }

    chartData = {
        labels: monthsOfTheYear,
        datasets: finalDatasets
    };
}
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
	<h3 class="text-center text-lg font-semibold mb-3 text-black">Tendência de Agendamentos por Mês</h3>
	<div class="max-h-[500px] overflow-y-auto min-h-[300px]">
        {#if data.length > 0 && chartData.labels?.length > 0}
		<Line data={chartData} options={chartOptions} />
        {:else}
        <p class="text-center text-gray-400 italic mt-10">Sem dados para exibir.</p>
		{/if}
	</div>
</div>
