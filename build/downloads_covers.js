// Created by: Claude Cowork
// Date: 2026-11-18
// Purpose: Render 1200x750 covers for the /downloads cards in the blog cover style
//          (lavender grid, bold title with italic accent, yellow sticker) with a
//          3D mockup of the real PDF pages. Writes site/img/downloads/<file>-cover.jpg/.webp.
// Owner: Syed Hadi
// Usage: node build/downloads_covers.js   (needs pdftoppm; pages rendered to /tmp/dlcov)
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { execSync } = require('child_process');
const fs = require('fs'), path = require('path');

const SITE = path.join(__dirname, '..', 'site');
const TMP = '/tmp/dlcov';
const ITEMS = [
  { file: 'india-pmm-salary-guide-2026', title: 'India PMM pay,', accent: 'decoded', tag: '2026 guide, 8 pages', badge: 'Free with email', tint: '#5b3df5' },
  { file: 'ai-job-search-setup-guide', title: 'Set up your AI job', accent: 'agent', tag: 'Setup guide, 1 page', badge: 'Free PDF', tint: '#1040C5' },
  { file: 'interview-questions-and-answers', title: '30 questions', accent: 'answered', tag: 'PMM, partnerships, sales', badge: 'Free PDF', tint: '#7c3aed' },
  { file: 'interview-loop-and-offer-playbook', title: 'First call to', accent: 'signed offer', tag: 'Interview playbook, 3 pages', badge: 'Free PDF', tint: '#4c1d95' },
];

