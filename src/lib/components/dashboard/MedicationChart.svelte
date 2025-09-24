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
			x: { ticks: { color: '#ccc' }, grid: { color: '#444' } },
			y: { ticks: { color: '#ccc' }, grid: { display: false } }
		}
	};

	$: {
		const counts = data.reduce((acc, item) => {
			if (item.Medicacao && item.Medicacao.toLowerCase() !== 'none') {
				const medications = item.Medicacao.split('+').map((m) => m.trim());
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

<div class="bg-[#1e1e2f] p-4 rounded-xl shadow-lg h-full flex flex-col">
	<h3 class="text-center text-lg font-semibold mb-3 text-white">Top 5 Medicações em Uso</h3>
	<div class="relative flex-grow min-h-[250px]">
		{#if data.length > 0}
			<Bar {chartData} {chartOptions} />
		{:else}
			<p class="text-center text-gray-400 italic mt-10">Carregando dados...</p>
		{/if}
	</div>
</div>
