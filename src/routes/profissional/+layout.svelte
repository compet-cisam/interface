<script lang="ts">
	// Esta função para imagens com erro é uma ótima ideia! Vamos mantê-la.
	function handleImageError(event: Event) {
		const target = event.target as HTMLImageElement;
		const placeholderUrl = target.dataset.placeholder;
		if (placeholderUrl) {
			target.src = placeholderUrl;
		}
	}
</script>

<main
	class="flex min-h-screen w-full flex-col items-center bg-gray-50 p-4"
	style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);"
>
	<div class="w-full max-w-md pt-8"> <div class="mb-8 flex justify-center">
			<img
				src="/NUTES CISAM.png"
				alt="Logo NUTES CISAM UPE"
				class="h-20"
				data-placeholder="https://placehold.co/150x50/DDDDDD/000000?text=NUTES"
				on:error={handleImageError}
			/>
		</div>

		<slot />
	</div>
</main>

