<script lang="ts">
  import { onMount } from 'svelte';

  let showMessage = false;

  // Mostra a mensagem após 2 segundos, se a página ainda não tiver carregado.
  // Você pode ajustar esse tempo.
  const timeoutId = setTimeout(() => {
    showMessage = true;
  }, 2000);

  // Quando a nova página é carregada, limpa o temporizador.
  // O componente é automaticamente destruído ao navegar para outra página.
  onMount(() => {
    return () => {
      clearTimeout(timeoutId);
    };
  });
</script>

{#if showMessage}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-75 text-white p-4">
    <div class="text-center">
      <div class="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-12 w-12 mb-4"></div>
      <p class="text-xl sm:text-2xl font-semibold">Redirecionando para a página...</p>
      <p class="text-sm mt-2">Por favor, aguarde um momento.</p>
    </div>
  </div>
{/if}

<style>
  .loader {
    border-top-color: #3498db;
    animation: spin 1s linear infinite;
    margin: auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>