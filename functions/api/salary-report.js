// Created by: Claude
// Date: 2026-11-03
// Purpose: Cloudflare Pages Function for /api/salary-report (Brevo email of the salary PDF)
// Owner: Syed Hadi
import mod from '../../netlify/functions/salary-report.js';
import { v1 } from '../../lib/platform.js';

export const onRequest = v1(mod.handler);
