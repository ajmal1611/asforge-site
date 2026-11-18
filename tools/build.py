#!/usr/bin/env python3
"""AS Forge site generator (optional). Rebuilds the HTML pages from shared pieces.
You can also edit the .html files directly; this script is only for convenience.
Run:  python tools/build.py   (from the site folder)
"""
import re, os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("NEXUS_SRC") or os.path.join(ROOT, "tools", "design-source.dc.html")
S = open(SRC, encoding="utf-8").read()
SITE = "https://asforge.app"

# ---------- pieces extracted from the approved design ----------
helm = re.search(r"<helmet>(.*?)</helmet>", S, re.S).group(1)
css = re.search(r"<style>(.*?)</style>", helm, re.S).group(1)
body = re.search(r"<x-dc>(.*?)</x-dc>", S, re.S).group(1).replace(re.search(r"<helmet>.*?</helmet>", S, re.S).group(0), "")

def sec(i):
    m = re.search(r'<section id="%s".*?</section>' % i, body, re.S)
    return m.group(0)

hero = re.search(r"</header>\s*(<section.*?)(?=<section id=\"download\")", body, re.S).group(1)
cta = re.search(r'<section style="position:relative;z-index:2;padding:110px.*?</section>', body, re.S).group(0)
layers = '<div class="top"></div>\n<div class="nebula"></div>\n<div class="hex" style="position:absolute;inset:0;pointer-events:none"></div>\n<div class="streak"></div>\n<div class="grain"></div>'

# ---------- fix up shared text ----------
def fix(h):
    h = h.replace("about 215 MB. ", "")
    h = h.replace("Version 0.8.0 · Windows 10 and 11 · ", 'Version <span data-ver>0.8.0</span> · Windows 10 and 11. ')
    h = h.replace('<a class="b3d" href="#download" style="background:linear-gradient(135deg,#FFC53D,#FF5A1F);--sh:#9a3a0a;color:#04120A;font-weight:700;font-size:18px;padding:18px 36px;border-radius:14px">Download for Windows</a>',
                  '<a class="b3d" data-dl href="https://drive.google.com/uc?export=download&id=1Zin_GlSMAL0MabE-aLyw9UVgbLyjiVEy" style="background:linear-gradient(135deg,#FFC53D,#FF5A1F);--sh:#9a3a0a;color:#04120A;font-weight:700;font-size:18px;padding:18px 36px;border-radius:14px">Download for Windows</a>')
    h = h.replace('href="https://wa.me/923211478590"', 'data-wa href="https://wa.me/923211478590"')
    h = h.replace('<a class="b3d" href="#download" style="background:linear-gradient(135deg,#FFC53D,#FF5A1F);--sh:#9a3a0a;color:#04120A;font-weight:700;font-size:18px;padding:18px 40px', '<a class="b3d" data-dl href="https://drive.google.com/uc?export=download&id=1Zin_GlSMAL0MabE-aLyw9UVgbLyjiVEy" style="background:linear-gradient(135deg,#FFC53D,#FF5A1F);--sh:#9a3a0a;color:#04120A;font-weight:700;font-size:18px;padding:18px 40px')
    return h

NAV = [("/fetchly", "AS Fetchly"), ("/projects", "Projects"), ("/news", "News"), ("/about", "About"), ("/faq", "FAQ"), ("/contact", "Contact")]

def header(cur):
    links = "".join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page" class="cur"' if u == cur else "", t) for u, t in NAV)
    return f'''<header style="position:relative;z-index:5;display:flex;justify-content:center;padding:22px clamp(16px,4vw,40px) 0">
<div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px 28px;width:100%;max-width:1180px;box-sizing:border-box;padding:10px 12px 10px 20px;border-radius:16px;background:rgba(8,14,32,.78);border:1px solid rgba(120,180,255,.22);backdrop-filter:blur(14px)">
<a href="/" class="hd" aria-label="AS Forge home" style="display:flex;align-items:center;gap:10px;font-weight:700;font-size:20px;letter-spacing:.02em"><svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2l12 7v14l-12 7L4 23V9z" fill="none" stroke="#19E8FF" stroke-width="2"/><path d="M16 9l6 3.5v7L16 23l-6-3.5v-7z" fill="#7B61FF"/></svg>AS Forge</a>
<nav class="nav" aria-label="Main" style="display:flex;flex-wrap:wrap;align-items:center;gap:8px 22px;font-size:14px;color:#A9BBDD">{links}
<a class="b3d" href="/fetchly#download" style="background:linear-gradient(135deg,#FFC53D,#FF5A1F);--sh:#9a3a0a;color:#04120A;font-weight:700;padding:10px 20px;border-radius:10px">Download</a></nav>
</div></header>'''

