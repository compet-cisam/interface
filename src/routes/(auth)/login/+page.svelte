<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';

	const showToast = getContext<(message: string, type: 'success' | 'error') => void>('showToast');

	let cpf = '';
	let password = '';
	let isLoading = false;

	function handleLogin() {
		isLoading = true;
		setTimeout(() => {
			const storedDataString = localStorage.getItem(cpf);
			if (storedDataString) {
				const userData = JSON.parse(storedDataString);
				if (userData.password === password) {
					showToast('Login bem-sucedido!', 'success');
					sessionStorage.setItem('loggedInUser', JSON.stringify(userData));
					goto('/painel');
				} else {
					showToast('Senha incorreta.', 'error');
				}
			} else {
				showToast('Usuário não encontrado.', 'error');
			}
			isLoading = false;
		}, 500);
	}

	function togglePasswordVisibility(inputId: string) {
		const input = document.getElementById(inputId) as HTMLInputElement;
		if (input) {
			input.type = input.type === 'password' ? 'text' : 'password';
		}
	}
</script>

<div class="w-full max-w-md p-8 space-y-8 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-3xl font-bold text-gray-900">Bem-vindo!</h2>
		<p class="mt-2 text-sm text-gray-600">Faça login para acessar sua conta.</p>
	</div>
	<form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
		<div class="rounded-md shadow-sm -space-y-px">
			<div>
				<label for="login-cpf" class="sr-only">CPF</label>
				<input bind:value={cpf} id="login-cpf" type="text" required class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-2 focus:ring-primary sm:text-sm" placeholder="CPF" disabled={isLoading}>
			</div>
			<div class="relative">
				<label for="login-password" class="sr-only">Senha</label>
				<input bind:value={password} id="login-password" type="password" required class="appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-2 focus:ring-primary sm:text-sm" placeholder="Senha" disabled={isLoading}>
				<button type="button" on:click={() => togglePasswordVisibility('login-password')} class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500">
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
				</button>
			</div>
		</div>
		<div class="flex items-center justify-end">
			<a href="/esqueci-senha" class="text-sm font-medium text-primary hover:text-primary-hover">Esqueci minha senha</a>
		</div>
		<div>
			<button type="submit" class="group relative w-full flex justify-center items-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-accent hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-75" disabled={isLoading}>
				{#if isLoading}
					<span class="animate-spin h-5 w-5 mr-3 border-2 border-white border-t-transparent rounded-full"></span>
					Conectando...
				{:else}
					Entrar
				{/if}
			</button>
		</div>
	</form>
	<p class="mt-4 text-center text-sm text-gray-600">
		Não tem uma conta?
		<a href="/cadastro" class="font-medium text-primary hover:text-primary-hover">Cadastrar-se</a>
	</p>
</div>

