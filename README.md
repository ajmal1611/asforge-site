# AS Forge website

Plain static site: HTML + CSS + one small JS file. No build step, no database, nothing to hack on the server.

## Structure
```
index.html        Home
fetchly.html      AS Fetchly product + download + plans + install guide
projects.html     The Lab (projects + roadmap)
about.html        About us
faq.html          FAQ (also feeds Google rich results)
contact.html      WhatsApp + email
privacy.html  terms.html  404.html
css/site.css      all styling and animations
js/site.js        SETTINGS: download link, version, WhatsApp, email   <-- edit here
assets/           favicon.svg, og.png (social share image)
_headers          security headers for Cloudflare Pages
robots.txt  sitemap.xml
tools/            optional generator (build.py) + design source
```

## The 4 things to edit first
1. `js/site.js`: set `downloadUrl` (your GitHub Releases link), `version`, `email`.
2. Search all .html files for `YOUR-GITHUB-USER` (fallback link) and replace.
3. Replace `hello@asforge.app` once you set up email (Cloudflare Email Routing is free).
4. Update the Projects texts and progress bars when things change (`projects.html`, `index.html`).

## Put the installer on GitHub, not on the site
Cloudflare Pages allows files up to 25 MB. Your Setup.exe is bigger.
Create a GitHub repo (e.g. `as-fetchly-releases`) > Releases > "Draft a new release" > upload `AS-Fetchly-Setup-0.8.0.exe`.
Use `https://github.com/USER/as-fetchly-releases/releases/latest` as `downloadUrl`.

## Deploy (free)
1. Create a GitHub repo `asforge-site` and upload this folder.
2. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git > choose the repo.
3. Build command: (empty). Output directory: `/`. Deploy.
4. Pages > Custom domains > add `asforge.app` (buy it at Namecheap first, then point nameservers to Cloudflare).
5. Turn on: SSL "Full (strict)", Always Use HTTPS, 2-step verification on GitHub, Namecheap and Cloudflare.
6. Submit `https://asforge.app/sitemap.xml` in Google Search Console.

## Test locally
`python -m http.server 8000` in this folder, then open http://localhost:8000 (links like /fetchly need Cloudflare or a server that maps /fetchly to fetchly.html; open fetchly.html directly otherwise).

## Optional: regenerate pages
`python tools/build.py` rebuilds all pages from the shared header/footer. Editing the .html files directly also works.

## Add a news post
Easy way (no Python): copy `news/welcome-to-as-forge.html` to `news/my-new-post.html`, change the title, date, text and the two "canonical/og:url" lines, then copy one card in `news.html` and edit it. Add the new URL to `sitemap.xml`.
Generator way: add an entry to `tools/posts.json`, run `python tools/build.py`. News page, post page and sitemap update by themselves.
