<script lang="ts">
	// Página do profissional
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	// import { authToken } from '$lib/stores/auth'; // Se não estiver usando store, pode comentar

	// Função simples para pegar token do localStorage se a store não estiver disponível
	function getToken() {
		if (typeof localStorage !== 'undefined') {
			return localStorage.getItem('token');
		}
		return null;
	}

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast') || ((msg) => console.log(msg)); // Fallback se não houver contexto

	interface User {
		fullName: string;
		cpf?: string;
	}

	//TODO Backend atualmente não envia informações como nome do paciente
	let currentUser: User | null = null;
	let patientName = '';
	let foundPatient: User | null = null;
	let isLoading = false;

	onMount(() => {
		// Checando se existe alguém logado legitimamente
		const token = getToken();
		if (!token) {
			goto('/auth'); // Redireciona para login se não tiver token
		}

		// Tenta recuperar usuário do sessionStorage se existir (Lógica legada)
		const loggedInUserStr = sessionStorage.getItem('loggedInUser');
		if (loggedInUserStr) {
			currentUser = JSON.parse(loggedInUserStr);
		}
	});

	// Função de busca de paciente (Descomentada e ajustada)
	function handlePatientSearch() {
		if (!patientName.trim()) {
			// showToast('Por favor, digite o nome completo do paciente.', 'error');
			alert('Por favor, digite o nome completo do paciente.');
			return;
		}
		isLoading = true;
		foundPatient = null;

		// Simulação de busca (Aqui você conectaria com sua API nova no futuro)
		setTimeout(() => {
			let patientFound = false;
			
			// Lógica original que busca no localStorage (mantida conforme solicitado)
			for (let i = 0; i < localStorage.length; i++) {
				const key = localStorage.key(i);
				if (key && !key.startsWith('exams_')) {
					try {
						const item = localStorage.getItem(key);
						if (item) {
							const userData = JSON.parse(item);
							if (
								userData.fullName &&
								userData.fullName.toLowerCase() === patientName.trim().toLowerCase() &&
								userData.cpf
							) {
								foundPatient = userData;
								patientFound = true;
								break;
							}
						}
					} catch (e) {
						console.error('Erro ao analisar os dados do localStorage:', e);
					}
				}
			}

			if (!patientFound) {
				// showToast('Paciente não encontrado no sistema.', 'error');
				alert('Paciente não encontrado no sistema local.');
			}
			isLoading = false;
		}, 500);
	}

	function accessPatientPanel() {
		if (foundPatient) {
			sessionStorage.setItem('viewingPatient', JSON.stringify(foundPatient));
			goto('/painel'); // Certifique-se que a rota /painel existe
		}
	}

	function handleLogout() {
		sessionStorage.removeItem('loggedInUser');
		sessionStorage.removeItem('viewingPatient');
		localStorage.removeItem('token'); // Remove o token da API também
		goto('/auth');
	}
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 flex-grow">
	<div class="flex items-center justify-between mb-6">
		<div>
			<!-- Exibe nome se disponível -->
			<h1 class="text-3xl font-bold text-gray-900">
				{#if currentUser}Olá, Dr(a). {currentUser.fullName.split(' ')[0]}!{/if}
			</h1>
			<p class="mt-1 text-lg text-gray-600">Bem-vindo ao seu painel</p>
		</div>
		<button
			on:click={handleLogout}
			class="font-semibold text-red-600 hover:text-red-800 transition-colors text-lg"
		>
			Sair
		</button>
	</div>

	<div class="mt-12 flex flex-col md:flex-row gap-8 justify-center items-stretch">
		
		<!-- SEÇÃO DO MEDGEMMA (MANTIDA) -->
		<a
			href="http://localhost:8080"
			target="_blank"
			rel="noopener noreferrer"
			class="group flex flex-1 flex-col items-center justify-center rounded-2xl bg-white p-10 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl border border-gray-100"
		>
			<div
				class="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-blue-100 text-blue-600 transition-colors group-hover:bg-blue-600 group-hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-12 w-12"
					viewBox="0 -960 960 960"
					fill="currentColor"
				>
					<path
						d="M323-160q-11 0-20.5-5.5T288-181l-78-139h58l40 80h92v-40h-68l-40-80H188l-57-100q-2-5-3.5-10t-1.5-10q0-4 5-20l57-100h104l40-80h68v-40h-92l-40 80h-58l78-139q5-10 14.5-15.5T323-800h97q17 0 28.5 11.5T460-760v160h-60l-40 40h100v120h-88l-40-80h-92l-40 40h108l40 80h112v200q0 17-11.5 28.5T420-160h-97Zm217 0q-17 0-28.5-11.5T500-200v-200h112l40-80h108l-40-40h-92l-40 80h-88v-120h100l-40-40h-60v-160q0-17 11.5-28.5T540-800h97q11 0 20.5 5.5T672-779l78 139h-58l-40-80h-92v40h68l40 80h104l57 100q2 5 3.5 10t1.5 10q0 4-5 20l-57 100H668l-40 80h-68v40h92l40-80h58l-78 139q-5 10-14.5 15.5T637-160h-97Z"
					/>
				</svg>
			</div>
			<h3 class="text-2xl font-bold text-gray-800">Medgemma</h3>
			<p class="mt-3 text-base text-gray-600">
				Acesse a Inteligência Artificial Medgemma
			</p>
		</a>

		<div class="group flex flex-1 flex-col rounded-2xl bg-white p-10 text-center shadow-lg border border-gray-100">
			<div
				class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-blue-100 text-blue-600"
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
						class="flex-grow px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
						disabled={isLoading}
					/>
					<button
						type="submit"
						class="px-6 py-2 bg-blue-600 text-white font-bold rounded-md hover:bg-blue-700 disabled:opacity-75 transition-colors"
						disabled={isLoading}
					>
						{#if isLoading}
							<span
								class="inline-block animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"
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
							class="mt-3 w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
						>
							Acessar Painel
						</button>
					</div>
				{/if}
			</div>
		</div>

	</div>
</main>