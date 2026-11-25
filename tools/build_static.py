#!/usr/bin/env python3
"""Baut aus den Canvas-Dateien (design/*.dc.html) eine statische Website in dist/.

Aufruf:  python3 tools/build_static.py
Ergebnis: dist/ – Inhalt per FTP ins Web-Verzeichnis der Domain laden.
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN, DIST = ROOT / 'design', ROOT / 'dist'

BLOBS = {
    '2fdad768f1a061b16aa7e24bff4015b3': 'assets/crest-light.png',
    '8a80dee953d03c72f7bbbe3464760d61': 'assets/crest-dark.png',
    '5c9ddae80329417df34bb2175827b8b0': 'assets/weine/bekauri-kisi-2022.webp',
    '6aba8613f8d52a48d31a115d92842472': 'assets/weine/bekauri-mukuzani-reserve-2020.webp',
    'c30cfbe7d57a69fe9342d14c65b2e255': 'assets/weine/bekauri-rose-2023.webp',
    'a92e1df2327cd61ee8c6c8e6a5f738d9': 'assets/weine/bekauri-mtsvane-2023.webp',
    'e4c23e71741b203eedb7a14ea49b5db0': 'assets/weine/bekauri-kindzmarauli-2022.webp',
    '43d214b4f07b5aa1b886784286f2c59b': 'assets/weine/bekauri-saperavi-qvevri-2021.webp',
    'd798fa6f57885a9254f11d04be53c188': 'assets/weine/bekauri-saperavi-2022.webp',
    '1ec435f57ca15f65c8f7f2d7c38d3801': 'assets/weine/kopisa-amber-2019.webp',
    'be4df69a3c5b08282462d0f2f7b379a9': 'assets/weine/kopisa-kisi-2020.webp',
    '0533a58ce1b02ade6a6281ecaab966b2': 'assets/weine/kopisa-saperavi-2019.webp',
    '9fa10f9422d5680fbb8fac8a17784755': 'assets/weine/kvetera-noble-collection-signature-red-2023.webp',
    '8b6b8f76cd4fe1cf020617e32f8e1b3f': 'assets/weine/kvetera-noble-collection-reserve-2020.webp',
}

DRAFT_CSS = """.draft-note{background:#A84A2E;color:#fff;font:600 13px/1.4 Manrope,system-ui,sans-serif;text-align:center;padding:7px 16px}
"""
DRAFT_NOTE = '<div class="draft-note" role="note">Designentwurf · Warenkorb, Anmeldungen und Formulare sind noch nicht aktiv, einige Inhalte sind Platzhalter.</div>'


def parts(path):
    s = path.read_text()
    helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S).group(1)
    xdc = re.search(r'<x-dc>(.*?)</x-dc>', s, re.S).group(1)
    body = re.sub(r'<helmet>.*?</helmet>', '', xdc, flags=re.S).strip()
    script = re.search(r'<script type="text/x-dc" data-dc-script[^>]*>(.*?)</script>', s, re.S).group(1)
    title = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
    return helmet, body, script, title


def fix(s):
    for blob, rel in BLOBS.items():
        s = s.replace('/_blob/' + blob, rel)
    assert '/_blob/' not in s, 'Unbekanntes Bild: ' + re.search(r'/_blob/\w+', s).group(0)
    return s.replace('Main.dc.html', 'index.html').replace('.dc.html', '.html')


def page(title, desc, helmet, body, script, mount):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/crest-dark.png">
{fix(helmet).strip()}
<style>
{DRAFT_CSS}</style>
</head>
<body>
{DRAFT_NOTE}
<div id="app"></div>
<template id="dc-template">
{fix(body)}
</template>
<script src="assets/mini-dc.js"></script>
<script>
{fix(script).strip()}
</script>
<script>
{mount}
</script>
</body>
</html>
"""


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / 'assets' / 'weine').mkdir(parents=True)
    shutil.copy(ROOT / 'tools' / 'static' / 'mini-dc.js', DIST / 'assets')
    for f in ['crest-light.png', 'crest-dark.png']:
        shutil.copy(ROOT / 'assets' / f, DIST / 'assets')
    for f in (ROOT / 'assets' / 'weine').glob('*.webp'):
        shutil.copy(f, DIST / 'assets' / 'weine')

    # Startseite – Region/Sprache per URL testbar: ?region=ge&lang=ka
    h, b, s, t = parts(DESIGN / 'Main.dc.html')
    mount = """var q = new URLSearchParams(location.search);
MiniDC.mount(Component, { region: q.get('region') || 'auto', startLang: q.get('lang') || 'auto' });"""
    (DIST / 'index.html').write_text(page(t, 'Georgische Weine von Bekauri Family Vineyards – Weingut in Kachetien, Weinhandel bei Graz. Designentwurf.', h, b, s, mount))

    # SEO-Spezifikation
    h, b, s, t = parts(DESIGN / 'SEO.dc.html')
    (DIST / 'konzept-seo.html').write_text(page(t, 'SEO- und On-Page-Spezifikation zum Bekauri-Entwurf.', h, b, s, 'MiniDC.mount(Component, {});'))

    # Weinseiten: Vorlage Wein.dc.html + Styles der jeweiligen Weinseite
    _, wb, ws, _ = parts(DESIGN / 'Wein.dc.html')
    count = 0
    for f in sorted(DESIGN.glob('wein-*.dc.html')):
        if 'vorschau' in f.name:
            continue
        src = f.read_text()
        wine_id = re.search(r'wine-id="([^"]+)"', src).group(1)
        h, _, _, t = parts(f)
        mount = f"MiniDC.mount(Component, {json.dumps({'wineId': wine_id})});"
        (DIST / f.name.replace('.dc.html', '.html')).write_text(
            page(t, f'{t} – Steckbrief, Beschreibung und Bestellung. Designentwurf.', h, wb, ws, mount))
        count += 1

    (DIST / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    (DIST / '.htaccess').write_text(
        '# Entwurf: nicht in Suchmaschinen aufnehmen\n'
        '<IfModule mod_headers.c>\n  Header set X-Robots-Tag "noindex, nofollow"\n</IfModule>\n'
        'DirectoryIndex index.html\n'
        '<IfModule mod_mime.c>\n  AddType image/webp .webp\n</IfModule>\n')
    (DIST / 'LIESMICH.txt').write_text(
        'Bekauri – Designentwurf (statische Website)\n'
        '===========================================\n\n'
        'Hochladen: den GESAMTEN Inhalt dieses Ordners (inkl. assets/ und der versteckten Datei .htaccess)\n'
        'per FTP in das Web-Verzeichnis der Domain laden (oft "htdocs", "public_html" oder "www").\n'
        'Funktioniert auch in einem Unterordner, z. B. /entwurf/.\n\n'
        'Testen: index.html aufrufen. Region und Sprache lassen sich per Adresse erzwingen:\n'
        '  index.html?region=ge   -> Angebote Georgien\n'
        '  index.html?lang=ka     -> Georgisch\n\n'
        'Hinweise:\n'
        '- Die Seite ist fuer Suchmaschinen gesperrt (noindex, robots.txt).\n'
        '- Warenkorb, Formulare und Anmeldungen senden nichts ab.\n'
        '- Schriften werden von Google Fonts geladen; fuer den Live-Betrieb lokal einbinden (DSGVO).\n'
        '- konzept-seo.html enthaelt die SEO-Spezifikation (nicht verlinkt).\n')
    print(f'dist/ gebaut: index.html, konzept-seo.html, {count} Weinseiten')


if __name__ == '__main__':
    main()
