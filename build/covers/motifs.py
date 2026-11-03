# Created by: Claude
# Date: 2026-11-03
# Purpose: Hand drawn style SVG illustrations for syedcreates.com covers (viewBox 0 0 400 400)
# Owner: Syed Hadi

K = "#141228"   # ink outline
V = "#7c5cff"   # violet
VL = "#c9bdff"  # light violet
Y = "#ffd84d"   # highlighter yellow
C = "#ff8a65"   # coral
W = "#ffffff"

S = f'stroke="{K}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"'

def _wrap(inner):
    return f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'

def sparkle(x, y, r, fill=Y):
    return (f'<path d="M{x} {y-r} Q{x+r*.18} {y-r*.18} {x+r} {y} Q{x+r*.18} {y+r*.18} {x} {y+r} '
            f'Q{x-r*.18} {y+r*.18} {x-r} {y} Q{x-r*.18} {y-r*.18} {x} {y-r}Z" fill="{fill}" {S}/>')

M = {}

M["shield"] = _wrap(
    f'<path d="M200 50 L320 95 Q322 250 200 345 Q78 250 80 95Z" fill="{V}" {S}/>'
    f'<path d="M200 82 L292 116 Q292 236 200 312Z" fill="{VL}" stroke="none"/>'
    f'<path d="M150 200 L188 238 L258 160" fill="none" {S} stroke-width="14"/>'
    + sparkle(330, 60, 26) + sparkle(70, 300, 18, C))

M["cloud"] = _wrap(
    f'<path d="M110 270 Q50 270 55 215 Q60 165 115 168 Q120 95 195 92 Q265 92 280 155 Q345 150 348 212 Q350 270 290 270Z" fill="{VL}" {S}/>'
    f'<rect x="160" y="200" width="84" height="74" rx="12" fill="{Y}" {S}/>'
    f'<path d="M176 200 V178 Q176 152 202 152 Q228 152 228 178 V200" fill="none" {S}/>'
    f'<circle cx="202" cy="232" r="9" fill="{K}"/><path d="M202 238 V254" {S}/>'
    + sparkle(330, 100, 22, C))

M["code"] = _wrap(
    f'<rect x="60" y="80" width="280" height="210" rx="22" fill="{W}" {S}/>'
    f'<path d="M60 128 H340" {S}/><circle cx="92" cy="104" r="7" fill="{C}"/><circle cx="116" cy="104" r="7" fill="{Y}"/>'
    f'<path d="M135 170 L105 200 L135 230 M200 170 L230 200 L200 230" fill="none" {S}/>'
    f'<circle cx="275" cy="270" r="48" fill="{VL}" {S}/><path d="M309 304 L350 345" {S} stroke-width="14"/>'
    f'<path d="M258 270 L272 284 L296 256" fill="none" {S}/>')

M["clipboard"] = _wrap(
    f'<rect x="95" y="70" width="210" height="280" rx="20" fill="{W}" {S}/>'
    f'<rect x="150" y="50" width="100" height="44" rx="12" fill="{V}" {S}/>'
    + "".join(f'<rect x="125" y="{y}" width="34" height="34" rx="8" fill="{Y if i<2 else W}" {S}/>'
              f'<path d="M180 {y+17} H275" {S}/>' for i, y in enumerate((130, 195, 260)))
    + f'<path d="M132 147 L140 156 L154 138 M132 212 L140 221 L154 203" fill="none" {S} stroke-width="6"/>'
    + sparkle(330, 300, 22, C))

M["funnel"] = _wrap(
    f'<path d="M60 80 H340 L235 210 V320 L165 350 V210Z" fill="{V}" {S}/>'
    f'<path d="M60 80 H340 L300 130 H100Z" fill="{VL}" {S}/>'
    f'<circle cx="150" cy="50" r="16" fill="{Y}" {S}/><circle cx="210" cy="40" r="16" fill="{C}" {S}/><circle cx="265" cy="55" r="16" fill="{Y}" {S}/>'
    f'<path d="M290 330 Q330 300 345 250" fill="none" {S}/><path d="M325 250 L347 245 L352 268" fill="none" {S}/>')

