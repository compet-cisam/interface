<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	let fullName = '';
	let motherName = '';
	let fatherName = '';
	let birthDate = '';
	let cpf = '';
	let password = '';
	let passwordConfirm = '';

	// Novo objeto para validar os requisitos da senha
	let passwordRequirements = {
		length: false,
		uppercase: false,
		lowercase: false,
		number: false,
		symbol: false
	};

	// Função que verifica a senha em tempo real
	function validatePassword(pass: string) {
		passwordRequirements = {
			length: pass.length >= 8 && pass.length <= 15,
			uppercase: /[A-Z]/.test(pass),
			lowercase: /[a-z]/.test(pass),
			number: /[0-9]/.test(pass),
			symbol: /[^a-zA-Z0-9]/.test(pass)
		};
	}

	// Observa a variável 'password' e chama a validação sempre que ela muda
	$: validatePassword(password);

	function handleSignUp() {
		if (password !== passwordConfirm) {
			showToast('As senhas não coincidem.', 'error');
			return;
		}
		
		// Verifica se todos os requisitos da senha foram cumpridos
		const allRequirementsMet = Object.values(passwordRequirements).every(req => req === true);
		if (!allRequirementsMet) {
			showToast('A senha não cumpre todos os requisitos de segurança.', 'error');
			return;
		}

		if (localStorage.getItem(cpf)) {
			showToast('Este CPF já está cadastrado.', 'error');
			return;
		}

		const userData = {
			fullName,
			motherName,
			fatherName,
			birthDate,
			cpf,
			password
		};

		localStorage.setItem(cpf, JSON.stringify(userData));
		showToast('Cadastro realizado com sucesso!', 'success');
		goto('/login');
	}

	function togglePasswordVisibility(inputId: string) {
		const input = document.getElementById(inputId) as HTMLInputElement | null;
		if (input) {
			input.type = input.type === 'password' ? 'text' : 'password';
		}
	}
</script>

<div class="w-full max-w-md p-8 space-y-6 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-3xl font-bold text-gray-900">Crie a sua Conta</h2>
		<p class="mt-2 text-sm text-gray-600">Preencha os seus dados para aceder ao portal.</p>
	</div>

	<form class="space-y-4" on:submit|preventDefault={handleSignUp}>
		<div>
			<label for="fullName" class="block text-sm font-medium text-gray-700">Nome Completo</label>
			<input bind:value={fullName} id="fullName" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
		</div>
		<div>
			<label for="motherName" class="block text-sm font-medium text-gray-700">Nome da Mãe</label>
			<input bind:value={motherName} id="motherName" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
		</div>
		<div>
			<label for="fatherName" class="block text-sm font-medium text-gray-700">Nome do Pai</label>
			<input bind:value={fatherName} id="fatherName" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
		</div>
		<div>
			<label for="birthDate" class="block text-sm font-medium text-gray-700">Data de Nascimento</label>
			<input bind:value={birthDate} id="birthDate" type="date" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
		</div>
		<div>
			<label for="cpf" class="block text-sm font-medium text-gray-700">CPF</label>
			<input bind:value={cpf} id="cpf" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
		</div>

		<div class="relative">
			<label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
			<input bind:value={password} id="password" type="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
			<button type="button" on:click={() => togglePasswordVisibility('password')} class="absolute inset-y-0 right-0 top-6 px-3 flex items-center text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
			</button>
		</div>

		<!-- Bloco de Validação de Senha -->
		{#if password.length > 0}
			<div class="pt-1">
				<p class="text-sm font-medium text-gray-700 mb-2">A sua senha precisa de ter:</p>
				<div class="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
					<div class="flex items-center {passwordRequirements.length ? 'text-green-600' : 'text-gray-500'} transition-colors">
						<svg class="w-4 h-4 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
							{#if passwordRequirements.length}
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
							{/if}
						</svg>
						8-15 dígitos
					</div>
					<div class="flex items-center {passwordRequirements.uppercase ? 'text-green-600' : 'text-gray-500'} transition-colors">
						<svg class="w-4 h-4 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
							{#if passwordRequirements.uppercase}
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
							{/if}
						</svg>
						Letra maiúscula
					</div>
					<div class="flex items-center {passwordRequirements.lowercase ? 'text-green-600' : 'text-gray-500'} transition-colors">
						<svg class="w-4 h-4 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
							{#if passwordRequirements.lowercase}
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
							{/if}
						</svg>
						Letra minúscula
					</div>
					<div class="flex items-center {passwordRequirements.number ? 'text-green-600' : 'text-gray-500'} transition-colors">
						<svg class="w-4 h-4 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
							{#if passwordRequirements.number}
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
							{/if}
						</svg>
						Um número
					</div>
					<div class="flex items-center {passwordRequirements.symbol ? 'text-green-600' : 'text-gray-500'} transition-colors">
						<svg class="w-4 h-4 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
							{#if passwordRequirements.symbol}
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
							{/if}
						</svg>
						Um símbolo
					</div>
				</div>
			</div>
		{/if}

		<div class="relative">
			<label for="passwordConfirm" class="block text-sm font-medium text-gray-700">Confirmar Senha</label>
			<input bind:value={passwordConfirm} id="passwordConfirm" type="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
			<button type="button" on:click={() => togglePasswordVisibility('passwordConfirm')} class="absolute inset-y-0 right-0 top-6 px-3 flex items-center text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
			</button>
		</div>

		<div class="flex items-center space-x-4 pt-4">
			<button type="button" on:click={() => goto('/login')} class="group relative w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">Voltar</button>
			<button type="submit" class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-accent hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent">Criar Conta</button>
		</div>
	</form>
</div>



