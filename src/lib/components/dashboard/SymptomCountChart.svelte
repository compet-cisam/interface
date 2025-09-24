<script>
	import { Bar } from 'svelte-chartjs';
	import { Chart, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

	Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

	export let data = [];

	let chartData = {};
	let chartOptions = {
		indexAxis: 'y',
		responsive: true,
		maintainAspectRatio: false,
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
				ticks: { color: 'black', font: { family: 'Poppins', size: 12 } },
				grid: { color: '#ccc' }
			},
			y: {
				ticks: { color: 'black', font: { family: 'Poppins', size: 12 } },
				grid: {display: false}
			}
		},
		elements: {
			bar: {
				borderRadius: 6,
				barThickness: 24 
			}
		}
	};

	$: {
		const counts = {};
        data.forEach((item) => {
            if (item.Symptom && typeof item.Symptom === 'string') {

                const individualSymptoms = item.Symptom.split('+');

                individualSymptoms.forEach(symptomStr => {
                    const cleanedSymptom = symptomStr.trim();

                    if (cleanedSymptom) {
                        counts[cleanedSymptom] = (counts[cleanedSymptom] || 0) + 1;
                    }
                });
            }
        });

		// const labels = Object.keys(counts);
		// const dataPoints = Object.values(counts);

		const symptomEntries = Object.entries(counts);

        // Filtra o array, mantendo apenas os que têm contagem >= 2
        const filteredSymptoms = symptomEntries.filter(([symptom, count]) => count >= 2);
        // Converte o objeto de contagens para um array [chave, valor]
        // Ex: [['Infertilidade', 15], ['Dor pélvica', 10]]
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

{#if data.length > 0}
	<div class="rounded-xl bg-[#fcfeff] p-4 shadow-md">
		<h3 class="text-center text-black text-lg font-semibold mb-3">Ocorrência por Motivação de Consulta</h3>
		<div class="relative flex-grow h-[450px] overflow-y-auto pr-2">
            <div style="height: {Math.max(chartData.labels.length * 35, 450)}px">
                <Bar data={chartData} options={chartOptions} />
            </div>
        </div>
	</div>
{:else}
	<p class="text-center text-gray-400 italic">Sem dados para exibir nesta seleção.</p>
{/if}
