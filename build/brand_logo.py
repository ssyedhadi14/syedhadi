# Created by: Claude Cowork
# Date: 2026-11-17
# Purpose: Replace the avatar in the nav brand with the Syed Hadi logo mark
#          ("sh" monogram with a lilac dot, on a violet gradient), and rebuild the
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
        '<path d="M17.38 32.78Q15.31 32.78 13.78 31.8Q12.25 30.82 11.7 29.16L14.22 27.97Q14.71 28.98 15.54 29.56Q16.36 30.13 17.38 30.13Q18.11 30.13 18.5 29.83Q18.89 29.53 18.89 29Q18.89 28.73 18.76 28.53Q18.62 28.34 18.34 28.18Q18.07 28.02 17.65 27.9L15.51 27.3Q13.97 26.87 13.14 25.89Q12.32 24.91 12.32 23.58Q12.32 22.4 12.91 21.53Q13.51 20.66 14.59 20.16Q15.67 19.67 17.08 19.67Q18.92 19.67 20.31 20.53Q21.7 21.39 22.27 22.95L19.72 24.15Q19.45 23.37 18.72 22.9Q18 22.43 17.08 22.43Q16.41 22.43 16.03 22.7Q15.65 22.98 15.65 23.46Q15.65 23.71 15.79 23.92Q15.93 24.13 16.24 24.29Q16.55 24.45 17.01 24.59L19.01 25.19Q20.57 25.65 21.4 26.58Q22.23 27.51 22.23 28.87Q22.23 30.04 21.62 30.91Q21.01 31.79 19.93 32.28Q18.85 32.78 17.38 32.78ZM23.3 32.5V15.09H26.75V22.43L26.34 21.87Q26.77 20.75 27.75 20.21Q28.73 19.67 30.04 19.67Q31.46 19.67 32.53 20.26Q33.6 20.86 34.2 21.93Q34.8 23 34.8 24.43V32.5H31.35V25.16Q31.35 24.43 31.06 23.9Q30.77 23.37 30.26 23.07Q29.74 22.77 29.05 22.77Q28.38 22.77 27.85 23.07Q27.32 23.37 27.04 23.9Q26.75 24.43 26.75 25.16V32.5Z" fill="#fff"/>'
        '<circle cx="37.2" cy="31" r="2.6" fill="#c4b5fd"/></svg>')

OLD = re.compile(r'(class="brand">)(?:<img src="/img/avatar\.(?:webp|jpg)" alt="Syed Hadi" width="40" height="40">|<svg class="brand-mark".*?</svg>)', re.S)

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
