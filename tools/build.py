#!/usr/bin/env python3
"""Builds the static pages of mkandemir.com.tr.

Edit the texts below and run:  python3 tools/build.py
Outputs: index.html, en/index.html, tr/index.html (redirect), 404.html,
sitemap.xml
"""
import html, json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mkandemir.com.tr"
V = "9"  # cache-busting version for css/js
TODAY = datetime.date.today().isoformat()

MAIL = "mertkandemir01|gmail.com"
LINKEDIN = "https://www.linkedin.com/in/mert-kandemir-8798bb8b"
GITHUB = "https://github.com/mertkandemir"

e = html.escape

# --------------------------------------------------------------------------
def head(lang, title, desc, path, og, alt=None, extra="", theme="#f3efe6", body_class=""):
    alts = ""
    if alt:
        alts = (f'<link rel="alternate" hreflang="tr" href="{SITE}/">\n'
                f'<link rel="alternate" hreflang="en" href="{SITE}/en/">\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n')
    body_class = f' class="{body_class}"' if body_class else ""
    return f'''<!DOCTYPE html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="{theme}">
<link rel="canonical" href="{SITE}{path}">
{alts}<meta property="og:type" content="website">
<meta property="og:site_name" content="Mert Kandemir">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/{og}?v={V}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/geist-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/fonts.css?v={V}">
<link rel="stylesheet" href="/assets/css/site.css?v={V}">
<script>document.documentElement.classList.replace('no-js','js');</script>
{extra}</head>
<body{body_class}>
'''

def notfound_topbar():
    return '''<a class="skip" href="#main">İçeriğe geç</a>
<header class="wrap top"><a class="brand" href="/">mert kandemir<b>.</b></a><nav aria-label="Menü"><a href="/en/" lang="en" hreflang="en">EN</a></nav></header>
'''


def footer(lang):
    other = '<a href="/en/" lang="en">English</a>' if lang == "tr" else '<a href="/" lang="tr">Türkçe</a>'
    return f'''<footer><div class="wrap"><span>© {datetime.date.today().year} Mert Kandemir · İzmir</span><span>{other}</span></div></footer>
<script src="/assets/js/site.js?v={V}" defer></script>
</body>
</html>
'''

PERSON = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Mert Kandemir",
    "url": SITE + "/", "address": {"@type": "PostalAddress", "addressLocality": "İzmir", "addressCountry": "TR"},
    "sameAs": [GITHUB, LINKEDIN]}, ensure_ascii=False)

