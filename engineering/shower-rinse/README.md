# Self-rinsing shower-glass rail (RO/DI water) — feasibility study v0.3

Status: **concept / pre-prototype**. Not for production. Hebrew report: `report/index.html` (interactive 3D viewer, drawings, calculations, test plan).

## Bottom line
- The original concept (storage trough + continuous overflow weir + sloped channel) was rejected: at 2–4 L/min/m the weir head is only 0.69–1.10 mm, so ±10 % uniformity needs the crest level within ±0.05 mm over 1 m.
- Recommended concept C (v0.3 optimum, `calc/optimize.py`): PVDF manifold tube Ø10×1 with 198 × Ø0.35 holes at 5 mm pitch, jetting into a 1.0 mm capillary slot whose inner wall is the glass; jet-to-exit 8 mm (inside the capillary pool), knife exit 13.5 mm below the glass edge with hydrophobic drip-break tip. One tube serves 1.5–4 L/min/m (ΔP 2–15 kPa). No levelling mechanism needed.
- Main open risk (not a rail issue): film continuity on the glass. At 2 L/min/m a continuous film is predicted only for receding contact angle ≲17° (≲30° at 4 L/min/m). Must be measured (tests T0, T3, T4).

- Water source (v0.2): an existing GalClean direct-flow RO unit (1–9 L/min) in a dedicated wall compartment; no tank. One rail per glass panel around the shower. Sizing rule: flow per metre of glass being rinsed ≥2 L/min (≥1.5 in winter) → Business for one panel; corner showers need sequential zones (one solenoid per panel) or Expert. Orifice diameter series Ø0.35–0.70 keeps ≈3.5 kPa per hole.

## Contents
| Path | What |
|---|---|
| `calc/rinse_calc.py` | Base calculations → `calc/results/calc_results.{json,md}` |
| `calc/optimize.py` | Literature-based constraints + design optimisation → `calc/results/optimum.{json,md}` |
| `cad/geometry.py` | Single source of truth for the cross-section |
| `cad/build_cad.py` | Generates STEP/STL in `cad/out/` (needs `pip install cadquery`) |
| `cad/out/PRINT_*.stl` | 247.5 mm printable segments (×4), TPU wedge gasket |
| `cad/out/TEST300_*` | 300 mm hydraulic test section, covers with 0.8/1.2/1.6 mm slot |
| `cad/out/assembly_rail_1000_on_glass.step` | 1 m rail on 1000×2000×8 glass |
| `drawings/make_drawings.py` | Generates A3 sheets S1–S5 (SVG) |
| `renders/` | Static renders from the 3D viewer |
| `report/index.html` | Full report (Hebrew) |

Regenerate: `python3 calc/rinse_calc.py && python3 cad/build_cad.py && python3 drawings/make_drawings.py`
