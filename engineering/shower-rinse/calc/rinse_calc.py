"""
Feasibility calculations - self-rinsing shower-glass rail (RO/DI water).
All SI units internally. Run: python3 rinse_calc.py  -> results/calc_results.json + .md
Every result is a first-order engineering estimate; items marked [EXP] require test validation.
"""
import json, math, os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)
R = {}

# ---------- fluid properties (RO water, 25 C) ----------
rho, mu, sigma, g = 997.0, 0.89e-3, 0.072, 9.81
nu = mu / rho
lc = math.sqrt(sigma / (rho * g))                      # capillary length
R["props"] = dict(rho=rho, mu=mu, sigma=sigma, capillary_length_mm=lc * 1e3)

L = 1.0                                               # rail length [m]
H_glass = 2.0                                         # glass height [m]
flows_lpm = [1.0, 2.0, 3.0, 4.0, 6.0]

# ---------- 1. Falling film on vertical glass (Nusselt) ----------
film = []
for Q in flows_lpm:
    q = Q / 1000 / 60 / L                              # m2/s per unit width
    Gam = rho * q                                      # kg/(m s)
    d = (3 * mu * q / (rho * g)) ** (1 / 3)
    u = q / d
    Re = 4 * Gam / mu
    t_res = H_glass / (1.5 * u)                        # surface-velocity transit (u_s = 1.5 u_mean)
    film.append(dict(Q_lpm=Q, q_m2s=q, Gamma=Gam, delta_mm=d * 1e3, u_mean=u,
                     u_surface=1.5 * u, Re_film=Re, transit_s=t_res,
                     film_volume_L=d * L * H_glass * 1000))
R["film"] = film

# ---------- 2. Minimum wetting rate (film breakdown) vs contact angle ----------
# Hartley & Murgatroyd (1964) force balance:  Gmin = 1.69 (mu rho/g)^0.2 [sigma(1-cos th)]^0.6
# Hobler (1964) energy criterion: E_kin(film) = sigma(1-cos th) -> d_min=[15 mu^2 sigma(1-cos)/(rho^3 g^2)]^0.2
mwr = []
for th in [5, 10, 15, 20, 30, 40, 50, 60, 75, 90, 105]:
    c = 1 - math.cos(math.radians(th))
    G_hm = 1.69 * (mu * rho / g) ** 0.2 * (sigma * c) ** 0.6
    dmin = (15 * mu ** 2 * sigma * c / (rho ** 3 * g ** 2)) ** 0.2
    G_hob = rho ** 2 * g * dmin ** 3 / (3 * mu)
    to_lpm = lambda G: G / rho * L * 1000 * 60
    mwr.append(dict(theta_deg=th, Gmin_HM=G_hm, Gmin_Hobler=G_hob,
                    Qmin_lpm_per_m_HM=to_lpm(G_hm), Qmin_lpm_per_m_Hobler=to_lpm(G_hob)))
R["min_wetting"] = mwr
# soap-contaminated surface tension sensitivity (sigma = 0.035)
R["min_wetting_note"] = ("Correlations are for breakdown of an existing film (receding angle). "
                         "Forming a film on a dry surface needs more flow (advancing angle). [EXP]")

# ---------- 3. Original concept: continuous overflow weir ----------
Cd = 0.62
def weir_head(q):           # sharp-crested rectangular weir, q per unit width
    return (q / ((2 / 3) * Cd * math.sqrt(2 * g))) ** (2 / 3)