def footer():
    return '''<footer style="position:relative;z-index:2;border-top:1px solid rgba(120,180,255,.16);padding:56px clamp(20px,5vw,72px) 36px;box-sizing:border-box">
<div style="max-width:1180px;margin:0 auto;display:flex;flex-wrap:wrap;gap:40px 64px;justify-content:space-between">
<div style="flex:1 1 280px;min-width:0"><div class="hd" style="font-weight:700;font-size:22px;margin-bottom:10px">AS Forge</div><p style="margin:0;font-size:14.5px;line-height:1.7;color:#93A4C7;max-width:340px">A software company building fast, secure tools. First product: AS Fetchly.</p></div>
<nav class="fnav" aria-label="Footer" style="display:flex;flex-wrap:wrap;gap:36px 56px;font-size:14.5px">
<div style="display:flex;flex-direction:column;gap:10px"><b style="color:#E6F0FF">Company</b><a href="/about">About</a><a href="/projects">Projects</a><a href="/news">News</a><a href="/contact">Contact</a></div>
<div style="display:flex;flex-direction:column;gap:10px"><b style="color:#E6F0FF">AS Fetchly</b><a href="/fetchly">Overview</a><a href="/fetchly#download">Download</a><a href="/faq">FAQ</a></div>
<div style="display:flex;flex-direction:column;gap:10px"><b style="color:#E6F0FF">Legal</b><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div>
</nav></div>
<div style="max-width:1180px;margin:36px auto 0;padding-top:22px;border-top:1px solid rgba(120,180,255,.12);font-size:13px;line-height:1.7;color:#7F91B5">
<div>© <span data-year>2026</span> AS Forge. All rights reserved.</div>
<div>Download only content you own or have permission to save. AS Fetchly is not affiliated with YouTube or TikTok.</div></div>
</footer>'''

def pagehead(label, color, h1, p, extra=""):
    return f'''<section style="position:relative;z-index:2;padding:110px clamp(20px,5vw,72px) 40px;max-width:1280px;margin:0 auto;width:100%;box-sizing:border-box">
<div class="mono r1" style="font-size:13px;letter-spacing:.12em;color:{color};margin-bottom:18px">// {label}</div>
<h1 class="hd r2" style="margin:0 0 22px;font-weight:700;font-size:clamp(38px,5.6vw,76px);line-height:1.04;text-wrap:balance">{h1}</h1>
<p class="r3" style="margin:0 0 30px;max-width:680px;font-size:clamp(17px,1.8vw,20px);line-height:1.7;color:#C5D2EC">{p}</p>{extra}</section>'''

def block(inner, amb=""):
    a = f'<div class="amb" style="background:{amb}"></div>' if amb else ""
    return f'<section style="position:relative;z-index:2;padding:90px clamp(20px,5vw,72px);max-width:1280px;margin:0 auto;width:100%;box-sizing:border-box">{a}<div style="position:relative">{inner}</div></section>'

def prose(inner):
    return f'<section style="position:relative;z-index:2;padding:20px clamp(20px,5vw,72px) 110px;max-width:900px;margin:0 auto;width:100%;box-sizing:border-box"><div class="prose">{inner}</div></section>'

