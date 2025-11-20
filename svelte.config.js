import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'; // CORREÇÃO: Puxa o preprocessador do plugin correto
import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // 1. O pré-processamento agora usa o método correto (via plugin)
    preprocess: vitePreprocess(), 

    kit: {
        // Deixamos o adapter aqui, mesmo que não vá ser usado no modo dev.
        adapter: adapter() 
    },
    
    // (Omitindo o onwarn para manter o código limpo)
};

export default config;