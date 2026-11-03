const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const ROOT='/home/claude/work/site';
const ct=f=>({'.css':'text/css','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml'}[path.extname(f)]||'text/html');
(async()=>{const b=await chromium.launch();
for(const slug of ['/','/about']){const p=await b.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce',deviceScaleFactor:1.5});
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='local')return r.fulfill({status:204,body:''});let f=path.join(ROOT,u.pathname==='/'?'index.html':u.pathname);if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f+='.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({body:fs.readFileSync(f),contentType:ct(f)})});
await p.goto('http://local'+slug);await p.waitForTimeout(800);
const r=await p.evaluate(async()=>{const q=s=>document.querySelector(s);const vp=q('#featVP'),jr=q('.jr-track'),rc=q('#recTrack'),qb=q('.qb-q');
const a=[vp&&vp.scrollLeft,jr&&jr.scrollLeft,rc&&rc.scrollLeft,qb&&qb.textContent];
if(vp)vp.scrollIntoView({block:'center'});await new Promise(r=>setTimeout(r,2000));const f=vp&&vp.scrollLeft;
if(jr)jr.scrollIntoView({block:'center'});await new Promise(r=>setTimeout(r,5200));const j=jr&&jr.scrollLeft;
if(rc)rc.scrollIntoView({block:'center'});await new Promise(r=>setTimeout(r,6000));
return {start:a,feat:f,jr:j,rec:rc&&rc.scrollLeft,quote:qb&&qb.textContent}});
console.log(slug,JSON.stringify(r));await p.close();}
await b.close()})();
