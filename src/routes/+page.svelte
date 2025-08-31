<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		goto('/login');
	});
</script>

<div class="flex items-center justify-center min-h-screen">
	<p>Redirecionando para a página de login...</p>
</div>