weir = []
for Q in [2.0, 4.0]:
    q = Q / 60000 / L
    h0 = weir_head(q)
    # tilt sensitivity: crest tilted by dz across L; local q ~ h^1.5 (ignoring surface tension)
    rows = []
    for dz_mm in [0.05, 0.1, 0.2, 0.5, 1.0, 2.0]:
        dz = dz_mm / 1000
        x = np.linspace(0, L, 2001)
        h = h0 + dz * (x / L - 0.5)
        # conserve total flow: find offset so integral matches
        lo, hi = -0.01, 0.01
        for _ in range(80):
            m = (lo + hi) / 2
            hh = np.clip(h + m, 0, None)
            if np.trapezoid(hh ** 1.5, x) / L > h0 ** 1.5: hi = m
            else: lo = m
        hh = np.clip(h + m, 0, None)
        qq = hh ** 1.5 / h0 ** 1.5
        wet = float(np.mean(qq > 0))
        rows.append(dict(tilt_mm_per_m=dz_mm, q_max_over_mean=float(qq.max()),
                         q_min_over_mean=float(qq.min()), wetted_fraction=wet))
    # tolerance for +/-10 % : dq/q = 1.5 dh/h -> dh = 0.0667 h  (over full length)
    weir.append(dict(Q_lpm=Q, head_mm=h0 * 1e3, head_over_capillary_length=h0 / lc,
                     level_tol_for_pm10pct_mm=2 * 0.10 / 1.5 * h0 * 1e3, tilt=rows))
R["weir"] = weir
# thermal + creep reference
R["thermal"] = dict(dL_alu_mm_dT20=23e-6 * 20 * 1000, dL_PETG_mm_dT20=68e-6 * 20 * 1000,
                    tempered_glass_overall_bow_allow_mm_per_m=3.0)  # EN 12150-1 (horizontal toughening)

# ---------- 4. Alternative B: V-notch serrated weir ----------
vn = []
for Q in [2.0, 4.0]:
    for pitch_mm in [10, 20]:
        N = int(L * 1000 / pitch_mm)
        Qn = Q / 60000 / N
        Cdv = 0.59
        h = (Qn / ((8 / 15) * Cdv * math.sqrt(2 * g) * math.tan(math.radians(45)))) ** 0.4
        vn.append(dict(Q_lpm=Q, pitch_mm=pitch_mm, notches=N, head_mm=h * 1e3,
                       flow_change_pct_per_mm_level=250 * 1e-3 / h))
R["vnotch"] = vn

# ---------- 5. Recommended: pressurised micro-orifice manifold ----------
def orifice_dp(Qhole, d, Cd=0.65):
    A = math.pi * d ** 2 / 4
    v = Qhole / A
    return rho / 2 * (v / Cd) ** 2, v

man = []
for Q in [2.0, 4.0]:
    for d_mm in [0.4, 0.5, 0.6]:
        for pitch_mm in [10]:
            N = int(L * 1000 / pitch_mm)
            Qh = Q / 60000 / N
            dp, v = orifice_dp(Qh, d_mm / 1000)
            Re_j = v * d_mm / 1000 / nu
            man.append(dict(Q_lpm=Q, d_mm=d_mm, pitch_mm=pitch_mm, holes=N, dP_kPa=dp / 1000,
                            jet_v=v, Re_jet=Re_j,
                            hydrostatic_effect_pct_per_10mm_tilt=50 * (rho * g * 0.01) / dp))
R["orifice"] = man

