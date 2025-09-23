<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	interface UserData {
		fullName: string;
		motherName: string;
		fatherName: string;
		birthDate: string;
		cpf: string;
		email: string;
	}

	interface Exam {
		type: string;
		fileName: string;
		date: string;
		dataUrl: string;
	}

	let patient: UserData | null = null;
	let submittedExams: Exam[] = [];

	let showModal = false;
	let selectedExam: Exam | null = null;

	onMount(() => {
		const { cpf } = $page.params;

		const patientDataString = localStorage.getItem(cpf);
		if (patientDataString) {
			patient = JSON.parse(patientDataString) as UserData;

			const patientExamsString = localStorage.getItem(`exams_${patient.cpf}`);
			if (patientExamsString) {
				submittedExams = JSON.parse(patientExamsString);
			}
		} else {
			goto('/profissional/painel');
		}
	});

	function viewExam(exam: Exam) {
		selectedExam = exam;
		showModal = true;
	}

	function handleBackdropClick(event: MouseEvent) {
		if (event.currentTarget === event.target) {
			showModal = false;
		}
	}

	function formatCPF(cpf: string) {
		if (!cpf) return '';
		return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
	}

	function formatDate(dateString: string) {
		if (!dateString) return '';
		const [year, month, day] = dateString.split('-');
		return `${day}/${month}/${year}`;
	}
</script>

{#if showModal && selectedExam}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75"
		on:click={handleBackdropClick}
		role="button"
		tabindex="0"
	>
		<div
			class="relative mx-4 max-h-[90vh] w-full max-w-4xl rounded-lg bg-white p-6"
			role="dialog"
			aria-modal="true"
		>
			<h3 class="text-2xl font-bold mb-4">{selectedExam.fileName}</h3>
			<div class="overflow-auto max-h-[70vh]">
				<img src={selectedExam.dataUrl} alt={selectedExam.fileName} class="w-full h-auto" />
			</div>
			<button
				on:click={() => (showModal = false)}
				class="absolute top-4 right-4 text-gray-500 hover:text-gray-800"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-8 w-8"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					><path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M6 18L18 6M6 6l12 12"
					/></svg
				>
			</button>
		</div>
	</div>
{/if}

<div class="min-h-screen bg-gray-50 flex-grow" style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);">
	<main class="container mx-auto p-4 sm:p-6 lg:p-8">
		<div class="mx-auto max-w-2xl space-y-8">
			{#if patient}
				<div class="rounded-2xl bg-white p-6 sm:p-8 shadow-lg">
					<h1 class="text-3xl font-bold text-gray-900">Dados do Paciente</h1>
					<div class="mt-6 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8 text-lg">
						<div>
							<dt class="text-base font-semibold text-gray-500">Nome Completo</dt>
							<dd class="mt-1 text-gray-900">{patient.fullName}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">CPF</dt>
							<dd class="mt-1 text-gray-900">{formatCPF(patient.cpf)}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">Data de Nascimento</dt>
							<dd class="mt-1 text-gray-900">{formatDate(patient.birthDate)}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">E-mail</dt>
							<dd class="mt-1 text-gray-900">{patient.email}</dd>
						</div>
					</div>
				</div>
			{/if}

			<div class="rounded-2xl bg-white p-6 sm:p-8 shadow-lg">
				<h2 class="text-3xl font-bold text-gray-900">Exames Enviados</h2>
				<ul class="mt-6 space-y-4">
					{#if submittedExams.length > 0}
						{#each submittedExams as exam}
							<li class="flex items-center justify-between rounded-lg border bg-gray-50 p-5">
								<div>
									<p class="font-semibold text-lg text-gray-800">{exam.fileName}</p>
									<p class="text-base text-gray-500">Tipo: {exam.type}</p>
									<p class="text-base text-gray-500">Enviado em: {exam.date}</p>
								</div>
								<button on:click={() => viewExam(exam)} type="button" class="text-base font-medium text-primary hover:text-primary-hover">Visualizar</button>
							</li>
						{/each}
					{:else}
						<li class="text-center text-gray-500 py-4 text-lg">
							Este paciente ainda não enviou nenhum exame.
						</li>
					{/if}
				</ul>
			</div>

			<div class="pt-4 text-center">
				<a
					href="/profissional/painel"
					class="inline-block rounded-md border border-gray-300 bg-white px-10 py-4 text-lg font-bold text-gray-700 shadow-sm hover:bg-gray-50"
				>
					Voltar ao Painel do Profissional
				</a>
			</div>
		</div>
	</main>
</div>

