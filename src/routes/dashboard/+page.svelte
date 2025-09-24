<script>
	import { onMount } from 'svelte';
	import Papa from 'papaparse';

	// Componentes do Filtro e Gráficos
	import Filters from '$lib/components/dashboard/Filters.svelte';
	import MonthlyTrendChart from '$lib/components/dashboard/MonthlyTrendChart.svelte';
	import SymptomCountChart from '$lib/components/dashboard/SymptomCountChart.svelte';
	import DiseaseByAreaChart from '$lib/components/dashboard/DiseaseByAreaChart.svelte';

	//componentes para a visão GERAL
	import KPIs from '$lib/components/dashboard/KPIs.svelte';
	import AreaDistributionChart from '$lib/components/dashboard/AreaDistributionChart.svelte';
	import AgeDistributionChart from '$lib/components/dashboard/AgeDistributionChart.svelte';
	import TopComplaintsChart from '$lib/components/dashboard/TopComplaintsChart.svelte';

	import CityDistributionChart from '$lib/components/dashboard/CityDistributionChart.svelte';
	import MenstrualStatusChart from '$lib/components/dashboard/MenstrualStatusChart.svelte';

	import HisteroscopiaKPIs from '$lib/components/dashboard/HisteroscopiaKPIs.svelte';
	import ComorbidityChart from '$lib/components/dashboard/ComorbidityChart.svelte';
	import ObstetricProfileChart from '$lib/components/dashboard/ObstetricProfileChart.svelte';
	import MedicationChart from '$lib/components/dashboard/MedicationChart.svelte';
	import BasicKPIs from '$lib/components/dashboard/BasicKPIs.svelte';

	import IndicationChart from '$lib/components/dashboard/IndicationChart.svelte';

	// Variáveis de estado
	let allData = [];
	let filteredData = [];

	let allConditionsData = [];

	let selectedAreas = [];
	let selectedAgeRanges = [];
	let selectedMonths = [];
	let selectedYears = [];

	// Variáveis para os KPIs
	let totalAppointments = 0;
	let avgAge = 0;
	let busiestArea = '-';
	let peakMonth = '-';
	let peakSymptom = '-';
	let avgTimeToConsult = 0;
	let avgTimeToExam = 0;

	// KPIs da Visão Geral
	let generalKPIs = [];

	// KPIs da Visão de Histeroscopia
	let operationalKPIs = [];
	let clinicalKPIs = [];

	onMount(async () => {
		const response = await fetch('/medical_data.csv');
		const csvText = await response.text();

		Papa.parse(csvText, {
			header: true,
			skipEmptyLines: true,
			delimiter: ';',
			complete: (results) => {
				// Filtra linhas vazias ou malformadas que o Papa.parse pode criar
				allData = results.data.filter((item) => item.data_nascimento);
				filteredData = allData;
			}
		});
		Papa.parse('/medical_data.csv', {
			header: true,
			skipEmptyLines: true,
			delimiter: ';',
			complete: (results) => {
				allConditionsData = results.data.filter((item) => item.ID);
			}
		});
	});


	// Bloco reativo para calcular os KPIs
	$: {
		if (filteredData.length > 0) {
			totalAppointments = filteredData.length;

			// Média de Idade
			const totalAge = filteredData.reduce((sum, item) => sum + Number(item.Age), 0);
			avgAge = totalAge / totalAppointments;

			// Área Mais Ativa
			const areaCounts = filteredData.reduce((acc, item) => {
				acc[item.HealthArea] = (acc[item.HealthArea] || 0) + 1;
				return acc;
			}, {});
			busiestArea = Object.keys(areaCounts).reduce(
				(a, b) => (areaCounts[a] > areaCounts[b] ? a : b),
				'-'
			);

			// Mês de Pico
			const monthCounts = filteredData.reduce((acc, item) => {
				const month = item.AppointmentMonth?.trim();
				if (month) acc[month] = (acc[month] || 0) + 1;
				return acc;
			}, {});
			peakMonth = Object.keys(monthCounts).reduce(
				(a, b) => (monthCounts[a] > monthCounts[b] ? a : b),
				'-'
			);

			//Total de Sintomas
			const symptomCounts = filteredData.reduce((acc, item) => {
				const symptom = item.Symptom?.trim();

				if (symptom) {
					acc[symptom] = (acc[symptom] || 0) + 1;
				}
				return acc;
			}, {});

			peakSymptom = Object.keys(symptomCounts).reduce(
				(a, b) => (symptomCounts[a] > symptomCounts[b] ? a : b),
				'-'
			);

			// Média de tempo para a Teleconsulta (tempo_tc)
			const validTcTimes = filteredData
				.map((item) => Number(item.tempo_tc))
				.filter((time) => !isNaN(time) && time >= 0);

			if (validTcTimes.length > 0) {
				const sumTcTimes = validTcTimes.reduce((a, b) => a + b, 0);
				avgTimeToConsult = sumTcTimes / validTcTimes.length;
			} else {
				avgTimeToConsult = 0;
			}

			// Média de tempo da TC para o Exame (tempo_tc_hd)
			const validThdTimes = filteredData
				.map((item) => Number(item.tempo_tc_hd))
				.filter((time) => !isNaN(time) && time >= 0);

			if (validThdTimes.length > 0) {
				const sumThdTimes = validThdTimes.reduce((a, b) => a + b, 0);
				avgTimeToExam = sumThdTimes / validThdTimes.length;
			} else {
				avgTimeToExam = 0;
			}
		} else {
			// Reseta os KPIs se não houver dados
			totalAppointments = 0;
			avgAge = 0;
			busiestArea = '-';
			peakMonth = '-';
			peakSymptom = '-';
			avgTimeToConsult = 0;
			avgTimeToExam = 0;
		}
	}

	// --- Lógica de Filtragem e Cálculo de KPIs ---
	$: {
		// Filtra o CSV principal com base nos seletores
		if (allData.length > 0) {
			filteredData = allData.filter((item) => {
				const areaFilter = selectedAreas.length === 0 || selectedAreas.includes(item.HealthArea);
				const ageFilter =
					selectedAgeRanges.length === 0 || selectedAgeRanges.includes(item.AgeRange);
				const monthFilter =
					selectedMonths.length === 0 || selectedMonths.includes(item.AppointmentMonth?.trim());
				const yearFilter =
					selectedYears.length === 0 || selectedYears.includes(item.AppointmentYear);
				return areaFilter && ageFilter && monthFilter && yearFilter;
			});
		}

		// Calcula KPIs para a visão geral
		if (selectedAreas.length === 0 && filteredData.length > 0) {
			const totalAge = filteredData.reduce((sum, item) => sum + Number(item.Age), 0);
			const areaCounts = filteredData.reduce((acc, item) => {
				acc[item.HealthArea] = (acc[item.HealthArea] || 0) + 1;
				return acc;
			}, {});
			const monthCounts = filteredData.reduce((acc, item) => {
				const m = item.AppointmentMonth?.trim();
				if (m) acc[m] = (acc[m] || 0) + 1;
				return acc;
			}, {});
			const avgTimeToConsult =
				filteredData.reduce((sum, item) => {
					const time = Number(item.tempo_tc);
					return !isNaN(time) && time >= 0 ? sum + time : sum;
				}, 0) / filteredData.length;
			const avgTimeToExam =
				filteredData.reduce((sum, item) => {
					const time = Number(item.tempo_tc_hd);
					return !isNaN(time) && time >= 0 ? sum + time : sum;
				}, 0) / filteredData.length;

			generalKPIs = [
				{
					label: 'Total de Atendimentos',
					value: filteredData.length,
					color: 'text-blue-400'
				},
				{
					label: 'Média de Idade',
					value: `${(totalAge / filteredData.length).toFixed(1)} anos`,
					color: 'text-green-400'
				},
				{
					label: 'Área Mais Ativa',
					value: Object.keys(areaCounts).reduce(
						(a, b) => (areaCounts[a] > areaCounts[b] ? a : b),
						'-'
					),
					color: 'text-purple-400'
				},
				{
					label: 'Mês de Pico',
					value: Object.keys(monthCounts).reduce(
						(a, b) => (monthCounts[a] > monthCounts[b] ? a : b),
						'-'
					),
					color: 'text-yellow-400'
				},
				{
					label: 'Média Agendamento à TC',
					value: `${Math.round(avgTimeToConsult)} dias`,
					color: 'text-cyan-400'
				},
				{
					label: 'Média TC ao Exame',
					value: `${Math.round(avgTimeToExam)} dias`,
					color: 'text-orange-400'
				}
			];
		}

		// Calcula KPIs para a visão de Histeroscopia
		if (selectedAreas.length === 1 && selectedAreas[0] === 'Histeroscopia Diagnóstica') {
			const symptomCounts = filteredData.reduce((acc, item) => {
				acc[item.Symptom] = (acc[item.Symptom] || 0) + 1;
				return acc;
			}, {});

			if (allConditionsData.length > 0) {
				const polypCount = allConditionsData.filter(
					(item) => item.Polipo?.toLowerCase() === 'sim'
				).length;
				const miomaCount = allConditionsData.filter(
					(item) => item.Mioma?.toLowerCase() === 'sim'
				).length;
				clinicalKPIs = [
					{
						label: 'Pacientes na Amostra Clínica',
						value: allConditionsData.length,
						color: 'text-green-400'
					},
					{
						label: 'Taxa de Pólipos',
						value: `${((polypCount / allConditionsData.length) * 100).toFixed(1)}%`,
						color: 'text-purple-400'
					},
					{
						label: 'Taxa de Miomas',
						value: `${((miomaCount / allConditionsData.length) * 100).toFixed(1)}%`,
						color: 'text-red-400'
					}
				];
			}
		}
	}
