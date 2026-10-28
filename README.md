# syedcreates.com

Personal site of Syed Hadi, Product Marketing and Partnerships Lead at AccuKnox. Live at https://syedcreates.com, hosted on Netlify.

## Layout

```
site/     The published website. Netlify serves this folder as is.
build/    Python scripts that generate the subpages and the tools page.
netlify.toml   Tells Netlify to publish site/ with no build step.
```

## Edit and publish

1. Edit content in `build/` (page copy in `build.py`, tools in `tools.py`, nav in `nav_mega.py`, SEO in `seo.py`). The home page is `site/index.html`, edited directly.
2. Regenerate pages:
   ```bash
   cd build
   python3 build.py
   python3 tools.py
   ```
3. Commit and push. Netlify deploys automatically once the repo is linked.

## Short links

`/book` opens Calendly, `/resume` opens the resume PDF, `/deck` opens the workproof deck, `/tools` opens the tool directory. They live in `site/_redirects`.
