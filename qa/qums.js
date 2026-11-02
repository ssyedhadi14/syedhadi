const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const ROOT='/home/claude/work/site';
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({acceptDownloads:true});
await ctx.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='local')return r.fulfill({status:204,body:''});let f=path.join(ROOT,u.pathname==='/'?'index.html':u.pathname);if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f+='.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({body:fs.readFileSync(f),contentType:f.endsWith('.js')?'application/javascript':f.endsWith('.css')?'text/css':f.endsWith('.ttf')?'font/ttf':'text/html'})});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});
await p.goto('http://local/qums');await p.waitForTimeout(800);
await p.fill('#kname','QA Test');await p.fill('#kdate','2026-11-02');await p.fill('#cash','200000');await p.fill('#bank','800000');await p.fill('#paid','300000');
await p.click('#goTotal');await p.waitForTimeout(500);console.log('modal',await p.textContent('#mdK'),await p.textContent('#mdI'),await p.textContent('#mdMeta'));
const [dl]=await Promise.all([p.waitForEvent('download',{timeout:30000}),p.click('#optPdf')]);await dl.saveAs('/home/claude/qa/pdfs/qums.pdf');console.log('pdf',dl.suggestedFilename(),fs.statSync('/home/claude/qa/pdfs/qums.pdf').size);
console.log('errs',errs);await b.close()})();
