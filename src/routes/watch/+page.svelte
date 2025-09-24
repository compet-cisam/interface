<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		const videoId = $page.url.searchParams.get('v');

		if (videoId) {
			goto(`/?youtube=${encodeURIComponent(videoId)}`);
		} else {
			goto('/');
		}
	});
</script>

<!-- Esta página serve apenas para redirecionamento e não precisa de conteúdo visível -->
<div class="flex h-screen w-full items-center justify-center bg-gray-100">
	<p class="text-gray-500">A redirecionar...</p>
</div>