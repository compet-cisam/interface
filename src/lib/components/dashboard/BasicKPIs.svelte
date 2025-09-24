<script>
	export let totalAppointments = 0;
	export let avgAge = 0;
	export let peakMonth = '-';
	export let peakSymptom = '-';
	export let avgTimeToConsult = 0;
	export let avgTimeToExam = 0;
</script>

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-white">
	<div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
		<p class="text-sm font-medium text-gray-800">Total de Atendimentos</p>
		<p class="text-3xl font-bold text-blue-400">{totalAppointments}</p>
	</div>

	<div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
		<p class="text-sm font-medium text-gray-800">Média de Idade</p>
		<p class="text-3xl font-bold text-green-400">{avgAge.toFixed(1)} anos</p>
	</div>

	<div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
		<p class="text-sm font-medium text-gray-800">Principal Indicação</p>
		<p class="text-3xl font-bold text-purple-400">{peakSymptom}</p>
	</div>

	<div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
		<p class="text-sm font-medium text-gray-800">Mês de Pico</p>
		<p class="text-3xl font-bold text-yellow-400">{peakMonth}</p>
	</div>
	<div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
		<p class="text-sm font-medium text-gray-800">Média Agendamento à TC</p>
		<p class="text-3xl font-bold text-cyan-400">{Math.round(avgTimeToConsult)} dias</p>
	</div>

	<div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
		<p class="text-sm font-medium text-gray-800">Média TC ao Exame</p>
		<p class="text-3xl font-bold text-orange-400">{Math.round(avgTimeToExam)} dias</p>
	</div>
</div>
