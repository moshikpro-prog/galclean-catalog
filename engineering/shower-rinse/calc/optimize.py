"""
v0.3 - Extended physics checks + constrained design optimisation.
Imports the base models from rinse_calc.py (manifold 1-D model, smoothing, orifice law).
Outputs results/optimum.json and results/optimum.md
"""
import json, math, os, itertools, importlib.util, io, contextlib
import numpy as np
spec = importlib.util.spec_from_file_location("rc", os.path.join(os.path.dirname(__file__), "rinse_calc.py"))
rc = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(rc)
rho, mu, sigma, g = rc.rho, rc.mu, rc.sigma, rc.g
nu = mu / rho
OUT = rc.OUT
O = {}

# ---------------- constants / literature-based inputs ----------------
TCF = lambda T: math.exp(2700 * (1 / (273.15 + T) - 1 / 298.15))      # RO temperature correction (composite membranes)
O["ro_flow_factor"] = {f"{T}C": round(1 / TCF(T), 3) for T in (12, 15, 18, 20, 25, 28)}
SPOT_FREE_TDS = 10.0   # ppm target for final film (conservative end of 10-50 ppm vendor range)
TAP_TDS = 450.0
TRAVEL = 1.5e-3        # jet travel tube->glass (v0.4)
L = 1.0

def Qmin_lpm_m(theta_deg, sig=sigma):
    c = 1 - math.cos(math.radians(theta_deg))
    G = 1.69 * (mu * rho / g) ** 0.2 * (sig * c) ** 0.6       # Hartley-Murgatroyd (~ El-Genk & Saber per literature)
    return G / rho * 60000

def theta_max_for(q_lpm_m, SF=1.0, sig=sigma):
    lo, hi = 0.1, 120
    for _ in range(60):
        m = (lo + hi) / 2
        if SF * Qmin_lpm_m(m, sig) > q_lpm_m: hi = m
        else: lo = m
    return lo

def film(q_lpm_m, H=2.0):
    q = q_lpm_m / 60000
    d = (3 * mu * q / (rho * g)) ** (1 / 3); u = q / d
    return d, u, H / (1.5 * u)

def cap_rise(w, th_g=30, th_f=60):
    return sigma * (math.cos(math.radians(th_g)) + math.cos(math.radians(th_f))) / (rho * g * w)

def jet(d, Qh):
    v = Qh / (math.pi * d ** 2 / 4) / 1.0          # vena-contracta ignored (conservative for We)
    We = rho * v ** 2 * d / sigma
    Re = v * d / nu
    Oh = math.sqrt(We) / Re
    Lb = 19.5 * d * math.sqrt(We) * (1 + 3 * Oh) ** 0.85     # Grant & Middleman (Rayleigh regime)
    return v, We, Re, Lb

# ---------------- design-space search ----------------
pitches = [5.0, 7.5, 10.0]
diams = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80]
tube_ids = [8.0, 8.4, 10.0]
flows = [1.0, 1.5, 2.0, 3.0, 4.0]
SIG_D = 10e-6                 # hole diameter std-dev (CNC micro-drill / laser)
FILTER = 50e-6
cands = []
for q, p, d, Di in itertools.product(flows, pitches, diams, tube_ids):
    N = int(round(L * 1000 / p))
    Qh = q / 60000 / N
    dp, v = rc.orifice_dp(Qh, d / 1000)
    A_ratio = N * math.pi * (d / 1000) ** 2 / 4 / (math.pi * (Di / 1000) ** 2 / 4)
    V_in = q / 60000 / (math.pi * (Di / 1000) ** 2 / 4)
    KE = rho * V_in ** 2 / 2
    tilt_pct = 50 * rho * g * 0.010 / dp
    vj, We, Rej, Lb = jet(d / 1000, Qh)
    cv_hole = 2 * SIG_D / (d / 1000) * 100
    checks = dict(
        dp_ge_10KE=dp >= 10 * KE,
        area_ratio_le_05=A_ratio <= 0.5,
        tilt_le_2pct=tilt_pct <= 2.0,
        clog_d_ge_6filter=d / 1000 >= 6 * FILTER,
        jet_mode_We_gt_4=We > 4,
        jet_intact_to_glass=Lb > 2 * TRAVEL,
        cv_hole_le_6=cv_hole <= 6.0)
    ok = all(checks.values())
    cands.append(dict(q=q, pitch=p, d=d, ID=Di, N=N, dP_kPa=dp / 1000, KE_ratio=KE / dp, area_ratio=A_ratio,
                      tilt10_pct=tilt_pct, jet_v=vj, We=We, Lb_mm=Lb * 1000, cv_hole_pct=cv_hole, feasible=ok,
                      failed=[k for k, v_ in checks.items() if not v_]))

