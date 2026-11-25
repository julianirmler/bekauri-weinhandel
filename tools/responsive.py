import re, sys, os
D = '/home/claude/bekauri-weinhandel/design/'

def rep(s, a, b, count=1, name=''):
    n = s.count(a)
    assert n >= 1, 'not found: ' + (name or a[:70])
    if count == 1:
        assert n == 1, f'ambiguous ({n}): ' + (name or a[:70])
    return s.replace(a, b) if count == 0 else s.replace(a, b, 1)

def vw(n): return f'{round(n/14.4, 2)}vw'
def ptok(t):
    if t == '0': return t
    n = int(t[:-2])
    if n == 28: return 'clamp(16px, 4vw, 28px)'
    if n >= 32: return f'clamp({max(16, round(n*0.5))}px, {vw(n)}, {n}px)'
    return t
def fluid(s):
    s = re.sub(r'minmax\((\d+)px, 1fr\)', r'minmax(min(100%, \1px), 1fr)', s)
    s = re.sub(r'padding: ((?:\d+px|0)(?: (?:\d+px|0)){0,3})(?=[;"\'])',
               lambda m: 'padding: ' + ' '.join(ptok(t) for t in m.group(1).split(' ')), s)
    s = re.sub(r'(?<![-\w])gap: (\d+)px(?=[;"])',
               lambda m: f'gap: clamp({round(int(m.group(1))/2)}px, {vw(int(m.group(1)))}, {m.group(1)}px)' if int(m.group(1)) >= 48 else m.group(0), s)
    return s

# ================= Main =================
s = open(D+'Main.dc.html').read()
CSS_MAIN = """html{-webkit-text-size-adjust:100%}
h1,h2,h3,h4,h5{overflow-wrap:break-word}
@media (max-width: 1023px){
.nav-desktop{gap:4px 18px!important;font-size:14px!important}
}
@media (max-width: 599px){
section[id]{scroll-margin-top:72px}
.topbar,.nav-desktop,.hide-m{display:none!important}
.menu-btn{display:inline-flex!important}
.logo-crest{height:44px!important}
.hero-panel{min-height:320px!important}
.hero-crest,.crest-img{width:190px!important}
.hero-crest{animation:none!important}
.hero-ctas a{flex:1 1 100%;text-align:center}
.stats{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.stats .rv{padding:22px 12px 22px 0!important}
.tl-row{grid-template-columns:minmax(0,1fr)!important;gap:4px!important}
.chips{flex-wrap:nowrap!important;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;margin:0 -16px;padding:2px 16px 6px}
.chips::-webkit-scrollbar{display:none}
.chips button{flex:none;white-space:nowrap}
.wine-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:28px 12px!important}
.wine-img{height:240px!important}
.wine-img svg.bottle{height:180px!important;width:54px!important}
.card-title{font-size:20px!important}
.card-foot{flex-direction:column;align-items:stretch!important;gap:8px!important}
.card-foot .btn{width:100%;text-align:center;justify-content:center;padding:11px 10px!important}
.insta{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.insta > div{height:160px!important}
}
@media (min-width: 600px){
.mobile-menu{display:none!important}
}
"""
s = rep(s, 'body{margin:0}\n', 'body{margin:0}\n' + CSS_MAIN, name='helmet')
s = rep(s, "font-size: 16px; line-height: 1.6\">\n<div class=\"progress\"", "font-size: 16px; line-height: 1.6; overflow-x: clip\">\n<div class=\"progress\"", name='root')
s = rep(s, '<div style="background: #0E1310; color: #D9DED6; font-size: 13px">', '<div class="topbar" style="background: #0E1310; color: #D9DED6; font-size: 13px">')
s = rep(s, '<nav aria-label="{{t.navLabel}}" style="display: flex; flex-wrap: wrap; gap: 4px 30px', '<nav class="nav-desktop" aria-label="{{t.navLabel}}" style="display: flex; flex-wrap: wrap; gap: 4px 30px')
s = rep(s, '<div role="group" aria-label="Sprache / ენა" style=', '<div class="hide-m" role="group" aria-label="Sprache / ენა" style=')
MENU_BTN = '''<button type="button" class="menu-btn" onClick="{{toggleMenu}}" aria-expanded="{{menuExpanded}}" aria-controls="mobile-menu" aria-label="{{t.menuLabel}}" style="display: none; width: 44px; height: 44px; border-radius: 999px; border: 1px solid #3C4A40; background: transparent; color: #FAFAF7; cursor: pointer; align-items: center; justify-content: center">
<sc-if value="{{menuOpen}}" hint-placeholder-val="{{ false }}"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></sc-if>
<sc-if value="{{menuClosed}}" hint-placeholder-val="{{ true }}"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></sc-if>
</button>
'''
s = rep(s, '<span style="font-weight: 700">0</span>\n</a>\n</div>', '<span style="font-weight: 700">0</span>\n</a>\n' + MENU_BTN + '</div>', name='cart end')
LINK = '<a href="#{id}" onClick="{{{{closeMenu}}}}" style="color: #FAFAF7; text-decoration: none; font-size: 18px; padding: 12px 0; border-bottom: 1px solid #2C382F">{{{{t.{k}}}}}</a>'
links = '\n'.join(LINK.format(id=i, k=k) for i, k in [('shop','nav1'),('wissen','nav2'),('weingut','nav3'),('besuch','nav4'),('kontakt','nav5')])
MENU = f'''<sc-if value="{{{{menuOpen}}}}" hint-placeholder-val="{{{{ false }}}}">
<div id="mobile-menu" class="mobile-menu" style="border-top: 1px solid #2C382F; padding: 8px 16px 20px; display: flex; flex-direction: column; gap: 4px">
<nav aria-label="{{{{t.navLabel}}}}" style="display: flex; flex-direction: column">
{links}
</nav>
<div style="display: flex; flex-wrap: wrap; gap: 14px 18px; align-items: center; padding-top: 14px">
<div role="group" aria-label="Sprache / ენა" style="display: flex; gap: 4px; border: 1px solid #3C4A40; border-radius: 999px; padding: 3px">
<sc-for list="{{{{langs}}}}" as="l" hint-placeholder-count="2">
<button type="button" class="btn btn-lang" onClick="{{{{l.pick}}}}" aria-pressed="{{{{l.pressed}}}}" aria-label="{{{{l.name}}}}" lang="{{{{l.code}}}}" style="{{{{l.style}}}}">{{{{l.label}}}}</button>
</sc-for>
</div>
<div role="group" aria-label="{{{{r.switchLabel}}}}" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px">
<span style="font-size: 13px; color: #C9D0C5">{{{{r.switchLabel}}}}</span>
<sc-for list="{{{{regions}}}}" as="g" hint-placeholder-count="2">
<button type="button" class="btn btn-lang" onClick="{{{{g.pick}}}}" aria-pressed="{{{{g.pressed}}}}" style="{{{{g.style}}}}">{{{{g.label}}}}</button>
</sc-for>
</div>
</div>
<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 14px; font-size: 14px">
<a href="tel:+436764117799" style="color: #D9DED6; padding: 6px 0">AT +43 676 411 77 99</a>
<a href="tel:+995591425555" style="color: #D9DED6; padding: 6px 0">GE +995 591 42 55 55</a>
</div>
</div>
</sc-if>
'''
s = rep(s, '</div>\n</header>', '</div>\n' + MENU + '</header>', name='header end')
s = rep(s, "cartLabel: 'Warenkorb, 0 Artikel',", "cartLabel: 'Warenkorb, 0 Artikel', menuLabel: 'Menü',")
s = rep(s, "cartLabel: 'კალათა, 0 ნივთი',", "cartLabel: 'კალათა, 0 ნივთი', menuLabel: 'მენიუ',")
s = rep(s, "this.state = { estate: 'all',", "this.state = { menuOpen: false, estate: 'all',")
s = rep(s, "    return {\n      k: k,", """    return {
      menuOpen: this.state.menuOpen,
      menuClosed: !this.state.menuOpen,
      menuExpanded: this.state.menuOpen ? 'true' : 'false',
      toggleMenu: function () { self.setState({ menuOpen: !self.state.menuOpen }); },
      closeMenu: function () { self.setState({ menuOpen: false }); },
      k: k,""")
