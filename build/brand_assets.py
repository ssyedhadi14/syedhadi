#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-11-02
# Purpose: Generate the Syed Hadi brand logo files (mark, wordmark, lockups) as SVG with outlined type, plus PNG exports
# Owner: Syed Hadi
import os, subprocess, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FD = "/home/claude/fonts/ttf2"
OUT = "/home/claude/work/site/brand-assets"
os.makedirs(OUT, exist_ok=True)
ACC, ACC2, INK, WHITE = "#5b3df5", "#7c5cff", "#0d0b1a", "#ffffff"


def text_path(font_path, text, size, x=0, y=0, tracking=0):
    """Return (svg path d, advance width) for text rendered at baseline y, scaled to size px."""
    f = TTFont(font_path)
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    kern = {}
    s = size / upm
    pen = SVGPathPen(gs)
    adv = 0.0
    names = [cmap[ord(c)] for c in text]
    for i, n in enumerate(names):
        tp = TransformPen(pen, (s, 0, 0, -s, x + adv, y))
        gs[n].draw(tp)
        adv += gs[n].width * s + tracking
    return pen.getCommands(), adv - tracking


def mark(size=96, fill=None, grad=True, letter_fill=WHITE, idp="g"):
    r = size * 0.26
    d, w = text_path(f"{FD}/plus-jakarta-sans-latin-800-normal.ttf", "S", size * 0.62)
    # center the S
    f = TTFont(f"{FD}/plus-jakarta-sans-latin-800-normal.ttf"); upm = f["head"].unitsPerEm
    cap = f["OS/2"].sCapHeight * (size * 0.62 / upm)
    tx = (size - w) / 2 - size * 0.055; ty = (size + cap) / 2
    defs = f'<defs><linearGradient id="{idp}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC2}"/></linearGradient></defs>' if grad else ""
    bg = f"url(#{idp})" if grad else fill
    # growth tick: small ascending arrow in the corner
    tick = f'<path d="M{size*0.69:.1f} {size*0.80:.1f} l{size*0.10:.1f} -{size*0.10:.1f} m0 0 h-{size*0.055:.1f} m{size*0.055:.1f} 0 v{size*0.055:.1f}" fill="none" stroke="{letter_fill}" stroke-width="{size*0.045:.1f}" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
    return (f'{defs}<rect width="{size}" height="{size}" rx="{r:.1f}" fill="{bg}"/>'
            f'<path transform="translate({tx:.2f},{ty:.2f})" d="{d}" fill="{letter_fill}"/>{tick}')


def svg(w, h, body, bg=None):
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Syed Hadi">{bgr}{body}</svg>'


def lockup(ink=INK, mark_fill=None, grad=True, letter_fill=WHITE, sub=True, idp="g"):
    size = 96
    d, w = text_path(f"{FD}/plus-jakarta-sans-latin-800-normal.ttf", "Syed Hadi", 64, tracking=-1.6)
    body = f'<g>{mark(size, mark_fill, grad, letter_fill, idp)}</g>'
    body += f'<path transform="translate(124,72)" d="{d}" fill="{ink}"/>'
    width = 124 + w + 8
    if sub:
        d2, w2 = text_path(f"{FD}/instrument-serif-latin-400-italic.ttf", "growth, in public", 30)
        body += f'<path transform="translate(126,104)" d="{d2}" fill="{ink}" opacity=".62"/>'
        width = max(width, 126 + w2 + 8)
    return svg(round(width), 120 if sub else 96, body)


def wordmark(ink=INK):
    d, w = text_path(f"{FD}/plus-jakarta-sans-latin-800-normal.ttf", "syedcreates", 64, tracking=-1.8)
    d2, w2 = text_path(f"{FD}/instrument-serif-latin-400-italic.ttf", ".com", 56)
    body = f'<path transform="translate(4,66)" d="{d}" fill="{ink}"/><path transform="translate({4+w+4:.1f},66)" d="{d2}" fill="{ACC}"/>'
    return svg(round(w + w2 + 16), 84, body)


files = {
    "syed-hadi-mark.svg": svg(96, 96, mark()),
    "syed-hadi-mark-mono-black.svg": svg(96, 96, mark(fill=INK, grad=False)),
    "syed-hadi-mark-mono-white.svg": svg(96, 96, mark(fill=WHITE, grad=False, letter_fill=INK)),
    "syed-hadi-logo.svg": lockup(),
    "syed-hadi-logo-white.svg": lockup(ink=WHITE),
    "syed-hadi-logo-black.svg": lockup(ink=INK, mark_fill=INK, grad=False),
    "syed-hadi-logo-compact.svg": lockup(sub=False),
    "syedcreates-wordmark.svg": wordmark(),
    "syedcreates-wordmark-white.svg": wordmark(ink=WHITE),
}
for n, s in files.items():
    open(os.path.join(OUT, n), "w").write(s)

# PNG exports via Playwright (2x)
spec = {n: (2, "#ffffff" if "white" not in n else "#0d0b1a") for n in files}
json.dump(spec, open("/tmp/brand_png.json", "w"))
js = r'''
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const spec=JSON.parse(fs.readFileSync('/tmp/brand_png.json'));const OUT=process.argv[2];
for(const [n,[scale,bg]] of Object.entries(spec)){const s=fs.readFileSync(OUT+'/'+n,'utf8');const m=s.match(/width="(\d+)" height="(\d+)"/);const w=+m[1],h=+m[2];
await p.setViewportSize({width:w+48,height:h+48});await p.setContent(`<body style="margin:0;background:${bg};display:grid;place-items:center;width:${w+48}px;height:${h+48}px">${s}</body>`);
await p.screenshot({path:OUT+'/'+n.replace('.svg','.png'),scale:'css',clip:{x:0,y:0,width:w+48,height:h+48},omitBackground:false});}
// large mark for avatars
const s=fs.readFileSync(OUT+'/syed-hadi-mark.svg','utf8');await p.setViewportSize({width:1024,height:1024});await p.setContent(`<body style="margin:0;background:transparent">${s.replace('width="96" height="96"','width="1024" height="1024"')}</body>`);await p.screenshot({path:OUT+'/syed-hadi-mark-1024.png',omitBackground:true});
await b.close();})();'''
open("/tmp/brand_png.js", "w").write(js)
subprocess.run(["node", "/tmp/brand_png.js", OUT], check=True, cwd="/home/claude")
print(sorted(os.listdir(OUT)))
