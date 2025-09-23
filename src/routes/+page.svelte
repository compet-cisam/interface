<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		goto('/login');
	});
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-50">
	<p class="text-lg text-gray-600">Estamos lhe redirecionando para a nossa plataforma.</p>
	<p class="text-lg text-gray-600">Por favor, aguarde mais um pouco...</p>
</div>