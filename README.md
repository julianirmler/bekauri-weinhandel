# Bekauri – Gesamtkonzept Weingut & Weinhandel

Design-Konzept für einen gemeinsamen Webauftritt von **Bekauri Family Vineyards** (Weingut in Kachetien, Georgien – bekaurivineyards.com) und **Bekauri Weinhandel** (Feldkirchen bei Graz – bekauri-weinhandel.at).

Live-Entwurf (Claude Design Canvas): https://claude.ai/artifact/MLxKTqi7dkdp8DSSN7UMsK

## Inhalt

```
design/
  canvas.json                 Index des Canvas (Artboards, Seiten, Positionen)
  Main.dc.html                One-Pager / Startseite
  SEO.dc.html                 SEO- & On-Page-Spezifikation
  Wein.dc.html                Vorlage Produktseite (alle Weindaten)
  wein-<weingut>-<wein>-<jahrgang>.dc.html   18 Weinseiten (binden Wein.dc.html ein)
  Main-mobil / Main-tablet, wein-vorschau-*   Responsive-Vorschauen (generierte Kopien)
assets/
  crest-dark.png / crest-light.png        Bekauri-Wappen, freigestellt (dunkel / hell)
  wordmark-dark.png / wordmark-light.png  Schriftzug, freigestellt
```

Die `.dc.html`-Dateien sind Design-Komponenten des Claude-Design-Canvas (HTML mit Vorlagen-Platzhaltern `{{…}}`), kein fertiger Produktions-Code. Bilder im Entwurf werden über Canvas-Uploads (`/_blob/…`) geladen; die Originale liegen in `assets/`.

## Statische Website (für Webspace / FTP)

`python3 tools/build_static.py` erzeugt aus `design/` eine eigenständige Website in `dist/` (HTML, CSS, JS, Bilder – läuft auf jedem Webserver, auch in einem Unterordner). Den Inhalt von `dist/` per FTP hochladen; Details in `dist/LIESMICH.txt`. Die Seite ist für Suchmaschinen gesperrt und trägt einen Entwurfs-Hinweis.

## Funktionen im Entwurf

- **Startseite:** Hero mit Wappen-Effekt, Kennzahlen, Geschichte, Shop mit Filter (Weingut / Weinart), Weinwissen, FAQ, Besuch & Verkostung, Newsletter, Kontakt
- **Mehrsprachig:** Umschalter DE | KA (Georgisch)
- **Regionale Angebote:** Österreich (Shop-Aktionen, Euro-Preise) bzw. Georgien (Touren, Partner in Tiflis); Erkennung im Entwurf per Zeitzone, live per IP-Land (siehe SEO-Spezifikation, Abschnitt 7)
- **Weinseiten:** 18 Produktseiten mit Steckbrief, Beschreibung, Videoplatz für Weinpräsentation, verwandten Weinen
- **Responsive:** Breakpoints Mobil (bis 599 px), Tablet (600–1023 px), Desktop (ab 1024 px); Menü-Button, fließende Abstände mit `clamp()`, mobile Kaufleiste auf Weinseiten
- **Effekte:** Scroll-Animationen (CSS Scroll-driven Animations), Logo-Schimmer, Button-Hover; `prefers-reduced-motion` wird respektiert
- **SEO:** Keyword-Mapping, Meta-Daten, Überschriften-Struktur, JSON-LD (LiquorStore, Winery, Product, FAQPage), hreflang-Strategie

## Offene Punkte

- Fotos und Videos (Bildplätze sind beschriftet)
- Verkostungsnotizen, Alkoholgehalt und einige Rebsorten vom Weingut
- Echte Aktionen für AT und GE (derzeit Platzhalter)
- Georgische Texte von Muttersprachler:in prüfen lassen
