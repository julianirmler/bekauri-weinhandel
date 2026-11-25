import sys, json, re
sys.path.insert(0, '/home/claude/tools')
exec(open('/home/claude/tools/responsive.py').read().split('# ================= Main')[0])
s = open(D+'SEO.dc.html').read()
SEC = '''<!-- 8 Mobile -->
<section style="display: flex; flex-direction: column; gap: 20px">
<h2 style="margin: 0; font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 600; font-size: 38px">8 · Mobile &amp; Responsive</h2>
<p style="margin: 0; color: #4B524C">Google bewertet und indexiert die Seite in der mobilen Fassung (Mobile-First-Indexing). Inhalte, Überschriften, strukturierte Daten und Links müssen auf dem Smartphone vollständig vorhanden sein – auch wenn sie dort anders angeordnet sind.</p>
<div style="overflow-x: auto; border: 1px solid #E2DDD4; border-radius: 18px; background: #FFFFFF">
<table style="width: 100%; border-collapse: collapse; font-size: 15px; min-width: 640px">
<thead><tr style="background: #ECE8E1; text-align: left"><th style="padding: 14px 18px">Breakpoint</th><th style="padding: 14px 18px">Breite</th><th style="padding: 14px 18px">Was sich ändert</th></tr></thead>
<tbody>
<tr style="border-top: 1px solid #E2DDD4"><td style="padding: 14px 18px; font-weight: 700">Mobil</td><td style="padding: 14px 18px">bis 599 px</td><td style="padding: 14px 18px; color: #4B524C">Menü-Button statt Navigation, Infoleiste im Menü, alles einspaltig, Kennzahlen 2×2, Weinkarten 2-spaltig, Filter wischbar, Kaufleiste unten auf Weinseiten, kein Parallax</td></tr>
<tr style="border-top: 1px solid #E2DDD4"><td style="padding: 14px 18px; font-weight: 700">Tablet</td><td style="padding: 14px 18px">600–1023 px</td><td style="padding: 14px 18px; color: #4B524C">Kompaktere Navigation, Raster mit 2 Spalten, Abstände und Schriftgrößen fließend skaliert</td></tr>
<tr style="border-top: 1px solid #E2DDD4"><td style="padding: 14px 18px; font-weight: 700">Desktop</td><td style="padding: 14px 18px">ab 1024 px</td><td style="padding: 14px 18px; color: #4B524C">Volles Layout wie im Entwurf (max. 1280 px Inhaltsbreite)</td></tr>
</tbody>
</table>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px">
<div style="background: #FFFFFF; border: 1px solid #E2DDD4; border-radius: 18px; padding: 24px; display: flex; flex-direction: column; gap: 10px">
<h3 style="margin: 0; font-size: 18px">Für die Entwicklung</h3>
<ul style="margin: 0; padding-left: 20px; color: #4B524C; display: flex; flex-direction: column; gap: 4px">
<li><code>&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</code> auf jeder Seite</li>
<li>Raster mit <code>minmax(min(100%, …), 1fr)</code> – nie breiter als der Bildschirm</li>
<li>Abstände und Überschriften mit <code>clamp()</code>, keine festen Pixelhöhen für Inhaltsbereiche</li>
<li>Eingabefelder mindestens 16 px Schrift (kein Auto-Zoom auf dem iPhone), Tippflächen mindestens 44 × 44 px</li>
<li>Mobiles Menü: Navigation bleibt im HTML vorhanden (nur ausgeblendet), damit Google alle Links sieht</li>
</ul>
</div>
<div style="background: #FFFFFF; border: 1px solid #E2DDD4; border-radius: 18px; padding: 24px; display: flex; flex-direction: column; gap: 10px">
<h3 style="margin: 0; font-size: 18px">Ladezeit &amp; Core Web Vitals (mobil)</h3>
<ul style="margin: 0; padding-left: 20px; color: #4B524C; display: flex; flex-direction: column; gap: 4px">
<li>Zielwerte: LCP unter 2,5 s, INP unter 200 ms, CLS unter 0,1</li>
<li>Bilder als WebP/AVIF mit <code>srcset</code>/<code>sizes</code> und festen <code>width</code>/<code>height</code> gegen Layout-Sprünge</li>
<li>Hero-Bild mit <code>fetchpriority="high"</code>, alles unterhalb des sichtbaren Bereichs mit <code>loading="lazy"</code></li>
<li>Google Fonts nur in benötigten Schnitten laden, <code>font-display: swap</code></li>
<li>Prüfen mit Lighthouse (Mobil), PageSpeed Insights und der Search Console sowie auf echten Geräten (iPhone, Android)</li>
</ul>
</div>
</div>
</section>

'''
s = rep(s, '</div>\n</div>\n</x-dc>', SEC + '</div>\n</div>\n</x-dc>', name='seo end')
s = s.replace('"$preview":{"width":1440,"height":4500}', '"$preview":{"width":1440,"height":5300}')
s = fluid(s)
open(D+'SEO.dc.html', 'w').write(s)

# previews
m = open(D+'Main.dc.html').read()
for name, wdt, label in [('Main-mobil', 390, 'Mobil 390 px'), ('Main-tablet', 820, 'Tablet 820 px')]:
    t = m.replace('<title>Georgischer Wein kaufen in Österreich | Bekauri Family Vineyards</title>', f'<title>Vorschau {label} – Startseite</title>', 1)
    t = re.sub(r'"\$preview":\{"width":\d+,"height":\d+\}', f'"$preview":{{"width":{wdt},"height":8000}}', t)
    open(D+name+'.dc.html', 'w').write(t)
wp = open(D+'wein-bekauri-saperavi-qvevri-2021.dc.html').read()
for name, wdt, h, label in [('wein-vorschau-mobil', 390, 6000, 'Mobil 390 px'), ('wein-vorschau-tablet', 820, 4200, 'Tablet 820 px')]:
    t = re.sub(r'<title>.*?</title>', f'<title>Vorschau {label} – Weinseite</title>', wp, 1)
    t = re.sub(r'"\$preview":\{"width":\d+,"height":\d+\}', f'"$preview":{{"width":{wdt},"height":{h}}}', t)
    open(D+name+'.dc.html', 'w').write(t)

c = json.load(open(D+'canvas.json'))
c['pages'].append({"id": "responsive", "name": "Responsive-Vorschau"})
c['boards']['SEO.dc.html']['h'] = 5300
for f, x, w_, h, ttl in [('Main-mobil.dc.html', 0, 390, 8000, 'Startseite · Mobil 390 px'),
                          ('Main-tablet.dc.html', 470, 820, 8000, 'Startseite · Tablet 820 px'),
                          ('wein-vorschau-mobil.dc.html', 1370, 390, 6000, 'Weinseite · Mobil 390 px'),
                          ('wein-vorschau-tablet.dc.html', 1840, 820, 4200, 'Weinseite · Tablet 820 px')]:
    c['boards'][f] = {"x": x, "y": 0, "w": w_, "h": h, "is_interactive": True, "title": ttl, "page": "responsive"}
    c['order'].append(f)
c['notes']['responsive-info'] = {"x": -760, "y": 0, "w": 640, "page": "responsive", "fill": "blue",
  "text": "Responsive-Vorschau: Kopien der Startseite und der Weinseite (Saperavi Qvevri 2021) in Handy- und Tablet-Breite. Die Originale auf den anderen Seiten passen sich selbst an jede Breite an – Änderungen bitte dort machen, die Vorschauen werden danach neu erzeugt."}
json.dump(c, open(D+'canvas.json', 'w'), ensure_ascii=False)
print('ok', len(c['boards']))
