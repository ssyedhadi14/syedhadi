# Created by: Claude Cowork
# Date: 2026-11-17
# Purpose: Replace the avatar in the nav brand with the Syed Hadi logo mark
#          (an S that turns into a growth arrow, with a spark), and rebuild the
#          favicons from the same mark. Idempotent, rerun after builder scripts.
# Owner: Syed Hadi
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

MARK = ('<svg class="brand-mark" viewBox="0 0 48 48" width="40" height="40" aria-hidden="true" focusable="false">'
        '<defs><linearGradient id="shLogoG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c5cff"/>'
        '<stop offset="1" stop-color="#4527e0"/></linearGradient></defs>'
        '<rect width="48" height="48" rx="14" fill="url(#shLogoG)"/>'
        '<path d="M14 34h12.5a5.5 5.5 0 0 0 0-11h-5a5.5 5.5 0 0 1 0-11H31" fill="none" stroke="#fff" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M28.5 7.5L33.5 12l-5 4.5" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M37 30.5l1.1 2.9 2.9 1.1-2.9 1.1-1.1 2.9-1.1-2.9-2.9-1.1 2.9-1.1z" fill="#d8ccff"/></svg>')

OLD = re.compile(r'(class="brand">)<img src="/img/avatar\.(?:webp|jpg)" alt="Syed Hadi" width="40" height="40">')

CSS = """
/* brand logo 2026-11-17 */
.brand .brand-mark{width:38px;height:38px;flex:none;display:block;filter:drop-shadow(0 4px 10px rgba(91,61,245,.28));transition:transform .3s var(--ease)}
.brand:hover .brand-mark{transform:rotate(-6deg) scale(1.06)}
.brand .brand-t{letter-spacing:0}
"""

def pages():
    n = 0
    for f in SITE.rglob("*.html"):
        if "/x-" in str(f):
            continue
        h = f.read_text(encoding="utf-8")
        nh = OLD.sub(lambda m: m.group(1) + MARK, h)
        if nh != h:
            f.write_text(nh, encoding="utf-8"); n += 1
    for b in [ROOT / "build" / "nav_mega.py"]:
        t = b.read_text(encoding="utf-8")
        nt = OLD.sub(lambda m: m.group(1) + MARK, t)
        if nt != t:
            b.write_text(nt, encoding="utf-8")
    print("nav logo on", n, "pages")

def css():
    p = SITE / "assets" / "site.css"
    s = p.read_text(encoding="utf-8")
    if "brand logo 2026-11-17" not in s:
        p.write_text(s.rstrip("\n") + "\n" + CSS.lstrip("\n"), encoding="utf-8")

def favicons():
    svg = MARK.replace('class="brand-mark" ', '').replace(' aria-hidden="true" focusable="false"', '').replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ')
    (SITE / "img" / "logo-mark.svg").write_text(svg, encoding="utf-8")
    js = """const {chromium}=require('/opt/npm-tools/node_modules/playwright');(async()=>{const b=await chromium.launch();
for(const s of [32,192,512]){const p=await b.newPage({viewport:{width:s,height:s}});
await p.setContent(`<style>html,body{margin:0;background:transparent}svg{width:${s}px;height:${s}px;display:block}</style>`+require('fs').readFileSync('%s','utf8'));
await p.screenshot({path:'%s/img/favicon-'+s+'.png',omitBackground:true});await p.close()}await b.close()})()""" % (SITE / "img" / "logo-mark.svg", SITE)
    subprocess.run(["node", "-e", js], check=True)
    from PIL import Image
    Image.open(SITE / "img" / "favicon-192.png").save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicons rebuilt")

if __name__ == "__main__":
    pages(); css(); favicons()
