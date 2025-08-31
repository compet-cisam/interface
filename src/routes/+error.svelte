<script lang="ts">
	import { page } from '$app/stores';
</script>

<div class="flex h-screen w-full flex-col items-center justify-center bg-gray-100">
	<div class="text-center">
		<h1 class="text-8xl font-bold text-primary">{$page.status}</h1>
		
		{#if $page.error}
			<p class="mt-4 text-2xl font-medium text-gray-700">Oops! Algo correu mal.</p>
			<p class="mt-2 text-gray-500">{$page.error.message}</p>
		{:else}
			<p class="mt-4 text-2xl font-medium text-gray-700">Página não encontrada</p>
		{/if}

		<div class="mt-8">
			<a href="/login" class="rounded-md bg-primary px-6 py-3 text-lg font-semibold text-white shadow-sm hover:bg-primary-hover">
				Voltar para o Login
			</a>
		</div>
	</div>
</div>
