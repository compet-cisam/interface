<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	interface MedicoData {
		fullName: string;
		crm: string;
		email: string;
	}

	let medico: MedicoData | null = null;

	onMount(() => {
		const userDataString = sessionStorage.getItem('loggedInUser');
		if (userDataString) {
			medico = JSON.parse(userDataString);
		} else {
			goto('/login');
		}
	});
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 flex-grow">
	<div class="flex items-center justify-between mb-8">
		<h1 class="text-3xl font-bold text-gray-900">Meus Dados Cadastrais</h1>
		<button on:click={() => goto('/profissional')} class="font-semibold text-primary hover:text-primary-hover transition-colors">
			&larr; Voltar ao Painel
		</button>
	</div>

	{#if medico}
		<div class="p-8 bg-white rounded-2xl shadow-lg">
			<div class="space-y-4">
				<div>
					<h3 class="font-semibold text-gray-600">Nome Completo</h3>
					<p class="text-lg text-gray-900">{medico.fullName}</p>
				</div>
				<div>
					<h3 class="font-semibold text-gray-600">E-mail</h3>
					<p class="text-lg text-gray-900">{medico.email}</p>
				</div>
				<div>
					<h3 class="font-semibold text-gray-600">CRM</h3>
					<p class="text-lg text-gray-900">{medico.crm}</p>
				</div>
			</div>
		</div>
	{:else}
		<p>Carregando dados...</p>
	{/if}
</main>
