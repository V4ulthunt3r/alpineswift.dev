"""Build custom SF Symbols (template v4.0) for Alpine Swift and its tools.

    python3 -I scripts/generate_sf_symbol.py [outDir]

For every symbol, writes <name>.svg (for the SF Symbols app) and
<name>.symbolset (for an Xcode asset catalog) to outDir (default brand/sf-symbol).

  alpineswift  the studio mark: swift above a peak with its glacier facet
  scout        code quality: a scouting swift gliding over a snow-capped peak
  beacon       ASO: a lighthouse on a peak, sending two beams
  trail        project management: a dashed trail up a peak to the summit flag

The marks are logos, so their shape stays the same in every weight (like
Apple's own apple.logo). Ultralight-S, Regular-S and Black-S share one
outline, which keeps the templates valid and interpolable.

Every symbol has two layers, so hierarchical and palette rendering show the
brand's two tones (navy and cyan):
  layer 0 (primary)    mountain, swift, lighthouse, flagpole
  layer 1 (secondary)  the cyan parts: facets, snow caps, beams, lamp, flag
Small gaps between touching parts keep the cyan details readable in monochrome.
Holes (the trail's dashes, the lantern) are subpaths wound the other way.
"""
import math
import os
import re
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "brand/sf-symbol"

# ---------- path helpers (absolute M/L/C/Z only) ----------

num = re.compile(r"-?\d+(?:\.\d+)?")


def f(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def poly(pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + " Z"


def area(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
               for i in range(len(pts))) / 2


def wound(pts, clockwise):
    """Polygon points in the requested winding (on screen, y down)."""
    return pts if (area(pts) > 0) == clockwise else pts[::-1]


def circle(cx, cy, r, clockwise=True):
    k = 0.5523 * r
    if clockwise:
        return (f"M{f(cx)} {f(cy - r)} C{f(cx + k)} {f(cy - r)} {f(cx + r)} {f(cy - k)} {f(cx + r)} {f(cy)} "
                f"C{f(cx + r)} {f(cy + k)} {f(cx + k)} {f(cy + r)} {f(cx)} {f(cy + r)} "
                f"C{f(cx - k)} {f(cy + r)} {f(cx - r)} {f(cy + k)} {f(cx - r)} {f(cy)} "
                f"C{f(cx - r)} {f(cy - k)} {f(cx - k)} {f(cy - r)} {f(cx)} {f(cy - r)} Z")
    return (f"M{f(cx)} {f(cy - r)} C{f(cx - k)} {f(cy - r)} {f(cx - r)} {f(cy - k)} {f(cx - r)} {f(cy)} "
            f"C{f(cx - r)} {f(cy + k)} {f(cx - k)} {f(cy + r)} {f(cx)} {f(cy + r)} "
            f"C{f(cx + k)} {f(cy + r)} {f(cx + r)} {f(cy + k)} {f(cx + r)} {f(cy)} "
            f"C{f(cx + r)} {f(cy - k)} {f(cx + k)} {f(cy - r)} {f(cx)} {f(cy - r)} Z")


def inside(pt, pts):
    x, y = pt
    hit = False
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            hit = not hit
    return hit


def on_line(p, q, y):
    """x where the line p-q crosses height y."""
    return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])


# ---------- alpineswift: the studio mark (1254 px frame of the original draft) ----------

