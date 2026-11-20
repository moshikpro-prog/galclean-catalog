"""Sensitivity of the tube-to-glass jet distance L (hole exit -> glass)."""
import math, json, os
rho, mu, sig, g = 997, 0.89e-3, 0.072, 9.81
d = 0.35e-3; N = 200
def jet(q):
    Qh = q / 60000 / N; v = Qh / (math.pi * d * d / 4)
    We = rho * v * v * d / sig; Re = v * d * rho / mu; Oh = math.sqrt(We) / Re
    Lb = 19.5 * d * math.sqrt(We) * (1 + 3 * Oh) ** 0.85
    return v, We, Lb
# pendant drop that forms at a hole at very low flow (start/stop): Tate's law, wetted radius r_w
drops = {f"r_w={rw}mm": (6 * rw / 1000 * sig / (rho * g)) ** (1 / 3) * 1000 for rw in (0.175, 0.3, 0.5)}
rows = []
for L in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0):
    v15, _, Lb15 = jet(1.5)
    v2, _, Lb2 = jet(2.0)
    rows.append(dict(L_mm=L,
                     jet_intact_margin_q15=Lb15 * 1000 / L,
                     droop_mm_q15=0.5 * g * (L / 1000 / v15) ** 2 * 1000,
                     impact_error_mm_1deg=L * math.tan(math.radians(1)),
                     impact_error_mm_3deg=L * math.tan(math.radians(3)),
                     window_ok_3deg=L * math.tan(math.radians(3)) < 1.6,
                     drop_regime=("bridge (drop touches glass)" if L <= 1.9 else
                                  "mixed" if L <= 3.0 else "free drop onto cradle"),
                     profile_depth_change_mm=L - 3.5))
out = dict(drops_mm=drops, rows=rows)
os.makedirs("results", exist_ok=True)
json.dump(out, open("results/jet_distance.json", "w"), indent=1)
print("pendant drop diameter:", {k: round(v, 2) for k, v in drops.items()})
print(f"{'L':>5} {'Lb/L@1.5':>9} {'droop':>7} {'err1°':>6} {'err3°':>6}  regime                       Δdepth")
for r in rows:
    print(f"{r['L_mm']:5.1f} {r['jet_intact_margin_q15']:9.1f} {r['droop_mm_q15']:7.3f} {r['impact_error_mm_1deg']:6.2f} {r['impact_error_mm_3deg']:6.2f}  {r['drop_regime']:<28} {r['profile_depth_change_mm']:+.1f}")
