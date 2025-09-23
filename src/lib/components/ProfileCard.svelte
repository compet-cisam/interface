<script lang="ts">
	import { goto } from '$app/navigation';

	export let href: string;
	export let imageSrc: string;
	export let imageAlt: string;
	export let label: string;
</script>

<button
	on:click={() => goto(href)}
	class="group text-center bg-white p-10 rounded-2xl shadow-lg border border-transparent hover:border-blue-500 hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 ease-in-out cursor-pointer"
	aria-label="Selecionar perfil de {label}"
>
	<div class="mb-6 flex h-28 w-28 items-center justify-center mx-auto">
		<img src={imageSrc} alt={imageAlt} class="h-full w-full object-contain" />
	</div>
	<h3 class="text-2xl font-semibold text-gray-800 group-hover:text-blue-600 transition-colors">
		{label}
	</h3>
</button>