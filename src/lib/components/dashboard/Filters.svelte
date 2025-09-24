<script>
    export let data = [];
    export let selectedAreas = [];
    export let selectedAgeRanges = [];
    export let selectedMonths = []; 
    export let selectedYears = [];  

    let uniqueAreas = [];
    let uniqueAgeRanges = [];
    let uniqueMonths = []; 
    let uniqueYears = [];  

    const orderedMonths = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];

    $: {
        if (data.length > 0) {
            uniqueAreas = [...new Set(data.map(item => item.HealthArea))];
            uniqueAgeRanges = [...new Set(data.map(item => item.AgeRange))].sort();
            uniqueYears = [...new Set(data.map(item => item.AppointmentYear))].sort();

            const monthsInData = new Set(data.map(item => item.AppointmentMonth));
            uniqueMonths = orderedMonths.filter(month => monthsInData.has(month));
        }
    }
</script>

<div class="bg-[#fcfeff] text-black rounded-xl p-5 shadow-lg space-y-6 w-full">
    
    <!-- Área Médica -->
    <div>
        <h3 class="text-md font-semibold mb-2 text-black">Área Médica</h3>
        <div class="space-y-2">
            {#each uniqueAreas as area}
                <label class="flex items-center space-x-2 cursor-pointer">
                    <input type="checkbox" class="accent-blue-500" bind:group={selectedAreas} value={area} />
                    <span class="text-sm">{area}</span>
                </label>
            {/each}
        </div>
    </div>

    <!-- Faixa Etária -->
    <div>
        <h3 class="text-md font-semibold mb-2 text-black">Faixa Etária</h3>
        <div class="space-y-2">
            {#each uniqueAgeRanges as range}
                <label class="flex items-center space-x-2 cursor-pointer">
                    <input type="checkbox" class="accent-blue-500" bind:group={selectedAgeRanges} value={range} />
                    <span class="text-sm">{range}</span>
                </label>
            {/each}
        </div>
    </div>

    <!-- Ano -->
    <div>
        <h3 class="text-md font-semibold mb-2 text-black">Ano</h3>
        <div class="space-y-2">
            {#each uniqueYears as year}
                <label class="flex items-center space-x-2 cursor-pointer">
                    <input type="checkbox" class="accent-blue-500" bind:group={selectedYears} value={year} />
                    <span class="text-sm">{year}</span>
                </label>
            {/each}
        </div>
    </div>

    <!-- Mês -->
    <div>
        <h3 class="text-md font-semibold mb-2 text-black">Mês</h3>
        <div class="border border-gray-600 rounded-lg bg-[#fcfeff] p-3">
            <div class="max-h-[200px] overflow-y-auto space-y-2 pr-2">
                {#each uniqueMonths as month}
                    <label class="flex items-center space-x-2 cursor-pointer">
                        <input type="checkbox" class="accent-blue-500" bind:group={selectedMonths} value={month} />
                        <span class="text-sm">{month}</span>
                    </label>
                {/each}
            </div>
        </div>
    </div>
</div>