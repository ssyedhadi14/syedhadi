// Created by: Claude
// Date: 2026-11-03
// Purpose: Cloudflare Pages Function for /api/company-research. Cache and quotas in the CR_KV namespace.
// Owner: Syed Hadi
import { handle } from '../../lib/company-core.mjs';
import { loadEnv, clientIp, kvStore } from '../../lib/platform.js';

export async function onRequest(context) {
  loadEnv(context.env);
  return handle(context.request, { ip: clientIp(context.request) }, kvStore(context.env.CR_KV, 8));
}