M["puzzle"] = _wrap(
    f'<path d="M60 120 H140 Q130 80 165 80 Q200 80 190 120 H250 V180 Q290 170 290 205 Q290 240 250 230 V300 H60Z" fill="{V}" {S}/>'
    f'<path d="M250 180 Q290 170 290 205 Q290 240 250 230 V180 M270 130 H350 V310 H270 V260 Q300 270 300 235 Q300 200 270 210Z" fill="{Y}" {S}/>'
    + sparkle(345, 70, 24, C) + sparkle(70, 330, 16, VL))

M["megaphone"] = _wrap(
    f'<path d="M80 170 L250 90 V310 L80 230Z" fill="{V}" {S}/>'
    f'<rect x="50" y="165" width="46" height="70" rx="12" fill="{Y}" {S}/>'
    f'<path d="M115 238 L135 320 H175 L160 252" fill="{VL}" {S}/>'
    f'<ellipse cx="252" cy="200" rx="26" ry="110" fill="{W}" {S}/>'
    f'<path d="M300 150 Q330 140 345 115 M310 200 H355 M300 250 Q330 260 345 285" fill="none" {S}/>')

M["search"] = _wrap(
    f'<circle cx="175" cy="170" r="110" fill="{W}" {S}/>'
    f'<rect x="115" y="185" width="30" height="55" rx="6" fill="{VL}" {S}/><rect x="160" y="150" width="30" height="90" rx="6" fill="{V}" {S}/><rect x="205" y="115" width="30" height="125" rx="6" fill="{Y}" {S}/>'
    f'<path d="M255 255 L340 340" {S} stroke-width="22"/>' + sparkle(320, 70, 28, C))

M["calculator"] = _wrap(
    f'<rect x="95" y="50" width="210" height="300" rx="28" fill="{V}" {S}/>'
    f'<rect x="125" y="80" width="150" height="62" rx="12" fill="{W}" {S}/><path d="M200 111 H255" {S}/>'
    + "".join(f'<rect x="{x}" y="{y}" width="40" height="40" rx="10" fill="{Y if (x, y) == (235, 290) else W}" {S}/>'
              for y in (170, 230, 290) for x in (125, 180, 235))
    + sparkle(340, 330, 20, C))

M["pin"] = _wrap(
    f'<path d="M40 330 H360" {S}/>'
    f'<path d="M70 330 V250 H110 V330 M290 330 V220 H335 V330 M120 330 V280 H150 V330" fill="{VL}" {S}/>'
    f'<path d="M200 315 Q120 215 120 155 Q120 75 200 75 Q280 75 280 155 Q280 215 200 315Z" fill="{V}" {S}/>'
    f'<circle cx="200" cy="155" r="36" fill="{Y}" {S}/>' + sparkle(330, 80, 22, C))

M["scales"] = _wrap(
    f'<path d="M200 70 V320 M140 330 H260 M90 110 H310" fill="none" {S}/>'
    f'<circle cx="200" cy="70" r="14" fill="{Y}" {S}/>'
    f'<path d="M90 110 L50 220 H130Z M310 110 L270 200 H350Z" fill="none" {S} stroke-width="5"/>'
    f'<path d="M45 220 Q90 270 135 220Z" fill="{V}" {S}/><path d="M265 200 Q310 250 355 200Z" fill="{VL}" {S}/>')

M["sparkles"] = _wrap(
    sparkle(180, 180, 120, V) + sparkle(310, 90, 46, Y) + sparkle(300, 300, 34, C) + sparkle(80, 330, 24, VL)
    + f'<path d="M180 120 Q186 174 240 180 Q186 186 180 240 Q174 186 120 180 Q174 174 180 120Z" fill="{W}" stroke="none"/>')

