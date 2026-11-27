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
            title="Mert Kandemir | Üretim Yazılımları ve TROIA",
            desc="Mert Kandemir’in Canias ERP, TROIA ve üretim süreçleri üzerine kişisel teknik yazıları.",
            nav="Ana menü", skip="İçeriğe geç", notes="Teknik Yazılar", about="Hakkımda", contact="İletişim",
            hero_title="Üretim yazılımları", hero_emphasis="ve TROIA",
            specialty="Canias ERP / TROIA",
            intro="İş emirleri, ürün ağaçları ve üretim maliyetleri üzerine çalışıyorum. Bu sitede karşılaştığım problemleri ve çözüm yaklaşımlarımı paylaşıyorum.",
            explore_notes="Teknik yazıları oku",
            notes_intro="Canias ERP ve üretim yazılımı geliştirirken karşılaşılan problemlerden iki örnek.",
            open_note="Örneği aç",
            about_intro="İzmir’de yaşayan bir yazılım geliştiricisiyim. Canias ERP üzerinde üretim süreçlerini analiz ediyor, TROIA ile ekranlar ve iş akışları geliştiriyorum.",
            about_detail="Bu sitede bir problemi nasıl ele aldığımı, hangi ayrıntıların sonucu değiştirdiğini ve uygulamada nelere dikkat ettiğimi yazıyorum.",
            contact_intro="Buradaki yazılar üzerine konuşmak veya bir örnek hakkında görüş paylaşmak için bana ulaşabilirsin.",
            mail="E-posta", path="/", og="og-home-tr.jpg", alternate="/en/", alternate_lang="en", alternate_label="EN",
        )
        notes = (
            ("TROIA", "Ay sonu tarihini hesaplamak",
             "Varsayılan bir tarih aralığında başlangıcı bugüne, bitişi içinde bulunulan ayın son gününe ayarlamak.",
             "Başlangıç için bugünün tarihini kullan. Bitiş için bir sonraki ayın ilk gününü bul ve bir gün geri git. Aynı yöntem artık yıllarda ve Aralık’tan Ocak’a geçerken de çalışır.",
             "10 Şubat 2028 → 29 Şubat 2028"),
            ("Üretim / ERP", "İş emri ve ürün ağacı karşılaştırması",
             "Planlanan bileşenlerle ürün ağacındaki bileşenleri karşılaştırırken miktar farklarını ve eksik satırları göstermek.",
             "Bileşenleri malzeme ve varyant bilgisine göre eşleştir. Miktarları ortak bir ölçü biriminde karşılaştır. Bir bileşen yalnızca bir tarafta varsa bunu ayrı bir sonuç olarak kaydet.",
             "Ürün ağacı 4 adet · İş emri 5 adet → 1 adet fark"),
        )
    else:
        t = dict(
            title="Mert Kandemir | Manufacturing Software and TROIA",
            desc="Mert Kandemir’s technical writing on Canias ERP, TROIA, and manufacturing processes.",
            nav="Main navigation", skip="Skip to content", notes="Technical Writing", about="About", contact="Contact",
            hero_title="Manufacturing software", hero_emphasis="and TROIA",
            specialty="Canias ERP / TROIA",
            intro="I work with production orders, bills of materials, and manufacturing costs. I write about the problems I encounter and how I approach them.",
            explore_notes="Read the technical notes",
            notes_intro="Two examples of problems that come up when developing manufacturing software with Canias ERP.",
            open_note="Open example",
            about_intro="I’m a software developer based in İzmir. I analyse manufacturing processes in Canias ERP and build screens and workflows with TROIA.",
            about_detail="I use this site to explain how I approach a problem, which details affect the outcome, and what I look out for during implementation.",
            contact_intro="Get in touch if you’d like to discuss a note or share your perspective on an example.",
            mail="Email", path="/en/", og="og-home-en.jpg", alternate="/", alternate_lang="tr", alternate_label="TR",
        )
        notes = (
            ("TROIA", "Calculating the month-end date",
             "Set the default date range from today to the last day of the current month.",
             "Use today as the start date. To find the end date, take the first day of the next month and subtract one day. The same approach works in leap years and when moving from December to January.",
             "10 February 2028 → 29 February 2028"),
            ("Manufacturing / ERP", "Comparing production orders and bills of materials",
             "Identify quantity differences and missing lines when comparing planned components with a bill of materials.",
             "Match components by material and variant. Convert quantities to a common unit before comparing them. Record any component present on only one side as a separate result.",
             "Bill of materials 4 units · Production order 5 units → 1 unit difference"),
        )
    articles = "\n".join(f'''      <article class="home-note">
        <p class="home-label">{e(topic)}</p>
        <h3>{e(title)}</h3>
        <p>{e(intro)}</p>
        <details>
          <summary>{t["open_note"]}</summary>
          <p>{e(detail)}</p>
          <p class="home-example">{e(example)}</p>
        </details>
      </article>''' for topic, title, intro, detail, example in notes)
    extra = (f'<link rel="stylesheet" href="/assets/css/home.css?v=3">\n'
             f'<script type="application/ld+json">{PERSON}</script>\n')

    return (head(lang, t["title"], t["desc"], t["path"], t["og"], alt=True, extra=extra,
                 theme="#171410", body_class="home-page") + f'''<a class="skip" href="#main">{t["skip"]}</a>
<header class="home-header">
  <div class="home-wrap home-navigation">
    <a class="home-brand" href="{t["path"]}">Mert Kandemir</a>
    <nav aria-label="{t["nav"]}">
      <a href="#notlar">{t["notes"]}</a>
      <a href="#hakkimda">{t["about"]}</a>
      <a href="#iletisim">{t["contact"]}</a>
      <a class="home-language" href="{t["alternate"]}" lang="{t["alternate_lang"]}" hreflang="{t["alternate_lang"]}">{t["alternate_label"]}</a>
    </nav>
  </div>
</header>
<main id="main">
  <section class="home-hero" aria-labelledby="home-title">
    <div class="home-wrap home-hero-layout">
      <div class="home-hero-copy">
        <p class="home-label">{t["specialty"]}</p>
        <h1 id="home-title">{t["hero_title"]} <em>{t["hero_emphasis"]}</em></h1>
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
{articles}
    </div>
  </section>

  <section id="hakkimda" class="home-about" aria-labelledby="about-title">
    <div class="home-section home-wrap home-about-layout">
      <div>
        <h2 id="about-title">{t["about"]}</h2>
        <p class="home-about-name">Mert Kandemir</p>
      </div>
      <div class="home-about-copy">
        <p>{t["about_intro"]}</p>
        <p>{t["about_detail"]}</p>
      </div>
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
