<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	let loginIdentifier = '';
	let password = '';
	let isLoading = false;
	let showPassword = false;

	const cpfValidator = (cpf: string) => {
		cpf = cpf.replace(/[^\d]+/g, '');
		if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;
		let add = 0;
		for (let i = 0; i < 9; i++) add += parseInt(cpf.charAt(i)) * (10 - i);
		let rev = 11 - (add % 11);
		if (rev === 10 || rev === 11) rev = 0;
		if (rev !== parseInt(cpf.charAt(9))) return false;
		add = 0;
		for (let i = 0; i < 10; i++) add += parseInt(cpf.charAt(i)) * (11 - i);
		rev = 11 - (add % 11);
		if (rev === 10 || rev === 11) rev = 0;
		if (rev !== parseInt(cpf.charAt(10))) return false;
		return true;
	};

	function handleLogin() {
		isLoading = true;
		let key = '';
		let userType = '';
		const sanitizedIdentifier = loginIdentifier.replace(/[^\d]+/g, '');

		if (/^\d{8}$/.test(loginIdentifier)) {
			key = loginIdentifier;
			userType = 'admin';
		} else if (/^\d{11}$/.test(sanitizedIdentifier)) {
			if (!cpfValidator(sanitizedIdentifier)) {
				showToast('O CPF inserido é inválido.', 'error');
				isLoading = false;
				return;
			}
			key = sanitizedIdentifier;
			userType = 'patient';
		} else if (/^CRM-PE \d+$/i.test(loginIdentifier)) {
			key = loginIdentifier;
			userType = 'doctor';
		} else {
			showToast('O campo de login inserido não está correto. Verifique o que foi digitado.', 'error');
			isLoading = false;
			return;
		}

		setTimeout(() => {
			const storedDataString = localStorage.getItem(key);
			if (storedDataString) {
				const userData = JSON.parse(storedDataString);
				if (userData.password === password) {
					showToast('Login bem-sucedido!', 'success');
					sessionStorage.setItem('loggedInUser', JSON.stringify(userData));

					if (userType === 'admin') {
						goto('/admin');
					} else if (userType === 'doctor') {
						goto('/profissional');
					} else {
						goto('/painel');
					}
				} else {
					showToast('Senha incorreta.', 'error');
				}
			} else {
				let errorMsg = 'Utilizador não encontrado.';
				if (userType === 'patient') errorMsg = 'CPF não registado.';
				if (userType === 'doctor') errorMsg = 'CRM não registado.';
				if (userType === 'admin') errorMsg = 'Código de Acesso não registado.';
				showToast(errorMsg, 'error');
			}
			isLoading = false;
		}, 500);
	}
</script>

<div class="w-full max-w-md p-8 space-y-6 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-4xl font-bold text-gray-900">Bem-vindo(a)!</h2>
		<p class="mt-2 text-lg text-gray-600">Faça login para acessar a sua conta na nossa plataforma.</p>
	</div>
	<form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
		<div>
			<div class="flex items-center justify-between">
				<label for="login-identifier" class="block text-base font-semibold text-gray-700"
					>Login</label
				>
				<div class="relative group">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5 text-gray-400"
						viewBox="0 0 20 20"
						fill="currentColor"
					>
						<path
							fill-rule="evenodd"
							d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
							clip-rule="evenodd"
						/>
					</svg>
					<div
						class="absolute bottom-full right-0 mb-2 w-72 p-3 bg-gray-800 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
						role="tooltip"
					>
						- <span class="font-semibold">Paciente:</span> Digite o seu CPF (apenas números).
						<br />
						- <span class="font-semibold">Médico:</span> Digite o seu CRM (ex: CRM-PE 12345).
						<br />
						- <span class="font-semibold">Administrador:</span> Digite o seu Código de Acesso (8
						dígitos).
						<div
							class="absolute top-full right-4 w-3 h-3 bg-gray-800 transform rotate-45 -mt-1"
						></div>
					</div>
				</div>
			</div>
			<input
				bind:value={loginIdentifier}
				id="login-identifier"
				type="text"
				required
				class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
				placeholder="Seu CPF, CRM ou Código"
				disabled={isLoading}
			/>
		</div>
		<div class="relative">
			<label for="login-password" class="block text-base font-semibold text-gray-700">Senha</label>
			{#if showPassword}
				<input
					bind:value={password}
					id="login-password"
					type="text"
					required
					class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					placeholder="Sua senha"
					disabled={isLoading}
				/>
			{:else}
				<input
					bind:value={password}
					id="login-password"
					type="password"
					required
					class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					placeholder="Sua senha"
					disabled={isLoading}
				/>
			{/if}
			<button
				type="button"
				on:click={() => (showPassword = !showPassword)}
				class="absolute inset-y-0 right-0 top-6 px-3 flex items-center text-gray-500"
			>
				{#if showPassword}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="20"
						height="20"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle
							cx="12"
							cy="12"
							r="3"
						></circle></svg
					>
				{:else}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="20"
						height="20"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						><path
							d="M9.88 9.88a3 3 0 1 0 4.24 4.24"
						></path><path
							d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"
						></path><path
							d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"
						></path><line x1="2" x2="22" y1="2" y2="22"></line></svg
					>
				{/if}
			</button>
		</div>
		<div class="flex items-center justify-end">
			<a href="/esqueci-senha" class="text-base font-semibold text-primary hover:text-primary-hover"
				>Esqueci a minha senha</a
			>
		</div>
		<div>
			<button
				type="submit"
				class="w-full flex justify-center py-3 px-4 text-lg font-bold rounded-md text-white bg-accent hover:bg-accent-hover"
				disabled={isLoading}
			>
				{#if isLoading}
					<span
						class="animate-spin h-5 w-5 mr-3 border-2 border-white border-t-transparent rounded-full"
					></span>
					A entrar...
				{:else}
					Entrar
				{/if}
			</button>
		</div>
	</form>
	<p class="mt-4 text-center text-base text-gray-600">
		Não tem uma conta?
		<a href="/cadastro" class="font-semibold text-primary hover:text-primary-hover">Registre-se</a>
	</p>
</div>