# hero
s = rep(s, 'class="in-panel" style="position: relative;', 'class="in-panel hero-panel" style="position: relative;')
s = rep(s, 'alt="{{t.crestAlt}}" style="display: block; width: 300px; height: auto"', 'alt="{{t.crestAlt}}" class="crest-img" style="display: block; width: 300px; height: auto"')
s = rep(s, '<div class="in4" style="display: flex; flex-wrap: wrap; gap: 12px">', '<div class="in4 hero-ctas" style="display: flex; flex-wrap: wrap; gap: 12px">')
s = rep(s, 'font-size: clamp(46px, 6vw, 88px)', 'font-size: clamp(36px, 6vw, 88px)')
# stats
s = rep(s, '<section aria-label="{{t.statsLabel}}" style="background: #ECE8E1">\n<div style=', '<section aria-label="{{t.statsLabel}}" style="background: #ECE8E1">\n<div class="stats" style=')
s = rep(s, 'font-size: 60px;', 'font-size: clamp(38px, 4.2vw, 60px);')
# timeline
s = rep(s, '<li class="rv-left" style="display: grid; grid-template-columns: 120px', '<li class="rv-left tl-row" style="display: grid; grid-template-columns: 120px')
# shop
s = rep(s, 'aria-label="{{t.filterEstate}}" style="display: flex; flex-wrap: wrap; gap: 8px"', 'aria-label="{{t.filterEstate}}" class="chips" style="display: flex; flex-wrap: wrap; gap: 8px"')
s = rep(s, 'aria-label="{{t.filterType}}" style="display: flex; flex-wrap: wrap; gap: 8px"', 'aria-label="{{t.filterType}}" class="chips" style="display: flex; flex-wrap: wrap; gap: 8px"')
s = rep(s, '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 36px 24px">', '<div class="wine-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(270px, 1fr)); gap: 36px 24px">')
s = rep(s, '<div style="background: {{w.bg}}; border-radius: 24px; height: 360px;', '<div class="wine-img" style="background: {{w.bg}}; border-radius: 24px; height: 360px;')
s = rep(s, "'height: 310px; width: auto; max-width: 80%;", "'height: 86%; width: auto; max-width: 80%;")
s = rep(s, '<h3 class="serif" style="margin: 0; font-weight: 600; font-size: 26px; line-height: 1.15"><a href="{{w.page}}"', '<h3 class="serif card-title" style="margin: 0; font-weight: 600; font-size: 26px; line-height: 1.15"><a href="{{w.page}}"')
s = rep(s, '<div style="display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: auto">', '<div class="card-foot" style="display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: auto">', count=0)
# instagram
s = rep(s, '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px">\n<div class="rv-scale"', '<div class="insta" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px">\n<div class="rv-scale"')
# heading minimums
s = s.replace('clamp(38px, 4.4vw, 62px)', 'clamp(30px, 4.4vw, 62px)').replace('clamp(34px, 3.6vw, 50px)', 'clamp(28px, 3.6vw, 50px)').replace('clamp(36px, 4vw, 52px)', 'clamp(28px, 4vw, 52px)').replace('clamp(28px, 3.4vw, 44px)', 'clamp(24px, 3.4vw, 44px)')
s = s.replace('font-size: 42px; line-height: 1.05', 'font-size: clamp(30px, 2.9vw, 42px); line-height: 1.05')
s = fluid(s)
open(D+'Main.dc.html', 'w').write(s)