def score(c):
    # robustness: prefer smaller pitch (merging), larger d (clogging), lower KE ratio & area ratio, fewer holes as tie-break
    return (-c["pitch"], c["d"], -c["KE_ratio"] - c["area_ratio"], -c["N"])
best = {}
for q in flows:
    feas = [c for c in cands if c["q"] == q and c["feasible"]]
    feas.sort(key=score, reverse=True)
    best[q] = feas[0] if feas else None
O["optimum_by_flow"] = best

# detailed verification of the optima with the 1-D manifold model + Monte-Carlo + slot smoothing
H_POOL_MM = None
ver = {}
W_SLOT = 1.0e-3
h_pool = cap_rise(W_SLOT)          # conservative angles (glass 30, fin 60)
h_pool_worst = cap_rise(W_SLOT, 40, 75)
for q, c in best.items():
    if not c: continue
    qn, P0 = rc.manifold_distribution(q, d_hole=c["d"] / 1000, Dm=c["ID"] / 1000, N=c["N"])
    qt, _ = rc.manifold_distribution(q, d_hole=c["d"] / 1000, Dm=c["ID"] / 1000, N=c["N"], tilt_mm=10)
    cvs, rngs = [], []
    for s in range(150):
        qq, _ = rc.manifold_distribution(q, d_hole=c["d"] / 1000, Dm=c["ID"] / 1000, N=c["N"], dd_sigma=SIG_D, seed=s)
        sm = rc.smooth(qq, c["pitch"], h_pool_worst * 1000)
        core = sm[40:-40]; cvs.append(np.std(core)); rngs.append(core.max() - core.min())
    ver[q] = dict(spread_end_feed_pct=float((qn.max() - qn.min()) * 100),
                  spread_with_10mm_tilt_pct=float((qt.max() - qt.min()) * 100),
                  line_CV_pct=float(np.mean(cvs) * 100), line_range_p95_pct=float(np.percentile(rngs, 95) * 100),
                  ripple_pct=float(200 * math.exp(-2 * math.pi * h_pool_worst * 1000 / c["pitch"])))
O["verification"] = ver

# ---------------- slot sizing ----------------
slot = []
for w in (0.6, 0.8, 1.0, 1.2, 1.5, 2.0):
    wm = w / 1000
    slot.append(dict(w_mm=w, h_pool_best_mm=cap_rise(wm, 20, 50) * 1000, h_pool_nominal_mm=cap_rise(wm) * 1000,
                     h_pool_worst_mm=cap_rise(wm, 40, 75) * 1000,
                     full_slot_capacity_lpm_m=rho * g * wm ** 3 / (12 * mu) * 60000,
                     ripple_p5_worst_pct=200 * math.exp(-2 * math.pi * cap_rise(wm, 40, 75) * 1000 / 5),
                     ripple_p10_worst_pct=200 * math.exp(-2 * math.pi * cap_rise(wm, 40, 75) * 1000 / 10)))
O["slot"] = slot

# ---------------- rinse protocol optimisation ----------------
def rinse_time(q, eps):
    _, _, tau = film(q)
    return tau * (1 + math.log(1 / eps))
eps = (SPOT_FREE_TDS - 2.0) / TAP_TDS          # allow 2 ppm from RO permeate
prot = []
for q in (1.0, 1.5, 2.0, 3.0, 4.0):
    t = rinse_time(q, eps)
    prot.append(dict(q=q, tau_s=film(q)[2], t_s=t, volume_L_per_m=q * t / 60,
                     theta_r_max_SF1=theta_max_for(q), theta_r_max_SF13=theta_max_for(q, 1.3),
                     theta_r_max_soapy_sigma035=theta_max_for(q, 1.3, 0.035)))
O["rinse_protocol"] = dict(eps=eps, rows=prot,
                           note="Volume ∝ q^(1/3): lowest flow that keeps the film continuous minimises water.")

# zoning-as-flow-control for a fixed-flow GalClean source
def zone_plan(Q, panels):
    single = [Q / w for w in panels]
    both = Q / sum(panels)
    return dict(Q=Q, panels=panels, pulse_q_each=single, maintain_q_all=both,
                theta_pulse=min(theta_max_for(x, 1.3) for x in single), theta_maintain=theta_max_for(both, 1.3))
O["zone_pulse_examples"] = [zone_plan(2.0, [0.9, 0.9]), zone_plan(4.0, [0.9, 0.9]), zone_plan(4.0, [1.4, 0.9]),
                            zone_plan(4.0, [0.9, 1.4, 0.9])]

