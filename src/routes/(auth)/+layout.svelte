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
	class="flex min-h-screen w-full flex-col items-center justify-start bg-gray-50 p-4 pt-8"
	style="background: linear-gradient(to bottom, #FFFFFF, #EBF8FF);"
>
	<div class="w-full max-w-md">
		<div class="mb-8 flex justify-center items-center">
			<img
				src="/NUTES CISAM.png"
				alt="Logo NUTES CISAM UPE"
				class="h-28"
				data-placeholder="https://placehold.co/150x50/DDDDDD/000000?text=NUTES"
				on:error={handleImageError}
			/>
		</div>

		<slot />
	</div>
</main>
