const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const ROOT='/home/claude/work/site';
const ct=f=>({'.css':'text/css','.js':'application/javascript'}[path.extname(f)]||'text/html');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:1000}});
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='local')return r.fulfill({status:204,body:''});let f=path.join(ROOT,u.pathname==='/'?'index.html':u.pathname);if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f+='.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({body:fs.readFileSync(f),contentType:ct(f)})});
await p.goto('http://local/');await p.click('.nav-links .dd-btn[data-group="calc"]');await p.waitForTimeout(500);
console.log(await p.evaluate(()=>{const els=document.elementsFromPoint(282,84);return els.slice(0,5).map(e=>e.tagName+'.'+e.className+' '+(e.textContent||'').slice(0,20))}));
console.log(await p.evaluate(()=>getComputedStyle(document.querySelector('.gb-feature'),'::before').content+' | '+getComputedStyle(document.querySelector('.gb-feature .gb-img'),'::before').content+' | '+getComputedStyle(document.querySelector('.gb-feature .gb-img'),'::after').content));
await b.close()})();