M["calendar"] = _wrap(
    f'<rect x="70" y="90" width="260" height="240" rx="24" fill="{W}" {S}/>'
    f'<path d="M70 150 H330" {S}/><path d="M70 114 Q70 90 94 90 H306 Q330 90 330 114 V150 H70Z" fill="{V}" {S}/>'
    f'<path d="M130 60 V115 M270 60 V115" {S} stroke-width="12"/>'
    + "".join(f'<rect x="{x}" y="{y}" width="40" height="36" rx="8" fill="{Y if (x, y) == (180, 230) else VL}" {S} stroke-width="5"/>'
              for y in (180, 230, 280) for x in (110, 180, 250) if not (y == 280 and x == 250))
    + f'<path d="M188 248 L198 258 L214 240" fill="none" {S} stroke-width="5"/>')

M["trophy"] = _wrap(
    f'<path d="M130 70 H270 V160 Q270 240 200 240 Q130 240 130 160Z" fill="{Y}" {S}/>'
    f'<path d="M130 100 H80 Q75 175 140 190 M270 100 H320 Q325 175 260 190" fill="none" {S}/>'
    f'<path d="M200 240 V290 M140 335 H260 L245 290 H155Z" fill="{V}" {S}/>'
    f'<path d="M200 115 L210 140 L236 142 L216 158 L223 184 L200 170 L177 184 L184 158 L164 142 L190 140Z" fill="{W}" {S} stroke-width="5"/>'
    + sparkle(340, 70, 22, C) + sparkle(60, 300, 18, VL))

M["camera"] = _wrap(
    f'<rect x="55" y="120" width="290" height="200" rx="26" fill="{V}" {S}/>'
    f'<path d="M140 120 L160 80 H240 L260 120" fill="{VL}" {S}/>'
    f'<circle cx="200" cy="220" r="66" fill="{W}" {S}/><circle cx="200" cy="220" r="34" fill="{Y}" {S}/>'
    f'<rect x="285" y="145" width="34" height="20" rx="6" fill="{Y}" {S} stroke-width="5"/>' + sparkle(340, 70, 22, C))

M["gears"] = _wrap(
    "".join(
        f'<g transform="translate({cx} {cy})"><path d="' +
        " ".join(f'M{-11*s} {-r-18*s} H{11*s} V{-r+4} H{-11*s}Z' for _ in [0]) + '" fill="none"/></g>'
        for cx, cy, r, s in [])
    + f'<circle cx="160" cy="170" r="90" fill="{V}" {S} stroke-dasharray="34 14" stroke-width="20"/>'
    f'<circle cx="160" cy="170" r="72" fill="{V}" {S}/><circle cx="160" cy="170" r="28" fill="{W}" {S}/>'
    f'<circle cx="285" cy="285" r="58" fill="{Y}" {S} stroke-dasharray="24 12" stroke-width="18"/>'
    f'<circle cx="285" cy="285" r="44" fill="{Y}" {S}/><circle cx="285" cy="285" r="16" fill="{W}" {S}/>'
    + sparkle(320, 80, 24, C))

M["mountain"] = _wrap(
    f'<circle cx="300" cy="100" r="40" fill="{Y}" {S}/>'
    f'<path d="M30 330 L150 130 L220 240 L265 180 L370 330Z" fill="{V}" {S}/>'
    f'<path d="M150 130 L120 180 L150 170 L175 190Z" fill="{W}" {S} stroke-width="5"/>'
    f'<path d="M110 360 Q200 300 300 360" fill="none" {S}/>')

M["rocket"] = _wrap(
    f'<path d="M200 40 Q290 110 270 250 H130 Q110 110 200 40Z" fill="{W}" {S}/>'
    f'<circle cx="200" cy="150" r="32" fill="{VL}" {S}/>'
    f'<path d="M130 210 L85 280 L135 270 M270 210 L315 280 L265 270" fill="{V}" {S}/>'
    f'<path d="M165 255 Q200 360 235 255Z" fill="{C}" {S}/><path d="M185 255 Q200 310 215 255Z" fill="{Y}" stroke="none"/>'
    + sparkle(80, 90, 22, Y) + sparkle(330, 120, 18, V))

M["doc"] = _wrap(
    f'<path d="M90 50 H250 L310 110 V350 H90Z" fill="{W}" {S}/><path d="M250 50 V110 H310" fill="{VL}" {S}/>'
    f'<path d="M125 160 H275 M125 205 H275 M125 250 H220" {S}/>'
    f'<rect x="270" y="170" width="40" height="170" rx="8" transform="rotate(30 290 255)" fill="{Y}" {S}/>'
    f'<path d="M262 330 L250 368 L282 346" fill="{V}" {S} stroke-width="5"/>')

