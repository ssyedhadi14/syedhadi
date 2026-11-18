// Created by: Claude Cowork | Date: 2026-11-18 | Purpose: render the AI Job Search one page setup guide | Owner: Syed Hadi
const {chromium}=require('/opt/npm-tools/node_modules/playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.join(__dirname,'ai_job_search_pdf.html'));await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:path.join(__dirname,'..','site','downloads','ai-job-search-setup-guide.pdf'),format:'A4',printBackground:true,pageRanges:'1'});
await b.close()})();