def page(path, title, desc, content, cur, ld=None, noindex=False):
    url = SITE + (path if path != "/" else "/")
    ldh = "".join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in (ld or []))
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{robots}
<meta name="theme-color" content="#02030A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AS Forge">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/css/site.css">
{ldh}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="site">
{layers}
{header(cur)}
<main id="main">
{content}
</main>
{footer()}
</div>
<script src="/js/site.js" defer></script>
</body>
</html>
'''

def w(path, html):
    fn = os.path.join(ROOT, path.lstrip("/") if path != "/" else "index.html")
    if not fn.endswith(".html"):
        fn += ".html"
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w", encoding="utf-8").write(html)

# ---------- structured data ----------
ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "AS Forge", "url": SITE, "logo": SITE + "/assets/favicon.svg",
       "description": "AS Forge is a software company building fast, secure desktop tools."}
APP = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "AS Fetchly", "operatingSystem": "Windows 10, Windows 11",
       "applicationCategory": "MultimediaApplication", "publisher": {"@type": "Organization", "name": "AS Forge"},
       "description": "Windows app to download YouTube and TikTok videos, playlists and profiles up to 4K, with auto-download and video cutting.",
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free plan available, Pro on request"}}

# ---------- cross-page CSS ----------
extra_css = open(os.path.join(ROOT, "tools", "extra.css"), encoding="utf-8").read()
open(os.path.join(ROOT, "css", "site.css"), "w", encoding="utf-8").write(css.strip() + "\n" + extra_css)

# ---------- HOME ----------
home = fix(hero + sec("download") + sec("about") + sec("lab") + sec("mech") + sec("specs") + sec("live") + sec("plans") + cta)
home = home.replace('href="#about">About AS Forge', 'href="/about">About AS Forge')
w("/", page("/", "AS Forge | Fast, secure software from the future", "AS Forge builds fast, secure desktop software. Our first product, AS Fetchly, downloads YouTube and TikTok videos, playlists and profiles up to 4K.", home, "/", [ORG, APP]))

# ---------- FETCHLY ----------
steps = [("Download the installer", "Use the Download button. It is one setup file."),
         ("Run it", "Double-click AS-Fetchly-Setup. It installs by itself in a few seconds and opens AS Fetchly. Any older version is replaced automatically."),
         ("If Windows shows “protected your PC”", "This appears for new publishers. Click <b>More info</b>, then <b>Run anyway</b>."),
         ("Paste a link", "Choose a video, playlist or profile, pick quality and format, then press Download."),
         ("Go Pro (optional)", "Send us a message, pay, and enter the licence key you receive in the app.")]
st = "".join(f'<li class="panel" style="display:flex;gap:18px;align-items:flex-start;padding:22px 24px;border-radius:16px;border:1px solid rgba(25,232,255,.3);background:rgba(7,14,30,.9)"><span class="mono" style="flex:none;width:38px;height:38px;border-radius:50%;border:2px solid #19E8FF;color:#7DEBFF;display:flex;align-items:center;justify-content:center">{i+1}</span><div><b style="font-size:18px">{a}</b><div style="margin-top:6px;color:#A9BBDD;line-height:1.65">{b}</div></div></li>' for i, (a, b) in enumerate(steps))
install = block(f'<div class="mono" style="font-size:13px;letter-spacing:.12em;color:#19E8FF;margin-bottom:16px">// INSTALL</div><h2 class="hd" style="margin:0 0 40px;font-weight:700;font-size:clamp(30px,4.4vw,52px);line-height:1.06">Installed in five steps.</h2><ol style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:16px;max-width:820px">{st}</ol><p style="margin:28px 0 0;color:#A9BBDD;line-height:1.7;max-width:820px"><b style="color:#E6F0FF">Requirements:</b> Windows 10 or 11 (64-bit) and an internet connection. <b style="color:#E6F0FF">Uninstall:</b> Windows Settings, Apps, AS Fetchly, or use the Uninstall button inside the app. Your settings stay in your user folder unless you delete them.</p>', "radial-gradient(800px 380px at 20% 40%,rgba(25,232,255,.16),transparent 70%)")
fh = pagehead("PRODUCT · DESKTOP APP", "#FFC53D", 'AS Fetchly: <span class="g" style="background-image:linear-gradient(90deg,#19E8FF,#7B61FF,#FF3DCB,#FF8A3D,#FFC53D,#19E8FF);-webkit-background-clip:text;background-clip:text;color:transparent">download anything you own.</span>',
              "Save YouTube and TikTok videos, playlists and whole profiles in 144p to 4K. Auto-download new videos daily, cut clips, and keep everything neatly named.",
              '<div style="display:flex;flex-wrap:wrap;gap:20px"><a class="b3d" data-dl href="https://drive.google.com/uc?export=download&id=1Zin_GlSMAL0MabE-aLyw9UVgbLyjiVEy" style="background:linear-gradient(135deg,#FFC53D,#FF5A1F);--sh:#9a3a0a;color:#04120A;font-weight:700;font-size:17px;padding:17px 32px;border-radius:14px">Download for Windows</a><a class="ghost" href="#plans" style="border:1.5px solid rgba(160,200,255,.5);color:#E6F0FF;font-weight:600;font-size:17px;padding:15.5px 30px;border-radius:14px">Free vs Pro</a></div>')
fetch = fix(fh + sec("download") + sec("specs") + sec("mech") + sec("live") + sec("plans") + install + cta)
fetch = fetch.replace('href="#download">Download free', 'href="#download">Download free')
w("/fetchly", page("/fetchly", "AS Fetchly | YouTube and TikTok downloader for Windows | AS Forge", "AS Fetchly downloads YouTube and TikTok videos, playlists and profiles in up to 4K. Auto-download, video cutting, English and Urdu. Free to start.", fetch, "/fetchly", [ORG, APP]))

# ---------- PROJECTS ----------
road = [("NOW", "#FFC53D", "AS Fetchly", "Live and improving. New versions replace the old one automatically."),
        ("NOW", "#19E8FF", "SentinelAI", "Research and build: adaptive red teaming and self-improving guardrails for an IT support assistant."),
        ("NEXT", "#FF3DCB", "Security Toolkit", "A practical cybersecurity tool. Name and details will be announced."),
        ("LATER", "#7B61FF", "More tools", "One careful product at a time, built on what we learn.")]
rd = "".join(f'<div class="panel" style="display:flex;gap:20px;align-items:flex-start;padding:24px 26px;border-radius:16px;border:1px solid {c}66;background:rgba(8,12,28,.9)"><span class="mono" style="flex:none;font-size:12px;letter-spacing:.1em;padding:6px 11px;border-radius:7px;border:1px solid {c};color:{c}">{n}</span><div><b style="font-size:19px">{t}</b><div style="margin-top:6px;color:#A9BBDD;line-height:1.65">{d}</div></div></div>' for n, c, t, d in road)
roadmap = block(f'<div class="mono" style="font-size:13px;letter-spacing:.12em;color:#7B61FF;margin-bottom:16px">// ROADMAP</div><h2 class="hd" style="margin:0 0 40px;font-weight:700;font-size:clamp(30px,4.4vw,52px);line-height:1.06">What we are building, in order.</h2><div style="display:flex;flex-direction:column;gap:16px;max-width:860px">{rd}</div>', "radial-gradient(800px 380px at 70% 40%,rgba(123,97,255,.22),transparent 70%)")
ph = pagehead("PROJECTS", "#19E8FF", "The Lab.", "Everything AS Forge is working on: live products, active research and what comes next. We update this page as projects move forward.")
w("/projects", page("/projects", "Projects | AS Forge", "Live products and active research at AS Forge: AS Fetchly, SentinelAI (AI security research) and upcoming cybersecurity tools.", ph + fix(sec("lab")) + roadmap + cta.replace("Ready to", "Want to follow").replace("fetch</span>?", "along</span>?"), "/projects", [ORG]))

# ---------- ABOUT ----------
vals = [("Fast", "#FFC53D", "Light apps and quick pages. Software should respect your time."),
        ("Secure", "#FF3DCB", "Signed licences, minimal data, and security built in from day one."),
        ("Honest", "#19E8FF", "Clear plans, clear prices and plain language. We say what our software does and does not do."),
        ("Personal", "#7B61FF", "Real support from the people who build it.")]
vc = "".join(f'<div class="panel fu1" style="min-width:0;border-radius:18px;border:1px solid {c}66;background:rgba(8,12,28,.9);padding:30px 28px;box-sizing:border-box"><div class="hd" style="font-weight:700;font-size:24px;color:{c};margin-bottom:10px">{t}</div><p style="margin:0;color:#A9BBDD;line-height:1.7">{d}</p></div>' for t, c, d in vals)
values = block(f'<div class="mono" style="font-size:13px;letter-spacing:.12em;color:#FFC53D;margin-bottom:16px">// HOW WE WORK</div><h2 class="hd" style="margin:0 0 40px;font-weight:700;font-size:clamp(30px,4.4vw,52px);line-height:1.06">Four principles.</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:26px">{vc}</div>')
resp = block('<div class="mono" style="font-size:13px;letter-spacing:.12em;color:#FF3DCB;margin-bottom:16px">// RESPONSIBLE USE</div><h2 class="hd" style="margin:0 0 18px;font-weight:700;font-size:clamp(28px,4vw,46px);line-height:1.08">Built for content you own.</h2><p style="margin:0 0 14px;max-width:760px;font-size:18px;line-height:1.75;color:#C5D2EC">Our downloader is meant for your own content and content you have permission to save. Please respect creators, copyright and each platform\'s terms. We test security tools only on systems we own or control.</p>', "radial-gradient(700px 360px at 20% 50%,rgba(255,61,203,.16),transparent 70%)")
w("/about", page("/about", "About AS Forge | Software company", "AS Forge is a software company building fast, secure tools. Learn who we are, what we build and how we work.", pagehead("ABOUT US", "#FF8A3D", "We forge tools people rely on.", "AS Forge is a software company. We take a real, everyday problem, build a fast and secure solution for it, and stand behind every customer personally.") + fix(sec("about")).replace('padding:150px', 'padding:60px') + values + resp + cta.replace("Ready to", "Try").replace("fetch</span>?", "AS Fetchly</span>"), "/about", [ORG]))

# ---------- FAQ ----------
faq = [
 ("What is AS Fetchly?", "A Windows app that downloads YouTube and TikTok videos, playlists and whole profiles in quality from 144p up to 4K, in MP4, MKV, WebM, MP3 or M4A."),
 ("Is it free?", "Yes, there is a free plan for single videos up to 720p. Pro unlocks playlists and profiles, saved accounts with daily auto-download, video cutting and quality up to 4K."),
 ("How do I get Pro?", "Message us on WhatsApp. After payment (JazzCash or Easypaisa) you receive a licence key to enter inside the app."),
 ("Windows says it protected my PC. Is the file safe?", "Windows shows this for new publishers that have not yet bought a code-signing certificate. Click More info, then Run anyway. Only download from this website or our official releases page."),
 ("How do I update or uninstall?", "Run the newer setup file and it replaces the old version automatically. To uninstall, use Windows Settings, Apps, or the Uninstall button in the app."),
 ("How many devices can one licence use?", "Each key allows a limited number of devices, set when you buy. If you change your computer, contact us and we will move it."),
 ("Does Pro need internet?", "The licence is checked online from time to time. If you are offline, it keeps working for up to 7 days."),
 ("Is it legal to use?", "Download only content you own or have permission to save, and follow each platform's terms. You are responsible for how you use the software."),
 ("Which systems and languages are supported?", "Windows 10 and 11 (64-bit). The app is available in English and Urdu."),
 ("What data do you collect?", "AS Fetchly runs on your computer. For Pro, we receive your licence key and a device ID to verify the licence. See the Privacy page for details."),
 ("Where is AS Forge from, and how do I reach you?", "See the Contact page for WhatsApp and email.")]
fl = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
w("/faq", page("/faq", "FAQ | AS Fetchly and AS Forge", "Answers about AS Fetchly: pricing, Pro licences, installation, Windows SmartScreen, updates, devices and privacy.", pagehead("FAQ", "#7B61FF", "Questions, answered.", "Can't find what you need? Message us and a real person will reply.") + f'<section style="position:relative;z-index:2;padding:10px clamp(20px,5vw,72px) 110px;max-width:900px;margin:0 auto;width:100%;box-sizing:border-box">{fl}</section>', "/faq", [ORG, faqld]))

# ---------- CONTACT ----------
cards = '''<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;max-width:900px">
<a class="panel" data-wa href="https://wa.me/923211478590" style="display:block;border-radius:20px;border:1px solid rgba(255,197,61,.55);background:rgba(34,20,8,.9);padding:34px 30px"><div class="mono" style="font-size:12px;color:#FFC53D;letter-spacing:.1em;margin-bottom:14px">WHATSAPP · FASTEST</div><div class="hd" style="font-weight:700;font-size:26px;margin-bottom:10px">+92 321 1478590</div><p style="margin:0;color:#C5D2EC;line-height:1.65">Support, Pro licences and payments. Tap to open a chat.</p></a>
<a class="panel" data-mail href="mailto:hello@asforge.app" style="display:block;border-radius:20px;border:1px solid rgba(25,232,255,.55);background:rgba(5,14,32,.92);padding:34px 30px"><div class="mono" style="font-size:12px;color:#19E8FF;letter-spacing:.1em;margin-bottom:14px">EMAIL</div><div class="hd" style="font-weight:700;font-size:26px;margin-bottom:10px">hello@asforge.app</div><p style="margin:0;color:#C5D2EC;line-height:1.65">Business, partnerships and anything that needs more detail.</p></a></div>
<p style="margin:30px 0 0;max-width:760px;color:#A9BBDD;line-height:1.7">When you write about a licence, include your licence key and the name you used when buying. Never send us passwords or payment card details.</p>'''
w("/contact", page("/contact", "Contact | AS Forge", "Contact AS Forge for AS Fetchly support, Pro licences and business enquiries via WhatsApp or email.", pagehead("CONTACT", "#FFC53D", "Talk to us.", "Questions, support, Pro licences or ideas. We read every message.") + block(cards), "/contact", [ORG]))

# ---------- PRIVACY / TERMS ----------
priv = '''<h2>Summary</h2><p>AS Forge keeps data collection to a minimum. This website has no accounts, no advertising and no tracking cookies. AS Fetchly runs on your own computer.</p>
<h2>This website</h2><p>Our hosting provider (Cloudflare) may process technical data such as IP address and browser type to deliver the site and protect it from attacks. We do not use this data for advertising. If you open our WhatsApp or email links, that service handles your message under its own policy.</p>
<h2>AS Fetchly</h2><ul><li>Downloads, links and settings stay on your computer.</li><li>For Pro licences we process your licence key, a device identifier and a computer name so that we can check the licence and the device limit.</li><li>We do not sell personal data.</li></ul>
<h2>Fonts</h2><p>This site loads fonts from Google Fonts, which may receive your IP address when fonts are requested.</p>
<h2>Your choices</h2><p>Contact us to ask what we hold about you or to have a licence record removed. Contact details are on the <a href="/contact">Contact page</a>.</p>
<h2>Changes</h2><p>We will update this page if our practices change. Last updated: 17 November 2026.</p>'''
terms = '''<h2>Using AS Fetchly</h2><p>By installing or using AS Fetchly you agree to these terms. If you do not agree, please do not use the software.</p>
<h2>Lawful use</h2><p>Use AS Fetchly only for content you own or have permission to save, and follow the terms of the platform the content comes from. You are responsible for how you use the software. AS Forge does not encourage copyright infringement.</p>
<h2>Licences</h2><ul><li>The free plan may be used without a key within its limits.</li><li>A Pro licence is personal, limited to the number of devices stated when you buy, and must not be shared or resold.</li><li>We may revoke a licence that is shared, resold or obtained by fraud.</li></ul>
<h2>Payments and refunds</h2><p>Payments are made directly to AS Forge through the methods we list. Refund requests are considered case by case if the software does not work as described and we cannot fix the problem.</p>
<h2>No affiliation</h2><p>AS Fetchly is an independent product. It is not affiliated with, endorsed by or sponsored by YouTube, Google or TikTok. Names belong to their owners.</p>
<h2>Warranty and liability</h2><p>The software is provided “as is”. To the extent allowed by law, AS Forge is not liable for indirect or consequential loss arising from its use.</p>
<h2>Changes</h2><p>We may update these terms. Continued use means you accept the updated terms. Last updated: 17 November 2026.</p>'''
w("/privacy", page("/privacy", "Privacy Policy | AS Forge", "How AS Forge and AS Fetchly handle data. Minimal collection, no tracking cookies, no data sales.", pagehead("LEGAL", "#19E8FF", "Privacy Policy", "") + prose(priv), "/privacy", [ORG]))
w("/terms", page("/terms", "Terms of Use | AS Forge", "Terms for using the AS Forge website and AS Fetchly software.", pagehead("LEGAL", "#19E8FF", "Terms of Use", "") + prose(terms), "/terms", [ORG]))

# ---------- 404 ----------
w("/404", page("/404", "Page not found | AS Forge", "This page could not be found.", pagehead("404", "#FF3DCB", "Lost in space.", "That page does not exist. Let's get you back.", '<a class="b3d" href="/" style="background:linear-gradient(135deg,#FFC53D,#FF5A1F);--sh:#9a3a0a;color:#04120A;font-weight:700;padding:16px 30px;border-radius:14px">Back to home</a>'), "", [], noindex=True))


# ---------- NEWS (reads tools/posts.json) ----------
import datetime
posts = sorted(json.load(open(os.path.join(ROOT, "tools", "posts.json"), encoding="utf-8")), key=lambda x: x["date"], reverse=True)
def nice(d):
    return datetime.date.fromisoformat(d).strftime("%d %B %Y")
cards = "".join(f'<a class="panel" href="/news/{x["slug"]}" style="display:block;border-radius:20px;border:1px solid rgba(25,232,255,.4);background:rgba(7,14,30,.9);padding:30px 28px;color:inherit"><div class="mono" style="font-size:12px;letter-spacing:.1em;color:#19E8FF;margin-bottom:14px">{x["tag"].upper()} \u00b7 {nice(x["date"])}</div><h2 class="hd" style="margin:0 0 12px;font-weight:600;font-size:24px;line-height:1.25">{x["title"]}</h2><p style="margin:0;color:#A9BBDD;line-height:1.7">{x["summary"]}</p></a>' for x in posts)
w("/news", page("/news", "News | AS Forge", "News, releases and updates from AS Forge: AS Fetchly versions, SentinelAI progress and new tools.", pagehead("NEWS", "#19E8FF", "News and updates.", "Releases, progress and announcements from the forge.") + block(f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px">{cards}</div>'), "/news", [ORG]))
for x in posts:
    url = f"{SITE}/news/{x['slug']}"
    share = f'<div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:40px"><a class="ghost" rel="noopener" href="https://wa.me/?text={url}" style="border:1.5px solid rgba(160,200,255,.4);padding:10px 18px;border-radius:10px;font-size:14px">Share on WhatsApp</a><a class="ghost" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url={url}" style="border:1.5px solid rgba(160,200,255,.4);padding:10px 18px;border-radius:10px;font-size:14px">Share on LinkedIn</a><a class="ghost" href="/news" style="border:1.5px solid rgba(160,200,255,.4);padding:10px 18px;border-radius:10px;font-size:14px">All news</a></div>'
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": x["title"], "datePublished": x["date"], "author": {"@type": "Organization", "name": "AS Forge"}, "publisher": {"@type": "Organization", "name": "AS Forge"}, "description": x["summary"], "mainEntityOfPage": url}
    w(f"/news/{x['slug']}", page(f"/news/{x['slug']}", x["title"] + " | AS Forge", x["summary"], pagehead(x["tag"].upper() + " \u00b7 " + nice(x["date"]), "#19E8FF", x["title"], "") + prose(x["body"] + share), "/news", [ORG, ld]))

# ---------- sitemap ----------
urls = ["/", "/fetchly", "/projects", "/news", "/about", "/faq", "/contact", "/privacy", "/terms"] + ["/news/" + x["slug"] for x in posts]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("built", len(urls) + 1, "pages")
