<script lang="ts">
	import { page } from '$app/stores';
	import { browser } from '$app/environment';

	function goBack() {
		if (browser) {
			window.history.back();
		}
	}
</script>

<main
	class="flex min-h-screen w-full flex-col items-center justify-center bg-gray-100 p-4 text-center"
>
	<div class="max-w-lg">
		<h1 class="text-9xl font-bold text-primary">{$page.status}</h1>
		<h2 class="mt-4 text-4xl font-bold text-gray-800">Oops! Algo correu mal.</h2>
		{#if $page.error?.message}
			<p class="mt-2 text-lg text-gray-500">{$page.error.message}</p>
		{/if}

		<div class="mt-12 flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
			<button
				on:click={goBack}
				class="w-full rounded-md border border-gray-300 bg-white px-8 py-4 text-lg font-bold text-gray-700 shadow-sm hover:bg-gray-50"
			>
				Voltar à página anterior
			</button>
			<a
				href="/"
				class="w-full inline-block rounded-md border border-transparent bg-primary px-8 py-4 text-lg font-bold text-white shadow-sm hover:bg-primary-hover"
			>
				Voltar para a Página Inicial
			</a>
		</div>
	</div>
</main>
