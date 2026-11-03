// Created by: Claude
// Date: 2026-11-03
// Purpose: Netlify wrapper for the company research core (lib/company-core.mjs), cache in Netlify Blobs
// Owner: Syed Hadi
import { getStore } from '@netlify/blobs';
import { handle } from '../../lib/company-core.mjs';

function blobs() {
  try {
    const s = getStore({ name: 'company-research', consistency: 'strong' });
    return { getJSON: (k) => s.get(k, { type: 'json' }), setJSON: (k, v) => s.setJSON(k, v) };
  } catch (e) { return null; }
}

export default async (req, context) => handle(req, context, blobs());
