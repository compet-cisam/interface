<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	interface User {
		fullName: string;
		cpf?: string;
		crm?: string;
	}

	interface FileWithType {
		file: File;
		type: string;
	}

	let currentUser: User | null = null;
	let patient: User | null = null;
	let isDoctorViewing = false;

	let filesWithTypes: FileWithType[] = [];
	let isLoading = false;

	onMount(() => {
		const viewingPatientStr = sessionStorage.getItem('viewingPatient');
		const loggedInUserStr = sessionStorage.getItem('loggedInUser');

		if (viewingPatientStr) {
			const viewingPatient = JSON.parse(viewingPatientStr);
			const patientDataStr = localStorage.getItem(viewingPatient.cpf);
			if (patientDataStr) {
				patient = JSON.parse(patientDataStr);
			}
			isDoctorViewing = true;
		} else if (loggedInUserStr) {
			patient = JSON.parse(loggedInUserStr);
		}

		if (!loggedInUserStr) {
			goto('/login');
		} else {
			currentUser = JSON.parse(loggedInUserStr);
		}
	});

	function handleFileSelect(e: Event) {
		const input = e.currentTarget as HTMLInputElement;
		if (input.files && input.files.length > 0) {
			const newFiles = Array.from(input.files).map((f) => ({ file: f, type: '' }));
			filesWithTypes = [...filesWithTypes, ...newFiles];
		}
	}

	function handleDrop(e: DragEvent) {
		if (e.dataTransfer && e.dataTransfer.files.length > 0) {
			const newFiles = Array.from(e.dataTransfer.files).map((f) => ({ file: f, type: '' }));
			filesWithTypes = [...filesWithTypes, ...newFiles];
		}
	}

	function removeFile(indexToRemove: number) {
		filesWithTypes = filesWithTypes.filter((_, index) => index !== indexToRemove);

		if (filesWithTypes.length === 0) {
			const fileInput = document.getElementById('exam-file') as HTMLInputElement;
			if (fileInput) fileInput.value = '';
		}
	}

	async function handleExamSubmit() {
		if (!patient || !patient.cpf || filesWithTypes.length === 0) {
			showToast('Por favor, selecione pelo menos um ficheiro.', 'error');
			return;
		}

		const hasEmptyType = filesWithTypes.some(f => !f.type);
		if (hasEmptyType) {
			showToast('Por favor, selecione um tipo para cada exame.', 'error');
			return;
		}

		isLoading = true;

		try {
			const examsKey = `exams_${patient.cpf}`;
			const existingExamsString = localStorage.getItem(examsKey);
			let existingExams = [];
			if (existingExamsString) {
				existingExams = JSON.parse(existingExamsString);
			}

			const fileReadPromises = filesWithTypes.map(({ file, type }, i) => {
				return new Promise((resolve, reject) => {
					const reader = new FileReader();
					reader.readAsDataURL(file);
					reader.onload = () => {
						const newExam = {
							id: Date.now() + i,
							type: type,
							fileName: file.name,
							timestamp: new Date().toLocaleString('pt-BR'),
							dataUrl: reader.result as string,
							submittedBy: currentUser?.fullName
						};
						resolve(newExam);
					};
					reader.onerror = (error) => reject(error);
				});
			});

			const newExams = await Promise.all(fileReadPromises);
			const updatedExams = [...existingExams, ...newExams];
			localStorage.setItem(examsKey, JSON.stringify(updatedExams));

			showToast(`${newExams.length} exame(s) enviado(s) com sucesso!`, 'success');

			filesWithTypes = [];
			const fileInput = document.getElementById('exam-file') as HTMLInputElement;
			if (fileInput) fileInput.value = '';
		} catch (e) {
			showToast('Ocorreu um erro ao salvar os exames.', 'error');
		} finally {
			isLoading = false;
		}
	}

	function goBack() {
		// Correção: Leva sempre de volta ao painel do paciente em visualização
		goto('/painel');
	}
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 flex-grow">
	<div class="max-w-3xl mx-auto">
		<button
			on:click={goBack}
			class="flex items-center text-lg font-semibold text-primary hover:text-primary-hover mb-6"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"
				><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg
			>
			<span class="ml-2">Voltar ao Painel do Paciente</span>
		</button>

		<div class="p-8 bg-white rounded-2xl shadow-lg">
			<h1 class="text-3xl font-bold text-gray-900">Enviar Exame de Imagem</h1>
			{#if patient}
				<p class="mt-2 text-lg text-gray-600">
					Enviando exame para: <span class="font-semibold">{patient.fullName}</span>
				</p>
			{/if}

			<form class="mt-8 space-y-6" on:submit|preventDefault={handleExamSubmit}>
				<div>
					<label for="exam-file" class="block text-base font-semibold text-gray-700"
						>Anexar Documento(s)</label
					>
					<div
						class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md"
						on:dragover|preventDefault
						on:drop|preventDefault={handleDrop}
					>
						<div class="space-y-1 text-center">
							<svg
								class="mx-auto h-12 w-12 text-gray-400"
								stroke="currentColor"
								fill="none"
								viewBox="0 0 48 48"
								aria-hidden="true"
							>
								<path
									d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"></path>
							</svg>
							<div class="flex justify-center text-sm text-gray-600">
								<label
									for="exam-file"
									class="relative cursor-pointer bg-white rounded-md font-medium text-primary hover:text-primary-hover focus-within:outline-none"
								>
									<span>Carregue um ou mais ficheiros</span>
									<input
										id="exam-file"
										name="exam-file"
										type="file"
										class="sr-only"
										on:change={handleFileSelect}
										accept="image/*,application/pdf"
										multiple
									/>
								</label>
								<p class="pl-1">ou arraste e solte</p>
							</div>
							<p class="text-xs text-gray-500">PNG, JPG, PDF até 10MB</p>
							{#if filesWithTypes.length > 0}
								<div class="pt-4 text-left">
									<p class="font-semibold text-gray-800">Ficheiros selecionados:</p>
									<ul class="mt-2 space-y-4">
										{#each filesWithTypes as { file, type }, i}
											<li class="p-3 rounded-md border border-gray-200 bg-gray-50">
												<div class="flex items-center justify-between">
													<span class="truncate font-medium text-gray-700">{file.name}</span>
													<button
														type="button"
														on:click={() => removeFile(i)}
														class="ml-2 text-gray-400 hover:text-danger"
														aria-label="Remover {file.name}"
													>
														<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
															<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
														</svg>
													</button>
												</div>
												<div class="mt-2">
													<label for="exam-type-{i}" class="sr-only">Tipo do Exame para {file.name}</label>
													<select
														bind:value={filesWithTypes[i].type}
														id="exam-type-{i}"
														required
														class="block w-full px-2 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm"
													>
														<option value="" disabled>Selecione um tipo de exame</option>
														<option value="Ultrassonografia">Ultrassonografia</option>
														<option value="Ressonância Magnética">Ressonância Magnética</option>
														<option value="Tomografia Computadorizada">Tomografia Computadorizada</option>
														<option value="Raio-X">Raio-X</option>
														<option value="Mamografia">Mamografia</option>
														<option value="Outro">Outro</option>
													</select>
												</div>
											</li>
										{/each}
									</ul>
								</div>
							{/if}
						</div>
					</div>
				</div>
				<div>
					<button
						type="submit"
						class="w-full flex justify-center py-3 px-4 text-lg font-bold rounded-md text-white bg-accent hover:bg-accent-hover"
						disabled={isLoading || filesWithTypes.length === 0}
					>
						{#if isLoading}
							<span
								class="animate-spin h-5 w-5 mr-3 border-2 border-white border-t-transparent rounded-full"
							></span>
							Enviando...
						{:else}
							Enviar Exame(s)
						{/if}
					</button>
				</div>
			</form>
		</div>
	</div>
</main>



