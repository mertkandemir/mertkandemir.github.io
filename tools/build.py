#!/usr/bin/env python3
"""Builds the static pages of mkandemir.com.tr.

Edit the texts / glossary entries below and run:  python3 tools/build.py
Outputs: index.html, en/index.html, tr/index.html (redirect), sozluk/index.html,
404.html, sitemap.xml
"""
import html, json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mkandemir.com.tr"
V = "9"  # cache-busting version for css/js
TODAY = datetime.date.today().isoformat()

MAIL = "mertkandemir01|gmail.com"
LINKEDIN = "https://www.linkedin.com/in/mert-kandemir-8798bb8b"
GITHUB = "https://github.com/mertkandemir"

# --------------------------------------------------------------------------
# Glossary (Turkish, with English equivalents). Keep entries general —
# not tied to any specific product or company.
# --------------------------------------------------------------------------
TERMS = [
    dict(tr="Ana üretim planı", en="Master production schedule", abbr="MPS",
         d="Hangi mamulden, hangi dönemde, ne kadar üretileceğini gösteren plan. Satış tahminleri ve müşteri siparişlerinden beslenir; malzeme ihtiyaç planlamasının ana girdisidir.",
         see=["Malzeme ihtiyaç planlaması", "Mamul"]),
    dict(tr="Darboğaz", en="Bottleneck",
         d="Bir üretim akışında kapasitesi en düşük olan ve bu yüzden tüm hattın çıktısını belirleyen kaynak. Darboğazda kaybedilen bir saat, bütün sistemde kaybedilmiş bir saattir.",
         see=["Kapasite planlama", "İş merkezi"]),
    dict(tr="Emniyet stoku", en="Safety stock",
         d="Talepteki ya da tedarik süresindeki belirsizliğe karşı tutulan ek stok. Malzeme ihtiyaç planlaması, net ihtiyacı hesaplarken bu seviyenin altına düşmemeye çalışır.",
         see=["Tedarik süresi", "Malzeme ihtiyaç planlaması"]),
    dict(tr="Fason üretim", en="Subcontracting",
         d="Bir operasyonun ya da ürünün tamamının dışarıdaki bir firmaya yaptırılması. Malzeme genellikle fasoncuya gönderilir ve işlenmiş olarak geri alınır; stok ve maliyet takibi buna göre yapılır.",
         see=["Operasyon"]),
    dict(tr="Fire", en="Scrap",
         d="Üretim sırasında kullanılamaz hale gelen malzeme ya da ürün. Ürün ağacında planlı bir fire oranı tanımlanabilir; gerçekleşen fire ise üretim teyidiyle kaydedilir.",
         ex="%2 planlı fire tanımlanmış bir bileşen için 100 adetlik üretimde 102 adet malzeme ayrılır.",
         see=["Ürün ağacı", "Üretim teyidi"]),
    dict(tr="Hammadde", en="Raw material",
         d="Üretime girdi olarak alınan, henüz işlenmemiş malzeme. Genellikle satın alma ile temin edilir ve ürün ağaçlarının en alt seviyesinde yer alır.",
         see=["Yarı mamul", "Mamul"]),
    dict(tr="Hazırlık süresi", en="Setup time",
         d="Bir makineyi ya da iş merkezini yeni bir işe hazırlamak için gereken süre: kalıp değişimi, ayar, ilk parça kontrolü. Üretilen miktardan bağımsızdır; bu yüzden büyük partilerde birim başına düşen payı azalır.",
         see=["Çevrim süresi", "Operasyon"]),
    dict(tr="Çevrim süresi", en="Cycle time",
         d="Bir birimin bir operasyonda işlenmesi için geçen süre. Hazırlık süresiyle birlikte operasyonun toplam süresini oluşturur.",
         ex="Hazırlık 30 dk, çevrim 2 dk olan bir operasyonda 100 adet için toplam süre: 30 + 100 × 2 = 230 dakika.",
         see=["Hazırlık süresi", "Rota"]),
    dict(tr="İş emri", en="Production order / work order",
         d="Belirli bir üründen, belirli bir miktarın, belirli tarihler arasında üretilmesi talimatı. Malzeme ihtiyacını ürün ağacından, operasyonları rotadan alır; planlandı, serbest bırakıldı, üretimde, teyit edildi ve kapandı gibi durumlardan geçer.",
         see=["Ürün ağacı", "Rota", "Üretim teyidi"]),
    dict(tr="İş merkezi", en="Work center",
         d="Operasyonların yapıldığı, kapasitesi ve maliyeti tanımlı kaynak: bir makine, bir hat ya da bir montaj istasyonu. Rotadaki her operasyon bir iş merkezine bağlanır.",
         see=["Rota", "Kapasite planlama"]),
    dict(tr="İzlenebilirlik", en="Traceability",
         d="Bir ürünün hangi partiden hammaddelerle, hangi iş emriyle, ne zaman ve hangi makinede üretildiğinin geriye ve ileriye doğru takip edilebilmesi. Otomotiv ve gıda gibi sektörlerde geri çağırmalar için hayati önemdedir.",
         see=["Parti", "İş emri"]),
    dict(tr="Kanban", en="Kanban",
         d="Tüketilen malzemenin bir kart ya da sinyal aracılığıyla yeniden üretim veya ikmal talebi oluşturduğu çekme sistemi. Stok, plana göre değil gerçek tüketime göre yenilenir.",
         see=["Emniyet stoku"]),
    dict(tr="Kapasite planlama", en="Capacity requirements planning", abbr="CRP",
         d="Planlanan iş emirlerinin iş merkezlerinde ne kadar yük oluşturacağını hesaplayıp mevcut kapasiteyle karşılaştırma. Aşırı yüklenen dönemler ve darboğazlar burada görünür hale gelir.",
         see=["İş merkezi", "Darboğaz"]),
    dict(tr="Malzeme ihtiyaç planlaması", en="Material requirements planning", abbr="MRP",
         d="Ana üretim planı, ürün ağaçları ve stok bilgisinden yola çıkarak hangi malzemeden, ne zaman, ne kadar gerektiğini hesaplayan yöntem. Sonuç olarak satın alma talepleri ve planlı iş emirleri önerir.",
         ex="500 bisiklet için 2'şer teker gerekiyorsa ve stokta 300 teker varsa, MRP 700 tekerlik ihtiyaç önerir (emniyet stoku ve fire hariç).",
         see=["Ana üretim planı", "Ürün ağacı", "Tedarik süresi"]),
    dict(tr="Mamul", en="Finished good",
         d="Satışa hazır son ürün. Ürün ağacının en üst seviyesinde yer alır.",
         see=["Yarı mamul", "Hammadde"]),
    dict(tr="MES", en="Manufacturing execution system", abbr="MES",
         d="Sahadaki üretimi anlık olarak izleyen ve yöneten sistem: makine durumları, gerçekleşen miktarlar, duruşlar ve kalite verileri. Genellikle ERP ile PLC/SCADA katmanı arasında köprü kurar.",
         see=["PLC", "SCADA", "OEE"]),
    dict(tr="Mühendislik değişikliği", en="Engineering change", abbr="ECN / ECO",
         d="Bir ürünün tasarımında, ürün ağacında ya da rotasında yapılan kontrollü değişiklik. Geçerlilik tarihi ya da seri numarasıyla devreye alınır; böylece eski ve yeni sürüm birbirine karışmaz.",
         see=["Ürün ağacı", "Rota"]),
    dict(tr="OEE", en="Overall equipment effectiveness", abbr="OEE",
         d="Ekipman verimliliğinin üç bileşenin çarpımıyla ölçülmesi: kullanılabilirlik × performans × kalite. Duruşları, yavaş çalışmayı ve hatalı üretimi tek bir sayıda toplar.",
         ex="%90 kullanılabilirlik × %95 performans × %99 kalite ≈ %85 OEE.",
         see=["MES", "Darboğaz"]),
    dict(tr="Operasyon", en="Operation",
         d="Rotadaki tek bir işlem adımı: kesim, kaynak, boya, montaj gibi. Her operasyonun bir iş merkezi, bir hazırlık süresi ve bir çevrim süresi vardır.",
         see=["Rota", "İş merkezi"]),
    dict(tr="Otomatik tüketim", en="Backflush",
         d="Bileşen tüketiminin tek tek elle girilmesi yerine, üretim teyidi sırasında ürün ağacına göre otomatik olarak stoktan düşülmesi. Hızlıdır, ama gerçek tüketim ürün ağacından saparsa stoklar şaşar.",
         see=["Üretim teyidi", "Ürün ağacı"]),
    dict(tr="Parti", en="Batch / lot",
         d="Aynı koşullarda birlikte üretilen ya da teslim alınan malzeme grubu. Parti numarası izlenebilirliğin temelidir.",
         see=["İzlenebilirlik"]),
    dict(tr="PLC", en="Programmable logic controller", abbr="PLC",
         d="Makineleri ve süreçleri kontrol eden endüstriyel bilgisayar. Sensörlerden sinyal okur ve programına göre motorları, valfleri ve diğer çıkışları yönetir. Sahadan veri toplamanın ilk durağıdır.",
         see=["SCADA", "MES"]),
    dict(tr="Rezervasyon", en="Reservation",
         d="Bir iş emri için gereken malzemenin stokta ayrılması. Böylece aynı malzeme başka bir işe verilmez ve eksikler önceden görülür.",
         see=["İş emri", "Malzeme ihtiyaç planlaması"]),
    dict(tr="Rota", en="Routing",
         d="Bir ürünün üretilmesi için gereken operasyonların sırası, her operasyonun yapılacağı iş merkezi ve süreleri. Ürün ağacı “neyden yapılır?”, rota ise “nasıl yapılır?” sorusunu cevaplar.",
         see=["Operasyon", "İş merkezi", "Ürün ağacı"]),
    dict(tr="SCADA", en="Supervisory control and data acquisition", abbr="SCADA",
         d="PLC'lerden ve sahadaki cihazlardan veri toplayıp operatörlere ekranlar üzerinden izleme ve kontrol imkânı veren sistem. Alarmlar, trendler ve proses görüntüleri burada yaşar.",
         see=["PLC", "MES"]),
    dict(tr="Tedarik süresi", en="Lead time",
         d="Bir malzemenin sipariş edilmesinden ya da üretimine başlanmasından kullanılabilir hale gelmesine kadar geçen süre. Malzeme ihtiyaç planlaması, ihtiyaç tarihinden bu süre kadar geriye giderek sipariş tarihini belirler.",
         see=["Malzeme ihtiyaç planlaması", "Emniyet stoku"]),
    dict(tr="Ürün ağacı", en="Bill of materials", abbr="BOM",
         d="Bir ürünü oluşturan bileşenlerin, miktarlarıyla birlikte hiyerarşik listesi. Çok seviyeli olabilir: mamul → yarı mamuller → hammaddeler.",
         ex="Bir bisikletin ürün ağacında 1 kadro, 2 teker ve 1 zincir bulunur; her teker de kendi içinde jant, jant teli ve lastikten oluşur.",
         see=["Rota", "Yarı mamul", "Malzeme ihtiyaç planlaması"]),
    dict(tr="Üretim teyidi", en="Production confirmation",
         d="Sahada gerçekte ne yapıldığının sisteme kaydedilmesi: üretilen miktar, fire ve harcanan süre. Teyitle birlikte stoklar güncellenir, malzeme tüketimi ve maliyet oluşur.",
         see=["İş emri", "Fire", "Otomatik tüketim"]),
    dict(tr="Yarı mamul", en="Semi-finished good",
         d="Üretimin bir aşamasını tamamlamış ama henüz son ürüne dönüşmemiş malzeme. Kendi ürün ağacı ve rotası olabilir; çoğu zaman ara stokta bekler.",
         ex="Boyanmış bir bisiklet kadrosu, montaja girmeden önce bir yarı mamuldür.",
         see=["Mamul", "Hammadde", "Ürün ağacı"]),
]

