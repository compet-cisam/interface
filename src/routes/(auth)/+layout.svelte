<script lang="ts">
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';

	const showToast: (message: string, type: 'success' | 'error') => void =
		getContext('showToast');
</script>

<main class="flex min-h-screen w-full items-center justify-center bg-gray-50 p-4" style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);">
	<div class="w-full max-w-md">
		<slot />
	</div>
</main>