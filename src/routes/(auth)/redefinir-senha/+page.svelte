<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	let newPassword = '';
	let confirmPassword = '';
	let isVerified = false;
	let identifierToReset: string | null = null;

	onMount(() => {
		identifierToReset = sessionStorage.getItem('resetPasswordIdentifier');
		if (!identifierToReset) {
			showToast('Acesso não autorizado. Por favor, valide os seus dados primeiro.', 'error');
			goto('/esqueci-senha');
		} else {
			isVerified = true;
		}
	});

	function handleResetPassword() {
		if (!identifierToReset) {
			showToast('Sessão de redefinição inválida.', 'error');
			goto('/login');
			return;
		}
		if (newPassword !== confirmPassword) {
			showToast('As novas senhas não coincidem.', 'error');
			return;
		}
		
		const userDataString = localStorage.getItem(identifierToReset);
		if (userDataString) {
			const userData = JSON.parse(userDataString);
			userData.password = newPassword;
			localStorage.setItem(identifierToReset, JSON.stringify(userData));
			showToast('Senha redefinida com sucesso!', 'success');
			sessionStorage.removeItem('resetPasswordIdentifier');
			goto('/login');
		} else {
			showToast('Ocorreu um erro ao atualizar a senha.', 'error');
		}
	}
</script>

{#if isVerified}
	<div class="w-full p-8 space-y-8 bg-white rounded-2xl shadow-lg">
		<div class="text-center">
			<h2 class="text-4xl font-bold text-gray-900">Crie uma Nova Senha</h2>
			<p class="mt-2 text-lg text-gray-600">A sua nova senha deve ser diferente da anterior.</p>
		</div>
		<form class="mt-8 space-y-6" on:submit|preventDefault={handleResetPassword}>
			<div>
				<label for="reset-password" class="block text-base font-semibold text-gray-700">Nova Senha</label>
				<input bind:value={newPassword} id="reset-password" type="password" required class="mt-2 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg">
			</div>
			<div>
				<label for="reset-password-confirm" class="block text-base font-semibold text-gray-700">Confirmar Nova Senha</label>
				<input bind:value={confirmPassword} id="reset-password-confirm" type="password" required class="mt-2 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg">
			</div>
			<div class="pt-4">
				<button type="submit" class="group relative w-full flex justify-center py-4 px-4 border border-transparent text-lg font-bold rounded-md text-white bg-accent hover:bg-accent-hover focus:outline-none focus:ring-4 focus:ring-offset-2 focus:ring-accent">Salvar Nova Senha</button>
			</div>
		</form>
	</div>
{:else}
	<div class="text-center">
		<p class="text-lg text-gray-600">A redirecionar...</p>
	</div>
{/if}