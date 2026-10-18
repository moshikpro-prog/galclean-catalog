# Duotone line icons, 32x32 grid. Stroke = currentColor, soft fill via .f (currentColor at low opacity).
S = 'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'
F = 'class="f"'

def svg(body): return f'<svg viewBox="0 0 32 32" {S}>{body}</svg>'

ICONS2 = {
 # RO unit: tall rounded cabinet with dark front panel and logo line
 "device": svg(f'''
  <path {F} d="M9 4.5h14a2.5 2.5 0 0 1 2.5 2.5v19.5a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2V7A2.5 2.5 0 0 1 9 4.5z"/>
  <path d="M9 4.5h14a2.5 2.5 0 0 1 2.5 2.5v19.5a2 2 0 0 1-2 2h-15a2 2 0 0 1-2-2V7A2.5 2.5 0 0 1 9 4.5z"/>
  <rect x="10" y="7.5" width="9" height="18" rx="1.2" fill="currentColor" fill-opacity=".35"/>
  <path d="M12 10.5h5" stroke-width="1.2"/><path d="M12 12.5h3" stroke-width="1.2"/>
  <path d="M21.5 8v17" stroke-opacity=".5"/>
  <path d="M9.5 28.5v1.2M22.5 28.5v1.2"/>'''),

 # Hose reel: drum with flanges, crank, A-frame stand, hose tail
 "reel": svg(f'''
  <circle {F} cx="15" cy="13" r="8"/>
  <circle cx="15" cy="13" r="8"/>
  <circle cx="15" cy="13" r="5.2" stroke-opacity=".55"/>
  <circle cx="15" cy="13" r="1.6" fill="currentColor"/>
  <path d="M15 13l4.5-4" /><circle cx="20.3" cy="8.2" r="1.1"/>
  <path d="M9.5 20l-2.5 8M20.5 20l2.5 8M5.5 28h19"/>
  <path d="M23 13c3.5 0 5 1.8 5 4.5s-1.5 4-3.5 4" stroke-dasharray="0"/>'''),

 # Window cleaning head: wide brush head on swivel neck, bristles + spray holes
 "head": svg(f'''
  <rect {F} x="3" y="15" width="26" height="5" rx="1.5"/>
  <rect x="3" y="15" width="26" height="5" rx="1.5"/>
  <path d="M5 20v4M8 20v4M11 20v4M14 20v4M18 20v4M21 20v4M24 20v4M27 20v4"/>
  <path d="M13.5 15v-3h5v3"/>
  <circle cx="16" cy="10" r="2"/>
  <path d="M16 8V3.5"/>
  <path d="M9 17.5h.01M16 17.5h.01M23 17.5h.01" stroke-width="2"/>'''),

 # Telescopic pole: three tapering sections with clamps
 "pole": svg(f'''
  <path {F} d="M3.6 27.2l7.2-7.2 2.2 2.2-7.2 7.2z"/><path d="M3.6 27.2l7.2-7.2 2.2 2.2-7.2 7.2z"/>
  <path d="M12.6 19.6l6.4-6.4 1.4 1.4-6.4 6.4z" fill="currentColor" fill-opacity=".16"/><path d="M12.6 19.6l6.4-6.4 1.4 1.4-6.4 6.4z"/>
  <rect x="10.4" y="18.6" width="3.6" height="4.4" rx=".8" transform="rotate(45 12.2 20.8)" fill="currentColor" fill-opacity=".6" stroke-width="1.2"/>
  <path d="M20.2 13 27 6.2"/>
  <rect x="18.3" y="12" width="3" height="3.6" rx=".7" transform="rotate(45 19.8 13.8)" fill="currentColor" fill-opacity=".6" stroke-width="1.2"/>
  <path d="M27 6.2c1.3-1.3 2.8-1.1 3.2.3"/>'''),

 # Trolley / hand truck with device on it
 "trolley": svg(f'''
  <path d="M8 3.5h3l4.5 20"/>
  <path d="M15.5 23.5H28"/>
  <rect {F} x="15" y="9" width="10" height="13" rx="1.5"/>
  <rect x="15" y="9" width="10" height="13" rx="1.5"/>
  <path d="M17.5 12h5" stroke-opacity=".6"/>
  <circle {F} cx="14" cy="26.5" r="2.5"/><circle cx="14" cy="26.5" r="2.5"/>'''),

 # Digital TDS meter pen with display
 "tds": svg(f'''
  <path {F} d="M11 3h10a1.5 1.5 0 0 1 1.5 1.5V21H9.5V4.5A1.5 1.5 0 0 1 11 3z"/>
  <path d="M11 3h10a1.5 1.5 0 0 1 1.5 1.5V21H9.5V4.5A1.5 1.5 0 0 1 11 3z"/>
  <rect x="12" y="6" width="8" height="5" rx=".8" fill="currentColor" fill-opacity=".45"/>
  <path d="M13.5 8.5h1M15.5 8.5h1M17.5 8.5h1" stroke-width="1.3"/>
  <circle cx="16" cy="15.5" r="1.4"/>
  <path d="M12.5 21v3.5a3.5 3.5 0 0 0 7 0V21"/>
  <path d="M15 27.5v2M17 27.5v2"/>'''),

 # Blinds / louvre brush: round cylindrical bristle brush on angled adapter + pole
 "brush": svg(f'''
  <path {F} d="M9 6.5h15.5a4 4 0 0 1 4 4v3a4 4 0 0 1-4 4v2H9z"/>
  <path {F} d="M9 6.5h16.5a3 3 0 0 1 3 3V16a3.5 3.5 0 0 1-3.5 3.5H9z"/>
  <path d="M10.5 11.2V6.5M10.5 14.8v4.7 M12.5 11.2V6.5M12.5 14.8v4.7 M14.5 11.2V6.5M14.5 14.8v4.7 M16.5 11.2V6.5M16.5 14.8v4.7 M18.5 11.2V6.5M18.5 14.8v4.7 M20.5 11.2V6.5M20.5 14.8v4.7 M22.5 11.2V6.5M22.5 14.8v4.7 M24.5 11.2V6.5M24.5 14.8v4.7" stroke-width="1.3"/>
  <path d="M26.5 8.2l1.6-1.4M26.8 13h2.4M26.5 17.8l1.6 1.4" stroke-width="1.3"/>
  <path d="M8.5 11.2h18v3.6h-18z" fill="currentColor" fill-opacity=".55"/>
  <path d="M8.5 13 5.5 16.5"/>
  <circle cx="5.5" cy="16.5" r="1.4" fill="currentColor"/>
  <path d="M5.5 16.5 3.5 29.5" stroke-width="2.2"/>'''),

 # Long flat brush for cladding & fences (block with dense bristles on pole)
 "flatbrush": svg(f'''
  <rect {F} x="4" y="11" width="24" height="5.5" rx="1.5"/>
  <rect x="4" y="11" width="24" height="5.5" rx="1.5"/>
  <path d="M5.5 16.5v6M7.5 16.5v6M9.5 16.5v6M11.5 16.5v6M13.5 16.5v6M15.5 16.5v6M17.5 16.5v6M19.5 16.5v6M21.5 16.5v6M23.5 16.5v6M25.5 16.5v6" stroke-width="1.2"/>
  <path d="M16 11V3"/><rect x="14.5" y="7.5" width="3" height="3.5" rx=".6"/>'''),

 # Quick-connect hose fittings (male / female)
 "connect": svg(f'''
  <path d="M2.5 16H7"/>
  <path {F} d="M7 12h5.5l1.5 1.5v5L12.5 20H7z"/><path d="M7 12h5.5l1.5 1.5v5L12.5 20H7z"/>
  <path d="M14 14.5h3v3h-3"/>
  <path {F} d="M18 12h5.5l1.5 1.5v5L23.5 20H18z" /><path d="M18 12h5.5l1.5 1.5v5L23.5 20H18z"/>
  <path d="M25 16h4.5"/>
  <path d="M9.5 12v8M20.5 12v8" stroke-opacity=".5"/>'''),

 # Absorbent mat with water drops
 "mat": svg(f'''
  <path {F} d="M3 23 8.5 15h20.5L23.5 23z"/><path d="M3 23 8.5 15h20.5L23.5 23z"/>
  <path d="M6.5 20.5h19M8 18h19" stroke-opacity=".5"/>
  <path d="M3 23v2.5h20.5V23M23.5 25.5 29 17.5V15"/>
  <path d="M13 4c-1.4 2-2.2 3.1-2.2 4.2a2.2 2.2 0 0 0 4.4 0c0-1.1-.8-2.2-2.2-4.2z"/>
  <path d="M19.5 7.5c-.9 1.3-1.4 2-1.4 2.7a1.4 1.4 0 0 0 2.8 0c0-.7-.5-1.4-1.4-2.7z"/>'''),

 # Filter set: three cartridges with caps
 "filter": svg(f'''
  <rect {F} x="4" y="7" width="6.5" height="20" rx="2"/><rect x="4" y="7" width="6.5" height="20" rx="2"/>
  <rect {F} x="12.75" y="7" width="6.5" height="20" rx="2"/><rect x="12.75" y="7" width="6.5" height="20" rx="2"/>
  <rect {F} x="21.5" y="7" width="6.5" height="20" rx="2"/><rect x="21.5" y="7" width="6.5" height="20" rx="2"/>
  <path d="M5.5 4.5h3.5M14.25 4.5h3.5M23 4.5h3.5"/>
  <path d="M4 11.5h6.5M12.75 11.5h6.5M21.5 11.5h6.5" stroke-opacity=".55"/>
  <path d="M6 15v8M14.75 15v8M23.5 15v8" stroke-opacity=".35"/>'''),

 # Microfiber pad: ribbed sleeve
 "pad": svg(f'''
  <rect {F} x="3" y="10" width="26" height="12" rx="3"/><rect x="3" y="10" width="26" height="12" rx="3"/>
  <path d="M6.5 13.5c1.2 1.2 2.4 1.2 3.6 0s2.4-1.2 3.6 0 2.4 1.2 3.6 0 2.4-1.2 3.6 0 2.4 1.2 3.6 0"/>
  <path d="M6.5 18.5c1.2 1.2 2.4 1.2 3.6 0s2.4-1.2 3.6 0 2.4 1.2 3.6 0 2.4-1.2 3.6 0 2.4 1.2 3.6 0"/>'''),
}
