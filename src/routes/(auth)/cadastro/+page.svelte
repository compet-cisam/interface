<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';

	const showToast = getContext<(message: string, type: 'success' | 'error') => void>('showToast');

	let fullName = '';
	let motherName = '';
	let fatherName = '';
	let birthDate = '';
	let cpf = '';
	let password = '';
	let passwordConfirm = '';

	function handleSignUp() {
		if (password !== passwordConfirm) {
			showToast('As senhas não coincidem.', 'error');
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
</script>

<div class="w-full max-w-md p-8 space-y-6 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-3xl font-bold text-gray-900">Criar Conta</h2>
		<p class="mt-2 text-sm text-gray-600">Preencha seus dados para se cadastrar.</p>
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
		<div>
			<label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
			<input bind:value={password} id="password" type="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
		</div>
		<div>
			<label for="passwordConfirm" class="block text-sm font-medium text-gray-700">Confirmar Senha</label>
			<input bind:value={passwordConfirm} id="passwordConfirm" type="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary" />
		</div>

		<div class="flex items-center space-x-4 pt-2">
			<a href="/login" class="group relative w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">Voltar</a>
			<button type="submit" class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-accent hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent">Criar Conta</button>
		</div>
	</form>
</div>

