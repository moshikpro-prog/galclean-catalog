# Self-rinsing shower-glass rail (RO/DI water) — feasibility study v0.1

Status: **concept / pre-prototype**. Not for production. Hebrew report: `report/index.html` (interactive 3D viewer, drawings, calculations, test plan).

## Bottom line
- The original concept (storage trough + continuous overflow weir + sloped channel) was rejected: at 2–4 L/min/m the weir head is only 0.69–1.10 mm, so ±10 % uniformity needs the crest level within ±0.05 mm over 1 m.
- Recommended concept C: pressurised micro-orifice manifold (316L tube Ø10×0.8, 101 × Ø0.5 laser-drilled holes) jetting horizontally into a 1.2 mm capillary slot whose inner wall is the glass itself. Orifice ΔP 3.4 kPa @ 2 L/min → 10 mm tilt changes local flow ≈1.4 %. No levelling mechanism needed.
- Main open risk (not a rail issue): film continuity on the glass. At 2 L/min/m a continuous film is predicted only for receding contact angle ≲17° (≲30° at 4 L/min/m). Must be measured (tests T0, T3, T4).

## Contents
| Path | What |
|---|---|
| `calc/rinse_calc.py` | All calculations → `calc/results/calc_results.{json,md}` |
| `cad/geometry.py` | Single source of truth for the cross-section |
| `cad/build_cad.py` | Generates STEP/STL in `cad/out/` (needs `pip install cadquery`) |
| `cad/out/PRINT_*.stl` | 247.5 mm printable segments (×4), TPU wedge gasket |
| `cad/out/TEST300_*` | 300 mm hydraulic test section, covers with 0.8/1.2/1.6 mm slot |
| `cad/out/assembly_rail_1000_on_glass.step` | 1 m rail on 1000×2000×8 glass |
| `drawings/make_drawings.py` | Generates A3 sheets S1–S5 (SVG) |
| `renders/` | Static renders from the 3D viewer |
| `report/index.html` | Full report (Hebrew) |

Regenerate: `python3 calc/rinse_calc.py && python3 cad/build_cad.py && python3 drawings/make_drawings.py`
