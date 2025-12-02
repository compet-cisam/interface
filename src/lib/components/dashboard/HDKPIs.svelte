<script>
    export let totalAppointments = 0;
    export let avgAge = 0;
    export let peakSymptom = '-';
    export let peakMonth = '-'; 
    export let avgTimeToConsult = 0;
    export let avgTimeToExam = 0;


    const monthMap = {
        '1': 'Janeiro',
        '2': 'Fevereiro',
        '3': 'Março',
        '4': 'Abril',
        '5': 'Maio',
        '6': 'Junho',
        '7': 'Julho',
        '8': 'Agosto',
        '9': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Dezembro',
        '-': '-' 
    };

    $: formattedPeakMonth = monthMap[peakMonth] || peakMonth;
</script>

<div class="grid grid-cols-1 sm:grid-cols-5 lg:grid-cols-5 gap-4 text-white">
    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Total de Atendimentos</p>
        <p class="text-3xl font-bold text-blue-400">{totalAppointments}</p>
    </div>

    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Média de Idade</p>
        <p class="text-3xl font-bold text-green-400">{Math.round(avgAge)} anos</p>
    </div>

    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Mês de Pico de Agendamentos</p>
        <p class="text-3xl font-bold text-yellow-400">{formattedPeakMonth}</p>
    </div>
    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Média de Dias do Agendamento à Teleconsulta</p>
        <p class="text-3xl font-bold text-cyan-400">{Math.round(avgTimeToConsult)} dias</p>
    </div>
    <div class="bg-[#fcfeff] p-5 rounded-xl shadow-lg flex flex-col justify-between">
        <p class="text-sm font-medium text-black">Média de Dias da Teleconsulta ao Exame</p>
        <p class="text-3xl font-bold text-orange-400">{Math.round(avgTimeToExam)} dias</p>
    </div> 
</div>