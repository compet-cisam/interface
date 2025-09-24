<script>
	import { Bar } from 'svelte-chartjs';
	import { Chart, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

	Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

	export let data = [];

	let chartData = {};
	let chartOptions = {
		indexAxis: 'y',
		responsive: true,
		maintainAspectRatio: false, // permite que o gráfico use a altura disponível
		plugins: { legend: {
			display: false },
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
				ticks: { color: '#ccc', font: { family: 'Poppins', size: 12 } },
				grid: { color: '#444' }
			},
			y: {
				ticks: { color: '#ccc', font: { family: 'Poppins', size: 12 } },
				grid: { color: '#444' }
			}
		},
		elements: {
			bar: {
				borderRadius: 6,
				barThickness: 24 // aumentamos a espessura mínima das barras
			}
		}
	};

	$: {
		const counts = {};
		data.forEach((item) => {
			const symptom = item.Symptom;
			counts[symptom] = (counts[symptom] || 0) + 1;
		});

		const labels = Object.keys(counts);
		const dataPoints = Object.values(counts);

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

{#if data.length > 0}
	<div class="rounded-xl bg-[#1e1e2f] p-4 shadow-md">
		<h3 class="text-center text-white text-lg font-semibold mb-3">Ocorrência por Motivação de Consulta</h3>
		<div class="max-h-[500px] overflow-y-auto min-h-[300px]" style="height: {data.length * 30}px">
			<Bar data={chartData} options={chartOptions} />
		</div>
	</div>
{:else}
	<p class="text-center text-gray-400 italic">Sem dados para exibir nesta seleção.</p>
{/if}
