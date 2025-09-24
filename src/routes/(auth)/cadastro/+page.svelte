<script lang="ts">
	import { getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	type UserType = 'paciente' | 'medico' | 'admin';
	let selectedUserType: UserType = 'paciente';

	// Campos Comuns
	let fullName = '';
	let email = '';
	let password = '';
	let confirmPassword = '';

	// Campos do Paciente
	let birthDate = '';
	let cpf = '';
	let medicalRecordNumber = '';
	let zipCode = '';
	let phoneNumber = '';
	let cnsNumber = '';
	let city = '';
	let age = '';

	// Campos do Médico
	let crm = '';
	
	// Campos do Admin
	let adminCode = '';

	let isLoading = false;

	function handleRegister() {
		isLoading = true;

		setTimeout(() => {
			if (password !== confirmPassword) {
				showToast('As senhas não coincidem.', 'error');
				isLoading = false;
				return;
			}

			const strength = checkPasswordStrength(password);
			if (strength.level !== 'Forte') {
				showToast('A sua senha não cumpre todos os requisitos de segurança.', 'error');
				isLoading = false;
				return;
			}

			let userData: any = {};
			let userKey: string = '';

			if (selectedUserType === 'paciente') {
				if (!fullName || !cpf || !email) {
					showToast('Por favor, preencha todos os campos obrigatórios.', 'error');
					isLoading = false;
					return;
				}
				userData = {
					fullName,
					birthDate,
					cpf,
					email,
					password,
					medicalRecordNumber,
					zipCode,
					phoneNumber,
					cnsNumber,
					city,
					age
				};
				userKey = cpf;
			} else if (selectedUserType === 'medico') {
				if (!fullName || !crm || !email) {
					showToast('Por favor, preencha todos os campos obrigatórios.', 'error');
					isLoading = false;
					return;
				}
				userData = { fullName, crm, email, password };
				userKey = crm;
			} else if (selectedUserType === 'admin') {
				if (!adminCode) {
					showToast('Por favor, preencha o código de acesso.', 'error');
					isLoading = false;
					return;
				}
				userData = { adminCode, password, fullName: 'Administrador' };
				userKey = adminCode;
			}

			if (localStorage.getItem(userKey)) {
				showToast('Este utilizador já está registado.', 'error');
				isLoading = false;
				return;
			}

			localStorage.setItem(userKey, JSON.stringify(userData));
			showToast('Conta criada com sucesso! Faça o login.', 'success');
			goto('/login');

			isLoading = false;
		}, 500);
	}

	function checkPasswordStrength(pass: string) {
		let score = 0;
		const checks = {
			length: pass.length >= 8 && pass.length <= 15,
			lowercase: /[a-z]/.test(pass),
			uppercase: /[A-Z]/.test(pass),
			number: /[0-9]/.test(pass),
			special: /[^a-zA-Z0-9]/.test(pass)
		};

		if (checks.length) score++;
		if (checks.lowercase) score++;
		if (checks.uppercase) score++;
		if (checks.number) score++;
		if (checks.special) score++;

		let level: 'Fraca' | 'Moderada' | 'Forte' = 'Fraca';
		let color = 'bg-red-500';
		const widths = ['w-0', 'w-[20%]', 'w-[40%]', 'w-[60%]', 'w-[80%]', 'w-full'];
		const width = widths[score];

		if (score >= 5) {
			level = 'Forte';
			color = 'bg-green-500';
		} else if (score >= 3) {
			level = 'Moderada';
			color = 'bg-yellow-500';
		}

		return { level, color, width, checks };
	}

	let passwordStrength = {
		level: 'Fraca',
		color: 'bg-red-500',
		width: 'w-0',
		checks: {
			length: false,
			lowercase: false,
			uppercase: false,
			number: false,
			special: false
		}
	};

	$: passwordStrength = checkPasswordStrength(password);

	function togglePasswordVisibility(inputId: string) {
		const input = document.getElementById(inputId) as HTMLInputElement | null;
		if (input) {
			input.type = input.type === 'password' ? 'text' : 'password';
		}
	}
</script>

<div class="w-full max-w-2xl p-8 space-y-6 bg-white rounded-2xl shadow-lg">
	<div class="text-center">
		<h2 class="text-4xl font-bold text-gray-900">Crie sua Conta</h2>
		<p class="mt-2 text-lg text-gray-600">Selecione o seu tipo de perfil para se cadastrar na nossa plataforma.</p>
	</div>

	<div class="flex border-b border-gray-200">
		<button
			class="flex-1 py-3 text-lg font-semibold text-center transition-colors {selectedUserType ===
			'paciente'
				? 'border-b-2 border-primary text-primary'
				: 'text-gray-500 hover:text-gray-700'}"
			on:click={() => (selectedUserType = 'paciente')}>Paciente</button
		>
		<button
			class="flex-1 py-3 text-lg font-semibold text-center transition-colors {selectedUserType ===
			'medico'
				? 'border-b-2 border-primary text-primary'
				: 'text-gray-500 hover:text-gray-700'}"
			on:click={() => (selectedUserType = 'medico')}>Médico</button
		>
		<button
			class="flex-1 py-3 text-lg font-semibold text-center transition-colors {selectedUserType ===
			'admin'
				? 'border-b-2 border-primary text-primary'
				: 'text-gray-500 hover:text-gray-700'}"
			on:click={() => (selectedUserType = 'admin')}>Administrador</button
		>
	</div>

	<form class="mt-8 space-y-6" on:submit|preventDefault={handleRegister}>
		{#if selectedUserType === 'paciente'}
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div>
					<label for="fullName" class="block text-base font-semibold text-gray-700"
						>Nome Completo</label
					>
					<input
						bind:value={fullName}
						type="text"
						required
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="cpf" class="block text-base font-semibold text-gray-700">CPF</label>
					<input
						bind:value={cpf}
						type="text"
						required
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="email" class="block text-base font-semibold text-gray-700">E-mail</label>
					<input
						bind:value={email}
						type="email"
						required
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="birthDate" class="block text-base font-semibold text-gray-700"
						>Data de Nascimento</label
					>
					<input
						bind:value={birthDate}
						type="date"
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="age" class="block text-base font-semibold text-gray-700">Idade</label>
					<input
						bind:value={age}
						type="number"
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="phoneNumber" class="block text-base font-semibold text-gray-700"
						>Número de Celular</label
					>
					<input
						bind:value={phoneNumber}
						type="tel"
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="cnsNumber" class="block text-base font-semibold text-gray-700">CNS</label>
					<input
						bind:value={cnsNumber}
						type="text"
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="medicalRecordNumber" class="block text-base font-semibold text-gray-700"
						>Número de Prontuário</label
					>
					<input
						bind:value={medicalRecordNumber}
						type="text"
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="zipCode" class="block text-base font-semibold text-gray-700">CEP</label>
					<input
						bind:value={zipCode}
						type="text"
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
				<div>
					<label for="city" class="block text-base font-semibold text-gray-700">Cidade</label>
					<input
						bind:value={city}
						type="text"
						class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					/>
				</div>
			</div>
		{:else if selectedUserType === 'medico'}
			<div>
				<label for="fullName" class="block text-base font-semibold text-gray-700"
					>Nome Completo</label
				>
				<input
					bind:value={fullName}
					type="text"
					required
					class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
				/>
			</div>
			<div>
				<label for="crm" class="block text-base font-semibold text-gray-700">CRM</label>
				<input
					bind:value={crm}
					type="text"
					required
					class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
					placeholder="CRM-PE 123456"
				/>
			</div>
			<div>
				<label for="email" class="block text-base font-semibold text-gray-700">E-mail</label>
				<input
					bind:value={email}
					type="email"
					required
					class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
				/>
			</div>
		{:else if selectedUserType === 'admin'}
			<div>
				<label for="adminCode" class="block text-base font-semibold text-gray-700"
					>Código de Acesso</label
				>
				<input
					bind:value={adminCode}
					type="text"
					required
					class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
				/>
			</div>
		{/if}

		<div class="relative">
			<label for="password" class="block text-base font-semibold text-gray-700">Senha</label>
			<input
				bind:value={password}
				id="password"
				type="password"
				required
				class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
			/>
			<button
				type="button"
				on:click={() => togglePasswordVisibility('password')}
				class="absolute inset-y-0 right-0 top-6 px-3 flex items-center text-gray-500"
			>
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
					><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" /><circle
						cx="12"
						cy="12"
						r="3"
					/></svg
				>
			</button>
		</div>

		{#if password}
			<!-- Password Strength Indicator -->
			<div class="space-y-2">
				<div class="flex items-center justify-between">
					<p class="text-sm font-medium text-gray-700">Força da senha:</p>
					<p
						class="text-sm font-bold {passwordStrength.level === 'Forte'
							? 'text-green-600'
							: passwordStrength.level === 'Moderada'
							? 'text-yellow-600'
							: 'text-red-600'}"
					>
						{passwordStrength.level}
					</p>
				</div>
				<div class="w-full bg-gray-200 rounded-full h-2">
					<div
						class="h-2 rounded-full transition-all duration-300 {passwordStrength.color} {passwordStrength.width}"
					/>
				</div>
				<ul class="pt-2 text-sm text-gray-500 space-y-1">
					<li class="flex items-center">
						<svg
							class="w-4 h-4 mr-2 {passwordStrength.checks.length ? 'text-green-500' : 'text-gray-400'}"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							><path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M5 13l4 4L19 7"
							/></svg
						>
						Entre 8 e 15 caracteres
					</li>
					<li class="flex items-center">
						<svg
							class="w-4 h-4 mr-2 {passwordStrength.checks.uppercase && passwordStrength.checks.lowercase
								? 'text-green-500'
								: 'text-gray-400'}"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							><path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M5 13l4 4L19 7"
							/></svg
						>
						Letras maiúsculas e minúsculas
					</li>
					<li class="flex items-center">
						<svg
							class="w-4 h-4 mr-2 {passwordStrength.checks.number ? 'text-green-500' : 'text-gray-400'}"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							><path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M5 13l4 4L19 7"
							/></svg
						>
						Pelo menos um número
					</li>
					<li class="flex items-center">
						<svg
							class="w-4 h-4 mr-2 {passwordStrength.checks.special ? 'text-green-500' : 'text-gray-400'}"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							><path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M5 13l4 4L19 7"
							/></svg
						>
						Pelo menos um caracter especial
					</li>
				</ul>
			</div>
		{/if}

		<div class="relative">
			<label for="confirmPassword" class="block text-base font-semibold text-gray-700"
				>Confirmar Senha</label
			>
			<input
				bind:value={confirmPassword}
				id="confirmPassword"
				type="password"
				required
				class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md"
			/>
			<button
				type="button"
				on:click={() => togglePasswordVisibility('confirmPassword')}
				class="absolute inset-y-0 right-0 top-6 px-3 flex items-center text-gray-500"
			>
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
					><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" /><circle
						cx="12"
						cy="12"
						r="3"
					/></svg
				>
			</button>
		</div>

		<div>
			<button
				type="submit"
				class="w-full flex justify-center py-3 px-4 text-lg font-bold rounded-md text-white bg-accent hover:bg-accent-hover disabled:opacity-75"
				disabled={isLoading}
			>
				{#if isLoading}
					<span
						class="animate-spin h-5 w-5 mr-3 border-2 border-white border-t-transparent rounded-full"
					/>
					Criando conta...
				{:else}
					Criar Conta
				{/if}
			</button>
		</div>
	</form>

	<p class="mt-4 text-center text-base text-gray-600">
		Já tem uma conta?
		<a href="/login" class="font-semibold text-primary hover:text-primary-hover">Faça o login</a>
	</p>
</div>