TR_ALPHA = "abcçdefgğhıijklmnoöprsştuüvyz"
def tr_key(s):
    s = s.replace("I", "ı").replace("İ", "i").lower()
    return [TR_ALPHA.index(c) if c in TR_ALPHA else 100 + ord(c) for c in s]
def tr_upper(c):
    return {"i": "İ", "ı": "I"}.get(c, c.upper())
def slug(s):
    m = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return re.sub(r"[^a-z0-9]+", "-", s.translate(m).lower()).strip("-")

e = html.escape

# --------------------------------------------------------------------------
def head(lang, title, desc, path, og, alt=None, extra=""):
    alts = ""
    if alt:
        alts = (f'<link rel="alternate" hreflang="tr" href="{SITE}/">\n'
                f'<link rel="alternate" hreflang="en" href="{SITE}/en/">\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n')
    return f'''<!DOCTYPE html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#f3efe6">
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
<body>
'''

def topbar(lang, current):
    if lang == "tr":
        nav = [("/sozluk/", "Sözlük", current == "sozluk"), ("/en/", "EN", False)]
        home, skip = "/", "İçeriğe geç"
    else:
        nav = [("/sozluk/", "Glossary (TR)", False), ("/", "TR", False)]
        home, skip = "/en/", "Skip to content"
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if c else ""}{" lang=\"en\" hreflang=\"en\"" if t=="EN" else ""}{" lang=\"tr\" hreflang=\"tr\"" if t=="TR" else ""}>{t}</a>' for h, t, c in nav)
    return f'''<a class="skip" href="#main">{skip}</a>
<header class="wrap top"><a class="brand" href="{home}">mert kandemir<b>.</b></a><nav aria-label="{"Menü" if lang=="tr" else "Menu"}">{links}</nav></header>
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
        t = dict(title="Mert Kandemir", desc="İzmir'de yaşayan bir yazılımcı. Üretim yazılımları, atölyede PLC ve sensörler, hafta sonları deniz ve kort.",
                 hello="Merhaba · İzmir",
                 intro="İzmir'de yaşayan bir yazılımcıyım. Günlerim <strong>üretim yazılımlarıyla</strong>, akşamlarım atölyede PLC ve sensörlerle, hafta sonlarım çoğu zaman <strong>denizde ya da kortta</strong> geçiyor.",
                 links=[("/sozluk/", "Üretim Sözlüğü", "Ücretsiz kaynak →", True), (LINKEDIN, "LinkedIn", "↗", False), (GITHUB, "GitHub", "↗", False)],
                 mail="E-posta", clock="İzmir'de saat şu an", path="/", og="og-home-tr.jpg")
    else:
        t = dict(title="Mert Kandemir", desc="A software developer in İzmir. Manufacturing software, PLCs and sensors in the workshop, and weekends on the water or the court.",
                 hello="Hello · İzmir",
                 intro="I'm a software developer living in İzmir. My days go into <strong>manufacturing software</strong>, my evenings into PLCs and sensors in the workshop, and my weekends usually <strong>on the water or the court</strong>.",
                 links=[("/sozluk/", "Manufacturing glossary", "Free · in Turkish →", True), (LINKEDIN, "LinkedIn", "↗", False), (GITHUB, "GitHub", "↗", False)],
                 mail="E-mail", clock="Local time in İzmir", path="/en/", og="og-home-en.jpg")
    items = "".join(
        f'<li><a{" class=\"feature\"" if f else ""} href="{h}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""}>{n}<span>{s}</span></a></li>'
        for h, n, s, f in t["links"])
    items += f'<li><a href="#" data-mail="{MAIL}"><span data-mail-text style="font:inherit;letter-spacing:inherit;color:inherit">{t["mail"]}</span><span>@</span></a></li>'
    return (head(lang, t["title"], t["desc"], t["path"], t["og"], alt=True,
                 extra=f'<script type="application/ld+json">{PERSON}</script>\n')
            + topbar(lang, "home") + f'''<main id="main" class="home">
  <div class="wrap">
    <div>
      <div class="hello rise"><i aria-hidden="true"></i>{t["hello"]}</div>
      <h1 class="rise d1">Mert<br><em>Kandemir.</em></h1>
      <p class="intro rise d2">{t["intro"]}</p>
    </div>
    <div class="rise d3">
      <ul class="links">{items}</ul>
      <p class="clock mono">{t["clock"]} <span data-clock>—</span></p>
    </div>
  </div>
