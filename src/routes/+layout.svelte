<script lang="ts">
	import { setContext, onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { browser } from '$app/environment';
	import '../tailwind.css';

	type Toast = {
		id: number;
		message: string;
		type: 'success' | 'error';
	};
	const toasts = writable<Toast[]>([]);

	function showToast(message: string, type: 'success' | 'error' = 'success') {
		const newToast: Toast = { id: Date.now(), message, type };
		toasts.update((all) => [newToast, ...all]);
		setTimeout(() => {
			toasts.update((all) => all.filter((t) => t.id !== newToast.id));
		}, 3000);
	}
	setContext('showToast', showToast);
</script>

<style>
	:global(html) {
		--primary-color: #0038a8;
		--primary-hover-color: #002b82;
		--accent-color: #16a34a;
		--accent-hover-color: #15803d;
		--danger-color: #d8292f;
		--danger-hover-color: #b91c1c;
	}
	:global(.bg-primary) { background-color: var(--primary-color); }
	:global(.hover\:bg-primary-hover:hover) { background-color: var(--primary-hover-color); }
	:global(.focus\:ring-primary:focus) { --tw-ring-color: var(--primary-color); }
	:global(.bg-accent) { background-color: var(--accent-color); }
	:global(.hover\:bg-accent-hover:hover) { background-color: var(--accent-hover-color); }
	:global(.focus\:ring-accent:focus) { --tw-ring-color: var(--accent-color); }
	:global(.text-primary) { color: var(--primary-color); }
	:global(.hover\:text-primary-hover:hover) { color: var(--primary-hover-color); }
    :global(.bg-danger) { background-color: var(--danger-color); }
	:global(.hover\:bg-danger-hover:hover) { background-color: var(--danger-hover-color); }
	:global(.text-danger) { color: var(--danger-color); }
	:global(.hover\:text-danger-hover:hover) { color: var(--danger-hover-color); }
	:global(body) {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}
	:global(.flex-grow) {
		flex-grow: 1;
	}
</style>

<div aria-live="assertive" class="pointer-events-none fixed inset-0 flex items-start px-4 py-6 sm:p-6 z-50">
	<div class="flex w-full flex-col items-center space-y-4 sm:items-end">
		{#each $toasts as toast (toast.id)}
			<div class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5">
				<div class="p-4">
					<div class="flex items-start">
						<div class="flex-shrink-0">
							{#if toast.type === 'success'}
								<svg class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
							{:else}
								<svg class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>
							{/if}
						</div>
						<div class="ml-3 w-0 flex-1 pt-0.5">
							<p class="text-sm font-medium text-gray-900">{toast.message}</p>
						</div>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>

<div class="flex-grow">
	<slot />
</div>