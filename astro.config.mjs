import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
export const SITE_URL = process.env.SITE_URL || 'https://creatordeals.pages.dev';
export default defineConfig({site:SITE_URL, integrations:[sitemap()]});
