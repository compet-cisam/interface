<script lang="ts">
	function handleImageError(event: Event) {
		const target = event.target as HTMLImageElement;
		const placeholderUrl = target.dataset.placeholder;
		if (placeholderUrl) {
			target.src = placeholderUrl;
		}
	}
</script>

<main
	class="flex min-h-screen w-full flex-col items-center justify-center bg-gray-50 p-4"
	style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);"
>
	<div class="mb-8 flex items-center space-x-6">
		<img
			src="/NUTES CISAM.png"
			alt="Logo NUTES CISAM UPE"
			class="h-16"
		/>
		<img
			src="/POLI UPE.png"
			alt="Logo Escola Politécnica de Pernambuco"
			class="h-20"
		/>
	</div>

	<div class="w-full max-w-md">
		<slot />
	</div>
</main>