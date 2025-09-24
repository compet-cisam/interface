<script lang="ts">
    import { goto } from '$app/navigation';
    import { getContext } from 'svelte';
    import { onMount } from 'svelte';

    const showToast: (message: string, type?: 'success' | 'error') => void = getContext('showToast');

    let email = '';
    let senha = '';
    let showPassword = false;

    function togglePasswordVisibility() {
        showPassword = !showPassword;
    }

    async function handleSubmit() {
        const professionalDataString = localStorage.getItem(email);

        if (professionalDataString) {
            try {
                const professionalData = JSON.parse(professionalDataString);
                
                if (professionalData.password === senha) {
                    showToast('Login bem-sucedido! Redirecionando...', 'success');
                    sessionStorage.setItem('loggedInUser', professionalDataString);

                    setTimeout(() => {
                        goto('/profissional/painel');
                    }, 1500);
                } else {
                    showToast('Email ou senha incorretos.', 'error');
                }
            } catch (e) {
                showToast('Ocorreu um erro. Tente novamente.', 'error');
            }
        } else {
            showToast('Email ou senha incorretos.', 'error');
        }
    }
</script>

<div class="flex flex-col items-center min-h-screen pt-12 sm:pt-24 bg-gradient-to-br from-blue-50 to-gray-50">
    <main class="flex-grow flex flex-col items-center justify-center p-4">
        <a href="/" class="flex items-center text-primary hover:text-primary-hover font-semibold transition-colors mb-6 text-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Voltar à Página Inicial
        </a>

        <div class="w-full max-w-sm sm:max-w-md md:max-w-xl bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
            <h1 class="text-3xl font-bold text-gray-800 text-center">Médico, acesse sua conta.</h1>
            <form on:submit|preventDefault={handleSubmit} class="mt-8 space-y-6">
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                    <input type="email" id="email" bind:value={email} class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" required />
                </div>
                <div>
                    <label for="senha" class="block text-sm font-medium text-gray-700">Senha</label>
                    <div class="mt-1 relative">
                        {#if showPassword}
                            <input type="text" id="senha" bind:value={senha} class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" required />
                        {:else}
                            <input type="password" id="senha" bind:value={senha} class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary" required />
                        {/if}
                        <button type="button" on:click={togglePasswordVisibility} class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-400 hover:text-primary" aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}></button>
                    </div>
                </div>
                <div class="text-right">
                    <a href="/esqueci-senha" class="text-base font-medium text-primary hover:text-primary-hover">Esqueci minha senha</a>
                </div>
                <button
                    type="submit"
                    class="w-full py-3 px-4 bg-accent text-white rounded-lg font-semibold hover:bg-accent-hover focus:outline-none focus:ring-4 focus:ring-accent/50 transition-colors text-lg"
                >
                    Entrar
                </button>
            </form>
            <p class="mt-8 text-center text-gray-600">
                Não tem uma conta?
                <a href="/profissional/cadastro" class="font-semibold text-primary hover:text-primary-hover transition-colors">Cadastrar-se</a>
            </p>
        </div>
    </main>
</div>