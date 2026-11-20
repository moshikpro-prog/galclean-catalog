"""Builds STEP + STL for the recommended rail (concept C). Run: python3 build_cad.py"""
import os, math
import cadquery as cq
from geometry import *

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)
W_GLASS = 1000.0
CAP_T = 5.0
LB = W_GLASS - 2 * CAP_T          # body / cover length 990

def prism(poly, length, y0=0.0):
    """Extrude an (x,z) polygon along +y from y0."""
    wp = cq.Workplane(cq.Plane(origin=(0, y0, 0), xDir=(1, 0, 0), normal=(0, 1, 0)))
    # in this plane local (u,v) = (x, -z)?? -> compute: zDir=normal=(0,1,0), xDir=(1,0,0) -> yDir = z x x = (0,0,-1)
    pts = [(x, -z) for x, z in poly]
    return wp.polyline(pts).close().extrude(length)

def tube(length, y0=0.0, holes=None):
    pl = cq.Plane(origin=(TUBE_C[0], y0, TUBE_C[1]), xDir=(1, 0, 0), normal=(0, 1, 0))
    t = cq.Workplane(pl).circle(TUBE_OD / 2).circle(TUBE_ID / 2).extrude(length)
    if holes:
        cutters = None
        for y in holes:
            c = (cq.Workplane(cq.Plane(origin=(TUBE_C[0], y, TUBE_C[1]), xDir=(0, 1, 0), normal=(-1, 0, 0)))
                 .circle(HOLE_D / 2).extrude(TUBE_OD / 2 + 0.5))
            cutters = c if cutters is None else cutters.union(c)
        t = t.cut(cutters)
    return t

def end_cap(inlet=True):
    """Moulded end cap (ASA / PA12), 5 mm plate + locating plug into tube chamber."""
    plate = prism(CAP_OUTLINE, CAP_T, 0)
    plug_poly = [(2.7, -10.3), (15.8, -10.3), (15.8, -1.3), (2.7, -1.3)]
    plug = prism(plug_poly, 8, CAP_T)
    hole_len = CAP_T + 8 + 1
    bore = (cq.Workplane(cq.Plane(origin=(TUBE_C[0], -0.5, TUBE_C[1]), xDir=(1, 0, 0), normal=(0, 1, 0)))
            .circle(TUBE_OD / 2 + 0.1).extrude(hole_len))
    cap = plate.union(plug)
    if inlet:
        cap = cap.cut(bore)
    else:  # blind: tube seats 6 mm into plug, end face closed (plug = sealed with push-in stopper)
        blind = (cq.Workplane(cq.Plane(origin=(TUBE_C[0], CAP_T + 2, TUBE_C[1]), xDir=(1, 0, 0), normal=(0, 1, 0)))
                 .circle(TUBE_OD / 2 + 0.1).extrude(7))
        cap = cap.cut(blind)
    return cap

def export(shape, name, stl=True, step=True):
    if step: cq.exporters.export(shape, os.path.join(OUT, name + ".step"))
    if stl: cq.exporters.export(shape, os.path.join(OUT, name + ".stl"), tolerance=0.02, angularTolerance=0.1)
    print("exported", name)

if __name__ == "__main__":
    holes = [CAP_T + y for y in hole_positions(LB)]
    body = prism(BODY, LB, CAP_T)
    cover = prism(COVER, LB, CAP_T)
    tube_y0, tube_y1 = -20.0, W_GLASS - CAP_T + 6
    man = tube(tube_y1 - tube_y0, tube_y0, holes)
    cap_in = end_cap(True)
    cap_bl = end_cap(False).mirror("XZ").translate((0, W_GLASS, 0))
    land = prism(LAND_GASKET, LB, CAP_T)
    block = prism(SETTING_BLOCK, LB, CAP_T)
    wedge = prism(WEDGE, LB, CAP_T)
    glass = prism([(-T_GLASS, -2000), (0, -2000), (0, 0), (-T_GLASS, 0)], W_GLASS, 0)

    # --- individual production parts (1 m) ---
    export(body, "rail_body_990_6063T6", stl=False)
    export(cover, "rail_cover_990", stl=False)
    export(man, "manifold_tube_PVDF_10x1_198x0.35", stl=False)
    export(cap_in, "end_cap_inlet")
    export(end_cap(False), "end_cap_blind")

    # --- assembly (1 m rail on 1000 x 2000 x 8 glass) ---
    asm = cq.Assembly(name="shower_rinse_rail_1000")
    asm.add(glass, name="glass_8mm", color=cq.Color(0.75, 0.88, 0.92, 0.35))
    asm.add(body, name="body", color=cq.Color(0.78, 0.79, 0.80))
    asm.add(cover, name="cover", color=cq.Color(0.70, 0.71, 0.72))
    asm.add(man, name="manifold", color=cq.Color(0.55, 0.56, 0.58))
    asm.add(cap_in, name="cap_inlet", color=cq.Color(0.2, 0.2, 0.22))
    asm.add(cap_bl, name="cap_blind", color=cq.Color(0.2, 0.2, 0.22))
    asm.add(land, name="land_gasket", color=cq.Color(0.1, 0.1, 0.1))
    asm.add(block, name="setting_block", color=cq.Color(0.1, 0.1, 0.1))
    asm.add(wedge, name="wedge_gasket", color=cq.Color(0.1, 0.1, 0.1))
    asm.save(os.path.join(OUT, "assembly_rail_1000_on_glass.step"))
    print("exported assembly")

    # --- printable prototype parts ---
    SEG = LB / 4                               # 247.5 mm -> fits 256 mm beds
    export(prism(BODY, SEG, 0), "PRINT_body_segment_247.5_x4", step=False)
    export(prism(COVER, SEG, 0), "PRINT_cover_segment_247.5_x4_SLA_recommended", step=False)
    export(prism(WEDGE, SEG, 0), "PRINT_wedge_gasket_TPU95A_247.5_x4", step=False)
    # 300 mm hydraulic test section (3 cover variants: slot 0.8 / 1.2 / 1.6 mm)
    export(prism(BODY, 300, 0), "TEST300_body", step=True)
    for s in (0.8, 1.0, 1.2):
        dx = s - 1.0
        cv = [(x + dx if x < 3.0 else x, z) for x, z in COVER]
        export(prism(cv, 300, 0), f"TEST300_cover_slot_{s:.1f}mm", step=True)
    export(tube(330, -20, hole_positions(300.0)), "TEST300_tube_A_p5_d0.35", stl=False)
    export(tube(330, -20, hole_positions(300.0, 10.0)), "TEST300_tube_B_p10_d0.35_reference", stl=False)
    print("done")
