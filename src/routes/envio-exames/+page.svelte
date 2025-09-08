<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	interface ExamFile {
		id: number;
		type: string;
		file: File | null;
		fileName: string;
		dataUrl: string | null;
	}

	interface UserData {
		cpf: string;
	}

	let examList: ExamFile[] = [];
	let currentUser: UserData | null = null;

	onMount(() => {
		const userDataString = sessionStorage.getItem('loggedInUser');
		if (userDataString) {
			currentUser = JSON.parse(userDataString);
		} else {
			goto('/login');
		}
		addExamField();
	});

	function addExamField() {
		const newExam: ExamFile = {
			id: Date.now(),
			type: '',
			file: null,
			fileName: 'Nenhum ficheiro escolhido',
			dataUrl: null
		};
		examList = [...examList, newExam];
	}

	function removeExamField(id: number) {
		examList = examList.filter((exam) => exam.id !== id);
	}

	function handleFileSelect(event: Event, id: number) {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files.length > 0) {
			const file = input.files[0];
			const reader = new FileReader();
			reader.onload = (e) => {
				examList = examList.map((exam) =>
					exam.id === id
						? { ...exam, file: file, fileName: file.name, dataUrl: e.target?.result as string }
						: exam
				);
			};
			reader.readAsDataURL(file);
		}
	}

	function handleSubmit() {
		if (!currentUser) {
			showToast('Erro: Utilizador não encontrado. Por favor, faça login novamente.', 'error');
			return;
		}

		const examsToSubmit = examList.filter((exam) => exam.type && exam.file && exam.dataUrl);
		if (examsToSubmit.length === 0) {
			showToast('Por favor, preencha e anexe pelo menos um exame.', 'error');
			return;
		}

		const storageKey = `exams_${currentUser.cpf}`;
		const existingExamsString = localStorage.getItem(storageKey);
		let existingExams = existingExamsString ? JSON.parse(existingExamsString) : [];

		const newExams = examsToSubmit.map((exam) => ({
			id: exam.id,
			type: exam.type,
			fileName: exam.fileName,
			timestamp: new Date().toLocaleString('pt-BR'),
			dataUrl: exam.dataUrl
		}));

		const updatedExams = [...existingExams, ...newExams];
		localStorage.setItem(storageKey, JSON.stringify(updatedExams));

		showToast(`${examsToSubmit.length} exame(s) enviado(s) com sucesso!`, 'success');
		goto('/painel');
	}
</script>

<div class="min-h-screen bg-gray-50 flex-grow" style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);">
	<main class="container mx-auto p-4 sm:p-6 lg:p-8">
		<div class="mx-auto max-w-2xl rounded-2xl bg-white p-8 shadow-lg">
			<div class="text-center">
				<h1 class="text-3xl font-bold text-gray-900">Envio de Exames</h1>
				<p class="mt-2 text-gray-600">Adicione um ou mais exames para enviar à plataforma.</p>
			</div>

			<form on:submit|preventDefault={handleSubmit} class="mt-8 space-y-6">
				<div id="exam-list-container" class="space-y-6">
					{#each examList as exam (exam.id)}
						<div class="rounded-lg border bg-gray-50 p-4">
							<div class="mb-4 flex items-center justify-between">
								<span class="font-medium text-gray-800">Exame</span>
								{#if examList.length > 1}
									<button
										type="button"
										on:click={() => removeExamField(exam.id)}
										class="text-gray-400 hover:text-red-500"
									>
										<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
											<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
										</svg>
									</button>
								{/if}
							</div>

							<div class="space-y-4">
								<div>
									<label for="exam-type-{exam.id}" class="mb-1 block text-sm font-medium text-gray-700">Tipo de Exame</label>
									<select bind:value={exam.type} id="exam-type-{exam.id}" required class="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary">
										<option value="" disabled>Selecione o tipo</option>
										<option value="Ultrassonografia">Ultrassonografia</option>
										<option value="Ressonância Magnética">Ressonância Magnética</option>
										<option value="Mamografia">Mamografia</option>
										<option value="Tomografia Computadorizada">Tomografia Computadorizada</option>
										<option value="Raio-X">Raio-X</option>
										<option value="Outro">Outro</option>
									</select>
								</div>
								<div>
									<label for="file-upload-{exam.id}" class="mb-1 block text-sm font-medium text-gray-700">Arquivo do Exame</label>
									<div class="flex items-center space-x-4">
										<label class="cursor-pointer rounded-md bg-white px-4 py-2 text-sm font-medium text-primary shadow-sm border border-primary hover:bg-blue-50">
											<span>Escolher arquivo</span>
											<input id="file-upload-{exam.id}" on:change={(e) => handleFileSelect(e, exam.id)} type="file" class="sr-only" accept=".pdf,.png,.jpg,.jpeg"/>
										</label>
										<span class="text-sm text-gray-500">{exam.fileName}</span>
									</div>
								</div>
							</div>
						</div>
					{/each}
				</div>

				<button type="button" on:click={addExamField} class="flex w-full items-center justify-center space-x-2 rounded-lg border-2 border-dashed border-gray-300 py-3 text-sm font-medium text-gray-700 hover:border-primary hover:text-primary">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
						<path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
					</svg>
					<span>Adicionar outro exame</span>
				</button>

				<div class="flex items-center space-x-4 pt-4">
					<button type="button" on:click={() => goto('/painel')} class="w-full rounded-md border border-gray-300 bg-white py-3 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50">Voltar</button>
					<button type="submit" class="w-full rounded-md border border-transparent bg-accent py-3 text-sm font-medium text-white shadow-sm hover:bg-accent-hover">Enviar Exames</button>
				</div>
			</form>
		</div>
	</main>
</div>

