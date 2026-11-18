# Created by: Claude Cowork
# Date: 2026-11-18
# Purpose: Add the "Import from LinkedIn" card, loader and script to the resume
#          builder on /interview-prep, in both build/interview_prep.py and the
#          built site/interview-prep.html. Idempotent.
# Owner: Syed Hadi
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "site" / "interview-prep.html", ROOT / "build" / "interview_prep.py"]
VER = "20261118a"

CARD = '''<div class="li-card reveal" id="liImport" data-k="li-import">
        <div class="li-copy"><span class="li-tag">New &middot; about 30 seconds</span>
          <h3>Start from your LinkedIn profile</h3>
          <p>Paste your profile URL, save it as a PDF from LinkedIn, drop it here, and the builder fills itself. Your PDF is read in this browser and never uploaded.</p></div>
        <div class="li-steps">
          <div class="li-s"><span class="li-n">1</span><div class="li-field"><label class="sr" for="liUrl">Your LinkedIn profile URL</label><input id="liUrl" type="url" inputmode="url" placeholder="linkedin.com/in/yourname" autocomplete="url"><button type="button" class="btn btn-primary" id="liOpen">Open my profile</button></div></div>
          <p class="li-hint">On your profile click <b>More</b> (or <b>Resources</b>), then <b>Save to PDF</b>.</p>
          <div class="li-s"><span class="li-n">2</span><label class="li-drop" id="liDrop" tabindex="0" role="button" aria-label="Upload your LinkedIn profile PDF"><input id="liFile" type="file" accept="application/pdf,.pdf" hidden>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M12 18v-6M9 15l3-3 3 3"/></svg>
            <span><b>Drop your LinkedIn PDF</b> or click to choose it</span></label></div>
          <p class="li-msg" id="liMsg" role="status" aria-live="polite"></p>
        </div>
      </div>
      <div class="li-loader" id="liLoader" hidden role="dialog" aria-modal="true" aria-label="Building your resume">
        <div class="li-box">
          <div class="li-orb" aria-hidden="true"><span></span><span></span><span></span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M8 13h8M8 17h5"/></svg></div>
          <h4>Building your resume</h4>
          <div class="li-prog"><i id="liBar"></i></div><div class="li-pct" id="liPct">0%</div>
          <ol class="li-list"><li class="li-step">Reading your PDF</li><li class="li-step">Finding your roles and dates</li><li class="li-step">Writing bullet points</li><li class="li-step">Building your resume</li></ol>
        </div>
      </div>
      '''

