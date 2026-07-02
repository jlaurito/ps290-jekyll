# ps290.org — Jekyll mirror

A static Jekyll copy of [ps290.org](https://www.ps290.org/) (PS 290 Manhattan New School), built to match the current Edlio-hosted site's content and look.

## What's included

- All content from the site's four main nav sections: **About PS 290**, **Curriculum**, **Families**, **PTA** (external items still point to mnspta.org), plus **Staff** and the homepage.
- A static snapshot of **News & Announcements**.
- Design matched to the live site's own colors (crimson `#ce0037` / cream `#edddd4`, confirmed from the site's CSS custom properties) rather than guessed.

## What's excluded (per request)

- Site search, language switcher (Google Translate widget)
- `/apps/events/` and the homepage events carousel — no calendar/date logic is reproduced
- All "Edlio Login" / "Powered by Edlio" references

## Verification status

Every page in this repo was built from **real page source** (view-source / saved HTML) pasted in during this project, not guessed — including the full staff directory with verified `@schools.nyc.gov` emails. A few things are worth knowing before you publish:

- **`families/required-documents.md`**: the sidebar nav on the real site also lists an internal **"Sign Up for Emails and Alerts"** page and a **"Parent Handbook"** page (different from the external mnspta.org link used elsewhere in the main nav). Neither's content was captured — `nav.yml` currently points "Sign Up for Emails and Alerts" at the external mnspta.org link as a stand-in. Send the real source for these two if you want them included properly.
- **`news/rooftop-playground.md`** and **`news/welcome-to-our-new-website.md`**: only the homepage teaser text was available for these (the article bodies are JS-rendered and weren't captured); the rooftop one links out to the original for the full story.
- The **PTA** section's sidebar sub-nav will show a slightly redundant single-item list on `pta/meeting-dates.md` (since every other PTA nav item is an external mnspta.org link) — cosmetic only, matches the real site's data structure.

## Before you deploy

1. **Download the real assets.** All images/PDFs currently point to their original `files.edl.io` / `ps290.org` URLs won't be self-hosted until you run:
   ```
   pip3 install requests --break-system-packages
   python3 scripts/download_assets.py
   ```
   This downloads everything listed in `scripts/asset-manifest.tsv` into the matching `assets/` paths already referenced by the content files — no further edits needed afterward.

2. **Local build/test** (this was not build-tested in the sandbox — no network access to rubygems.org — so please verify locally before pushing):
   ```
   bundle install
   bundle exec jekyll serve
   ```

3. **Deploy**: push to `main` and the included GitHub Actions workflow (`.github/workflows/jekyll.yml`, Ruby 3.3 pinned, same pattern as mnspta.org) will build and publish to GitHub Pages automatically.

## Structure

```
_config.yml          Site config
_data/nav.yml         Main navigation (mirrors the live site's nav exactly)
_data/footer_links.yml Footer "Useful Links"
_layouts/             default.html (site chrome), page.html (breadcrumb + content + section sub-nav)
_includes/            header.html, footer.html
assets/css/style.css  All site styling
about/ curriculum/ families/ pta/ staff/ news/   Content pages
scripts/download_assets.py   One-time asset migration script
scripts/asset-manifest.tsv   local_path <TAB> source_url mapping (40 assets)
```