def alpineswift():
    mountain = "M88 1095 L617 621 L1068 1050 L665 740 L567 925 L509 862 Z"
    # the swift with the lower-wing facet cut out, so the two layers never overlap
    swift = ("M647 118 C700 225 820 350 975 402 C1000 390 1030 376 1058 377 "
             "C1074 378 1084 386 1088 393 L1106 401 C1082 403 1061 412 1047 429 "
             "C1040 440 1036 452 1035 461 C1100 540 1150 680 1135 812 "
             "C1116 664 1062 562 988 503 L945 515 C870 545 800 585 737 628 L823 533 L678 546 "
             "C740 530 800 510 850 487 L875 463 C760 380 660 255 647 118 Z")
    wing = "M1135 812 C1115 690 1050 582 945 515 L988 503 C1062 562 1116 664 1135 812 Z"
    # glacier facet A-B-C shares A-B with the ridge; pull that edge back by a gap
    A, B, C, gap = (665, 740), (1068, 1050), (722, 900), 26
    ab = (B[0] - A[0], B[1] - A[1])
    n = (-ab[1] / math.hypot(*ab), ab[0] / math.hypot(*ab))
    if (C[0] - A[0]) * n[0] + (C[1] - A[1]) * n[1] < 0:
        n = (-n[0], -n[1])
    t = gap / ((C[0] - A[0]) * n[0] + (C[1] - A[1]) * n[1])
    facet = poly([(A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t),
                  (B[0] + (C[0] - B[0]) * t, B[1] + (C[1] - B[1]) * t), C])
    return [(0, mountain), (0, swift), (1, facet), (1, wing)]


# ---------- shared: a peak with a snow cap (Scout and Trail) ----------

def capped_peak(base_left, apex, base_right, snow, gap, extra_left=(), extra_right=()):
    """Mountain polygon plus a snow cap. `snow` is the cap's jagged lower edge
    from the left slope to the right slope; the rock starts `gap` below it."""
    left_slope_pt, right_slope_pt = extra_left[-1] if extra_left else base_left, extra_right[0] if extra_right else base_right
    cap = [apex] + [(on_line(apex, left_slope_pt, snow[0][1]), snow[0][1])] + snow[1:-1] + \
          [(on_line(apex, right_slope_pt, snow[-1][1]), snow[-1][1])]
    rock_top = [(on_line(apex, left_slope_pt, snow[0][1] + gap), snow[0][1] + gap)] + \
               [(x, y + gap) for x, y in snow[1:-1]] + \
               [(on_line(apex, right_slope_pt, snow[-1][1] + gap), snow[-1][1] + gap)]
    rock = [base_left, *extra_left, *rock_top, *extra_right, base_right]
    return rock, cap


# ---------- scout (600 px frame, traced from the app icon) ----------

def scout():
    # forked-tail swift gliding in from the upper left, as on the Scout icon
    swift = ("M95 63 C200 58 310 100 365 185 C380 176 400 174 413 182 L432 195 L408 199 "
             "C432 250 440 330 421 392 C408 330 380 282 328 252 L146 318 L262 252 L133 270 "
             "L278 226 C300 214 300 200 288 188 C240 120 160 78 95 63 Z")
    rock, cap = capped_peak((120, 560), (345, 372), (570, 560),
                            snow=[(0, 428), (320, 418), (332, 436), (356, 412), (0, 428)], gap=12)
    return [(0, swift), (0, poly(rock)), (1, poly(cap))]


# ---------- beacon (600 px frame) ----------

def beacon():
    peak = poly([(120, 560), (300, 372), (480, 560)])
    roof = poly([(300, 236), (346, 268), (254, 268)])
    pillars = poly([(266, 276), (281, 276), (281, 318), (266, 318)]) + " " + \
              poly([(319, 276), (334, 276), (334, 318), (319, 318)])
    gallery = poly([(256, 325), (344, 325), (334, 339), (266, 339)])
    tower = poly([(274, 346), (326, 346), (338, 402), (262, 402)])
    lamp = circle(300, 297, 12)
    # beams start a gap away from the lantern, so they stay separate in monochrome
    beam_l = poly([(252, 297), (40, 190), (40, 278)])
    beam_r = poly([(348, 297), (560, 190), (560, 278)])
    return [(0, peak), (0, tower), (0, gallery), (0, pillars), (0, roof),
            (1, lamp), (1, beam_l), (1, beam_r)]


# ---------- trail (1024 px frame, same scene as the Trail app icon) ----------