</main>
''' + footer(lang))

def glossary():
    terms = sorted(TERMS, key=lambda x: tr_key(x["tr"]))
    names = {x["tr"] for x in terms}
    for x in terms:
        for s in x.get("see", []):
            assert s in names, f"unknown see-also: {s}"
    out, letter, letters = [], None, []
    for x in terms:
        L = tr_upper(x["tr"][0])
        if L != letter:
            letter = L; letters.append(L)
            out.append(f'<h2 class="letter" id="harf-{slug(L) or L}">{L}</h2>')
        sid = slug(x["tr"])
        abbr = f'<span class="abbr">{e(x["abbr"])}</span>' if x.get("abbr") and x["abbr"] != x["tr"] else ""
        ex = f'<div class="ex"><b>Örnek</b>{e(x["ex"])}</div>' if x.get("ex") else ""
        see = ""
        if x.get("see"):
            see = '<p class="see">Ayrıca bak: ' + ", ".join(f'<a href="#{slug(s)}">{e(s)}</a>' for s in x["see"]) + "</p>"
        out.append(f'''<article class="term" id="{sid}">
  <div><h3 style="margin:0"><a href="#{sid}">{e(x["tr"])}</a></h3><span class="en mono">{e(x["en"])}</span>{abbr}</div>
  <div><p>{e(x["d"])}</p>{ex}{see}</div>