const HTML = (it, p1, p2) => `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:PJS;font-weight:800;src:url(file://${SITE}/assets/fonts/web/plus-jakarta-sans-latin-800-normal.woff2)}
@font-face{font-family:PJS;font-weight:700;src:url(file://${SITE}/assets/fonts/web/plus-jakarta-sans-latin-700-normal.woff2)}
@font-face{font-family:IS;font-style:italic;src:url(file://${SITE}/assets/fonts/web/instrument-serif-latin-400-italic.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
.cv{position:relative;width:1200px;height:750px;overflow:hidden;background:#ece7ff;
 background-image:linear-gradient(#ddd5ff 1.5px,transparent 1.5px),linear-gradient(90deg,#ddd5ff 1.5px,transparent 1.5px);background-size:60px 60px;background-position:-2px -2px}
.cv:before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 76% 46%,rgba(255,255,255,.9),rgba(255,255,255,0) 58%)}
.glow{position:absolute;right:40px;top:90px;width:560px;height:560px;border-radius:50%;background:radial-gradient(circle,${it.tint}33,transparent 65%);filter:blur(10px)}
.txt{position:absolute;left:80px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center}
.kick{align-self:flex-start;display:flex;align-items:center;gap:10px;font:700 22px PJS;color:#141228;background:#fff;border:3px solid #141228;border-radius:999px;padding:8px 18px 9px 12px;margin-bottom:30px;box-shadow:4px 4px 0 #141228}
.kick i{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:${it.tint};color:#fff;font-style:normal}
.kick svg{width:17px;height:17px}
h1{font-family:PJS;font-weight:800;color:#141228;letter-spacing:-.035em;line-height:1.02;font-size:90px}
h1 em{font-family:IS;font-style:italic;font-weight:400;font-size:1.14em;line-height:.9;letter-spacing:-.01em;padding:0 .06em 0 .02em;background:linear-gradient(90deg,#5b3df5,#b43ea0);-webkit-background-clip:text;background-clip:text;color:transparent}
.tag{align-self:flex-start;margin-top:34px;font:800 29px PJS;color:#141228;background:#ffd84d;padding:8px 20px 10px;border:4px solid #141228;border-radius:10px;transform:rotate(-2.5deg);box-shadow:6px 6px 0 #141228}
.stack{position:absolute;right:112px;top:92px;width:400px;height:566px;perspective:1600px}
.pg{position:absolute;inset:0;border-radius:10px;overflow:hidden;background:#fff;border:3px solid #141228}
.pg img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.b2{transform:translate(48px,26px) rotate(7deg);box-shadow:10px 14px 0 #141228;filter:saturate(.9) brightness(.97)}
.b1{transform:rotate(-4deg);box-shadow:12px 16px 0 #141228,0 30px 60px rgba(20,18,40,.25)}
.b1:after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.35) 0%,rgba(255,255,255,0) 32%)}
.dl{position:absolute;right:70px;bottom:52px;width:112px;height:112px;border-radius:50%;background:#ffd84d;border:4px solid #141228;display:grid;place-items:center;box-shadow:6px 6px 0 #141228;transform:rotate(-8deg)}
.dl svg{width:50px;height:50px}
.badge{position:absolute;right:300px;top:58px;font:800 21px PJS;color:#fff;background:${it.badge.includes('email') ? '#141228' : '#16a34a'};border:3px solid #141228;border-radius:999px;padding:7px 16px 8px;transform:rotate(-6deg);box-shadow:4px 4px 0 #141228;z-index:3}
.spark{position:absolute;width:44px;height:44px;color:#f97362}
.me{position:absolute;left:80px;bottom:34px;display:flex;align-items:center;gap:12px}
.me img{width:56px;height:56px;border-radius:50%;object-fit:cover;border:4px solid #fff;box-shadow:0 0 0 3px #141228}
.me b{font:700 20px PJS;color:#141228}
</style></head><body><div class="cv">
<div class="glow"></div>
<div class="stack">
 <div class="pg b2">${p2 ? `<img src="${p2}">` : '<div style="width:100%;height:100%;background:linear-gradient(160deg,#f6f3ff,#e4dcff)"></div>'}</div>
 <div class="pg b1"><img src="${p1}"></div>
</div>
<div class="badge">${it.badge}</div>
<svg class="spark" style="right:560px;top:128px" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1l2.6 7.4L22 11l-7.4 2.6L12 21l-2.6-7.4L2 11l7.4-2.6z"/></svg>
<svg class="spark" style="right:56px;top:300px;width:30px;height:30px;color:#5b3df5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1l2.6 7.4L22 11l-7.4 2.6L12 21l-2.6-7.4L2 11l7.4-2.6z"/></svg>
<div class="dl"><svg viewBox="0 0 24 24" fill="none" stroke="#141228" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11M7 10.5l5 5 5-5M5 20h14"/></svg></div>
<div class="txt">
 <span class="kick"><i><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/></svg></i>Free download</span>
 <h1 id="t">${it.title} <em>${it.accent}</em></h1>
 <span class="tag">${it.tag}</span>
</div>
<div class="me"><img src="file://${SITE}/img/syed-hadi-2026.jpg"><b>syedcreates.com</b></div>
</div>
<script>(async()=>{await document.fonts.ready;const t=document.getElementById('t');let s=90;while((t.scrollHeight>300||t.scrollWidth>560)&&s>46){s-=2;t.style.fontSize=s+'px'}document.body.dataset.ready=1})();</script>
</body></html>`;

(async () => {
  const b = await chromium.launch();
  for (const it of ITEMS) {
    const p1 = `file://${TMP}/${it.file}-p1.png`;
    const p2f = `${TMP}/${it.file}-p2.png`;
    const htmlPath = `${TMP}/${it.file}.html`;
    fs.writeFileSync(htmlPath, HTML(it, p1, fs.existsSync(p2f) ? `file://${p2f}` : null));
    const p = await b.newPage({ viewport: { width: 1200, height: 750 } });
    await p.goto(`file://${htmlPath}`);
    await p.waitForFunction(() => document.body.dataset.ready === '1');
    await p.waitForTimeout(150);
    const jpg = path.join(SITE, 'img', 'downloads', `${it.file}-cover.jpg`);
    await p.screenshot({ path: jpg, type: 'jpeg', quality: 90 });
    await p.close();
    execSync(`python3 -c "from PIL import Image;im=Image.open('${jpg}');im.save('${jpg.replace('.jpg', '.webp')}','WEBP',quality=82,method=6);im.resize((800,500),Image.LANCZOS).save('${jpg.replace('.jpg', '-800.webp')}','WEBP',quality=80,method=6)"`);
    console.log('cover', it.file);
  }
  await b.close();
})();