# ---------------- other physics checks ----------------
O["checks"] = dict(
    manifold_fill_time_s={f"ID{D}": (math.pi / 4 * (D / 1000) ** 2 * 1.0) / (2 / 60000) for D in (8.0, 8.4, 10.0)},
    bubble_point_hole_Pa={f"d{d}": 4 * sigma / (d / 1000) for d in (0.35, 0.5)},
    thermal_shock_dT_K=25, tempered_glass_dT_resistance_K=200,
    PVDF_expansion_mm_per_m_dT25=120e-6 * 25 * 1000, SS316_expansion_mm_per_m_dT25=16e-6 * 25 * 1000,
    Al_expansion_mm_per_m_dT25=23e-6 * 25 * 1000,
    wedge_force_to_flatten_2mm_bow_N=48 * 70e9 * 0.3 * 0.008 ** 3 / 12 * 0.002 / 1.0 ** 3,
    stagnant_volume_mL_per_m={f"ID{D}": math.pi / 4 * D ** 2 for D in (8.0, 8.4, 10.0)},
    slot_mean_velocity_mm_s=2 / 60000 / 1.0e-3 * 1000,
)
json.dump(O, open(os.path.join(OUT, "optimum.json"), "w"), indent=2, ensure_ascii=False, default=float)

# ---------------- report ----------------
md = ["# v0.3 optimisation results\n", "RO flow factor vs temperature: " + ", ".join(f"{k}: {v}" for k, v in O["ro_flow_factor"].items())]
md.append("\n## Optimum manifold per flow (L/min per m)\n| q | pitch | d | tube ID | N | ΔP kPa | KE/ΔP | area ratio | tilt 10mm % | jet v | We | L_b mm | CV hole % |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for q, c in best.items():
    if c: md.append(f"| {q} | {c['pitch']} | {c['d']} | {c['ID']} | {c['N']} | {c['dP_kPa']:.2f} | {c['KE_ratio']:.3f} | {c['area_ratio']:.2f} | {c['tilt10_pct']:.2f} | {c['jet_v']:.2f} | {c['We']:.1f} | {c['Lb_mm']:.0f} | {c['cv_hole_pct']:.1f} |")
    else: md.append(f"| {q} | no feasible design |")
md.append("\n## Verification (1-D model, MC σd=10µm, slot w=1.0 worst-case wetting)\n| q | spread % | +10mm tilt % | line CV % | line p95 range % | ripple % |\n|---|---|---|---|---|---|")
for q, v in ver.items():
    md.append(f"| {q} | {v['spread_end_feed_pct']:.2f} | {v['spread_with_10mm_tilt_pct']:.2f} | {v['line_CV_pct']:.2f} | {v['line_range_p95_pct']:.1f} | {v['ripple_pct']:.3f} |")
md.append("\n## Slot width\n| w mm | pool best | nominal | worst | capacity L/min/m | ripple p5 % | ripple p10 % |\n|---|---|---|---|---|---|---|")
for s in slot:
    md.append(f"| {s['w_mm']} | {s['h_pool_best_mm']:.1f} | {s['h_pool_nominal_mm']:.1f} | {s['h_pool_worst_mm']:.1f} | {s['full_slot_capacity_lpm_m']:.0f} | {s['ripple_p5_worst_pct']:.3f} | {s['ripple_p10_worst_pct']:.2f} |")
md.append(f"\n## Rinse protocol (ε = {eps:.4f})\n| q | τ s | t s | L per m | θr max SF1 | θr max SF1.3 | θr max SF1.3 soapy σ |\n|---|---|---|---|---|---|---|")
for r in prot:
    md.append(f"| {r['q']} | {r['tau_s']:.1f} | {r['t_s']:.0f} | {r['volume_L_per_m']:.2f} | {r['theta_r_max_SF1']:.1f} | {r['theta_r_max_SF13']:.1f} | {r['theta_r_max_soapy_sigma035']:.1f} |")
md.append("\n## Zone-pulse examples\n" + "\n".join(f"- Q={z['Q']} panels={z['panels']}: pulse q={[round(x,2) for x in z['pulse_q_each']]} (θr≤{z['theta_pulse']:.0f}°), maintain all q={z['maintain_q_all']:.2f} (θr≤{z['theta_maintain']:.0f}°)" for z in O["zone_pulse_examples"]))
md.append("\n## Other checks\n```\n" + json.dumps(O["checks"], indent=1, default=float) + "\n```")
open(os.path.join(OUT, "optimum.md"), "w").write("\n".join(md))
print("\n".join(md))
