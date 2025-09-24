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
				bodyColor: '#eee',
				padding: 10,
				cornerRadius: 4
			}
		},
		scales: {
			x: {
				ticks: { color: '#black', precision: 0 }, 
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
			
			const comorbidityString = item.comorbidade?.trim();

			if (
				comorbidityString &&
				comorbidityString.toLowerCase() !== 'none' &&
				comorbidityString.toLowerCase() !== 'nega' &&
                comorbidityString.toLowerCase() !== 'outros'
			) {
				
				const individualComorbidities = comorbidityString.split('+').map((c) => c.trim());

				individualComorbidities.forEach((c) => {
					if (c) {
						
						acc[c] = (acc[c] || 0) + 1;
					}
				});
			}
			return acc;
		}, {});

	
		const sortedTop10 = Object.entries(counts)
			.sort(([, a], [, b]) => b - a)
			.slice(0, 10)
			

		const labels = sortedTop10.map((item) => item[0]);
		const dataPoints = sortedTop10.map((item) => item[1]);

		chartData = {
			labels,
			datasets: [
				{
					label: 'Pacientes',
					data: dataPoints,
					backgroundColor: '#af7aa1',
					borderRadius: 4,
					barThickness: 20
				}
			]
		};
	}
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
	<h3 class="text-center text-lg font-semibold mb-3 text-black">Comorbidades Prevalentes</h3>
	<div class="relative flex-grow min-h-[300px]">
		{#if data.length > 0 && chartData.labels?.length > 0}
			<Bar data={chartData} options={chartOptions} />
		{:else}
			<p class="text-center text-gray-400 italic mt-10">Sem dados de comorbidade para exibir.</p>
		{/if}
	</div>
</div>
