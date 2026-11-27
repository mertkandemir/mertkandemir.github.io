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
            title="Mert Kandemir | Kişisel Web Sitesi",
            desc="İzmir’de yaşayan yazılım geliştiricisi Mert Kandemir’in kişisel web sitesi.",
            nav="Ana menü", skip="İçeriğe geç", about="Hakkımda", contact="İletişim",
            location="İzmir, Türkiye", role="Yazılım geliştirici",
            specialty="Karmaşık süreçleri, sade ve çalışan dijital sistemlere dönüştürüyorum.",
            atelier="Code Atelier", atelier_nav="Atölye", atelier_kicker="İnteraktif deneyim · 01",
            atelier_intro="Kodu değiştir. Çalıştır. Fikrin ekranda nasıl bir şeye dönüştüğünü anında gör.",
            html_tab="HTML", css_tab="CSS", js_tab="JavaScript", output="Canlı çıktı",
            run="Çalıştır", reset="Sıfırla", shortcut="Ctrl / ⌘ + Enter",
            updated="Çıktı güncellendi.", reset_done="Başlangıç kodu geri yüklendi.",
            lab_nav="Atölye modu", web_lab="Web Lab", troia_lab="TROIA Lab",
            troia_intro="Gerçek üretim problemlerinin TROIA ile nasıl modellendiğini keşfet.",
            scenarios="TROIA senaryoları", production_diff="Üretim farkı", month_end="Ay sonu tarihi",
            material_cost="Malzeme maliyeti", scenario_code="Senaryo kodu",
            simulation="ERP çıktı simülasyonu", simulation_note="Bu alan TROIA motoru değildir. Sonuçlar örnek ERP senaryosunu güvenli biçimde simüle eder.",
            plan_qty="Planlanan miktar", actual_qty="Gerçekleşen miktar", start_date="Başlangıç tarihi",
            main_cost="Ana malzeme maliyeti", reuse_cost="Geri kullanım maliyeti", extra_cost="Ek maliyet",
            run_simulation="Simülasyonu çalıştır", status_label="Durum", difference_label="Fark",
            total_label="Toplam", successful="Başarılı", troia_updated="ERP simülasyonu güncellendi.",
            no_script="Code Atelier’i kullanmak için JavaScript’i etkinleştir.",
            proof_one="Kurumsal sistemler", proof_two="Süreç tasarımı", proof_three="Dijital ürünler",
            about_intro="Üretim süreçleri için yazılım geliştiriyorum. Çalışmalarım Canias ERP, süreç analizi ve TROIA ile uygulama geliştirme üzerine yoğunlaşıyor.",
            mail="E-posta", path="/", og="og-home-tr.jpg", alternate="/en/", alternate_lang="en", alternate_label="EN",
        )
    else:
        t = dict(
            title="Mert Kandemir | Personal Website",
            desc="Personal website of Mert Kandemir, a software developer based in İzmir.",
            nav="Main navigation", skip="Skip to content", about="About", contact="Contact",
            location="İzmir, Türkiye", role="Software developer",
            specialty="I turn complex processes into clear, dependable digital systems.",
            atelier="Code Atelier", atelier_nav="Atelier", atelier_kicker="Interactive experience · 01",
            atelier_intro="Change the code. Run it. See an idea become something real, instantly.",
            html_tab="HTML", css_tab="CSS", js_tab="JavaScript", output="Live output",
            run="Run", reset="Reset", shortcut="Ctrl / ⌘ + Enter",
            updated="Output updated.", reset_done="Starter code restored.",
            lab_nav="Atelier mode", web_lab="Web Lab", troia_lab="TROIA Lab",
            troia_intro="Explore how real manufacturing problems can be modeled with TROIA.",
            scenarios="TROIA scenarios", production_diff="Production variance", month_end="Month-end date",
            material_cost="Material cost", scenario_code="Scenario code",
            simulation="ERP output simulation", simulation_note="This is not a TROIA runtime. The results safely simulate an example ERP scenario.",
            plan_qty="Planned quantity", actual_qty="Actual quantity", start_date="Start date",
            main_cost="Main material cost", reuse_cost="Reuse material cost", extra_cost="Additional cost",
            run_simulation="Run simulation", status_label="Status", difference_label="Difference",
            total_label="Total", successful="Successful", troia_updated="ERP simulation updated.",
            no_script="Enable JavaScript to use the Code Atelier.",
            proof_one="Enterprise systems", proof_two="Process design", proof_three="Digital products",
            about_intro="I develop software for manufacturing operations, with a focus on Canias ERP, process analysis, and application development in TROIA.",
            mail="Email", path="/en/", og="og-home-en.jpg", alternate="/", alternate_lang="tr", alternate_label="TR",
        )
    extra = (f'<link rel="stylesheet" href="/assets/css/home.css?v=7">\n'
             '<script src="/assets/js/code-atelier.js?v=2" defer></script>\n'
             f'<script type="application/ld+json">{PERSON}</script>\n')

    return (head(lang, t["title"], t["desc"], t["path"], t["og"], alt=True, extra=extra,
                 theme="#111519", body_class="home-page") + f'''<a class="skip" href="#main">{t["skip"]}</a>
<header class="home-header">
  <div class="home-wrap home-navigation">
    <a class="home-brand" href="{t["path"]}"><span aria-hidden="true">MK</span>Mert Kandemir</a>
    <nav aria-label="{t["nav"]}">
      <a href="#atelier">{t["atelier_nav"]}</a>
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
        <p class="home-label">{t["location"]}</p>
        <h1 id="home-title">Mert <em>Kandemir</em></h1>
        <p class="home-role">{t["role"]}</p>
        <p class="home-specialty">{t["specialty"]}</p>
      </div>
      <aside class="home-manifest" aria-label="{t["role"]}">
        <span>MK / 001</span>
        <ol>
          <li><b>01</b>{t["proof_one"]}</li>
          <li><b>02</b>{t["proof_two"]}</li>
          <li><b>03</b>{t["proof_three"]}</li>
        </ol>
        <p aria-hidden="true">&#123; build / refine / deliver &#125;</p>
      </aside>
    </div>
  </section>

  <section class="atelier-section" id="atelier" aria-labelledby="atelier-title" data-code-atelier data-lang="{lang}"
    data-updated="{e(t['updated'])}" data-reset-done="{e(t['reset_done'])}" data-troia-updated="{e(t['troia_updated'])}">
    <div class="home-wrap">
      <header class="atelier-intro">
        <p>{t["atelier_kicker"]}</p>
        <h2 id="atelier-title">{t["atelier"]}</h2>
        <div>
          <p>{t["atelier_intro"]}</p>
          <span>{t["shortcut"]}</span>
        </div>
      </header>

      <div class="lab-switch" role="tablist" aria-label="{t['lab_nav']}">
        <button id="lab-web-tab" type="button" role="tab" aria-selected="true" data-lab-tab="web">{t["web_lab"]}</button>
        <button id="lab-troia-tab" type="button" role="tab" aria-selected="false" data-lab-tab="troia" tabindex="-1">{t["troia_lab"]}</button>
      </div>

      <div id="lab-web-panel" role="tabpanel" aria-labelledby="lab-web-tab" data-lab-panel="web">
      <div class="atelier-window">
        <div class="atelier-bar" aria-hidden="true"><i></i><i></i><i></i><span>mkandemir.com.tr / atelier</span></div>
        <div class="atelier-grid">
          <div class="atelier-editor">
            <div class="atelier-tabs" role="tablist" aria-label="Code editor" data-code-tabs>
              <button id="tab-html" type="button" role="tab" aria-selected="true" data-language="html">{t["html_tab"]}</button>
              <button id="tab-css" type="button" role="tab" aria-selected="false" data-language="css" tabindex="-1">{t["css_tab"]}</button>
              <button id="tab-js" type="button" role="tab" aria-selected="false" data-language="js" tabindex="-1">{t["js_tab"]}</button>
            </div>
            <div class="atelier-panel" id="panel-html" role="tabpanel" aria-labelledby="tab-html">
              <label class="sr-only" for="atelier-html">{t["html_tab"]}</label>
              <textarea id="atelier-html" name="html" spellcheck="false" autocomplete="off" autocapitalize="off" data-code-input></textarea>
            </div>
            <div class="atelier-panel" id="panel-css" role="tabpanel" aria-labelledby="tab-css" hidden>
              <label class="sr-only" for="atelier-css">{t["css_tab"]}</label>
              <textarea id="atelier-css" name="css" spellcheck="false" autocomplete="off" autocapitalize="off" data-code-input></textarea>
            </div>
            <div class="atelier-panel" id="panel-js" role="tabpanel" aria-labelledby="tab-js" hidden>
              <label class="sr-only" for="atelier-js">{t["js_tab"]}</label>
              <textarea id="atelier-js" name="js" spellcheck="false" autocomplete="off" autocapitalize="off" data-code-input></textarea>
            </div>
            <div class="atelier-actions">
              <button class="atelier-reset" type="button" data-reset>{t["reset"]}</button>
              <button class="atelier-run" type="button" data-run>{t["run"]}</button>
            </div>
          </div>
          <div class="atelier-preview">
            <div class="atelier-preview-title"><span>{t["output"]}</span><i aria-hidden="true"></i></div>
            <iframe title="{t["output"]}" sandbox="allow-scripts" data-preview></iframe>
          </div>
        </div>
      </div>
      </div>

      <div id="lab-troia-panel" role="tabpanel" aria-labelledby="lab-troia-tab" data-lab-panel="troia" hidden>
        <div class="troia-heading">
          <p>{t["troia_intro"]}</p>
          <span>CANIAS ERP / TROIA</span>
        </div>
        <div class="troia-scenarios" aria-label="{t['scenarios']}">
          <button type="button" aria-pressed="true" data-scenario="production">{t["production_diff"]}</button>
          <button type="button" aria-pressed="false" data-scenario="date">{t["month_end"]}</button>
          <button type="button" aria-pressed="false" data-scenario="cost">{t["material_cost"]}</button>
        </div>

        <div class="troia-workspace">
          <section class="troia-code" aria-labelledby="troia-code-title">
            <div class="troia-pane-title"><h3 id="troia-code-title">{t["scenario_code"]}</h3><span>TROIA</span></div>
            <pre tabindex="0"><code data-troia-code></code></pre>
            <form class="troia-controls" data-troia-form>
              <div data-field="first"><label for="troia-first" data-field-label>{t["plan_qty"]}</label><input id="troia-first" name="first" type="number" value="100" inputmode="decimal"></div>
              <div data-field="second"><label for="troia-second" data-field-label>{t["actual_qty"]}</label><input id="troia-second" name="second" type="number" value="92" inputmode="decimal"></div>
              <div data-field="third" hidden><label for="troia-third" data-field-label>{t["extra_cost"]}</label><input id="troia-third" name="third" type="number" value="0" inputmode="decimal"></div>
              <button type="submit">{t["run_simulation"]}</button>
            </form>
          </section>

          <section class="troia-output" aria-labelledby="troia-output-title">
            <div class="troia-pane-title"><h3 id="troia-output-title">{t["simulation"]}</h3><span>SIMULATION</span></div>
            <div class="erp-screen">
              <div class="erp-screen-top"><span>ERP / OUTPUT</span><b data-erp-state>ONLINE</b></div>
              <dl>
                <div><dt data-output-label="first">{t["plan_qty"]}</dt><dd data-output-value="first">100</dd></div>
                <div><dt data-output-label="second">{t["actual_qty"]}</dt><dd data-output-value="second">92</dd></div>
                <div><dt data-output-label="result">{t["difference_label"]}</dt><dd class="erp-result" data-output-value="result">−8</dd></div>
                <div><dt>{t["status_label"]}</dt><dd data-output-value="status">{t["successful"]}</dd></div>
              </dl>
            </div>
            <p class="simulation-note">{t["simulation_note"]}</p>
          </section>
        </div>
      </div>
      <p class="atelier-status" role="status" aria-live="polite" data-status></p>
      <noscript><p>{t["no_script"]}</p></noscript>
    </div>
  </section>

  <div class="home-wrap home-profile">
    <section id="hakkimda" aria-labelledby="about-title">
      <h2 id="about-title">{t["about"]}</h2>
      <p>{t["about_intro"]}</p>
    </section>

    <section id="iletisim" aria-labelledby="contact-title">
      <h2 id="contact-title">{t["contact"]}</h2>
      <ul class="home-contact-links">
        <li><a href="#iletisim" data-mail="{MAIL}">{t["mail"]}</a></li>
        <li><a href="{LINKEDIN}">LinkedIn</a></li>
        <li><a href="{GITHUB}">GitHub</a></li>
      </ul>
    </section>
  </div>
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
