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
	let email = ''; // Novo campo
	let password = '';
	let passwordConfirm = '';
	let securityQuestion = '';
	let securityAnswer = '';

	let validation = {
		length: false,
		uppercase: false,
		lowercase: false,
		number: false,
		symbol: false
	};

	function validatePassword(pass: string) {
		validation = {
			length: pass.length >= 8 && pass.length <= 15,
			uppercase: /[A-Z]/.test(pass),
			lowercase: /[a-z]/.test(pass),
			number: /[0-9]/.test(pass),
			symbol: /[^A-Za-z0-9]/.test(pass)
		};
	}

	$: validatePassword(password);

	function handleSignUp() {
		const allValid = Object.values(validation).every(Boolean);

		if (!allValid) {
			showToast('A sua senha não cumpre todos os requisitos de segurança.', 'error');
			return;
		}

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
			email,
			password,
			securityQuestion,
			securityAnswer
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
		<h2 class="text-4xl font-bold text-gray-900">Crie a sua conta</h2>
		<p class="mt-2 text-lg text-gray-600">
			Preencha seus dados abaixo corretamente para acessar a nossa plataforma.
		</p>
	</div>

	<form class="space-y-4" on:submit|preventDefault={handleSignUp}>
		<div>
			<label for="fullName" class="block text-base font-semibold text-gray-700">Nome Completo</label>
			<input bind:value={fullName} id="fullName" type="text" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
		</div>
		<div>
			<label for="motherName" class="block text-base font-semibold text-gray-700">Nome da Mãe</label>
			<input bind:value={motherName} id="motherName" type="text" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
		</div>
		<div>
			<label for="fatherName" class="block text-base font-semibold text-gray-700">Nome do Pai</label>
			<input bind:value={fatherName} id="fatherName" type="text" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
		</div>
		<div>
			<label for="birthDate" class="block text-base font-semibold text-gray-700">Data de Nascimento</label>
			<input bind:value={birthDate} id="birthDate" type="date" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
		</div>
		<div>
			<label for="cpf" class="block text-base font-semibold text-gray-700">CPF</label>
			<input bind:value={cpf} id="cpf" type="text" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
		</div>
		<div>
			<label for="email" class="block text-base font-semibold text-gray-700">E-mail</label>
			<input bind:value={email} id="email" type="email" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
		</div>

		<div>
			<label for="securityQuestion" class="block text-base font-semibold text-gray-700">Pergunta de Segurança</label>
			<select bind:value={securityQuestion} id="securityQuestion" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg bg-white">
				<option value="" disabled>Selecione uma pergunta...</option>
				<option value="animal">Nome do animal de estimação</option>
				<option value="cor">Cor preferida</option>
				<option value="comida">Comida preferida</option>
				<option value="amigo">Melhor amigo da infância</option>
				<option value="cidade">Cidade onde os pais se conheceram</option>
			</select>
		</div>

		<div>
			<label for="securityAnswer" class="block text-base font-semibold text-gray-700">Resposta de Segurança</label>
			<input bind:value={securityAnswer} id="securityAnswer" type="text" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
		</div>

		<div class="relative">
			<label for="password" class="block text-base font-semibold text-gray-700">Senha</label>
			<input bind:value={password} id="password" type="password" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
			<button type="button" on:click={() => togglePasswordVisibility('password')} class="absolute inset-y-0 right-0 top-6 px-3 flex items-center text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
			</button>
		</div>

		{#if password.length > 0}
			<div class="pt-2">
				<p class="text-sm text-gray-600 mb-2">A sua senha precisa de se encaixar nestes moldes:</p>
				<ul class="space-y-1 text-sm">
					<li class="flex items-center {validation.length ? 'text-green-600' : 'text-gray-500'}">
						<svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d={validation.length ? 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z' : 'M10 18a8 8 0 100-16 8 8 0 000 16zM9.293 11.293a1 1 0 011.414 0L12 12.586l1.293-1.293a1 1 0 111.414 1.414L13.414 14l1.293 1.293a1 1 0 01-1.414 1.414L12 15.414l-1.293 1.293a1 1 0 01-1.414-1.414L10.586 14 9.293 12.707a1 1 0 010-1.414z'} clip-rule="evenodd"></path></svg>
						Senha entre 8 - 15 dígitos
					</li>
					<li class="flex items-center {validation.lowercase ? 'text-green-600' : 'text-gray-500'}">
						<svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d={validation.lowercase ? 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z' : 'M10 18a8 8 0 100-16 8 8 0 000 16zM9.293 11.293a1 1 0 011.414 0L12 12.586l1.293-1.293a1 1 0 111.414 1.414L13.414 14l1.293 1.293a1 1 0 01-1.414 1.414L12 15.414l-1.293 1.293a1 1 0 01-1.414-1.414L10.586 14 9.293 12.707a1 1 0 010-1.414z'} clip-rule="evenodd"></path></svg>
						Pelo menos uma letra minúscula
					</li>
					<li class="flex items-center {validation.uppercase ? 'text-green-600' : 'text-gray-500'}">
						<svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d={validation.uppercase ? 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z' : 'M10 18a8 8 0 100-16 8 8 0 000 16zM9.293 11.293a1 1 0 011.414 0L12 12.586l1.293-1.293a1 1 0 111.414 1.414L13.414 14l1.293 1.293a1 1 0 01-1.414 1.414L12 15.414l-1.293 1.293a1 1 0 01-1.414-1.414L10.586 14 9.293 12.707a1 1 0 010-1.414z'} clip-rule="evenodd"></path></svg>
						Pelo menos uma letra maiúscula
					</li>
					<li class="flex items-center {validation.number ? 'text-green-600' : 'text-gray-500'}">
						<svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d={validation.number ? 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z' : 'M10 18a8 8 0 100-16 8 8 0 000 16zM9.293 11.293a1 1 0 011.414 0L12 12.586l1.293-1.293a1 1 0 111.414 1.414L13.414 14l1.293 1.293a1 1 0 01-1.414 1.414L12 15.414l-1.293 1.293a1 1 0 01-1.414-1.414L10.586 14 9.293 12.707a1 1 0 010-1.414z'} clip-rule="evenodd"></path></svg>
						Pelo menos um número
					</li>
					<li class="flex items-center {validation.symbol ? 'text-green-600' : 'text-gray-500'}">
						<svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d={validation.symbol ? 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z' : 'M10 18a8 8 0 100-16 8 8 0 000 16zM9.293 11.293a1 1 0 011.414 0L12 12.586l1.293-1.293a1 1 0 111.414 1.414L13.414 14l1.293 1.293a1 1 0 01-1.414 1.414L12 15.414l-1.293 1.293a1 1 0 01-1.414-1.414L10.586 14 9.293 12.707a1 1 0 010-1.414z'} clip-rule="evenodd"></path></svg>
						Pelo menos um símbolo (ex: !@#$%)
					</li>
				</ul>
			</div>
		{/if}

		<div class="relative">
			<label for="passwordConfirm" class="block text-base font-semibold text-gray-700">Confirmar Senha</label>
			<input bind:value={passwordConfirm} id="passwordConfirm" type="password" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-4 focus:ring-primary/50 text-lg" />
			<button type="button" on:click={() => togglePasswordVisibility('passwordConfirm')} class="absolute inset-y-0 right-0 top-6 px-3 flex items-center text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>
			</button>
		</div>

		<div class="flex items-center space-x-4 pt-4">
			<button type="button" on:click={() => goto('/login')} class="group relative w-full flex justify-center py-4 px-4 border border-gray-300 text-lg font-bold rounded-md text-gray-700 bg-white hover:bg-gray-50">Voltar</button>
			<button type="submit" class="group relative w-full flex justify-center py-4 px-4 border border-transparent text-lg font-bold rounded-md text-white bg-accent hover:bg-accent-hover focus:outline-none focus:ring-4 focus:ring-offset-2 focus:ring-accent">Criar Conta</button>
		</div>
	</form>
</div>





