# syedcreates.com

Personal site of Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox. Live at https://syedcreates.com on Netlify.

## Layout

```
site/                 The published website. Netlify serves this folder as is.
netlify/functions/    Two serverless functions: salary-report (emails the PDF via Brevo) and seo-aeo-score (scores a URL, DR from OpenSEO).
netlify.toml          Publishes site/, points Netlify at the functions folder.
_backups/             Dated copies of earlier versions. Never deploy from here.
```

## Publish

Option A, drag and drop (pages only, functions stay offline):
1. Zip the contents of `site/` (not the folder itself).
2. Drop it on the Deploys page of the syedhadi project in Netlify.

Option B, full deploy with the two tools working (recommended):
```bash
npm i -g netlify-cli
cd ~/syedhadi
netlify login
netlify link            # pick the existing "syedhadi" project
netlify deploy --prod   # uploads site/ and the functions
```

## Environment variables (Netlify > Project configuration > Environment variables)

| Variable | Used by | Notes |
|---|---|---|
| BREVO_API_KEY | salary-report | Brevo v3 key. Required for "Email me the PDF report". |
| REPORT_SENDER_EMAIL | salary-report | A sender verified in Brevo. Default ssyedhadi14@gmail.com. |
| REPORT_BCC | salary-report | Optional. Comma separated addresses that get a copy (lead capture). |
| OPENSEO_API_KEY | seo-aeo-score | Key from app.openseo.so > Settings > API keys. Without it the tool still scores, the DR card says not connected. |
| OPENSEO_PROJECT_ID | seo-aeo-score | Optional. Otherwise the first project is used. Each DR lookup costs about 50 OpenSEO credits, cached 12 hours per host. |

Both tools degrade gracefully: without the functions the salary page downloads the PDF instead of emailing it, and the score page shows a clear error.

## URLs

Clean URLs are canonical (`/about`, not `/about.html`). `site/_redirects` sends every `.html` URL to its clean version with a 301 and holds the short links (`/book`, `/resume`, `/deck`, `/linkedin`, `/medium`, `/substack`, `/whatsapp`, `/fire`, `/mf`, `/salary`, `/skills`, `/cases`).

## Short history

- 2026-10-28: v2 site launched.
- 2026-10-31: QA pass (SEO, AEO, UX), Calculator menu, salary growth calculator, SEO and AEO score tool, homepage changes.
