<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';

	const showToast = getContext<(message: string, type: 'success' | 'error') => void>('showToast');

	let newPassword = '';
	let confirmPassword = '';

	function handleResetPassword() {
		const identifierToReset = sessionStorage.getItem('resetPasswordIdentifier');
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
		}
	}
</script>

<div class="w-full max-w-md p-8 space-y-8 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-3xl font-bold text-gray-900">Crie uma Nova Senha</h2>
		<p class="mt-2 text-sm text-gray-600">Sua nova senha deve ser diferente da anterior.</p>
	</div>
	<form class="mt-8 space-y-6" on:submit|preventDefault={handleResetPassword}>
		<div>
			<label for="reset-password" class="block text-sm font-medium text-gray-700">Nova Senha</label>
			<input bind:value={newPassword} id="reset-password" type="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary">
		</div>
		<div>
			<label for="reset-password-confirm" class="block text-sm font-medium text-gray-700">Confirmar Nova Senha</label>
			<input bind:value={confirmPassword} id="reset-password-confirm" type="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary">
		</div>
		<div class="pt-2">
			<button type="submit" class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-accent hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent">Salvar Nova Senha</button>
		</div>
	</form>
</div>

