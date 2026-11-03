const {chromium}=require('playwright');const fs=require('fs'),path=require('path');const ROOT='/home/claude/work/site';
const ct=f=>({'.css':'text/css','.js':'application/javascript','.woff2':'font/woff2','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp'}[path.extname(f)]||'text/html');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:1000}});
await p.route('**/*',r=>{const u=new URL(r.request().url());if(u.host!=='local')return r.fulfill({status:204,body:''});let f=path.join(ROOT,decodeURIComponent(u.pathname==='/'?'index.html':u.pathname));if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f+='.html';if(!fs.existsSync(f))return r.fulfill({status:404,body:''});r.fulfill({body:fs.readFileSync(f),contentType:ct(f)})});
await p.goto('http://local/');await p.waitForTimeout(800);
const groups=await p.$$eval('.nav-links .dd-btn',bs=>bs.map(b=>b.dataset.group));console.log(groups);
for(const g of groups){await p.click(`.nav-links .dd-btn[data-group="${g}"]`);await p.waitForTimeout(500);
 const items=await p.$$(`.dd[data-group="${g}"] .mw-item`);
 if(items.length){for(let i=0;i<items.length;i++){await items[i].hover();await p.waitForTimeout(350);await p.screenshot({path:`/home/claude/qa/m-${g}-${i}.png`,clip:{x:0,y:60,width:1600,height:800}});}}
 else await p.screenshot({path:`/home/claude/qa/m-${g}.png`,clip:{x:0,y:60,width:1600,height:800}});
 await p.keyboard.press('Escape');await p.mouse.move(5,900);await p.waitForTimeout(300);}
await b.close()})();
