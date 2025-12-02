<script>
	export let data = [];
	export let selectedAreas = [];
	export let selectedAgeRanges = [];
	export let selectedRegion = [];
	export let selectedMonths = [];
	export let selectedYears = [];

	let uniqueAreas = [];
	let uniqueAgeRanges = [];
	let uniqueRegion = [];
	let uniqueMonths = [];
	let uniqueYears = [];

	const monthMap = [
        { num: '1', name: 'janeiro' },
        { num: '2', name: 'fevereiro' },
        { num: '3', name: 'março' },
        { num: '4', name: 'abril' },
        { num: '5', name: 'maio' },
        { num: '6', name: 'junho' },
        { num: '7', name: 'julho' },
        { num: '8', name: 'agosto' },
        { num: '9', name: 'setembro' },
        { num: '10', name: 'outubro' },
        { num: '11', name: 'novembro' },
        { num: '12', name: 'dezembro' }
    ];

    $: {
        if (data.length > 0) {
            uniqueAreas = [...new Set(data.map((item) => item.especialidade))].filter(Boolean);
            uniqueAgeRanges = [...new Set(data.map((item) => item.faixa_etaria))].filter(Boolean).sort();
            uniqueYears = [...new Set(data.map((item) => item.marcacao_ano))].filter(Boolean).sort();
            uniqueRegion = [...new Set(data.map(item => item.cidade))].filter(region => region && region.trim() !== '');

            const monthsInData = new Set(data.map((item) => item.marcacao_mes));
            
            uniqueMonths = monthMap.filter(monthObj => monthsInData.has(monthObj.num));
        }
    }
</script>

<div class="bg-[#fcfeff] text-black rounded-xl p-5 shadow-lg space-y-6 w-full">
	<!-- Área Médica -->
	<div>
		<h3 class="text-md font-semibold mb-2 text-black">Área Médica</h3>
		<div class="border border-gray-600 rounded-lg bg-[#fcfeff] p-3">
			<div class="max-h-[200px] overflow-y-auto space-y-0.5 pr-2">
				{#each uniqueAreas as area}
					<label class="flex items-center space-x-2 cursor-pointer">
						<input
							type="checkbox"
							class="accent-blue-500"
							bind:group={selectedAreas}
							value={area}
						/>
						<span class="text-sm">{area}</span>
					</label>
				{/each}
			</div>
		</div>
	</div>

	<!-- Faixa Etária -->
	<div>
		<h3 class="text-md font-semibold mb-2 text-black">Faixa Etária</h3>
		<div class="border border-gray-600 rounded-lg bg-[#fcfeff] p-3">
			<div class="max-h-[200px] overflow-y-auto space-y-0.5 pr-2">
				{#each uniqueAgeRanges as range}
					<label class="flex items-center space-x-2 cursor-pointer">
						<input
							type="checkbox"
							class="accent-blue-500"
							bind:group={selectedAgeRanges}
							value={range}
						/>
						<span class="text-sm">{range}</span>
					</label>
				{/each}
			</div>
		</div>
	</div>


	<div>
		<h3 class="text-md font-semibold mb-2 text-black">Região Estadual</h3>
		<div class="border border-gray-600 rounded-lg bg-[#fcfeff] p-3">
			<div class="max-h-[200px] overflow-y-auto space-y-0.5 pr-2">
				{#each uniqueRegion as region}
					<label class="flex items-center space-x-2 cursor-pointer">
						<input
							type="checkbox"
							class="accent-blue-500"
							bind:group={selectedRegion}
							value={region}
						/>
						<span class="text-sm">{region}</span>
					</label>
				{/each}
			</div>
		</div>
	</div>


	<!-- Ano -->
	<div>
		<h3 class="text-md font-semibold mb-2 text-black">Ano</h3>
		<div class="border border-gray-600 rounded-lg bg-[#fcfeff] p-3">
			<div class="max-h-[200px] overflow-y-auto space-y-1 pr-2">
				{#each uniqueYears as year}
					<label class="flex items-center space-x-2 cursor-pointer">
						<input
							type="checkbox"
							class="accent-blue-500"
							bind:group={selectedYears}
							value={year}
						/>
						<span class="text-sm">{year}</span>
					</label>
				{/each}
			</div>
		</div>
	</div>

	<!-- Mês -->
	<div>
    <h3 class="text-md font-semibold mb-2 text-black">Mês</h3>
    <div class="border border-gray-600 rounded-lg bg-[#fcfeff] p-3">
        <div class="max-h-[200px] overflow-y-auto space-y-1 pr-2">
            {#each uniqueMonths as monthObj}
                <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                        type="checkbox"
                        class="accent-blue-500"
                        bind:group={selectedMonths}
                        value={monthObj.num} />
                    <span class="text-sm">{monthObj.name}</span>
                </label>
            {/each}
        </div>
    </div>
</div>
</div>
