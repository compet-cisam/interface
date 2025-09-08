<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	interface UserData {
		fullName: string;
		cpf: string;
	}

	let user: UserData | null = null;

	onMount(() => {
		const userDataString = sessionStorage.getItem('loggedInUser');
		if (userDataString) {
			user = JSON.parse(userDataString);
		} else {
			goto('/login');
		}
	});

	function handleLogout() {
		sessionStorage.removeItem('loggedInUser');
		goto('/login');
	}

	function handleNavigation(path: string) {
		if (path === '/envio-exames') {
			goto('/envio-exames');
		} else if (path === '/dados-do-paciente') {
			goto('/dados-do-paciente');
		} else {
			alert(`Funcionalidade para "${path}" a ser implementada.`);
		}
	}
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8">
	<div class="flex items-center justify-between mb-8">
		<h1 class="text-3xl font-bold text-gray-900 sm:text-4xl">
			{#if user}
				Olá, {user.fullName.split(' ')[0]}!
			{/if}
		</h1>
		<button
			on:click={handleLogout}
			class="font-semibold text-danger hover:text-danger-hover transition-colors text-lg"
		>
			Sair
		</button>
	</div>
	
	<div class="mx-auto max-w-2xl text-center">
		<p class="mt-2 text-xl text-gray-600">Gerencie as suas informações e exames.</p>
	</div>

	<div class="mt-12 grid grid-cols-1 gap-8 md:grid-cols-2">
		<button
			on:click={() => handleNavigation('/envio-exames')}
			class="group flex flex-col items-center rounded-2xl bg-white p-8 text-center shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
		>
			<div
				class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-primary transition-colors group-hover:bg-primary group-hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-8 w-8"
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
			<p class="mt-2 text-base text-gray-600">
				Clique aqui para enviar os seus exames, como ultrassonografias, ressonâncias, entre outros.
			</p>
		</button>

		<button
			on:click={() => handleNavigation('/dados-do-paciente')}
			class="group flex flex-col items-center rounded-2xl bg-white p-8 text-center shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
		>
			<div
				class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-primary transition-colors group-hover:bg-primary group-hover:text-white"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-8 w-8"
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
			<p class="mt-2 text-base text-gray-600">
				Acesse aqui todas as informações e exames que você já enviou para a plataforma.
			</p>
		</button>
	</div>
</main>



