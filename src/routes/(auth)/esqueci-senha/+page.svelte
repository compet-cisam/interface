<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';

	const showToast = getContext<(message: string, type: 'success' | 'error') => void>('showToast');

	let cpf = '';

	function handleForgotPassword() {
		if (localStorage.getItem(cpf)) {
			sessionStorage.setItem('resetPasswordIdentifier', cpf);
			showToast('CPF encontrado. Crie uma nova senha.', 'success');
			goto('/redefinir-senha');
		} else {
			showToast('CPF não encontrado em nosso sistema.', 'error');
		}
	}
</script>

<div class="w-full max-w-md p-8 space-y-8 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-3xl font-bold text-gray-900">Redefinir Senha</h2>
		<p class="mt-2 text-sm text-gray-600">Digite seu CPF para continuar.</p>
	</div>
	<form class="mt-8 space-y-6" on:submit|preventDefault={handleForgotPassword}>
		<div>
			<label for="recovery-cpf" class="sr-only">CPF</label>
			<input bind:value={cpf} id="recovery-cpf" type="text" required class="appearance-none rounded-md relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary sm:text-sm" placeholder="Seu CPF">
		</div>
		<div class="flex items-center space-x-4">
			<a href="/login" class="group relative w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">Voltar</a>
			<button type="submit" class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">Continuar</button>
		</div>
	</form>
</div>