def trail():
    rock, cap = capped_peak((40, 900), (512, 400), (990, 900),
                            snow=[(0, 520), (486, 485), (498, 515), (545, 468), (0, 490)], gap=20,
                            extra_left=[(150, 830), (190, 850)], extra_right=[(840, 720), (880, 700), (990, 772)])
    # the trail: dashes cut out of the rock along a serpentine path
    route = [(470, 880), (300, 828), (680, 736), (440, 640), (560, 572)]
    dash, space, width = 58, 34, 30
    holes = []
    for (x1, y1), (x2, y2) in zip(route, route[1:]):
        seg = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / seg, (y2 - y1) / seg
        nx, ny = -uy * width / 2, ux * width / 2
        s = (seg - dash) % (dash + space) / 2  # centre the pattern on the segment
        while s + dash <= seg + 1e-6:
            a = (x1 + ux * s, y1 + uy * s)
            b = (x1 + ux * (s + dash), y1 + uy * (s + dash))
            rect = [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]
            # keep only dashes that sit fully inside the rock, with a margin
            grown = [(p[0] + (p[0] - (a[0] + b[0]) / 2) * .25, p[1] + (p[1] - (a[1] + b[1]) / 2) * .25) for p in rect]
            if all(inside(p, rock) for p in grown):
                holes.append(rect)
            s += dash + space
    rock_cw = area(rock) > 0
    rock_d = poly(rock) + " " + " ".join(poly(wound(h, not rock_cw)) for h in holes)
    pole = poly([(505, 262), (519, 262), (519, 402), (505, 402)])
    flag = "M527 266 C560 274 588 284 620 294 C588 304 560 314 527 324 Z"
    return [(0, rock_d), (0, pole), (1, poly(cap)), (1, flag)]


SYMBOLS = {"alpineswift": alpineswift(), "scout": scout(), "beacon": beacon(), "trail": trail()}

# ---------- template ----------

BASELINE = 696
CAP_HEIGHT = 70.459
GLYPH_HEIGHT = 88  # pictorial marks: taller than a capital, like mountain.2 or bird
MARGIN = 3
COLUMNS = {"Ultralight-S": 559.711, "Regular-S": 1449.84, "Black-S": 2933.4}

CLASSES = {
    0: "monochrome-0 multicolor-0:tintColor hierarchical-0:primary SFSymbolsPreviewWireframe",
    1: "monochrome-1 multicolor-1:systemMintColor hierarchical-1:secondary SFSymbolsPreviewWireframe",
}
STYLE = """.monochrome-0 {fill:#000000}
.monochrome-1 {fill:#000000}

.multicolor-0:tintColor {fill:#007AFF}
.multicolor-1:systemMintColor {fill:#00C7BE}

.hierarchical-0:primary {fill:#212121}
.hierarchical-1:secondary {fill:#8C8C8C}

.SFSymbolsPreviewWireframe {fill:none;opacity:1.0;stroke:black;stroke-width:0.5}
"""


def pairs(args):
    v = [float(x) for x in num.findall(args)]
    return list(zip(v[0::2], v[1::2]))


