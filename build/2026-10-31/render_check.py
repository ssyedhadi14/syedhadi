#!/usr/bin/env python3
# Created by: Claude
# Date: 2026-10-31
# Purpose: Render key pages of the fixed site with Playwright, capture console errors, overflow and screenshots
# Owner: Syed Hadi
import asyncio
import json
import os
import subprocess
import sys
import time

from playwright.async_api import async_playwright

ROOT = "/home/claude/work/site"
OUT = "/home/claude/shots"
os.makedirs(OUT, exist_ok=True)
PORT = 8123
PAGES = ["index.html", "tools.html", "case-studies.html", "salary-calculator.html", "seo-aeo-score.html", "fire-calculator.html",
         "about.html", "posts.html", "gtm-health-check.html", "skill-pack.html", "404.html", "one-pager-sent.html?for=gtmbox", "audit-requested.html"]
IGNORE = ("images.unsplash.com", "fonts.g", "calendly", "cdnjs", "googletagmanager", "youtube", "s2/favicons", "net::ERR_", "Failed to load resource")


async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    report = {}
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            for vp in [(1366, 900), (390, 844)]:
                ctx = await b.new_context(viewport={"width": vp[0], "height": vp[1]}, device_scale_factor=1)
                for pg in PAGES:
                    page = await ctx.new_page()
                    errs = []
                    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                    page.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
                    await page.route("**/*", lambda r: r.abort() if any(h in r.request.url for h in ("unsplash", "googleapis", "gstatic", "calendly", "cdnjs", "youtube")) else r.continue_())
                    try:
                        await page.goto(f"http://127.0.0.1:{PORT}/{pg}", wait_until="load", timeout=30000)
                    except Exception as e:
                        errs.append("NAV " + str(e))
                    await page.wait_for_timeout(600)
                    overflow = await page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    h1 = await page.evaluate("document.querySelectorAll('h1').length")
                    main = await page.evaluate("!!document.getElementById('main')")
                    extra = {}
                    if pg.startswith("salary-calculator"):
                        extra = await page.evaluate("({corp: document.getElementById('corpN').textContent, kpis: document.getElementById('miles').children.length, chart: document.getElementById('chart').children.length, verdict: document.getElementById('vd').textContent.slice(0,120)})")
                        await page.click("#tblBtn"); await page.wait_for_timeout(200)
                        extra["tableRows"] = await page.evaluate("document.querySelectorAll('#tbl tbody tr').length")
                        await page.click(".sc-tabs button[data-ch=flow]"); await page.wait_for_timeout(200)
                        extra["flowChart"] = await page.evaluate("document.getElementById('chart').children.length")
                    if pg == "index.html" and vp[0] > 1000:
                        await page.click('.dd-btn[data-group="calc"]'); await page.wait_for_timeout(400)
                        extra["calcMenuVisible"] = await page.evaluate("getComputedStyle(document.querySelector('.mm-calc')).display !== 'none' && document.querySelector('.mm-calc').getBoundingClientRect().height > 100")
                        await page.screenshot(path=f"{OUT}/nav-calc.png", clip={"x": 0, "y": 0, "width": 1366, "height": 520})
                        await page.keyboard.press("Escape")
                        extra["medium"] = await page.evaluate("!!document.querySelector('[data-medium-latest]')")
                        extra["featuredAfterHero"] = await page.evaluate("(function(){var h=document.querySelector('header.hero');var n=h.nextElementSibling;return n && n.classList.contains('feat-sec')})()")
                        extra["winsBeforeProof"] = await page.evaluate("(function(){var w=document.getElementById('wins');var n=w&&(w.nextElementSibling||w.parentElement.nextElementSibling);return !!(n&&n.classList.contains('proof-strip'))})()")
                        extra["has35B"] = await page.evaluate("document.body.innerText.includes('$35B')")
                        extra["internalLinks"] = await page.evaluate("document.querySelectorAll('main a[href^=\"/\"]').length")
                    errs = [e for e in errs if not any(i in e for i in IGNORE)]
                    report[f"{pg}@{vp[0]}"] = {"errors": errs, "overflow": overflow, "h1": h1, "main": main, **extra}
                    await page.screenshot(path=f"{OUT}/{pg.split('?')[0].replace('.html','')}-{vp[0]}.png", full_page=(vp[0] < 1000 and pg in ('index.html',)) or pg in ("tools.html", "case-studies.html", "salary-calculator.html", "seo-aeo-score.html", "index.html"))
                    await page.close()
                await ctx.close()
            await b.close()
    finally:
        srv.terminate()
    print(json.dumps(report, indent=1))


asyncio.run(main())
