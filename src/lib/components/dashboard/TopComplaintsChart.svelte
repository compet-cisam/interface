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
			const symptom = item.Symptom;
			if (symptom) {
				// Garante que o sintoma não seja nulo/vazio
				acc[symptom] = (acc[symptom] || 0) + 1;
			}
			return acc;
		}, {});

		// Pega os 10 sintomas mais comuns e ordena
		const top10 = Object.entries(counts)
			.sort(([, a], [, b]) => b - a)
			.slice(0, 10);

		const labels = top10.map(([symptom]) => symptom);
		const dataPoints = top10.map(([, count]) => count);

		chartData = {
			labels,
			datasets: [
				{
					label: 'Contagem',
					data: dataPoints,
					backgroundColor: '#e15759',
					borderRadius: 4,
					//barThickness: 20,
					barPercentage: 0.8,
					categoryPercentage: 0.9
				}
			]
		};
	}
</script>

<div class="bg-[#1e1e2f] p-4 rounded-xl shadow-lg h-full flex flex-col">
	<h3 class="text-center text-lg font-semibold mb-3 text-white">Top 10 Queixas Gerais</h3>
	<div class="max-h-[500px] overflow-y-auto min-h-[300px]" >
		{#if data.length > 0}
            <Bar data={chartData} options={chartOptions} />
        {:else}
            <p class="text-center text-gray-400 italic mt-10">Sem dados para exibir.</p>
        {/if}
		<!-- <Bar data={chartData} options={chartOptions} /> -->
	</div>
</div>