</article>''')
    az = "".join(f'<a href="#harf-{slug(L) or L}">{L}</a>' for L in letters)
    ld = json.dumps({"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Üretim Sözlüğü",
        "inLanguage": "tr", "url": SITE + "/sozluk/", "author": {"@type": "Person", "name": "Mert Kandemir"},
        "hasDefinedTerm": [{"@type": "DefinedTerm", "name": x["tr"], "alternateName": x["en"], "description": x["d"],
                            "url": f'{SITE}/sozluk/#{slug(x["tr"])}'} for x in terms]}, ensure_ascii=False)
    body = "\n".join(out)
    return (head("tr", "Üretim Sözlüğü — üretim ve ERP terimleri", f"İş emrinden ürün ağacına, MRP'den OEE'ye {len(terms)} üretim ve ERP teriminin sade Türkçe açıklamaları ve İngilizce karşılıkları.",
                 "/sozluk/", "og-sozluk.jpg", extra=f'<script type="application/ld+json">{ld}</script>\n')
            + topbar("tr", "sozluk") + f'''<main id="main">
  <section class="wrap g-head">
    <div class="hello rise"><i aria-hidden="true"></i>Ücretsiz kaynak · {len(terms)} terim</div>
    <h1 class="rise d1">Üretim <em>Sözlüğü.</em></h1>
    <p class="rise d2">Fabrikada ve ERP'de her gün kullanılan terimlerin sade Türkçe açıklamaları ve İngilizce karşılıkları. Yeni başlayanlar, yazılımcılar ve “bu ne demekti?” diyen herkes için.</p>
  </section>
  <div class="g-tools">
    <div class="wrap">
      <label class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><span class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Terim ara</span><input type="search" data-search placeholder="Terim ara (Türkçe / English)" autocomplete="off"></label>
      <nav class="az" aria-label="Harfler">{az}</nav>
      <span class="count mono"><span data-count>{len(terms)}</span> terim</span>
    </div>
  </div>
  <section class="wrap terms" aria-label="Terimler">
{body}
    <p class="empty">Bu aramayla eşleşen bir terim yok. Eklenmesini istediğin bir terim varsa <a href="#" data-mail="{MAIL}">bana yaz</a>.</p>
    <p class="note">Bu sözlük, genel üretim ve ERP kavramlarını anlatan kişisel bir not defteri olarak hazırlandı; belirli bir yazılıma ya da şirkete ait değildir. Bir hata görürsen ya da eklenmesini istediğin bir terim varsa <a href="#" data-mail="{MAIL}">yaz</a>.</p>
  </section>
</main>
''' + footer("tr"))

def notfound():
    return (head("tr", "Sayfa bulunamadı — Mert Kandemir", "Aradığın sayfa bulunamadı.", "/404.html", "og-home-tr.jpg",
                 extra='<meta name="robots" content="noindex">\n')
            + topbar("tr", "") + '''<main id="main" class="nf">
  <div class="wrap">
    <div class="hello rise"><i aria-hidden="true"></i>Hata · 404</div>
    <h1 class="rise d1">4<em>0</em>4</h1>
    <p class="intro rise d2">Bu sayfa artık yok ya da hiç olmadı. <span lang="en">This page doesn't exist.</span></p>
    <ul class="links rise d3" style="max-width:420px;margin-top:28px"><li><a href="/">Ana sayfa<span>→</span></a></li><li><a href="/sozluk/">Üretim Sözlüğü<span>→</span></a></li></ul>
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
  <url><loc>{SITE}/sozluk/</loc><lastmod>{TODAY}</lastmod></url>
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
    write("sozluk/index.html", glossary())
    write("404.html", notfound())
    write("sitemap.xml", SITEMAP)
