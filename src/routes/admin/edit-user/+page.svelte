<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');

	interface User {
		fullName: string;
		cpf?: string;
		crm?: string;
		userType: 'patient' | 'doctor' | 'admin';
	}

	let currentUser: User | null = null;
	let allUsers: User[] = [];
	let filteredUsers: User[] = [];
	let searchTerm = '';

	onMount(() => {
		const loggedInUserStr = sessionStorage.getItem('loggedInUser');
		if (loggedInUserStr) {
			currentUser = JSON.parse(loggedInUserStr);
			if (currentUser?.userType !== 'admin') {
				goto('/login');
			}
		} else {
			goto('/login');
		}

		loadAllUsers();
	});

	function loadAllUsers() {
		const users: User[] = [];
		for (let i = 0; i < localStorage.length; i++) {
			const key = localStorage.key(i);
			if (key) {
				try {
					const user = JSON.parse(localStorage.getItem(key) as string);
					if (user && user.userType && (user.userType === 'patient' || user.userType === 'doctor')) {
						users.push(user);
					}
				} catch (e) {
					console.error('Could not parse user from localStorage', e);
				}
			}
		}
		allUsers = users;
		filteredUsers = users;
	}

	function handleSearch() {
		if (!searchTerm) {
			filteredUsers = allUsers;
			return;
		}
		const lowerCaseSearch = searchTerm.toLowerCase();
		filteredUsers = allUsers.filter(user =>
			user.fullName.toLowerCase().includes(lowerCaseSearch)
		);
	}

	function editUser(user: User) {
		const identifier = user.cpf || user.crm;
		if (identifier) {
			sessionStorage.setItem('userToEdit', identifier);
			goto('/admin/edit-user');
		}
	}
	
	function loginAsUser(user: User) {
		sessionStorage.setItem('adminSession', JSON.stringify(currentUser));
		sessionStorage.setItem('loggedInUser', JSON.stringify(user));
		if(user.userType === 'patient'){
			goto('/painel');
		} else {
			goto('/profissional');
		}
	}

	function deleteUser(user: User) {
		const key = user.cpf || user.crm;
		if (key && confirm(`Tem a certeza que deseja apagar o utilizador ${user.fullName}?`)) {
			localStorage.removeItem(key);
			localStorage.removeItem(`exams_${key}`);
			loadAllUsers();
			showToast('Utilizador apagado com sucesso.', 'success');
		}
	}

	function handleLogout() {
		sessionStorage.removeItem('loggedInUser');
		goto('/login');
	}

</script>

<div class="min-h-screen bg-gray-50 flex-grow" style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);">
	<main class="container mx-auto p-4 sm:p-6 lg:p-8">
		<div class="flex justify-between items-center mb-6">
			<div>
				<h1 class="text-3xl font-bold text-gray-900">Painel do Administrador</h1>
				{#if currentUser}
					<p class="text-lg text-gray-600">Bem-vindo, {currentUser.fullName}!</p>
				{/if}
			</div>
			<button
				on:click={handleLogout}
				class="font-semibold text-danger hover:text-danger-hover transition-colors text-lg"
			>
				Sair
			</button>
		</div>

		<div class="space-y-12">
			<div class="bg-white p-6 rounded-2xl shadow-lg">
				<h2 class="text-2xl font-bold text-gray-800 mb-4">Gerir Utilizadores</h2>
				<div class="flex gap-4 mb-4">
					<input 
						type="text"
						bind:value={searchTerm}
						on:input={handleSearch}
						placeholder="Procurar por nome..."
						class="w-full px-4 py-2 border border-gray-300 rounded-md"
					/>
				</div>

				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Identificador (CPF/CRM)</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
								<th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							{#each filteredUsers as user (user.cpf || user.crm)}
								<tr>
									<td class="px-6 py-4 whitespace-nowrap">{user.fullName}</td>
									<td class="px-6 py-4 whitespace-nowrap">{user.cpf || user.crm}</td>
									<td class="px-6 py-4 whitespace-nowrap capitalize">{user.userType}</td>
									<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-4">
										<button on:click={() => loginAsUser(user)} class="text-primary hover:text-primary-hover">Aceder</button>
										<button on:click={() => editUser(user)} class="text-yellow-600 hover:text-yellow-800">Editar</button>
										<button on:click={() => deleteUser(user)} class="text-danger hover:text-danger-hover">Apagar</button>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
					{#if filteredUsers.length === 0}
						<p class="text-center text-gray-500 py-4">Nenhum utilizador encontrado.</p>
					{/if}
				</div>
			</div>
		</div>
	</main>
</div>

