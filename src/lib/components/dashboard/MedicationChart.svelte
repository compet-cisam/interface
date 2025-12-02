<script>
	import { Bar } from 'svelte-chartjs';
	import 'chart.js/auto';

	export let data = [];
	let chartData = {};

	let chartOptions = {
		indexAxis: 'y',
		responsive: true,
		maintainAspectRatio: false,
		plugins: { legend: { display: false } },
		scales: {
			x: { ticks: { color: 'rgba(99, 99, 99, 1)' }, 
                grid: { color: 'rgba(99, 99, 99, 0.25)' } },
			y: { ticks: { color: '#black' }, grid: { display: false } }
		}
	};

	$: {
		const counts = data.reduce((acc, item) => {
			if (item.medicacao && item.medicacao.toLowerCase() !== 'none' &&
				item.medicacao.toLowerCase() !== 'nega' &&
                item.medicacao.toLowerCase() !== 'outros') {
				const medications = item.medicacao.split('+').map((m) => m.trim());
				medications.forEach((m) => {
					acc[m] = (acc[m] || 0) + 1;
				});
			}
			return acc;
		}, {});

		const top5 = Object.entries(counts)
			.sort(([, a], [, b]) => b - a)
			.slice(0, 5);
		const labels = top5.map(([med]) => med);
		const dataPoints = top5.map(([, count]) => count);

		chartData = {
			labels,
			datasets: [
				{
					label: 'Contagem',
					data: dataPoints,
					backgroundColor: '#f28e2b',
					borderRadius: 4
				}
			]
		};
	}
</script>

<div class="bg-[#fcfeff] p-4 rounded-xl shadow-lg h-full flex flex-col">
	<h3 class="text-center text-lg font-semibold mb-3 text-black">Principais Medicações em Uso</h3>
	<div class="relative flex-grow min-h-[250px]">
		{#if data.length > 0}
			<Bar data={chartData} options={chartOptions} />
		{:else}
			<p class="text-center text-gray-400 italic mt-10">Sem dados para exibir.</p>
		{/if}
	</div>
</div>
