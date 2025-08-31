<script lang="ts">
	import { onMount } from 'svelte';
	import Papa from 'papaparse';

	// Componentes do Filtro e Gráficos
	import Filters from '$lib/components/dashboard/Filters.svelte';
	import MonthlyTrendChart from '$lib/components/dashboard/MonthlyTrendChart.svelte';
	import SymptomCountChart from '$lib/components/dashboard/SymptomCountChart.svelte';
	import KPIs from '$lib/components/dashboard/KPIs.svelte';
	import AreaDistributionChart from '$lib/components/dashboard/AreaDistributionChart.svelte';
	import AgeDistributionChart from '$lib/components/dashboard/AgeDistributionChart.svelte';
	import HisteroscopiaKPIs from '$lib/components/dashboard/HisteroscopiaKPIs.svelte';
	import ComorbidityChart from '$lib/components/dashboard/ComorbidityChart.svelte';
	import ObstetricProfileChart from '$lib/components/dashboard/ObstetricProfileChart.svelte';
	import MedicationChart from '$lib/components/dashboard/MedicationChart.svelte';

	// --- Definição de Tipos de Dados ---
	interface MedicalDataRecord {
		PatientID: string;
		HealthArea: string;
		Age: string;
		AgeRange: string;
		AppointmentMonth: string;
		AppointmentYear: string;
		Symptom: string;
	}

	interface ConditionRecord {
		ID: string;
		Polipo?: string;
		Mioma?: string;
	}

	interface Kpi {
		label: string;
		value: string | number;
		color: string;
	}

	// --- Variáveis de Estado ---
	let allData: MedicalDataRecord[] = [];
	let filteredData: MedicalDataRecord[] = [];
	let allConditionsData: ConditionRecord[] = [];

	// Filtros
	let selectedAreas: string[] = [];
	let selectedAgeRanges: string[] = [];
	let selectedMonths: string[] = [];
	let selectedYears: string[] = [];

	// KPIs da Visão Geral (variáveis individuais)
	let totalAppointments = 0;
	let avgAge = 0;
	let busiestArea = '-';
	let peakMonth = '-';
	
	// KPIs Específicos
	let operationalKPIs: Kpi[] = [];
	let clinicalKPIs: Kpi[] = [];

	onMount(async () => {
		const response = await fetch('/medical_data.csv');
		const csvText = await response.text();
		Papa.parse<MedicalDataRecord>(csvText, {
			header: true,
			skipEmptyLines: true,
			delimiter: ';',
			complete: (results: Papa.ParseResult<MedicalDataRecord>) => {
				allData = results.data.filter((item: MedicalDataRecord) => item.PatientID);
			}
		});

		const conditionsResponse = await fetch('/hd-condicoes.csv');
		const conditionsCsvText = await conditionsResponse.text();
		Papa.parse<ConditionRecord>(conditionsCsvText, {
			header: true,
			skipEmptyLines: true,
			delimiter: ';',
			complete: (results: Papa.ParseResult<ConditionRecord>) => {
				allConditionsData = results.data.filter((item: ConditionRecord) => item.ID);
			}
		});
	});

	// --- Bloco Reativo Principal ---
	$: {
		// 1. Filtragem dos dados
		if (allData.length > 0) {
			filteredData = allData.filter((item: MedicalDataRecord) => {
				const areaFilter = selectedAreas.length === 0 || selectedAreas.includes(item.HealthArea);
				const ageFilter =
					selectedAgeRanges.length === 0 || selectedAgeRanges.includes(item.AgeRange);
				const monthFilter =
					selectedMonths.length === 0 || selectedMonths.includes(item.AppointmentMonth?.trim());
				const yearFilter =
					selectedYears.length === 0 || selectedYears.includes(item.AppointmentYear);
				return areaFilter && ageFilter && monthFilter && yearFilter;
			});
		} else {
			filteredData = [];
		}

		// 2. Cálculo dos KPIs com base nos dados filtrados
		if (filteredData.length > 0) {
			totalAppointments = filteredData.length;
			const totalAge = filteredData.reduce((sum, item: MedicalDataRecord) => sum + Number(item.Age), 0);
			avgAge = totalAge / totalAppointments;

			const areaCounts = filteredData.reduce((acc: Record<string, number>, item: MedicalDataRecord) => {
				acc[item.HealthArea] = (acc[item.HealthArea] || 0) + 1;
				return acc;
			}, {});
			busiestArea = Object.keys(areaCounts).reduce((a, b) => (areaCounts[a] > areaCounts[b] ? a : b), '-');
			
			const monthCounts = filteredData.reduce((acc: Record<string, number>, item: MedicalDataRecord) => {
				const m = item.AppointmentMonth?.trim();
				if (m) acc[m] = (acc[m] || 0) + 1;
				return acc;
			}, {});
			peakMonth = Object.keys(monthCounts).reduce((a, b) => (monthCounts[a] > monthCounts[b] ? a : b), '-');

		} else {
			totalAppointments = 0;
			avgAge = 0;
			busiestArea = '-';
			peakMonth = '-';
		}

		// KPIs da Visão de Histeroscopia
		if (selectedAreas.length === 1 && selectedAreas[0] === 'Histeroscopia Diagnóstica') {
			const symptomCounts = filteredData.reduce((acc: Record<string, number>, item: MedicalDataRecord) => {
				acc[item.Symptom] = (acc[item.Symptom] || 0) + 1;
				return acc;
			}, {});
			operationalKPIs = [
				{ label: 'Total de Procedimentos', value: filteredData.length, color: 'text-blue-400' },
				{ label: 'Principal Indicação', value: Object.keys(symptomCounts).reduce((a, b) => (symptomCounts[a] > symptomCounts[b] ? a : b), '-'), color: 'text-yellow-400' }
			];

			if (allConditionsData.length > 0) {
				const polypCount = allConditionsData.filter((item: ConditionRecord) => item.Polipo?.toLowerCase() === 'sim').length;
				const miomaCount = allConditionsData.filter((item: ConditionRecord) => item.Mioma?.toLowerCase() === 'sim').length;
				clinicalKPIs = [
					{ label: 'Pacientes na Amostra Clínica', value: allConditionsData.length, color: 'text-green-400' },
					{ label: 'Taxa de Pólipos', value: `${((polypCount / allConditionsData.length) * 100).toFixed(1)}%`, color: 'text-purple-400' },
					{ label: 'Taxa de Miomas', value: `${((miomaCount / allConditionsData.length) * 100).toFixed(1)}%`, color: 'text-red-400' }
				];
			}
		} else {
			operationalKPIs = [];
			clinicalKPIs = [];
		}
	}
