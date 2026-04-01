// @ts-check
import { defineConfig } from 'astro/config';
import { fileURLToPath } from 'node:url';

import mdx from '@astrojs/mdx';

import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  server: { host: true },
  integrations: [mdx(), react()],
  vite: {
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  },
});