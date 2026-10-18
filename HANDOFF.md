# GalClean catalogs: handoff for continued work

## Live links
- Home-first (Lite, Plus, Business, then pro line): https://moshikpro-prog.github.io/galclean-catalog/
- Pro-first (Expert, Turbo, Ultra, then home line): https://moshikpro-prog.github.io/galclean-catalog/pro.html
- If WhatsApp shows an old preview, add `?v=2` (or bump the number).

## Repo
- GitHub: `moshikpro-prog/galclean-catalog` (public), branch `main`. GitHub Pages deploys automatically on push (about 1 minute).
- Start a new session with: `git clone https://github.com/moshikpro-prog/galclean-catalog`

## Source of truth
- **`index.html` and `pro.html` are edited directly.** They contain later changes than the build scripts (self-hosted videos, custom controls, OG tags, fade jump).
- **Do not regenerate them with `_work/scripts/build_html.py`.** That reverts to YouTube iframes and drops every later change.
- Any text or price change must be applied to **both** files, which are mirror images of each other in page order.
- Mobile layout is 430px wide, RTL Hebrew, Heebo fonts embedded as base64. The files are large, so use grep and targeted edits, not full reads.

## Files
| Path | Contents |
|---|---|
| `index.html`, `pro.html` | The two catalogs (8 sections each) |
| `preview.jpg`, `preview-pro.jpg` | 1200×630 WhatsApp/OG images, one per page with matching headline |
| `media/explain.mp4` + `.jpg` | Right video: autoplay, loop, starts muted with a "הפעל קול" pill |
| `media/demo.mp4` + `.jpg` | Left video: plays on tap; when it plays, the right video is muted |
| `_work/scripts/` | Python build scripts (Playwright HTML→PDF, rembg, OpenCV retouch, icons, OG) |
| `_work/images/` | Retouched product photos (`*_final*.png`, `*_cut.png`) and originals |
| `_work/pdf/` | PDF versions: combined home-first/pro-first (8 pages), A4 and per-model mobile |

## Current behavior (do not break)
- Videos: custom controls (play/pause, seek bar with tap or drag via pointer events, time, mute). They auto-hide after about 2.8s, and a thin blue progress line stays visible. Tapping a playing video shows the controls and does not pause it.
- Sound: the browser blocks unmuted autoplay, so the video starts muted. The first tap anywhere on the page, or on the pill, turns sound on. The pill is small and sits bottom-left, just above the controls bar.
- In-page links (`data-goto`, the model tiles, "חזרה לתחילת המסמך"): quick fade, instant jump, fade in, with no visible scrolling (`jump()` function).
- OG titles: home "GalClean | מהיום כל אחד מנקה חלונות כמו מקצוען"; pro "GalClean | המכשיר של המקצוענים לניקיון חלונות מהיר".

## Content decisions already made
- Lite: flow 1 L/min, no electricity, head 25 cm, **no demo** (7-day trial for 99 ₪ deducted from the price, not yet added to the pages). Plus/Business: head 35 cm.
- Business: "מאפשר ניוד קל" plus a "גם לבית פרטי" box (penthouses or homes with many or high windows).
- Kit section: original items, order and text were kept. Only the reel, head and pole use photos. The blue brush is the "מברשת לניקוי חיפויים וגדרות" add-on (500).
- Home add-ons: rounded catalog prices. Pro add-ons: catalog prices before VAT. No VAT wording on the pages.
- Intro texts were rewritten (home: minerals and white spots; pro: 0 minerals, street-level windows, hard access, up to 20 m).

## Open questions (not yet confirmed with Moshe)
- Pro add-on price gaps between the sources: filters Expert 350 vs 550, Ultra 550 vs 750; 20 L sprayer 390 vs 700; softener 5 L/8 L 3000/4000 vs 2000/3000; 18 m pole 8,500 (flyer only).
- Ultra: usage text was cut short; 20 m vs "6 floors".
- Asterisks on Expert/Turbo; whether a demo applies to the pro line.
- The older A4 and per-model mobile PDFs in `_work/pdf` do not include the latest text fixes.

## Testing tips
- Playwright Chromium can't play H.264. For tests, make a webm copy and serve it with a server that supports Range requests (Python's `http.server` doesn't support seeking).
- The cloud sandbox may not be able to reach github.io. Use `gh run list -L1` to confirm the deploy.
