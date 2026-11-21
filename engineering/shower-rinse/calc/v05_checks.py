"""v0.5 checks: series vs parallel feeding around corners, zone sizing, pass-through lines,
tube retention, rinse-aid pulse option. Uses the 1-D manifold model from rinse_calc.py."""
import json, math, os, io, contextlib, importlib.util
spec = importlib.util.spec_from_file_location("rc", os.path.join(os.path.dirname(__file__), "rinse_calc.py"))
rc = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(rc)
rho, mu, sig, g = rc.rho, rc.mu, rc.sigma, rc.g
R = {}

# ---- 1. one perforated tube running through the corner (series) vs one feed per rail (parallel)
cases = []
for name, Lm, Q, d, ID in [
    ("series 0.9+0.9 m, Q=4, d0.35, ID8", 1.8, 4.0, 0.35, 8.0),
    ("series 0.9+0.9 m, Q=4, d0.35, ID10", 1.8, 4.0, 0.35, 10.0),
    ("series 0.9+0.9 m, Q=4, d0.30, ID8", 1.8, 4.0, 0.30, 8.0),
    ("series 0.9+1.4+0.9 m, Q=6.5, d0.35, ID8", 3.2, 6.5, 0.35, 8.0),
    ("parallel: each rail 0.9 m, Q=2 each, d0.35, ID8", 0.9, 2.0, 0.35, 8.0),
    ("zone: one rail 1.0 m, Q=2, d0.35, ID8", 1.0, 2.0, 0.35, 8.0),
]:
    N = int(round(Lm * 1000 / 5))
    qn, P0 = rc.manifold_distribution(Q, d_hole=d / 1000, Dm=ID / 1000, N=N, Lm=Lm)
    A = math.pi * (ID / 1000) ** 2 / 4
    KE = rho * (Q / 60000 / A) ** 2 / 2
    dp, _ = rc.orifice_dp(Q / 60000 / N, d / 1000)
    cases.append(dict(case=name, spread_pct=round((qn.max() - qn.min()) * 100, 2), KE_over_dP=round(KE / dp, 3),
                      dP_hole_kPa=round(dp / 1000, 2), area_ratio=round(N * math.pi * (d / 1000) ** 2 / 4 / A, 2)))
R["feeding"] = cases

# ---- 2. zone sizing with Business (2 L/min) incl. winter factor (15 C -> 0.73)
def zones(total_m, q_target=2.0, Q=2.0, winter=0.73):
    Lz = Q * winter / q_target           # longest zone that still gets q_target in winter
    n = math.ceil(total_m / Lz - 1e-9)
    return dict(total_m=total_m, max_zone_m=round(Lz, 2), zones=n, time_s=45 * n, water_L=round(Q * winter * 0.75 * n, 1))
R["zones_business"] = [dict(layout=l, **zones(t)) for l, t in
                       [("דופן אחת 0.8", 0.8), ("דופן אחת 1.2", 1.2), ("פינה 0.9+0.9", 1.8), ("פינה 1.2+0.9", 2.1),
                        ("U 0.9+1.4+0.9", 3.2), ("גדול 1.0+2.0+1.0", 4.0)]]

# ---- 3. pass-through line (no holes) pressure drop, 4 m, 2 L/min
def dp_line(ID_mm, Lm=4.0, Q=2.0):
    D = ID_mm / 1000; V = Q / 60000 / (math.pi * D * D / 4); Re = rho * V * D / mu
    f = 64 / Re if Re < 2300 else 0.316 * Re ** -0.25
    return round(f * Lm / D * rho * V * V / 2 / 1000, 1), round(V, 2)
R["pass_through"] = {f"{od}x{idd}": dict(zip(("dP_kPa", "V"), dp_line(idd))) for od, idd in ((6, 4), (8, 6), (10, 8))}

# ---- 4. tube retention: radial jet reaction vs friction, thermal expansion, end-key
m_tube = 0.025 + math.pi / 4 * 0.008 ** 2 * 997          # kg/m PE tube + water
jet_reac = rho * (2 / 60000 / 200) * (2 / 60000 / 200) / (math.pi * 0.35e-3 ** 2 / 4) * 200   # N/m (rho*Q*v per hole x holes/m)
R["retention"] = dict(weight_N_per_m=round(m_tube * g, 2), jet_reaction_N_per_m=round(jet_reac, 3),
                      jet_torque="0 (jets are radial -> no twisting moment)",
                      thermal_dL_mm_per_m_dT25=round(150e-6 * 25 * 1000, 1),
                      note="Hold by form (3-surface pocket, 0.05-0.1 mm clearance) + keyed end plug; "
                           "do not rely on interference: PE/PP relax most clamp load in ~1000 h.")

# ---- 5. rinse-aid pulse option: how much does Gamma_min drop?
def qmin(theta, s=sig):
    c = 1 - math.cos(math.radians(theta))
    return 1.69 * (mu * rho / g) ** 0.2 * (s * c) ** 0.6 / rho * 60000
base = qmin(30)
R["rinse_aid"] = dict(
    qmin_clean_water_theta30=round(base, 2),
    qmin_sigma35_theta30=round(qmin(30, 0.035), 2),
    qmin_sigma35_theta15=round(qmin(15, 0.035), 2),
    reduction_factor_best=round(base / qmin(15, 0.035), 1),
    dose_note="Dishwasher rinse aids: 50-500 ppm in the rinse water. 10 s at 2 L/min x 100 ppm = 33 mg active per rinse.")
os.makedirs("results", exist_ok=True)
json.dump(R, open("results/v05_checks.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(R, indent=1, ensure_ascii=False))
