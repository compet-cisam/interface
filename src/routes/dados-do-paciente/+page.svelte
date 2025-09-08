<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	interface UserData {
		fullName: string;
		motherName: string;
		fatherName: string;
		birthDate: string;
		cpf: string;
		email: string;
	}

	interface Exam {
		id: number;
		type: string;
		fileName: string;
		timestamp: string;
		dataUrl: string;
	}

	let user: UserData | null = null;
	let submittedExams: Exam[] = [];

	let showModal = false;
	let selectedExam: Exam | null = null;

	let showDeleteConfirm = false;
	let examToDelete: Exam | null = null;

	onMount(() => {
		const userDataString = sessionStorage.getItem('loggedInUser');
		if (userDataString) {
			user = JSON.parse(userDataString) as UserData;
			loadExams();
		} else {
			goto('/login');
		}

		const handleEscape = (event: KeyboardEvent) => {
			if (event.key === 'Escape') {
				showModal = false;
				showDeleteConfirm = false;
			}
		};

		window.addEventListener('keydown', handleEscape);
		return () => {
			window.removeEventListener('keydown', handleEscape);
		};
	});

	function loadExams() {
		if (user) {
			const userExamsString = localStorage.getItem(`exams_${user.cpf}`);
			if (userExamsString) {
				submittedExams = JSON.parse(userExamsString);
			}
		}
	}

	function requestDeleteExam(exam: Exam) {
		examToDelete = exam;
		showDeleteConfirm = true;
	}

	function confirmDelete() {
		if (user && examToDelete) {
			const updatedExams = submittedExams.filter((exam) => exam.id !== examToDelete!.id);
			localStorage.setItem(`exams_${user.cpf}`, JSON.stringify(updatedExams));
			submittedExams = updatedExams;
			showToast('Exame removido com sucesso.', 'success');
		}
		showDeleteConfirm = false;
		examToDelete = null;
	}

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
		aria-label="Fechar modal"
	>
		<div
			class="relative mx-4 max-h-[90vh] w-full max-w-4xl rounded-lg bg-white p-6"
			role="dialog"
			aria-modal="true"
			aria-labelledby="modal-title"
		>
			<h3 id="modal-title" class="text-2xl font-bold mb-4">{selectedExam.fileName}</h3>
			<div class="overflow-auto max-h-[70vh]">
				{#if selectedExam.dataUrl.startsWith('data:image')}
					<img src={selectedExam.dataUrl} alt={selectedExam.fileName} class="w-full h-auto" />
				{:else if selectedExam.dataUrl.startsWith('data:application/pdf')}
					<iframe
						src={selectedExam.dataUrl}
						class="w-full h-[65vh]"
						title={selectedExam.fileName}></iframe>
				{:else}
					<p class="text-center text-gray-600 my-8">
						A pré-visualização não está disponível para este tipo de ficheiro. <a
							href={selectedExam.dataUrl}
							download={selectedExam.fileName}
							class="text-primary font-semibold">Faça o download aqui.</a>
					</p>
				{/if}
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

{#if showDeleteConfirm && examToDelete}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
		<div
			class="w-full max-w-md rounded-lg bg-white p-8 shadow-xl"
			role="alertdialog"
			aria-modal="true"
			aria-labelledby="delete-title"
		>
			<h3 id="delete-title" class="text-2xl font-bold text-gray-900">Confirmar Remoção</h3>
			<p class="mt-4 text-lg text-gray-600">
				Tem a certeza de que deseja remover o exame "{examToDelete.fileName}"? Esta ação não pode ser
				desfeita.
			</p>
			<div class="mt-6 flex justify-end space-x-4">
				<button
					on:click={() => (showDeleteConfirm = false)}
					class="rounded-md border border-gray-300 bg-white px-6 py-2 text-base font-semibold text-gray-700 hover:bg-gray-50"
				>
					Cancelar
				</button>
				<button
					on:click={confirmDelete}
					class="rounded-md border border-transparent bg-danger px-6 py-2 text-base font-semibold text-white hover:bg-danger-hover"
				>
					Remover
				</button>
			</div>
		</div>
	</div>
{/if}

<div
	class="min-h-screen bg-gray-50 flex-grow"
	style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);"
>
	<main class="container mx-auto p-4 sm:p-6 lg:p-8">
		<div class="mx-auto max-w-3xl space-y-8">
			{#if user}
				<div class="rounded-2xl bg-white p-6 sm:p-8 shadow-lg">
					<h1 class="text-3xl font-bold text-gray-900">Meus Dados Pessoais</h1>
					<div class="mt-6 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8 text-lg">
						<div>
							<dt class="text-base font-semibold text-gray-500">Nome Completo</dt>
							<dd class="mt-1 text-gray-900">{user.fullName}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">CPF</dt>
							<dd class="mt-1 text-gray-900">{formatCPF(user.cpf)}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">Data de Nascimento</dt>
							<dd class="mt-1 text-gray-900">{formatDate(user.birthDate)}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">E-mail</dt>
							<dd class="mt-1 text-gray-900">{user.email}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">Nome da Mãe</dt>
							<dd class="mt-1 text-gray-900">{user.motherName}</dd>
						</div>
						<div>
							<dt class="text-base font-semibold text-gray-500">Nome do Pai</dt>
							<dd class="mt-1 text-gray-900">{user.fatherName}</dd>
						</div>
					</div>
				</div>
			{/if}

			<div class="rounded-2xl bg-white p-6 sm:p-8 shadow-lg">
				<h2 class="text-3xl font-bold text-gray-900">Meus Exames Enviados</h2>
				<ul class="mt-6 space-y-4">
					{#if submittedExams.length > 0}
						{#each submittedExams as exam}
							<li class="flex items-center justify-between rounded-lg border bg-gray-50 p-5">
								<div class="flex-1 overflow-hidden">
									<p class="font-semibold text-lg text-gray-800 truncate">{exam.fileName}</p>
									<p class="text-base text-gray-500">Tipo: {exam.type}</p>
									<p class="text-base text-gray-500">Enviado em: {exam.timestamp}</p>
								</div>
								<div class="flex flex-shrink-0 items-center space-x-4 ml-4">
									<button
										on:click={() => viewExam(exam)}
										type="button"
										class="text-base font-medium text-primary hover:text-primary-hover"
										>Visualizar</button
									>
									<button
										on:click={() => requestDeleteExam(exam)}
										type="button"
										class="text-gray-400 hover:text-danger"
										aria-label="Remover exame"
									>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-6 w-6"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
											/>
										</svg>
									</button>
								</div>
							</li>
						{/each}
					{:else}
						<li class="text-center text-gray-500 py-4 text-lg">
							Você ainda não enviou nenhum exame.
						</li>
					{/if}
				</ul>
			</div>

			<div class="pt-4 text-center">
				<a
					href="/painel"
					class="inline-block rounded-md border border-gray-300 bg-white px-10 py-4 text-lg font-bold text-gray-700 shadow-sm hover:bg-gray-50"
				>
					Voltar ao Painel
				</a>
			</div>
		</div>
	</main>
</div>
