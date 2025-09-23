<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	let fullName = '';
	let email = '';
	let password = '';
	let passwordConfirm = '';

	function handleSignUp() {
		if (password !== passwordConfirm) {
			showToast('As senhas não coincidem.', 'error');
			return;
		}

		if (localStorage.getItem(email)) {
			showToast('Este e-mail já está cadastrado.', 'error');
			return;
		}

		const professionalData = {
			fullName,
			email,
			password,
			role: 'professional'
		};

		localStorage.setItem(email, JSON.stringify(professionalData));
		showToast('Cadastro de profissional realizado com sucesso!', 'success');
		goto('/profissional/login');
	}
</script>

<div class="w-full max-w-md p-8 space-y-6 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-4xl font-bold text-gray-900">Crie a sua Conta Profissional</h2>
		<p class="mt-2 text-lg text-gray-600">Preencha os seus dados para aceder à plataforma.</p>
	</div>

	<form class="space-y-4" on:submit|preventDefault={handleSignUp}>
		<div>
			<label for="prof-fullName" class="block text-base font-semibold text-gray-700">Nome Completo</label>
			<input
				bind:value={fullName}
				id="prof-fullName"
				type="text"
				required
				class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg"
			/>
		</div>
		<div>
			<label for="prof-email-signup" class="block text-base font-semibold text-gray-700"
				>E-mail</label
			>
			<input
				bind:value={email}
				id="prof-email-signup"
				type="email"
				required
				class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg"
			/>
		</div>
		<div>
			<label for="prof-password-signup" class="block text-base font-semibold text-gray-700"
				>Senha</label
			>
			<input
				bind:value={password}
				id="prof-password-signup"
				type="password"
				required
				class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg"
			/>
		</div>
		<div>
			<label for="prof-password-confirm" class="block text-base font-semibold text-gray-700"
				>Confirmar Senha</label
			>
			<input
				bind:value={passwordConfirm}
				id="prof-password-confirm"
				type="password"
				required
				class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg"
			/>
		</div>
		<div class="flex items-center space-x-4 pt-4">
			<button
				type="button"
				on:click={() => goto('/profissional/login')}
				class="group relative w-full flex justify-center py-4 px-4 border border-gray-300 text-lg font-bold rounded-md text-gray-700 bg-white hover:bg-gray-50"
				>Voltar</button
			>
			<button
				type="submit"
				class="group relative w-full flex justify-center py-4 px-4 border border-transparent text-lg font-bold rounded-md text-white bg-accent hover:bg-accent-hover focus:outline-none focus:ring-4 focus:ring-offset-2 focus:ring-accent"
				>Criar Conta</button
			>
		</div>
	</form>
</div>
