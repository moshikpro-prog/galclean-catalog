# ערכת פרומפטים ל-Magnific – מסילת שטיפה למקלחון

## איך משתמשים
1. **שפה:** הפרומפטים כתובים באנגלית, כי מודלי התמונה עובדים טוב יותר באנגלית.
2. **תמונת ייחוס:** כשכתוב "ייחוס", מעלים את התמונה שמצוינת. ב-Magnific/Freepik זו האפשרות **Structure reference** (או Image reference). כך הצורה של המסילה נשמרת.
   - חוזק ייחוס מומלץ: בינוני–גבוה, כ-60–80%.
   - בתמונות חתך מעלים את הייחוס בחוזק גבוה.
3. **מודל:** בוחרים מודל חינמי מהרשימה. לרוב מספיקה איכות רגילה, ואת ההגדלה (Upscale) עושים רק לתמונות שנבחרו.
4. **פרומפט שלילי:** בכל תמונה כדאי להוסיף את הפרומפט השלילי הכללי שבסוף הקובץ.
5. **מגבלה:** מודל AI לא שומר על מידות הנדסיות. תמונות אווירה מתאימות ל-AI. לחתכים מדויקים עדיף להשתמש בשרטוטים ובהדמיות שלנו, ואת ה-AI להפעיל רק לסגנון.

## קובצי ייחוס (בתיקייה `drawings/meeting/` ו-`renders/`)
- `render_overview.png` – זכוכית עם המסילה והווילון, מבט כללי.
- `render_close.png` – תקריב של המסילה על שפת הזכוכית.
- `render_cutaway.png` – קטע מסילה חתוך בקצה (מבחוץ ומבפנים).
- `F_SEC_steps.png` – חתך צבעוני עם ארבעת שלבי המים.
- `S1_section_AA.png` – שרטוט הנדסי של החתך.

---

## סט A – חדר מקלחון מותקן

### A1. מקלחון Walk-in, מבט כללי
יחס 16:9 · ייחוס: `render_overview.png` (חוזק 40–50%, רק לקומפוזיציה)
```
Photorealistic interior photo of a modern bright bathroom with a frameless walk-in shower: one clear tempered glass panel 1 m wide and 2 m high fixed to a light grey tiled wall. On the top edge of the glass sits a slim brushed-aluminium cap rail, about 3 cm wide. A thin, perfectly even, transparent sheet of water flows down the inner face of the glass from just below the rail to the floor, like a smooth glassy curtain, no droplets, no spray. Soft natural daylight from a window, spotless glass, minimalist Scandinavian style, rain shower head on the wall, wide angle, architectural photography, 35mm, high detail.
```

### A2. מקלחון פינתי עם שתי זכוכיות
יחס 16:9
```
Photorealistic photo of a corner shower enclosure with two frameless clear glass panels meeting at a 90-degree corner, in a contemporary bathroom with large-format beige stone tiles. A slim matte-aluminium rail caps the top edge of both glass panels and meets in a neat mitred corner. A thin, uniform transparent water film runs down the inside of both glass panels, gently reflecting the light. Clean, calm, premium hotel bathroom atmosphere, warm evening lighting, eye-level view from outside the shower, ultra realistic.
```

### A3. תקריב של המסילה והווילון
יחס 4:3 · ייחוס: `render_close.png` (חוזק 70%)
```
Macro close-up photo of the top edge of a clear glass shower panel capped by a slim brushed-aluminium rail. Just below the rail, a continuous thin transparent sheet of water emerges along the full width of the glass and flows straight down, perfectly smooth and attached to the glass, with subtle light refraction. Shallow depth of field, studio product lighting, dark soft background, crisp aluminium texture, product photography, 100mm macro.
```

### A4. לפני ואחרי
יחס 16:9
```
Split-screen comparison photo of the same frameless shower glass panel. Left half labeled visually by its condition: glass covered with white limescale spots and dried water marks, cloudy. Right half: crystal clear, spotless glass with a slim aluminium rail on top. Same bathroom, same lighting, sharp vertical dividing line in the middle, realistic product comparison photography.
```
(טקסט "לפני/אחרי" עדיף להוסיף אחר כך בעריכה. מודלים לא כותבים עברית היטב.)

### A5. גרסת גימור שחור מט
יחס 3:4 (לאורך)
```
Photorealistic bathroom with a frameless clear glass shower panel and a slim matte-black top cap rail, black shower fixtures, white marble tiles. A thin even curtain of water runs down the inner side of the glass from the rail. Elegant, high-end, soft overhead lighting, vertical composition, interior design magazine photo.
```

### A6. התא בקיר (טכני-אווירה)
יחס 4:3
```
Photorealistic photo of a neat service cabinet recessed into a bathroom wall next to a shower, door open, showing a compact white water purification unit with filter cartridges, a small manifold with three solenoid valves, thin white tubes, and a small controller box. Clean, organized, technical but friendly look, soft lighting.
```
(המכשיר בתמונה יהיה כללי. אם רוצים מכשיר GalClean אמיתי, מעלים צילום שלו כייחוס.)

---

## סט B – חתכים ומבט פנימי

### B1. חתך תלת-ממדי ריאליסטי
יחס 5:4 · ייחוס: `render_cutaway.png` (חוזק 80–90%)
```
Photorealistic 3D cutaway render of a slim aluminium rail mounted on the top edge of a glass panel, the near end cut open to reveal the inside: a round white plastic tube inside the profile, a removable aluminium cover cradling the tube, a black rubber gasket on the outer side, and a thin blue water sheet flowing down the inner face of the glass. Clean studio lighting, white background, product visualization, sharp edges, high detail.
```

### B2. חתך צבעוני פשוט עם דרך המים
יחס 16:9 · ייחוס: `F_SEC_steps.png` (חוזק 85–95%)
```
Clean technical illustration, cross-section of an aluminium rail on top of a glass panel, flat colors: light grey aluminium, dark grey rubber gasket, pale blue hatched glass, bright blue water. Water flows from a round tube through a tiny hole horizontally onto the glass, collects in a 1 mm gap between the cover and the glass, and exits below as a thin film running down the glass. Minimal infographic style, white background, no text.
```

### B3. מבט מפורק (Exploded view)
יחס 16:9 · ייחוס: `render_cutaway.png` (חוזק 50%)
```
Exploded view product render of a shower glass rinse rail: a 30 cm section of slim aluminium cap profile, a removable aluminium cover, a white plastic tube with a row of tiny holes, black rubber wedge gasket and two small end caps, all floating apart along one axis above a section of clear glass. Studio lighting, light grey background, technical product visualization, no text.
```

### B4. סגנון שרטוט טכני
יחס 4:3 · ייחוס: `S1_section_AA.png` (חוזק 90%+)
```
Engineering blueprint style drawing of a rail cross-section on a glass panel, fine black lines on white, hatched sections, dimension lines, clean CAD look, high resolution, no text.
```
(את הכיתוב והמידות עדיף להשאיר מהשרטוט המקורי. מודלים משבשים מספרים.)

---

## פרומפט שלילי כללי (להוסיף לכל תמונה)
```
blurry, distorted glass, water splashing, spray, droplets flying, thick waterfall, water falling away from the glass, extra rails, bent rail, gaps in the water sheet, text, watermark, logo, low quality, deformed fixtures
```
