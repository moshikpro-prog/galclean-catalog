from icons import svg, F

PRO_ICONS = {
 # crew / workers
 "crew": svg(f'''
  <circle {F} cx="16" cy="9" r="4.2"/><circle cx="16" cy="9" r="4.2"/>
  <path {F} d="M7.5 27c0-5 3.8-8.6 8.5-8.6s8.5 3.6 8.5 8.6z"/><path d="M7.5 27c0-5 3.8-8.6 8.5-8.6s8.5 3.6 8.5 8.6"/>'''),
 # dimensions / ruler box
 "ruler": svg(f'''
  <path {F} d="M5 11l11-5 11 5v11l-11 5-11-5z"/><path d="M5 11l11-5 11 5v11l-11 5-11-5z"/>
  <path d="M5 11l11 5 11-5M16 16v11"/>'''),
 # water softener tank
 "softener": svg(f'''
  <path {F} d="M10 9.5c0-2.5 2.7-4 6-4s6 1.5 6 4V26a2 2 0 0 1-2 2h-8a2 2 0 0 1-2-2z"/>
  <path d="M10 9.5c0-2.5 2.7-4 6-4s6 1.5 6 4V26a2 2 0 0 1-2 2h-8a2 2 0 0 1-2-2z"/>
  <rect x="12.5" y="2.5" width="7" height="3" rx="1"/><path d="M19.5 4h4.5v3M12.5 4H8v3"/>
  <path d="M13 14h6M13 18h6M13 22h6" stroke-opacity=".5"/>'''),
 # portable sprayer
 "sprayer": svg(f'''
  <path {F} d="M8 11h12a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V13a2 2 0 0 1 2-2z"/>
  <path d="M8 11h12a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V13a2 2 0 0 1 2-2z"/>
  <path d="M10 11V7.5a4 4 0 0 1 8 0V11"/><path d="M22 16c3 0 4.5 1.6 4.5 4v3.5"/><path d="M25 23.5h3"/>
  <path d="M9.5 17h9" stroke-opacity=".5"/>'''),
 # blade head (GALBLADE)
 "blade": svg(f'''
  <rect {F} x="4" y="14" width="24" height="5" rx="1"/><rect x="4" y="14" width="24" height="5" rx="1"/>
  <path d="M4 22.5h24" stroke-width="2"/><path d="M6 19v3.5M26 19v3.5"/>
  <path d="M16 14V9"/><rect x="14" y="4" width="4" height="5" rx="1"/>'''),
 # squeegee head (High Flyer)
 "squeegee": svg(f'''
  <path {F} d="M4 18h24l-2 4H6z"/><path d="M4 18h24l-2 4H6z"/>
  <path d="M5 25h22" stroke-width="2"/>
  <path d="M16 18l-3-8"/><rect x="10.2" y="4.5" width="4" height="6" rx="1" transform="rotate(-20 12.2 7.5)"/>'''),
 # soft fibre brush (original flat-brush line icon)
 "fiberbrush": svg(f'''
  <rect {F} x="4" y="11" width="24" height="5.5" rx="1.5"/>
  <rect x="4" y="11" width="24" height="5.5" rx="1.5"/>
  <path d="M5.5 16.5v6M7.5 16.5v6M9.5 16.5v6M11.5 16.5v6M13.5 16.5v6M15.5 16.5v6M17.5 16.5v6M19.5 16.5v6M21.5 16.5v6M23.5 16.5v6M25.5 16.5v6" stroke-width="1.2"/>
  <path d="M16 11V3"/><rect x="14.5" y="7.5" width="3" height="3.5" rx=".6"/>'''),
 # modular pole sections
 "modular": svg(f'''
  <path {F} d="M4.5 27.5l5.5-5.5 1.8 1.8-5.5 5.5z"/><path d="M4.5 27.5l5.5-5.5 1.8 1.8-5.5 5.5z"/>
  <path d="M12.5 21l5.5-5.5 1.8 1.8-5.5 5.5z"/>
  <path d="M20.5 13l5.5-5.5 1.8 1.8-5.5 5.5z"/>
  <path d="M10.6 22.4l1.9-1.4M18.6 14.4l1.9-1.4" stroke-width="2.2"/>'''),
}