</script>

<div class="min-h-screen w-full bg-[#0f0f1a] text-gray-200 p-4 md:p-6 lg:p-8 flex flex-col gap-6">
    <header class="text-center">
        <h1 class="text-3xl font-bold font-primary text-white">Dashboard de Apoio à Decisão Médica</h1>
    </header>

    <main class="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-grow">
        <aside class="lg:col-span-1 bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
            <div class="space-y-6">
                <div class="flex justify-center">
                    <img src="/logo-nutes.png" alt="Logo NUTES CISAM" class="h-20" />
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

        <section class="lg:col-span-3 flex flex-col gap-6">
            {#if selectedAreas.length === 0}
                <!-- Visão Geral -->
                <KPIs {totalAppointments} {avgAge} {busiestArea} {peakMonth} />
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <AreaDistributionChart data={filteredData} />
                    <AgeDistributionChart data={filteredData} />
                </div>
                <MonthlyTrendChart data={filteredData} />

            {:else if selectedAreas.length === 1 && selectedAreas[0] === 'Histeroscopia Diagnóstica'}
                <!-- Visão Histeroscopia -->
                <div>
                    <h2 class="text-xl font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">
                        Visão Operacional (Atendimentos)
                    </h2>
                    <HisteroscopiaKPIs kpis={operationalKPIs} />
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <SymptomCountChart data={filteredData} />
                    <AgeDistributionChart data={filteredData} />
                </div>
                <MonthlyTrendChart data={filteredData} />
                
            {:else if selectedAreas.length === 1 && selectedAreas[0] === 'Planejamento Reprodutivo'}
                 <!-- Visão Planejamento Reprodutivo -->
                 <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <SymptomCountChart data={filteredData} />
                    <AgeDistributionChart data={filteredData} />
                </div>
                <MonthlyTrendChart data={filteredData} />

            {:else}
                <!-- Visão para Múltiplas Áreas ou Área sem Dashboard Específico -->
                 <div class="bg-[#1e1e2f] p-8 rounded-xl shadow-lg text-center h-full flex flex-col justify-center">
                     <h2 class="text-2xl font-bold text-white mb-2">
                         Dashboard para: {selectedAreas.join(', ')}
                     </h2>
                     <p class="text-gray-400">
                         (Aqui serão exibidos os gráficos específicos para a(s) área(s) selecionada(s))
                     </p>
                 </div>
            {/if}
        </section>
    </main>
</div>

