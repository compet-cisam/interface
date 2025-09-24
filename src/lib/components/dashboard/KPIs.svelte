<script>
    export let totalAppointments = 0;
    export let avgAge = 0;
    export let busiestArea = '-';
    export let peakMonth = '-';
</script>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-white">
    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Total de Atendimentos</p>
        <p class="text-3xl font-bold text-blue-400">{totalAppointments}</p>
    </div>

    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Média de Idade</p>
        <p class="text-3xl font-bold text-green-400">{avgAge.toFixed(1)} anos</p>
    </div>

    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Área Mais Ativa</p>
        <p class="text-3xl font-bold text-purple-400 truncate">{busiestArea}</p>
    </div>

    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Mês de Pico</p>
        <p class="text-3xl font-bold text-yellow-400">{peakMonth}</p>
    </div>
</div>