CSS = """
/* LinkedIn import 2026-11-18 */
.li-card{display:grid;grid-template-columns:1fr 1.15fr;gap:26px;align-items:center;margin:0 0 22px;padding:24px 26px;border-radius:22px;border:1px solid var(--line);background:radial-gradient(120% 140% at 0 0,rgba(10,102,194,.10),transparent 55%),linear-gradient(140deg,rgba(91,61,245,.07),rgba(139,92,246,.03));position:relative;overflow:hidden}
.li-tag{display:inline-block;font:700 11.5px Inter,sans-serif;letter-spacing:.02em;padding:5px 10px;border-radius:999px;background:#0a66c2;color:#fff}
.li-copy h3{font:800 22px/1.25 "Plus Jakarta Sans",sans-serif;margin:10px 0 6px;color:var(--ink)}
.li-copy p{color:var(--ink-2);font-size:14.5px;line-height:1.55}
.li-steps{display:grid;gap:10px}
.li-s{display:flex;gap:12px;align-items:center}
.li-n{flex:none;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font:700 13px Inter,sans-serif;background:var(--accent);color:#fff}
.li-field{flex:1;display:flex;gap:8px;min-width:0}
.li-field input{flex:1;min-width:0;font:inherit;font-size:14.5px;padding:11px 13px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
.li-field input:focus{outline:2px solid #0a66c2;outline-offset:1px}
.li-field .btn{white-space:nowrap}
.li-hint{margin:0 0 0 40px;font-size:13px;color:var(--ink-3)}
.li-drop{flex:1;display:flex;align-items:center;gap:12px;padding:16px 18px;border:1.5px dashed color-mix(in srgb,var(--accent) 55%,transparent);border-radius:14px;background:var(--bg);cursor:pointer;color:var(--ink-2);font-size:14px;transition:border-color .2s,background .2s,transform .2s}
.li-drop svg{width:30px;height:30px;color:var(--accent);flex:none}
.li-drop b{color:var(--ink)}
.li-drop:hover,.li-drop.over,.li-drop:focus-visible{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 7%,var(--bg));transform:translateY(-1px)}
.li-card.li-s2 .li-drop{border-style:solid;box-shadow:0 0 0 4px color-mix(in srgb,var(--accent) 14%,transparent)}
.li-msg{margin:2px 0 0 40px;font-size:13.5px;color:var(--ink-2);min-height:1em}
.li-loader{position:fixed;inset:0;z-index:200;display:grid;place-items:center;background:rgba(10,8,30,.55);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
.li-loader[hidden]{display:none}
.li-box{width:min(380px,90vw);padding:30px 28px 24px;border-radius:24px;background:var(--bg);border:1px solid var(--line);box-shadow:0 30px 80px rgba(20,16,41,.35);text-align:center}
.li-box h4{font:800 19px "Plus Jakarta Sans",sans-serif;margin:14px 0 14px;color:var(--ink)}
.li-orb{position:relative;width:86px;height:86px;margin:0 auto;display:grid;place-items:center}
.li-orb span{position:absolute;inset:0;border-radius:50%;border:2px solid transparent;border-top-color:#0a66c2;border-right-color:var(--accent);animation:liSpin 1.1s linear infinite}
.li-orb span:nth-child(2){inset:9px;border-top-color:#c084fc;border-right-color:transparent;animation-duration:1.6s;animation-direction:reverse}
.li-orb span:nth-child(3){inset:18px;border-top-color:#ffd43b;animation-duration:2.2s}
.li-orb svg{width:28px;height:28px;color:var(--accent);animation:liPulse 1.4s ease-in-out infinite}
.li-prog{height:8px;border-radius:99px;background:var(--bg-soft);overflow:hidden}
.li-prog i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,#0a66c2,#5b3df5,#c084fc);background-size:200% 100%;animation:liShine 1.4s linear infinite;transition:width .45s ease}
.li-pct{margin-top:6px;font:600 12.5px "JetBrains Mono",monospace;color:var(--ink-3)}
.li-list{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:9px;text-align:left}
.li-step{position:relative;padding-left:28px;font-size:14px;color:var(--ink-3);transition:color .3s}
.li-step::before{content:"";position:absolute;left:0;top:1px;width:18px;height:18px;border-radius:50%;border:2px solid var(--line);box-sizing:border-box}
.li-step.run{color:var(--ink);font-weight:600}
.li-step.run::before{border-color:var(--accent);border-top-color:transparent;animation:liSpin .8s linear infinite}
.li-step.ok{color:var(--ink-2)}
.li-step.ok::before{border-color:#16a34a;background:#16a34a url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23fff' stroke-width='3.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12l5 5 9-10'/%3E%3C/svg%3E") center/11px no-repeat}
body.li-busy{overflow:hidden}
@keyframes liSpin{to{transform:rotate(360deg)}}
@keyframes liPulse{50%{transform:scale(.86);opacity:.7}}
@keyframes liShine{to{background-position:-200% 0}}
@media (prefers-reduced-motion:reduce){.li-orb span,.li-orb svg,.li-prog i,.li-step.run::before{animation:none}}
@media(max-width:860px){.li-card{grid-template-columns:1fr;padding:20px}.li-field{flex-wrap:wrap}.li-field .btn{width:100%;justify-content:center}.li-hint,.li-msg{margin-left:0}}
"""


def patch(text):
    if 'data-k="li-import"' not in text:
        anchor = '<div class="rs-wrap">'
        i = text.find('<div role="tabpanel" id="tabResume"')
        j = text.find(anchor, i)
        if i < 0 or j < 0:
            raise SystemExit("anchor not found")
        text = text[:j] + CARD + text[j:]
    tag = f'<script src="/assets/linkedin-import.js?v={VER}" defer></script>'
    if "linkedin-import.js" not in text:
        k = text.find('<script src="/assets/interview-prep.js')
        if k >= 0:
            e = text.find("</script>", k) + len("</script>")
            text = text[:e] + tag + text[e:]
    return text


if __name__ == "__main__":
    for t in TARGETS:
        s = t.read_text(encoding="utf-8")
        n = patch(s)
        if n != s:
            t.write_text(n, encoding="utf-8")
            print("patched", t.name)
    css = ROOT / "site" / "assets" / "site.css"
    c = css.read_text(encoding="utf-8")
    if "LinkedIn import 2026-11-18" not in c:
        css.write_text(c.rstrip("\n") + "\n" + CSS.lstrip("\n"), encoding="utf-8")
        print("css added")
