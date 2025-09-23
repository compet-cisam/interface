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

	let currentUser: User | null = null;
	let patientName = '';
	let foundPatient: User | null = null;
	let isLoading = false;

	onMount(() => {
		const loggedInUserStr = sessionStorage.getItem('loggedInUser');
		if (loggedInUserStr) {
			currentUser = JSON.parse(loggedInUserStr);
			if (!currentUser?.crm) {
				goto('/login');
			}
		} else {
			goto('/login');
		}
	});

	function handlePatientSearch() {
		if (!patientName.trim()) {
			showToast('Por favor, digite o nome completo do paciente.', 'error');
			return;
		}
		isLoading = true;
		foundPatient = null;

		setTimeout(() => {
			let patientFound = false;
			for (let i = 0; i < localStorage.length; i++) {
				const key = localStorage.key(i);
				if (key && !key.startsWith('exams_')) {
					try {
						const userData = JSON.parse(localStorage.getItem(key)!);
						if (
							userData.fullName &&
							userData.fullName.toLowerCase() === patientName.trim().toLowerCase() &&
							userData.cpf
						) {
							foundPatient = userData;
							patientFound = true;
							break;
						}
					} catch (e) {
						console.error('Erro ao analisar os dados do localStorage:', e);
					}
				}
			}

			if (!patientFound) {
				showToast('Paciente não encontrado no sistema.', 'error');
			}
			isLoading = false;
		}, 500);
	}

	function accessPatientPanel() {
		if (foundPatient) {
			sessionStorage.setItem('viewingPatient', JSON.stringify(foundPatient));
			goto('/painel');
		}
	}

	function handleLogout() {
		sessionStorage.removeItem('loggedInUser');
		sessionStorage.removeItem('viewingPatient');
		goto('/login');
	}
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 flex-grow">
	<div class="flex items-center justify-between mb-6">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">
				{#if currentUser}Olá, Dr(a). {currentUser.fullName.split(' ')[0]}!{/if}
			</h1>
			<p class="mt-1 text-lg text-gray-600">Bem-vindo ao seu painel.</p>
		</div>
		<button
			on:click={handleLogout}
			class="font-semibold text-danger hover:text-danger-hover transition-colors text-lg"
		>
			Sair
		</button>
	</div>

	<div class="mt-12 flex flex-col md:flex-row gap-8 justify-center items-stretch">
		<!-- Card de Acesso ao Paciente -->
		<div class="group flex flex-1 flex-col rounded-2xl bg-white p-10 text-center shadow-lg">
			<div
				class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-blue-100 text-primary"
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
						d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
					/>
				</svg>
			</div>
			<h3 class="text-2xl font-bold text-gray-800">Acessar Paciente</h3>
			<p class="mt-3 text-base text-gray-600 flex-grow">
				Busque pelo nome completo para ver dados e exames do paciente.
			</p>
			<div class="mt-6">
				<form
					class="flex items-center space-x-3"
					on:submit|preventDefault={handlePatientSearch}
				>
					<input
						bind:value={patientName}
						type="text"
						placeholder="Nome completo do paciente"
						class="flex-grow px-4 py-2 border border-gray-300 rounded-md"
						disabled={isLoading}
					/>
					<button
						type="submit"
						class="px-6 py-2 bg-accent text-white font-bold rounded-md hover:bg-accent-hover disabled:opacity-75"
						disabled={isLoading}
					>
						{#if isLoading}
							<span
								class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"
							></span>
						{:else}
							Buscar
						{/if}
					</button>
				</form>

				{#if foundPatient}
					<div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-md text-left">
						<h3 class="font-bold text-green-800">Paciente Encontrado</h3>
						<p>
							<span class="font-semibold">Nome:</span>
							{foundPatient.fullName}
						</p>
						<p>
							<span class="font-semibold">CPF:</span>
							{foundPatient.cpf}
						</p>
						<button
							on:click={accessPatientPanel}
							class="mt-3 w-full bg-primary text-white font-bold py-2 px-4 rounded-md hover:bg-primary-hover"
						>
							Acessar Painel
						</button>
					</div>
				{/if}
			</div>
		</div>

		<!-- Card de Meus Dados -->
		<button
			on:click={() => goto('/profissional/meus-dados')}
			class="group flex flex-1 flex-col items-center justify-center rounded-2xl bg-white p-10 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
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
						d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
					/>
				</svg>
			</div>
			<h3 class="text-2xl font-bold text-gray-800">Meus Dados</h3>
			<p class="mt-3 text-base text-gray-600">
				Acesse e gerencie suas informações de cadastro.
			</p>
		</button>
	</div>
</main>