def manifold_distribution(Q_lpm, d_hole=0.5e-3, Dm=8.4e-3, N=100, feed="end",
                          k_rec=0.9, Cd=0.65, dd_sigma=0.0, tilt_mm=0.0, seed=0, Lm=L):
    """1-D discrete manifold model: momentum recovery + Blasius/laminar friction,
    orifice law at each hole. Returns per-hole flow normalised to mean."""
    rng = np.random.default_rng(seed)
    d = d_hole + rng.normal(0, dd_sigma, N)
    A = math.pi * d ** 2 / 4
    Am = math.pi * Dm ** 2 / 4
    dx = Lm / N
    z = tilt_mm / 1000 * (np.arange(N) + 0.5) / N         # elevation of each hole
    Qt = Q_lpm / 60000
    if feed == "center":
        half, P0 = manifold_distribution(Q_lpm / 2, d_hole, Dm, N // 2, "end", k_rec, Cd, dd_sigma, 0, seed, Lm / 2)
        q = np.concatenate([half[::-1], half])
        return q / q.mean(), P0
    qh = np.full(N, Qt / N)
    for _ in range(200):
        P = np.zeros(N)
        Qin = Qt
        p = 0.0
        for i in range(N):
            V = Qin / Am
            Re = max(V * Dm / nu, 1.0)
            f = 64 / Re if Re < 2300 else 0.316 * Re ** -0.25
            Vout = (Qin - qh[i]) / Am
            p += -f * dx / Dm * rho * V ** 2 / 2 + k_rec * rho * (V ** 2 - Vout ** 2) / 2
            P[i] = p - rho * g * z[i]
            Qin -= qh[i]
        # unknown inlet pressure P0: sum Cd A sqrt(2(P0+P)/rho) = Qt
        lo, hi = 0, 1e6
        for _ in range(80):
            P0 = (lo + hi) / 2
            s = np.sum(Cd * A * np.sqrt(2 * np.clip(P0 + P, 0, None) / rho))
            if s > Qt: hi = P0
            else: lo = P0
        new = Cd * A * np.sqrt(2 * np.clip(P0 + P, 0, None) / rho)
        if np.max(np.abs(new - qh)) < 1e-12: break
        qh = 0.5 * qh + 0.5 * new
    return qh / qh.mean(), P0

def smooth(qn, pitch_mm=10, H_mm=10):
    """Lateral smoothing by the capillary slot: periodic Poisson kernel (Hele-Shaw, source at
    height H above a straight outlet line). Returns line-outflow profile at 0.5 mm resolution."""
    N = len(qn); res = 0.5
    x = np.arange(0, N * pitch_mm, res)
    xs = (np.arange(N) + 0.5) * pitch_mm
    out = np.zeros_like(x)
    for xi, q in zip(xs, qn):
        # method of images for the closed ends
        for img in (xi, -xi, 2 * N * pitch_mm - xi):
            out += q * (H_mm / math.pi) / ((x - img) ** 2 + H_mm ** 2)
    return out / out.mean()

dist = []
for Q in [2.0, 4.0]:
    for feed in ["end", "center"]:
        qn, P0 = manifold_distribution(Q, feed=feed)
        dist.append(dict(Q_lpm=Q, feed=feed, max=float(qn.max()), min=float(qn.min()),
                         spread_pct=float((qn.max() - qn.min()) * 100)))
    qn, _ = manifold_distribution(Q, tilt_mm=10.0)
    dist.append(dict(Q_lpm=Q, feed="end + 10 mm tilt", max=float(qn.max()), min=float(qn.min()),
                     spread_pct=float((qn.max() - qn.min()) * 100)))
R["manifold_distribution"] = dist

# Monte-Carlo: hole diameter tolerance (laser drilling) + smoothing by slot
mc = []
for sig_um in [5, 10, 20]:
    raw_cv, sm_cv, sm_rng = [], [], []
    for s in range(200):
        qn, _ = manifold_distribution(2.0, dd_sigma=sig_um * 1e-6, seed=s)
        raw_cv.append(np.std(qn))
        sm = smooth(qn, 10, 8)
        core = sm[40:-40]                       # exclude 20 mm at each end (end walls)
        sm_cv.append(np.std(core)); sm_rng.append(core.max() - core.min())
    mc.append(dict(hole_dia_sigma_um=sig_um, per_hole_CV_pct=100 * float(np.mean(raw_cv)),
                   line_CV_after_slot_pct=100 * float(np.mean(sm_cv)),
                   line_range_after_slot_pct_p95=100 * float(np.percentile(sm_rng, 95))))
R["tolerance_montecarlo"] = mc
R["slot_ripple_pct"] = {f"H={H}mm": 100 * 2 * math.exp(-2 * math.pi * H / 10) for H in (4, 6, 8, 10)}

# ---------- 6. Capillary slot ----------
cap = []
for w_mm in [0.8, 1.0, 1.2, 1.5, 2.0]:
    w = w_mm / 1000
    for th_glass, th_wall in [(20, 60), (40, 75)]:
        h = sigma * (math.cos(math.radians(th_glass)) + math.cos(math.radians(th_wall))) / (rho * g * w)
        cap.append(dict(slot_mm=w_mm, theta_glass=th_glass, theta_fin=th_wall, capillary_rise_mm=h * 1e3))
R["capillary_slot"] = cap

# ---------- 7. Supply line & pump ----------
def pipe_dp(Q_lpm, D, Lp):
    Qs = Q_lpm / 60000; A = math.pi * D ** 2 / 4; V = Qs / A
    Re = V * D / nu; f = 64 / Re if Re < 2300 else 0.316 * Re ** -0.25
    return f * Lp / D * rho * V ** 2 / 2, V, Re
sup = []
for name, D in [('1/4" OD (ID 4.3)', 4.3e-3), ('3/8" OD (ID 6.4)', 6.4e-3)]:
    for Q in [2.0, 4.0]:
        dp, V, Re = pipe_dp(Q, D, 4.0)
        sup.append(dict(tube=name, Q_lpm=Q, length_m=4.0, dP_kPa=dp / 1000, V=V, Re=Re))
R["supply_line"] = sup

# ---------- 8. Rinse water use, dilution & residue ----------
TDS_tap = 450      # mg/L, typical central-Israel tap (order of magnitude; measure locally)
res_water_g_m2 = 30   # residual water left on glass after draining (droplets/film), g/m2 [EXP]
rinse = []
for Q in [2.0, 4.0]:
    f = [x for x in film if x["Q_lpm"] == Q][0]
    tau = f["transit_s"]
    for t in [20, 30, 45, 60, 90]:
        # well-mixed-film approximation: tap fraction decays exp(-(t - tau)/tau) after first pass [EXP]
        frac = 1.0 if t <= tau else math.exp(-(t - tau) / tau)
        for TDS_rinse in [5, 30]:
            TDS_eff = TDS_rinse + frac * TDS_tap
            rinse.append(dict(Q_lpm=Q, t_s=t, volume_L=Q * t / 60, tap_fraction=frac,
                              TDS_rinse=TDS_rinse, TDS_final_film=TDS_eff,
                              residue_mg_m2=TDS_eff * res_water_g_m2 / 1000))
R["rinse"] = rinse
R["residue_baseline_tap_mg_m2"] = TDS_tap * res_water_g_m2 / 1000
# draining film after shut-off (Jeffreys):  delta = sqrt(mu x / (rho g t))
R["drain_film_um"] = {f"x={x}m,t={t}s": 1e6 * math.sqrt(mu * x / (rho * g * t))
                      for x in (0.5, 1.5) for t in (30, 120, 600)}

# DI resin life
meq_per_L = 30 / 50.0 * 1.0      # 30 mg/L as CaCO3 ~ 0.6 meq/L (RO permeate, rough)
R["DI_resin"] = dict(RO_permeate_TDS_assumed=30, daily_volume_L=4.0,
                     resin_capacity_eq_per_L=0.6,
                     resin_life_days_per_L=0.6 * 1000 / (meq_per_L * 4.0))

# ---------- 9. Delivery-blade / structure checks ----------
E_al = 69e9
# body section bending stiffness (approx, from CAD) used for sag under own weight + water
w_kg_m = 0.85
I_body = 2.0e-9   # m4, conservative lower bound of the cap profile about horizontal axis
R["structure"] = dict(mass_kg_per_m=w_kg_m,
                      sag_mm_unsupported_1m=5 * w_kg_m * g * L ** 4 / (384 * E_al * I_body) * 1e3,
                      note="Rail rests on the glass edge along its full length; sag is irrelevant. "
                           "Value shown for a rail spanning 1 m between two clamps (variant B).")

json.dump(R, open(os.path.join(OUT, "calc_results.json"), "w"), indent=2, ensure_ascii=False)

# ---------- markdown summary ----------
md = ["# Calculation results (auto-generated)\n"]
md.append(f"Capillary length of water: {lc*1e3:.2f} mm\n")
md.append("## Falling film on vertical glass (Nusselt)\n| Q L/min/m | Γ kg/m·s | δ mm | u m/s | Re | transit 2 m s | film vol L |\n|---|---|---|---|---|---|---|")
for f in film:
    md.append(f"| {f['Q_lpm']} | {f['Gamma']:.4f} | {f['delta_mm']:.3f} | {f['u_mean']:.3f} | {f['Re_film']:.0f} | {f['transit_s']:.1f} | {f['film_volume_L']:.2f} |")
md.append("\n## Minimum wetting rate vs contact angle\n| θ° | Γmin H-M | Q L/min/m H-M | Q L/min/m Hobler |\n|---|---|---|---|")
for m in mwr:
    md.append(f"| {m['theta_deg']} | {m['Gmin_HM']:.4f} | {m['Qmin_lpm_per_m_HM']:.2f} | {m['Qmin_lpm_per_m_Hobler']:.2f} |")
md.append("\n## Overflow weir (original concept)")
for w in weir:
    md.append(f"\nQ={w['Q_lpm']} L/min: head {w['head_mm']:.2f} mm (h/lc={w['head_over_capillary_length']:.2f}); level tolerance for ±10 %: ±{w['level_tol_for_pm10pct_mm']/2:.3f} mm over full length\n\n| tilt mm/m | qmax/mean | qmin/mean | wetted fraction |\n|---|---|---|---|")
    for r in w["tilt"]:
        md.append(f"| {r['tilt_mm_per_m']} | {r['q_max_over_mean']:.2f} | {r['q_min_over_mean']:.2f} | {r['wetted_fraction']:.2f} |")
md.append("\n## V-notch weir\n| Q | pitch | head mm | %/mm level |\n|---|---|---|---|")
for v in vn:
    md.append(f"| {v['Q_lpm']} | {v['pitch_mm']} | {v['head_mm']:.2f} | {v['flow_change_pct_per_mm_level']:.1f} |")
md.append("\n## Orifice manifold\n| Q | d mm | holes | ΔP kPa | jet m/s | Re | % per 10 mm tilt |\n|---|---|---|---|---|---|---|")
for o in man:
    md.append(f"| {o['Q_lpm']} | {o['d_mm']} | {o['holes']} | {o['dP_kPa']:.2f} | {o['jet_v']:.2f} | {o['Re_jet']:.0f} | {o['hydrostatic_effect_pct_per_10mm_tilt']:.2f} |")
md.append("\n## Manifold distribution (Ø0.5 × 100, ID 8.4)\n| Q | feed | min | max | spread % |\n|---|---|---|---|---|")
for d in dist:
    md.append(f"| {d['Q_lpm']} | {d['feed']} | {d['min']:.3f} | {d['max']:.3f} | {d['spread_pct']:.1f} |")
md.append("\n## Hole tolerance Monte-Carlo (2 L/min)\n| σ(d) µm | per-hole CV % | line CV after slot % | line range p95 % |\n|---|---|---|---|")
for m in mc:
    md.append(f"| {m['hole_dia_sigma_um']} | {m['per_hole_CV_pct']:.1f} | {m['line_CV_after_slot_pct']:.2f} | {m['line_range_after_slot_pct_p95']:.1f} |")
md.append("\n## Supply line (4 m)\n| tube | Q | ΔP kPa | V m/s |\n|---|---|---|---|")
for s in sup:
    md.append(f"| {s['tube']} | {s['Q_lpm']} | {s['dP_kPa']:.1f} | {s['V']:.2f} |")
md.append(f"\n## Rinse / residue (tap baseline {R['residue_baseline_tap_mg_m2']:.1f} mg/m²)\n| Q | t s | L | tap frac | TDS rinse | TDS final | residue mg/m² |\n|---|---|---|---|---|---|---|")
for r in rinse:
    md.append(f"| {r['Q_lpm']} | {r['t_s']} | {r['volume_L']:.2f} | {r['tap_fraction']:.3f} | {r['TDS_rinse']} | {r['TDS_final_film']:.1f} | {r['residue_mg_m2']:.3f} |")
md.append("\n## Draining film thickness after shut-off (µm)\n" + ", ".join(f"{k}: {v:.0f}" for k, v in R["drain_film_um"].items()))
md.append(f"\n## DI resin life: ~{R['DI_resin']['resin_life_days_per_L']:.0f} days per litre of mixed-bed resin (4 L/day, 30 ppm permeate)")
open(os.path.join(OUT, "calc_results.md"), "w").write("\n".join(md))
print("\n".join(md))