def home(lang):
    if lang == "tr":
        t = dict(
            title="Mert Kandemir | Yazılım ve Üretim",
            desc="Mert Kandemir’in kişisel sitesi. Canias ERP, TROIA ve üretim süreçleri üzerine teknik notlar.",
            nav="Ana menü", skip="İçeriğe geç", notes="Teknik Notlar", contact="İletişim",
            location="İzmir, Türkiye", specialty="Canias ERP ve TROIA",
            intro="Canias ERP ve TROIA ile üretim süreçleri için yazılım geliştiriyorum. Burada üretim yazılımları üzerine teknik notlarımı paylaşıyorum.",
            explore_notes="Teknik notları keşfet",
            notes_intro="Üretim süreçleri, ERP ve TROIA üzerine pratik örnekler ve başvuru kaynakları.",
            troia="TROIA’da ay sonu hesabı",
            troia_intro="Varsayılan tarih aralığı oluştururken başlangıç ve bitiş tarihini nasıl belirleriz?",
            troia_link="Örneği oku",
            troia_detail="Başlangıca bugünün tarihini al. Bitiş için bir sonraki ayın ilk gününü bul ve bir gün geri git. Böylece Şubat, artık yıl ve Aralık gibi durumlar için ayın gün sayısını ayrıca hesaplamak gerekmez.",
            troia_example="Örnek: 10 Şubat 2028 → 29 Şubat 2028",
            contact_intro="Teknik notlar üzerine konuşmak için bana ulaşabilirsin.",
            mail="E-posta", path="/", og="og-home-tr.jpg", alternate="/en/", alternate_lang="en", alternate_label="EN",
        )
    else:
        t = dict(
            title="Mert Kandemir | Software and Manufacturing",
            desc="Mert Kandemir’s personal site. Technical notes on Canias ERP, TROIA, and manufacturing processes.",
            nav="Main navigation", skip="Skip to content", notes="Technical Notes", contact="Contact",
            location="İzmir, Türkiye", specialty="Canias ERP and TROIA",
            intro="I develop software for manufacturing processes with Canias ERP and TROIA. I share technical notes on manufacturing software here.",
            explore_notes="Explore technical notes",
            notes_intro="Practical examples and reference material on manufacturing, ERP, and TROIA.",
            troia="Month-end dates in TROIA",
            troia_intro="How do you set the start and end dates for a default date range?",
            troia_link="Read the example",
            troia_detail="Use today as the start date. For the end date, find the first day of the following month and subtract one day. This handles February, leap years, and December without calculating each month’s length separately.",
            troia_example="Example: 10 February 2028 → 29 February 2028",
            contact_intro="Get in touch to discuss the technical notes.",
            mail="Email", path="/en/", og="og-home-en.jpg", alternate="/", alternate_lang="tr", alternate_label="TR",
        )
    extra = (f'<link rel="stylesheet" href="/assets/css/home.css?v=2">\n'
             f'<script type="application/ld+json">{PERSON}</script>\n')

    return (head(lang, t["title"], t["desc"], t["path"], t["og"], alt=True, extra=extra,
                 theme="#171410", body_class="home-page") + f'''<a class="skip" href="#main">{t["skip"]}</a>
<header class="home-header">
  <div class="home-wrap home-navigation">
    <a class="home-brand" href="{t["path"]}">Mert Kandemir</a>
    <nav aria-label="{t["nav"]}">
      <a href="#notlar">{t["notes"]}</a>
      <a href="#iletisim">{t["contact"]}</a>
      <a class="home-language" href="{t["alternate"]}" lang="{t["alternate_lang"]}" hreflang="{t["alternate_lang"]}">{t["alternate_label"]}</a>
    </nav>
  </div>
</header>
<main id="main">
  <section class="home-hero" aria-labelledby="home-title">
    <div class="home-wrap home-hero-layout">
      <div class="home-hero-copy">
        <p class="home-label">{t["location"]}</p>
        <h1 id="home-title">Mert <em>Kandemir</em></h1>
        <p class="home-specialty">{t["specialty"]}</p>
        <p class="home-intro">{t["intro"]}</p>
        <div class="home-actions">
          <a class="home-button" href="#notlar">{t["explore_notes"]}</a>
        </div>
      </div>
      <img class="home-art" src="/assets/bronze-study.webp" width="1200" height="800" fetchpriority="high" alt="">
    </div>
  </section>

  <section class="home-section home-wrap" id="notlar" aria-labelledby="notes-title">
    <div class="home-section-heading">
      <h2 id="notes-title">{t["notes"]}</h2>
      <p>{t["notes_intro"]}</p>
    </div>
    <div class="home-notes">
      <article class="home-note">
        <p class="home-label">Canias ERP / TROIA</p>
        <h3>{t["troia"]}</h3>
        <p>{t["troia_intro"]}</p>
        <details>
          <summary>{t["troia_link"]}</summary>
          <p>{t["troia_detail"]}</p>
          <p class="home-example">{t["troia_example"]}</p>
        </details>
      </article>
    </div>
  </section>

  <section class="home-section home-wrap home-contact" id="iletisim" aria-labelledby="contact-title">
    <div class="home-section-heading">
      <h2 id="contact-title">{t["contact"]}</h2>
      <p>{t["contact_intro"]}</p>
    </div>
    <ul class="home-contact-links">
      <li><a class="home-link" href="#iletisim" data-mail="{MAIL}">{t["mail"]}</a></li>
      <li><a class="home-link" href="{LINKEDIN}">LinkedIn</a></li>
      <li><a class="home-link" href="{GITHUB}">GitHub</a></li>
    </ul>
  </section>
</main>
''' + footer(lang))

def notfound():
    return (head("tr", "Sayfa bulunamadı — Mert Kandemir", "Aradığın sayfa bulunamadı.", "/404.html", "og-home-tr.jpg",
                 extra='<meta name="robots" content="noindex">\n')
            + notfound_topbar() + '''<main id="main" class="nf">
  <div class="wrap">
    <div class="hello rise"><i aria-hidden="true"></i>Hata · 404</div>
    <h1 class="rise d1">4<em>0</em>4</h1>
    <p class="intro rise d2">Bu sayfa artık yok ya da hiç olmadı. <span lang="en">This page doesn't exist.</span></p>
    <ul class="links rise d3" style="max-width:420px;margin-top:28px"><li><a href="/">Ana sayfa<span>→</span></a></li></ul>
  </div>
</main>
''' + footer("tr"))

REDIRECT = f'''<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><title>Mert Kandemir</title>
<link rel="canonical" href="{SITE}/"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=/"></head>
<body><a href="/">mkandemir.com.tr</a></body></html>
'''

SITEMAP = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>{SITE}/</loc><lastmod>{TODAY}</lastmod>
    <xhtml:link rel="alternate" hreflang="tr" href="{SITE}/"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/"/></url>
  <url><loc>{SITE}/en/</loc><lastmod>{TODAY}</lastmod>
    <xhtml:link rel="alternate" hreflang="tr" href="{SITE}/"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/"/></url>
</urlset>
'''

def write(rel, text):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel)

if __name__ == "__main__":
    write("index.html", home("tr"))
    write("en/index.html", home("en"))
    write("tr/index.html", REDIRECT)
    write("404.html", notfound())
    write("sitemap.xml", SITEMAP)