# ================= Wein =================
w = open(D+'Wein.dc.html').read()
w = rep(w, 'font-size: 16px; line-height: 1.6">\n\n<!-- Header -->', 'font-size: 16px; line-height: 1.6; overflow-x: clip">\n\n<!-- Header -->', name='wein root')
w = rep(w, '<nav aria-label="Hauptnavigation" style=', '<nav class="nav-desktop" aria-label="Hauptnavigation" style=')
w = rep(w, '<div style="background: {{w.bg}}; border-radius: 32px; height: 640px;', '<div class="w-hero-img" style="background: {{w.bg}}; border-radius: 32px; height: 640px;')
w = rep(w, "'height: 560px; width: auto;", "'height: 88%; width: auto;")
w = rep(w, "'height: 260px; width: auto;", "'height: 86%; width: auto;")
w = rep(w, 'grid-template-columns: 150px minmax(0, 1fr)', 'grid-template-columns: 150px minmax(0, 1fr)" class="facts-row', name='facts')
w = w.replace('<div style="display: grid; grid-template-columns: 150px minmax(0, 1fr)" class="facts-row', '<div class="facts-row" style="display: grid; grid-template-columns: 150px minmax(0, 1fr)')
w = rep(w, 'clamp(44px, 5vw, 72px)', 'clamp(34px, 5vw, 72px)')
w = rep(w, '<footer style="background: #0E1310;', '<footer class="w-footer" style="background: #0E1310;')
STICKY = '''<!-- Mobile Kaufleiste -->
<div class="sticky-buy" style="display: none; position: fixed; left: 0; right: 0; bottom: 0; z-index: 50; background: #141A16; color: #FAFAF7; padding: 12px 16px; gap: 12px; align-items: center; justify-content: space-between; box-shadow: 0 -8px 24px rgba(0,0,0,0.25)">
<span style="display: flex; flex-direction: column; line-height: 1.25; min-width: 0">
<span style="font-size: 13px; color: #C9D0C5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{w.name}} {{w.year}}</span>
<span style="font-size: 20px; font-weight: 700">€ {{w.price}}</span>
</span>
<button type="button" onClick="{{add}}" class="btn btn-primary" style="flex: none; font: inherit; font-weight: 700; background: #A84A2E; color: #FFFFFF; border: 0; border-radius: 999px; padding: 12px 20px; min-height: 48px; cursor: pointer">{{addLabelShort}}</button>
</div>

<!-- Footer -->'''
w = rep(w, '<!-- Footer -->', STICKY)
w = rep(w, "    return {\n      w: w,", "    return {\n      addLabelShort: this.state.added ? 'Hinzugefügt ✓' : 'In den Warenkorb',\n      w: w,")
w = fluid(w)
open(D+'Wein.dc.html', 'w').write(w)

# ================= Wrapper (Weinseiten) =================
CSS_WEIN = """html{-webkit-text-size-adjust:100%}
h1,h2,h3,h4,h5{overflow-wrap:break-word}
@media (max-width: 599px){
.nav-desktop{display:none!important}
.logo-crest{height:44px!important}
.w-hero-img{height:440px!important}
.w-hero-img svg.bottle{height:300px!important;width:90px!important}
.facts-row{grid-template-columns:minmax(0,1fr)!important;gap:2px!important}
.sticky-buy{display:flex!important}
.w-footer{padding-bottom:84px}
}
"""
import glob
for f in glob.glob(D+'wein-*.dc.html'):
    t = open(f).read()
    if 'sticky-buy' not in t:
        t = rep(t, '}\n</style>', '}\n' + CSS_WEIN + '</style>', name=f)
        open(f, 'w').write(t)
print('ok')
