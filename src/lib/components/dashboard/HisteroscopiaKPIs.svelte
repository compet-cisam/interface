<script>
    export let title = "KPIs";
    export let kpis = [];
</script>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-white">
    {#each kpis as kpi}
    <div class="bg-[#1e1e2f] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-gray-400">{kpi.label}</p>
        <p class="text-3xl font-bold {kpi.color || 'text-white'} truncate">{kpi.value}</p>
    </div>
    {/each}
</div>