def outline_points(d):
    """Anchors plus samples along each cubic, for a tight bounding box."""
    pts, cur = [], None
    for cmd, args in re.findall(r"([MLCZ])([^MLCZ]*)", d):
        p = pairs(args)
        if cmd in "ML":
            cur = p[0]; pts.append(cur)
        elif cmd == "C":
            p0, (c1, c2, p3) = cur, p
            for i in range(1, 33):
                t = i / 32; u = 1 - t
                pts.append((u**3 * p0[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3 * p3[0],
                            u**3 * p0[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3 * p3[1]))
            cur = p3
    return pts


def template(name, layers):
    allpts = [p for _, d in layers for p in outline_points(d)]
    minx, maxx = min(p[0] for p in allpts), max(p[0] for p in allpts)
    miny, maxy = min(p[1] for p in allpts), max(p[1] for p in allpts)
    scale = GLYPH_HEIGHT / (maxy - miny)
    width = (maxx - minx) * scale
    top = -(CAP_HEIGHT + GLYPH_HEIGHT) / 2  # centre the glyph on the cap height

    def place(d):
        return "".join(cmd + " ".join(f"{f(MARGIN + (x - minx) * scale)} {f(top + (y - miny) * scale)}"
                                      for x, y in pairs(args))
                       for cmd, args in re.findall(r"([MLCZ])([^MLCZ]*)", d))

    glyph = "\n".join(f'   <path class="{CLASSES[l]}" d="{place(d)}"/>' for l, d in layers)
    notes = "\n".join(
        f'  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:middle;" transform="matrix(1 0 0 1 {x} 322)">{label}</text>'
        for label, x in [("Ultralight", 559.711), ("Thin", 856.422), ("Light", 1153.13), ("Regular", 1449.84),
                         ("Medium", 1746.56), ("Semibold", 2043.27), ("Bold", 2339.98), ("Heavy", 2636.69),
                         ("Black", 2933.4)])

    def guide(id_, x1, x2, y1, y2, color="#27AAE1"):
        return (f'  <line id="{id_}" style="fill:none;stroke:{color};opacity:1;stroke-width:0.5;" '
                f'x1="{f(x1)}" x2="{f(x2)}" y1="{f(y1)}" y2="{f(y2)}"/>')

    guides, symbols = [], []
    for s, dy in (("S", 0), ("M", 430), ("L", 860)):
        guides.append(guide(f"Baseline-{s}", 263, 3036, BASELINE + dy, BASELINE + dy))
        guides.append(guide(f"Capline-{s}", 263, 3036, BASELINE + dy - CAP_HEIGHT, BASELINE + dy - CAP_HEIGHT))
    for wid, col in COLUMNS.items():
        left = col - (width + 2 * MARGIN) / 2
        right = left + width + 2 * MARGIN
        guides.append(guide(f"left-margin-{wid}", left, left, 600.785, 720.121, "#00AEEF"))
        guides.append(guide(f"right-margin-{wid}", right, right, 600.785, 720.121, "#00AEEF"))
        symbols.append(f'  <g id="{wid}" transform="matrix(1 0 0 1 {f(left)} {BASELINE})">\n{glyph}\n  </g>')
    symbols.reverse()
    nl = "\n"
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg
PUBLIC "-//W3C//DTD SVG 1.1//EN"
       "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="3300" height="2200">
 <!--glyph: "", point size: 100.0, template writer version: "101"-->
 <style>{STYLE}</style>
 <g id="Notes">
  <rect height="2200" id="artboard" style="fill:white;opacity:1" width="3300" x="0" y="0"/>
  <line style="fill:none;stroke:black;opacity:1;stroke-width:0.5;" x1="263" x2="3036" y1="292" y2="292"/>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;font-weight:bold;" transform="matrix(1 0 0 1 263 322)">Weight/Scale Variations</text>
{notes}
  <line style="fill:none;stroke:black;opacity:1;stroke-width:0.5;" x1="263" x2="3036" y1="1903" y2="1903"/>
  <text id="template-version" style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:end;" transform="matrix(1 0 0 1 3036 1933)">Template v.4.0</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:end;" transform="matrix(1 0 0 1 3036 1951)">Requires Xcode 14 or greater</text>
  <text id="descriptive-name" style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:end;" transform="matrix(1 0 0 1 3036 1969)">{name}</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:end;" transform="matrix(1 0 0 1 3036 1987)">Typeset at 100 points</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;" transform="matrix(1 0 0 1 263 726)">Small</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;" transform="matrix(1 0 0 1 263 1156)">Medium</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;" transform="matrix(1 0 0 1 263 1586)">Large</text>
 </g>
 <g id="Guides">
{nl.join(guides)}
 </g>
 <g id="Symbols">
{nl.join(symbols)}
 </g>
</svg>
"""
    return svg, width


for name, layers in SYMBOLS.items():
    svg, width = template(name, layers)
    symbolset = os.path.join(OUT, f"{name}.symbolset")
    os.makedirs(symbolset, exist_ok=True)
    for path in (os.path.join(OUT, f"{name}.svg"), os.path.join(symbolset, f"{name}.svg")):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
    with open(os.path.join(symbolset, "Contents.json"), "w", encoding="utf-8") as fh:
        fh.write('{\n  "info" : {\n    "author" : "xcode",\n    "version" : 1\n  },\n  "symbols" : [\n'
                 f'    {{\n      "filename" : "{name}.svg",\n      "idiom" : "universal"\n    }}\n  ]\n}}\n')
    print(f"{name}: {f(width)} x {GLYPH_HEIGHT} pt at 100 pt")