</script>

<div class="flex h-screen w-full bg-[#efefff] text-gray-200 overflow-hidden">
	
	<aside class="lg:col-span-1 bg-[#fcfeff] p-6 rounded-xl shadow-lg">
		<div class="space-y-6">
			<div class="flex justify-center mb-4">
				<img src="/cisam-color-horizontal.png" alt="Logo NUTES CISAM" class="h-20" />
			</div>

			<Filters
				data={allData}
				bind:selectedAreas
				bind:selectedAgeRanges
				bind:selectedMonths
				bind:selectedYears
			/>
		</div>
	</aside>
	<main class="flex-1 p-6 lg:p-8 flex flex-col gap-6 overflow-y-auto">

		<header class="text-center">
			<div class="bg-[#fcfeff] p-2 rounded-xl shadow-lg flex flex-col justify-between"><h1 class="text-3xl font-bold font-primary text-black">
				Dashboard de Apoio à Decisão Médica
			</h1></div>
			
		</header>

		<section class="lg:col-span-3 flex flex-col gap-6">
			{#if selectedAreas.length === 0 || selectedAreas.length > 1}
				<KPIs
					{totalAppointments}
					{avgAge}
					{busiestArea}
					{peakMonth}
					{avgTimeToConsult}
					{avgTimeToExam}
				/>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<AreaDistributionChart data={filteredData} />
					<AgeDistributionChart data={filteredData} />
				</div>

				<MonthlyTrendChart data={filteredData} />
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<TopComplaintsChart data={filteredData} />
					<CityDistributionChart data={filteredData} />
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<ComorbidityChart data={filteredData} />
					<MedicationChart data={filteredData} />
					</div>
			{:else if selectedAreas.length === 1 && selectedAreas[0] === 'Histeroscopia Diagnóstica'}
				<div>
					<!-- <h2 class="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">
						Visão Operacional (Atendimentos)
					</h2> -->
					<BasicKPIs
						{totalAppointments}
						{avgAge}
						{peakSymptom}
						{peakMonth}
						{avgTimeToConsult}
						{avgTimeToExam}
					/>
					<!-- <HisteroscopiaKPIs kpis={operationalKPIs} /> -->
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<SymptomCountChart data={filteredData} />
					<AgeDistributionChart data={filteredData} />
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<IndicationChart data={filteredData} />
					<MenstrualStatusChart data={filteredData} />
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<MonthlyTrendChart data={filteredData} />
					<CityDistributionChart data={filteredData} />
				</div>
				<!-- <div>
					<DiseaseByAreaChart data={filteredData} />
				</div> -->
				<!-- <hr class="border-gray-700 my-4" /> -->

				<!-- <div>
					<h2 class="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">
						Visão Clínica (Amostra de Pacientes)
					</h2>
					-->
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<ComorbidityChart data={filteredData} />
					<ObstetricProfileChart data={filteredData} />
					<div class="md:col-span-2">
						<MedicationChart data={filteredData} />
					</div>
				</div>
			{:else if selectedAreas.length === 1 && selectedAreas[0] === 'Métodos Contraceptivos'}
				<!-- <div>
					<h2 class="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">
						Visão Operacional (Atendimentos)
					</h2>
				</div> -->
				<BasicKPIs
					{totalAppointments}
					{avgAge}
					{peakSymptom}
					{peakMonth}
					{avgTimeToConsult}
					{avgTimeToExam}
				/>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<SymptomCountChart data={filteredData} />
					<AgeDistributionChart data={filteredData} />
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<MonthlyTrendChart data={filteredData} />
					<CityDistributionChart data={filteredData} />
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<ComorbidityChart data={filteredData} />
					<MedicationChart data={filteredData} />
					</div>
			{:else if selectedAreas.length === 1 && selectedAreas[0] === 'Odontologia'}
				<!-- <div>
					<h2 class="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">
						Visão Operacional (Atendimentos)
					</h2>
				</div> -->
				<BasicKPIs
					{totalAppointments}
					{avgAge}
					{peakSymptom}
					{peakMonth}
					{avgTimeToConsult}
					{avgTimeToExam}
				/>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<SymptomCountChart data={filteredData} />
					<AgeDistributionChart data={filteredData} />
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<MonthlyTrendChart data={filteredData} />
					<CityDistributionChart data={filteredData} />
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<ComorbidityChart data={filteredData} />
					<MedicationChart data={filteredData} />
					</div>
			{/if}

		</section>
	</main>
</div>
