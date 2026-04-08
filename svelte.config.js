import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'; // CORREÇÃO: Puxa o preprocessador do plugin correto
import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: vitePreprocess(), 

    kit: {
        adapter: adapter() 
    },

};

export default config;
