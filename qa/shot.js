const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const ROOT='/home/claude/work/site';
const ct=f=>({'.css':'text/css','.js':'application/javascript','.woff2':'font/woff2','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg'}[path.extname(f)]||'text/html');
(async()=>{const [slug,out,w,dark,fill]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w||1366,height:900}});
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='local')return r.fulfill({status:204,body:''});let f=path.join(ROOT,u.pathname==='/'?'index.html':u.pathname);if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f+='.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({body:fs.readFileSync(f),contentType:ct(f)})});
await p.goto('http://local'+slug);await p.waitForTimeout(600);
if(fill){for(const [k,v] of Object.entries(JSON.parse(fill)))await p.fill('#'+k,v);}
if(dark==='1')await p.evaluate(()=>document.documentElement.setAttribute('data-theme','dark'));
await p.addStyleTag({content:'.reveal{opacity:1!important;transform:none!important} nav{position:static!important} img[src^="https"]{background:#c9c4e8}'});
await p.waitForTimeout(400);await p.screenshot({path:out,fullPage:true});await b.close()})();