M["idcard"] = _wrap(
    f'<rect x="55" y="95" width="290" height="210" rx="24" fill="{W}" {S}/>'
    f'<rect x="85" y="130" width="100" height="120" rx="16" fill="{VL}" {S}/>'
    f'<circle cx="135" cy="175" r="24" fill="{V}" {S}/><path d="M100 245 Q135 200 170 245" fill="{V}" {S}/>'
    f'<path d="M215 150 H310 M215 190 H290 M215 230 H265" {S}/>'
    f'<rect x="160" y="60" width="80" height="50" rx="12" fill="{Y}" {S}/>' + sparkle(340, 330, 22, C))

M["chart"] = _wrap(
    f'<path d="M60 60 V330 H350" fill="none" {S}/>'
    f'<path d="M80 290 L150 230 L205 255 L310 120" fill="none" {S} stroke="{V}" stroke-width="16"/>'
    f'<path d="M80 290 L150 230 L205 255 L310 120" fill="none" {S} stroke-width="4"/>'
    f'<path d="M280 112 L318 110 L316 148" fill="none" {S}/>'
    f'<ellipse cx="270" cy="300" rx="48" ry="16" fill="{Y}" {S}/><path d="M222 280 V300 M318 280 V300" {S}/>'
    f'<ellipse cx="270" cy="280" rx="48" ry="16" fill="{Y}" {S}/>' + sparkle(120, 110, 20, C))

M["heart"] = _wrap(
    f'<path d="M200 330 Q60 240 60 150 Q60 80 130 80 Q180 80 200 130 Q220 80 270 80 Q340 80 340 150 Q340 240 200 330Z" fill="{C}" {S}/>'
    f'<path d="M90 190 H150 L170 150 L200 230 L225 175 L240 190 H310" fill="none" {S} stroke="{W}" stroke-width="12"/>'
    f'<path d="M90 190 H150 L170 150 L200 230 L225 175 L240 190 H310" fill="none" {S} stroke-width="4"/>'
    + sparkle(340, 60, 22, Y))

M["car"] = _wrap(
    f'<path d="M50 260 V215 Q50 195 75 190 L120 125 Q130 112 150 112 H255 Q275 112 288 128 L330 190 Q355 196 355 220 V260Z" fill="{V}" {S}/>'
    f'<path d="M140 135 H195 V188 H105Z M215 135 H260 L298 188 H215Z" fill="{W}" {S} stroke-width="5"/>'
    f'<circle cx="120" cy="265" r="34" fill="{W}" {S}/><circle cx="285" cy="265" r="34" fill="{W}" {S}/>'
    f'<circle cx="120" cy="265" r="11" fill="{K}"/><circle cx="285" cy="265" r="11" fill="{K}"/>'
    f'<rect x="300" y="60" width="44" height="60" rx="8" fill="{Y}" {S}/><path d="M344 80 Q365 85 360 110" fill="none" {S}/>')

M["coins"] = _wrap(
    "".join(f'<ellipse cx="160" cy="{y}" rx="80" ry="24" fill="{Y}" {S}/>' for y in (300, 268, 236, 204))
    + f'<path d="M80 204 V300 M240 204 V300" {S}/>'
    f'<circle cx="275" cy="150" r="70" fill="{V}" {S}/><text x="275" y="176" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="78" fill="{W}">&#8377;</text>'
    + sparkle(80, 90, 22, C))

M["briefcase"] = _wrap(
    f'<rect x="55" y="120" width="290" height="200" rx="24" fill="{V}" {S}/>'
    f'<path d="M150 120 V92 Q150 75 167 75 H233 Q250 75 250 92 V120" fill="none" {S}/>'
    f'<path d="M55 195 H345" {S}/><rect x="180" y="180" width="40" height="34" rx="8" fill="{Y}" {S}/>'
    + sparkle(345, 70, 22, C) + sparkle(60, 330, 16, Y))

M["handshake"] = M["puzzle"]
