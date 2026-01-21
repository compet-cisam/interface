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
	import HDKPIs from '$lib/components/dashboard/HDKPIs.svelte';	
	import ComorbidityChart from '$lib/components/dashboard/ComorbidityChart.svelte';
	import ObstetricProfileChart from '$lib/components/dashboard/ObstetricProfileChart.svelte';
	import MedicationChart from '$lib/components/dashboard/MedicationChart.svelte';
	import BasicKPIs from '$lib/components/dashboard/BasicKPIs.svelte';

	import IndicationChart from '$lib/components/dashboard/IndicationChart.svelte';

	// Variáveis de estado
	let allData = [];
	let filteredData = [];
	let isSidebarOpen = false;

	let allConditionsData = [];

	let selectedAreas = [];
	let selectedAgeRanges = [];
	let selectedRegion = [];
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



	onMount(async () => {
		const response = await fetch('/dados_medicos/dados_medicos.csv');
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
		Papa.parse('/dados_medicos/dados_medicos.csv', {
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
		
        if (allData.length > 0) {
            filteredData = allData.filter((item) => {
                
                const areaFilter = selectedAreas.length === 0 || selectedAreas.includes(item.especialidade_extenso);                
                const ageFilter = selectedAgeRanges.length === 0 || selectedAgeRanges.includes(item.faixa_etaria);
                const monthFilter = selectedMonths.length === 0 || selectedMonths.includes(item.marcacao_mes?.trim());
                const yearFilter = selectedYears.length === 0 || selectedYears.includes(item.marcacao_ano);
                const regionFilter = selectedRegion.length === 0 || selectedRegion.includes(item.cidade); 
                
                return areaFilter && ageFilter && monthFilter && yearFilter && regionFilter;
            });
        } else {
            filteredData = [];
        }

        // 2. Cálculo de KPIs 
        if (filteredData.length > 0) {
            totalAppointments = filteredData.length;
            const totalAge = filteredData.reduce((sum, item) => sum + Number(item.idade_fixa), 0);
            avgAge = totalAge / totalAppointments;

            const areaCounts = filteredData.reduce((acc, item) => {
                acc[item.especialidade_extenso] = (acc[item.especialidade_extenso] || 0) + 1;
                return acc;
            }, {});
            busiestArea = Object.keys(areaCounts).reduce((a, b) => (areaCounts[a] > areaCounts[b] ? a : b), '-');

            const monthCounts = filteredData.reduce((acc, item) => {
                const month = item.marcacao_mes?.trim();
                if (month) acc[month] = (acc[month] || 0) + 1;
                return acc;
            }, {});
            peakMonth = Object.keys(monthCounts).reduce((a, b) => (monthCounts[a] > monthCounts[b] ? a : b), '-');

            const symptomCounts = filteredData.reduce((acc, item) => {
                const symptom = item.motivo_solicitacao?.trim();
                if (symptom) acc[symptom] = (acc[symptom] || 0) + 1;
                return acc;
            }, {});
            peakSymptom = Object.keys(symptomCounts).reduce((a, b) => (symptomCounts[a] > symptomCounts[b] ? a : b), '-');

            const validTcTimes = filteredData.map((item) => Number(item.tempo_tc)).filter((time) => !isNaN(time) && time >= 0);
            avgTimeToConsult = validTcTimes.length > 0 ? validTcTimes.reduce((a, b) => a + b, 0) / validTcTimes.length : 0;

            const validThdTimes = filteredData.map((item) => Number(item.tempo_tc_hd)).filter((time) => !isNaN(time) && time >= 0);
            avgTimeToExam = validThdTimes.length > 0 ? validThdTimes.reduce((a, b) => a + b, 0) / validThdTimes.length : 0;
        } else {
            // Reseta KPIs
            totalAppointments = 0;
            avgAge = 0;
            busiestArea = '-';
            peakMonth = '-';
            peakSymptom = '-';
            avgTimeToConsult = 0;
            avgTimeToExam = 0;
        }
	}

</script>

<div class="relative min-h-screen w-full bg-[#0f0f1a] text-gray-200">
	<button 
    on:click={() => isSidebarOpen = !isSidebarOpen}
    class="lg:hidden fixed top-4 left-4 z-30 p-2 bg-white text-gray-800 rounded-md shadow-lg transition-transform hover:scale-110 active:scale-95"
    aria-label="Abrir ou Fechar filtros"
>
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
</button>

	{#if isSidebarOpen}
		<div
			on:click={() => isSidebarOpen = !isSidebarOpen}
			class="lg:hidden fixed inset-0 bg-black/60 z-10 transition-opacity"
			aria-hidden="true"
		></div>
	{/if}
	<div class="flex h-screen w-full bg-[#efefff] text-gray-200 overflow-hidden">
		<aside
			class="w-full max-w-xs flex-shrink-0 bg-[#fcfeff] p-6 flex flex-col gap-6 overflow-y-auto
                fixed top-0 left-0 h-full z-20 transform transition-transform duration-300 ease-in-out
                lg:relative lg:translate-x-0"
			class:-translate-x-full={!isSidebarOpen}
			class:translate-x-0={isSidebarOpen}
		>
			<div class="space-y-6">
				<div class="flex justify-center mb-4">
					<img src="/cisam-color-horizontal.png" alt="Logo NUTES CISAM" class="h-20" />
				</div>

				<Filters
					data={allData}
					bind:selectedAreas
					bind:selectedAgeRanges
					bind:selectedRegion
					bind:selectedMonths
					bind:selectedYears
				/>
			</div>
		</aside>
		<main class="flex-1 p-6 lg:p-8 flex flex-col gap-6 overflow-y-auto">
			<header class="text-center">
				<div class="bg-[#fcfeff] p-2 rounded-xl shadow-lg flex flex-col justify-between">
					<h1 class="text-3xl font-bold font-primary text-black">
						Dashboard de Apoio à Decisão Médica
					</h1>
				</div>
			</header>

			<section class="lg:col-span-3 flex flex-col gap-6">
				{#if selectedAreas.length === 0 || selectedAreas.length > 1}
					<KPIs
						{totalAppointments}
						{avgAge}
						{busiestArea}
						{peakMonth}
						{avgTimeToConsult}
						
					/>

					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<AreaDistributionChart data={filteredData} />
						<AgeDistributionChart data={filteredData} />
					</div>

					<MonthlyTrendChart data={filteredData} {selectedYears} />
				
					<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
						<ComorbidityChart data={filteredData} />
						<MedicationChart data={filteredData} />
						<CityDistributionChart data={filteredData} />
					</div>
				{:else if selectedAreas.length === 1 && selectedAreas[0] === 'Histeroscopia Diagnóstica'}
					<div>
					
						<HDKPIs
							{totalAppointments}
							{avgAge}
							{peakSymptom}
							{peakMonth}
							{avgTimeToConsult}
							{avgTimeToExam}		
						/>						
						
					
					</div>
					<MonthlyTrendChart data={filteredData} />
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<IndicationChart data={filteredData} />
						<MenstrualStatusChart data={filteredData} />
					</div>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<ObstetricProfileChart data={filteredData} />
						<AgeDistributionChart data={filteredData} />
					</div>
					

					<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
						<ComorbidityChart data={filteredData} />
						<MedicationChart data={filteredData} />
						<CityDistributionChart data={filteredData} />
					</div>
				{:else if selectedAreas.length === 1 && selectedAreas[0] === 'Métodos Contraceptivos'}
					
					<BasicKPIs
						{totalAppointments}
						{avgAge}
						{peakSymptom}
						{peakMonth}
						{avgTimeToConsult}
					/>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<MonthlyTrendChart data={filteredData} />
						<ObstetricProfileChart data={filteredData} />
					</div>
					
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<SymptomCountChart data={filteredData} />
						<AgeDistributionChart data={filteredData} />
					</div>
					
					<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
						<ComorbidityChart data={filteredData} />
						<MedicationChart data={filteredData} />
						<CityDistributionChart data={filteredData} />
					</div>
				{:else if selectedAreas.length === 1 && selectedAreas[0] === 'Odontologia'}

					<BasicKPIs
						{totalAppointments}
						{avgAge}
						{peakSymptom}
						{peakMonth}
						{avgTimeToConsult}
						
					/>
					<MonthlyTrendChart data={filteredData} />
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<SymptomCountChart data={filteredData} />
						<AgeDistributionChart data={filteredData} />
					</div>
					
					<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
						<ComorbidityChart data={filteredData} />
						<MedicationChart data={filteredData} />
						<CityDistributionChart data={filteredData} />
					</div>
				{:else}	
					<BasicKPIs
						{totalAppointments}
						{avgAge}
						{peakSymptom}
						{peakMonth}
						{avgTimeToConsult}
						
					/>
					<MonthlyTrendChart data={filteredData} />
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<SymptomCountChart data={filteredData} />
						<AgeDistributionChart data={filteredData} />
					</div>
					
					<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
						<ComorbidityChart data={filteredData} />
						<MedicationChart data={filteredData} />
						<CityDistributionChart data={filteredData} />
					</div>
				{/if}
			</section>
		</main>
	</div>
</div>
