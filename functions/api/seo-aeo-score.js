// Created by: Claude
// Date: 2026-11-03
// Purpose: Cloudflare Pages Function for /api/seo-aeo-score
// Owner: Syed Hadi
import mod from '../../netlify/functions/seo-aeo-score.js';
import { v1 } from '../../lib/platform.js';

export const onRequest = v1(mod.handler);
