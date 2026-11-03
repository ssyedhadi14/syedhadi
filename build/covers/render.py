#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-03
# Purpose: Render branded covers for every page of syedcreates.com in the site fonts.
#          Writes site/img/covers/<slug>.jpg (1200x750, cards and article headers) and
#          site/img/covers/og/<slug>.jpg (1200x630, Open Graph and X).
# Owner: Syed Hadi
# Usage: python3 build/covers/render.py [slug ...]
import json
import os
import subprocess
import sys
import tempfile
import threading
import http.server
import functools

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "..", "site"))
sys.path.insert(0, HERE)
from config import COVERS  # noqa: E402
from motifs import M  # noqa: E402

TEMPLATE = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"PJS";font-weight:800;src:url(/assets/fonts/web/plus-jakarta-sans-latin-800-normal.woff2)}
@font-face{font-family:"PJS";font-weight:700;src:url(/assets/fonts/web/plus-jakarta-sans-latin-700-normal.woff2)}
@font-face{font-family:"IS";font-style:italic;src:url(/assets/fonts/web/instrument-serif-latin-400-italic.woff2)}
@font-face{font-family:"Plus Jakarta Sans";font-weight:800;src:url(/assets/fonts/web/plus-jakarta-sans-latin-800-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff}
.cv{position:relative;width:1200px;overflow:hidden;background:#ece7ff;
 background-image:linear-gradient(#ddd5ff 1.5px,transparent 1.5px),linear-gradient(90deg,#ddd5ff 1.5px,transparent 1.5px);
 background-size:60px 60px;background-position:-2px -2px}
.cv:before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 78% 40%,rgba(255,255,255,.85),rgba(255,255,255,0) 55%)}
.txt{position:absolute;left:84px;top:0;bottom:0;width:610px;display:flex;flex-direction:column;justify-content:center}
h1{font-family:"PJS";font-weight:800;color:#141228;letter-spacing:-.035em;line-height:1.02}
h1 em{font-family:"IS";font-style:italic;font-weight:400;font-size:1.12em;line-height:.9;letter-spacing:-.01em;padding:0 .06em 0 .02em;
 background:linear-gradient(90deg,#5b3df5,#b43ea0);-webkit-background-clip:text;background-clip:text;color:transparent}
.tag{align-self:flex-start;margin-top:34px;font-family:"PJS";font-weight:800;font-size:30px;color:#141228;
 background:#ffd84d;padding:8px 20px 10px;border:4px solid #141228;border-radius:10px;transform:rotate(-2.5deg);box-shadow:6px 6px 0 #141228}
.art{position:absolute;width:390px;height:390px;right:72px;transform:rotate(4deg)}
.art svg{width:100%;height:100%}
.me{position:absolute;right:44px;bottom:30px;display:flex;flex-direction:column;align-items:center;gap:8px}
.me img{width:96px;height:96px;border-radius:50%;object-fit:cover;border:5px solid #fff;box-shadow:0 0 0 4px #141228}
.me b{font-family:"PJS";font-weight:700;font-size:19px;color:#141228;letter-spacing:-.01em}
</style></head><body>
<div class="cv" id="cv" style="height:__H__px">
 <div class="art" style="top:__ARTTOP__px">__ART__</div>
 <div class="txt"><h1 id="t">__TITLE__ <em>__ACCENT__</em></h1><span class="tag">__TAG__</span></div>
 <div class="me"><img src="/img/syed-hadi-2026.jpg" alt=""><b>syedcreates.com</b></div>
</div>
<script>
(async()=>{await document.fonts.ready;const t=document.getElementById('t');const H=__H__;let s=96;
 const max=H-(H>700?300:250);t.style.fontSize=s+'px';
 while((t.scrollHeight>max||t.scrollWidth>610)&&s>40){s-=2;t.style.fontSize=s+'px'}
 document.body.dataset.ready=1})();
</script></body></html>"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def page(slug, h):
    title, accent, tag, motif = COVERS[slug]
    art_top = 70 if h > 700 else 40
    return (TEMPLATE.replace("__H__", str(h)).replace("__ARTTOP__", str(art_top))
            .replace("__ART__", M[motif]).replace("__TITLE__", esc(title))
            .replace("__ACCENT__", esc(accent)).replace("__TAG__", esc(tag)))


def main(slugs):
    tmp = os.path.join(SITE, "_cover_tmp")
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(os.path.join(SITE, "img", "covers", "og"), exist_ok=True)
    jobs = []
    for slug in slugs:
        for h, out in ((750, f"img/covers/{slug}.jpg"), (630, f"img/covers/og/{slug}.jpg")):
            name = f"{slug}-{h}.html"
            open(os.path.join(tmp, name), "w", encoding="utf-8").write(page(slug, h))
            jobs.append({"url": f"/_cover_tmp/{name}", "out": os.path.join(SITE, out), "h": h})
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
    handler.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    js = r"""
const {chromium}=require('playwright');const jobs=JSON.parse(process.argv[2]);const port=process.argv[3];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:750}});
for(const j of jobs){await p.setViewportSize({width:1200,height:j.h});
 await p.goto('http://127.0.0.1:'+port+j.url);await p.waitForSelector('body[data-ready]');
 await p.screenshot({path:j.out,type:'jpeg',quality:86,clip:{x:0,y:0,width:1200,height:j.h}});}
await b.close();})().catch(e=>{console.error(e);process.exit(1)});"""
    jf = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, dir="/tmp")
    jf.write(js)
    jf.close()
    try:
        subprocess.run(["node", jf.name, json.dumps(jobs), str(port)], check=True, cwd="/tmp")
    finally:
        srv.shutdown()
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp, f))
        os.rmdir(tmp)
        os.remove(jf.name)
    print(f"rendered {len(jobs)} covers")


if __name__ == "__main__":
    main(sys.argv[1:] or list(COVERS))
