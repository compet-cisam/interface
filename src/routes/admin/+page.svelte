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
		accessCode?: string;
	}

	let currentUser: User | null = null;
	let allUsers: User[] = [];
	let searchTerm = '';
	let searchResults: User[] = [];

	onMount(() => {
		const loggedInUserStr = sessionStorage.getItem('loggedInUser');
		if (loggedInUserStr) {
			currentUser = JSON.parse(loggedInUserStr);
			if (!currentUser?.accessCode) {
				goto('/login');
			}
		} else {
			goto('/login');
		}
		loadUsers();
	});

	function loadUsers() {
		const users = [];
		for (let i = 0; i < localStorage.length; i++) {
			const key = localStorage.key(i);
			if (key) {
				try {
					const data = JSON.parse(localStorage.getItem(key)!);
					if (data && data.password) {
						users.push(data);
					}
				} catch (e) {
					// Ignorar
				}
			}
		}
		allUsers = users;
		searchResults = users;
	}

	function handleSearch() {
		if (!searchTerm) {
			searchResults = allUsers;
			return;
		}
		searchResults = allUsers.filter((user) =>
			user.fullName.toLowerCase().includes(searchTerm.toLowerCase())
		);
	}

	function editUser(user: User) {
		const id = user.cpf || user.crm || user.accessCode;
		if (id) {
			goto(`/admin/edit-user?id=${id}`);
		}
	}

	function deleteUser(user: User) {
		const id = user.cpf || user.crm || user.accessCode;
		if (id && confirm(`Tem a certeza de que deseja apagar o utilizador ${user.fullName}?`)) {
			localStorage.removeItem(id);
			loadUsers();
			handleSearch();
			showToast('Utilizador apagado com sucesso.', 'success');
		}
	}

	function loginAsUser(user: User) {
		sessionStorage.setItem('adminSession', JSON.stringify(currentUser));
		sessionStorage.setItem('loggedInUser', JSON.stringify(user));
		if (user.cpf) {
			goto('/painel');
		} else if (user.crm) {
			goto('/profissional');
		}
	}

	function handleLogout() {
		sessionStorage.removeItem('loggedInUser');
		goto('/login');
	}
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 flex-grow">
	<div class="flex items-center justify-between mb-2">
		<h1 class="text-3xl font-bold text-gray-900">Painel do Administrador</h1>
		<button
			on:click={handleLogout}
			class="font-semibold text-danger hover:text-danger-hover transition-colors text-lg"
		>
			Sair
		</button>
	</div>
	<p class="text-lg text-gray-600 mb-8">
		Bem-vindo, {currentUser?.fullName}. Gestão de utilizadores do sistema.
	</p>

	<div class="rounded-2xl bg-white p-6 sm:p-8 shadow-lg">
		<h2 class="text-2xl font-bold text-gray-900">Buscar Utilizador</h2>
		<form class="mt-4" on:submit|preventDefault={handleSearch}>
			<div class="flex items-center">
				<input
					bind:value={searchTerm}
					on:input={handleSearch}
					type="text"
					placeholder="Digite o nome do paciente ou médico"
					class="flex-grow block w-full px-4 py-3 border border-gray-300 rounded-l-md"
				/>
				<button
					type="submit"
					class="px-6 py-3 border border-transparent font-bold rounded-r-md text-white bg-accent hover:bg-accent-hover"
				>
					Buscar
				</button>
			</div>
		</form>

		<div class="mt-8 overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nome</th>
						<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
							>Identificador</th
						>
						<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
						<th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase"
							>Ações</th
						>
					</tr>
				</thead>
				<tbody class="bg-white divide-y divide-gray-200">
					{#each searchResults as user}
						<tr>
							<td class="px-6 py-4 whitespace-nowrap">{user.fullName}</td>
							<td class="px-6 py-4 whitespace-nowrap">{user.cpf || user.crm || 'N/A'}</td>
							<td class="px-6 py-4 whitespace-nowrap">
								{#if user.cpf}
									<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
										Paciente
									</span>
								{:else if user.crm}
									<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
										Médico
									</span>
								{:else if user.accessCode}
									<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
										Admin
									</span>
								{/if}
							</td>
							<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-4">
								{#if user.cpf || user.crm}
									<button on:click={() => loginAsUser(user)} class="text-primary hover:text-primary-hover">Aceder como</button>
								{/if}
								<button on:click={() => editUser(user)} class="text-yellow-600 hover:text-yellow-800">Editar</button>
								<button on:click={() => deleteUser(user)} class="text-danger hover:text-danger-hover">Apagar</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
			{#if searchResults.length === 0}
				<p class="text-center text-gray-500 py-8">Nenhum utilizador encontrado.</p>
			{/if}
		</div>
	</div>
</main>

