<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	interface UserData {
		fullName: string;
		cpf: string;
		crm?: string;
	}

	let patientToDisplay: UserData | null = null;
	let isDoctorViewing = false;

	onMount(() => {
		const loggedInUserStr = sessionStorage.getItem('loggedInUser');
		const viewingPatientStr = sessionStorage.getItem('viewingPatient');

		if (loggedInUserStr) {
			const loggedInUser: UserData = JSON.parse(loggedInUserStr);

			if (viewingPatientStr && loggedInUser.crm) {
				isDoctorViewing = true;
				patientToDisplay = JSON.parse(viewingPatientStr);
			} else if (loggedInUser.cpf) {
				isDoctorViewing = false;
				patientToDisplay = loggedInUser;
			} else {
				goto('/login');
			}
		} else {
			goto('/login');
		}
	});

	function handleLogout() {
		sessionStorage.removeItem('loggedInUser');
		goto('/login');
	}

	function handleBackToDoctorPanel() {
		sessionStorage.removeItem('viewingPatient');
		goto('/profissional');
	}

	function handleNavigation(path: string) {
		goto(path);
	}
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 flex-grow">
	<div class="flex items-start justify-between mb-6">
		<div>
			<h1 class="text-3xl font-bold text-gray-800">
				{#if patientToDisplay}
					{#if isDoctorViewing}
						Painel de {patientToDisplay.fullName}
					{:else}
						Olá, {patientToDisplay.fullName.split(' ')[0]}!
					{/if}
				{/if}
			</h1>
			<p class="mt-2 text-xl text-gray-600">Gerencie as informações e exames.</p>
		</div>

		{#if isDoctorViewing}
			<button
				on:click={handleBackToDoctorPanel}
				class="font-semibold text-primary hover:text-primary-hover transition-colors text-base"
			>
				Voltar ao Meu Painel
			</button>
		{:else}
			<button
				on:click={handleLogout}
				class="font-semibold text-danger hover:text-danger-hover transition-colors text-base"
			>
				Sair
			</button>
		{/if}
	</div>

	<div class="mt-12 flex flex-col md:flex-row gap-6 justify-center items-stretch">
		<button
			on:click={() => handleNavigation('/envio-exames')}
			class="group flex flex-col items-center rounded-2xl bg-white p-8 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl flex-1"
		>
			<div
				class="mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-primary transition-colors group-hover:bg-primary group-hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-9 w-9"
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
			<h3 class="text-2xl font-bold text-gray-800">Enviar Exames de Imagem</h3>
			<p class="mt-2 text-gray-600">
				Clique aqui para enviar os seus exames, como ultrassonografias e ressonâncias.
			</p>
		</button>

		<button
			on:click={() => handleNavigation('/dados-do-paciente')}
			class="group flex flex-col items-center rounded-2xl bg-white p-8 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl flex-1"
		>
			<div
				class="mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-primary transition-colors group-hover:bg-primary group-hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-9 w-9"
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
			<h3 class="text-2xl font-bold text-gray-800">Meus Dados e Exames</h3>
			<p class="mt-2 text-gray-600">
				Acesse aqui todas as informações e exames que você já enviou para a plataforma.
			</p>
		</button>
	</div>
</main>