<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		goto('/login');
	});
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-50">
	<p class="text-lg text-gray-600">A redirecionar para o portal do paciente...</p>
</div>