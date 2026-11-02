const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const ROOT='/home/claude/work/site';
const ct=f=>({'.css':'text/css','.js':'application/javascript','.woff2':'font/woff2','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg'}[path.extname(f)]||'text/html');
(async()=>{const jobs=JSON.parse(process.argv[2]);const b=await chromium.launch();
for(const [slug,sel,out,dark] of jobs){const p=await b.newPage({viewport:{width:1366,height:900}});
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='local')return r.fulfill({status:204,body:''});let f=path.join(ROOT,u.pathname==='/'?'index.html':u.pathname);if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f+='.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({body:fs.readFileSync(f),contentType:ct(f)})});
await p.goto('http://local'+slug);if(dark)await p.evaluate(()=>document.documentElement.setAttribute('data-theme','dark'));
await p.addStyleTag({content:'.reveal{opacity:1!important;transform:none!important}*{animation:none!important;transition:none!important}'});await p.waitForTimeout(500);
const el=await p.$(sel);if(el){await el.scrollIntoViewIfNeeded();await el.screenshot({path:out});}else console.log('missing',slug,sel);await p.close();}
await b.close()})();
