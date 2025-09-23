<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getContext } from 'svelte';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	interface UserData {
		fullName: string;
		crm: string;
	}

	interface PatientData {
		fullName: string;
		cpf: string;
	}

	let doctor: UserData | null = null;
	let patientNameSearch = '';
	let foundPatient: PatientData | null = null;
	let isSearching = false;

	// Simulação: Paciente cadastrado para fins de demonstração
	const mockPatient: PatientData = {
		fullName: 'Rodrigo Campos de Oliveira Cabral',
		cpf: '123.456.789-00'
	};

	onMount(() => {
		// Busca os dados do médico logado
		const userDataString = sessionStorage.getItem('loggedInUser');
		if (userDataString) {
			const userData = JSON.parse(userDataString);
			// Idealmente, você teria uma verificação de tipo de usuário aqui
			doctor = userData;
		} else {
			goto('/login');
		}

		// Simulação: Armazena o paciente mock no localStorage para ser "encontrado"
		localStorage.setItem(mockPatient.fullName, JSON.stringify(mockPatient));
	});

	function handleSearchPatient() {
		if (!patientNameSearch.trim()) {
			showToast('Por favor, digite o nome do paciente.', 'error');
			return;
		}
		isSearching = true;
		foundPatient = null;

		// Simulação de busca no banco de dados
		setTimeout(() => {
			const storedPatientString = localStorage.getItem(patientNameSearch);
			if (storedPatientString) {
				foundPatient = JSON.parse(storedPatientString);
				showToast('Paciente encontrado!', 'success');
			} else {
				showToast('Paciente não encontrado.', 'error');
			}
			isSearching = false;
		}, 1000);
	}

	function handleLogout() {
		sessionStorage.removeItem('loggedInUser');
		goto('/login');
	}

	function handleNavigation(path: string) {
		// Ao navegar para a área do paciente, você pode passar o ID/CPF dele como parâmetro
		if (foundPatient) {
			goto(`${path}?paciente_cpf=${foundPatient.cpf}`);
		} else {
			goto(path);
		}
	}
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 flex-grow">
	<div class="flex items-center justify-between mb-8">
		<h1 class="text-3xl font-bold text-gray-800">
			{#if doctor}
				Olá, Dr. {doctor.fullName.split(' ')[0]}!
			{/if}
		</h1>
		<button
			on:click={handleLogout}
			class="font-semibold text-danger hover:text-danger-hover transition-colors text-lg"
		>
			Sair
		</button>
	</div>

	<!-- Seção de Busca do Paciente -->
	<div class="mx-auto max-w-3xl text-center">
		<p class="mt-4 text-xl text-gray-600">Busque por um paciente para acessar seus dados e exames.</p>
		<form class="mt-8 flex gap-2" on:submit|preventDefault={handleSearchPatient}>
			<input
				type="text"
				bind:value={patientNameSearch}
				placeholder="Digite o nome completo do paciente"
				class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-base p-3 flex-grow"
				disabled={isSearching}
			/>
			<button
				type="submit"
				class="px-6 py-3 rounded-md text-white bg-primary hover:bg-primary-hover font-semibold disabled:opacity-75"
				disabled={isSearching}
			>
				{#if isSearching}
					Buscando...
				{:else}
					Buscar
				{/if}
			</button>
		</form>
	</div>

	<!-- Seção do Paciente Encontrado -->
	{#if foundPatient}
		<div class="mt-12 border-t pt-10">
			<h2 class="text-center text-2xl font-bold text-gray-800 mb-8">
				Acessando dados de: <span class="text-primary">{foundPatient.fullName}</span>
			</h2>
			<div class="flex flex-col md:flex-row gap-8 justify-center items-stretch">
				<button
					on:click={() => handleNavigation('/envio-exames')}
					class="group flex flex-col items-center rounded-2xl bg-white p-10 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl flex-1"
				>
					<div
						class="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-blue-100 text-primary transition-colors group-hover:bg-primary group-hover:text-white"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-10 w-10"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
							/>
						</svg>
					</div>
					<h3 class="text-2xl font-bold text-gray-800">Enviar Exames do Paciente</h3>
					<p class="mt-3 text-base text-gray-600">
						Envie novos exames, como ultrassonografias e ressonâncias, para este paciente.
					</p>
				</button>

				<button
					on:click={() => handleNavigation('/dados-do-paciente')}
					class="group flex flex-col items-center rounded-2xl bg-white p-10 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl flex-1"
				>
					<div
						class="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-blue-100 text-primary transition-colors group-hover:bg-primary group-hover:text-white"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-10 w-10"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
							/>
						</svg>
					</div>
					<h3 class="text-2xl font-bold text-gray-800">Dados e Exames do Paciente</h3>
					<p class="mt-3 text-base text-gray-600">
						Acesse todas as informações e exames que este paciente já enviou para a plataforma.
					</p>
				</button>
			</div>
		</div>
	{/if}

	<!-- Seção de Dados do Médico -->
	<div class="mt-16 border-t pt-10 flex flex-col md:flex-row gap-8 justify-center items-stretch">
		<button
			on:click={() => handleNavigation('/profissional/meus-dados')}
			class="group flex flex-col items-center rounded-2xl bg-white p-10 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl flex-1 max-w-lg mx-auto"
		>
			<div
				class="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-green-100 text-green-600 transition-colors group-hover:bg-green-600 group-hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-10 w-10"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
					/>
				</svg>
			</div>
			<h3 class="text-2xl font-bold text-gray-800">Meus Dados Cadastrais</h3>
			<p class="mt-3 text-base text-gray-600">
				Clique aqui para visualizar e gerenciar suas informações profissionais na plataforma.
			</p>
		</button>
	</div>
</main>