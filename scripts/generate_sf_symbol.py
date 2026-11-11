"""Build a custom SF Symbol (template v4.0) from the Alpine Swift mark.

    python3 -I scripts/generate_sf_symbol.py [outDir]

Output (default brand/sf-symbol/): alpineswift.svg for the SF Symbols app and
alpineswift.symbolset for an Xcode asset catalog.

The mark is a logo, so its shape stays the same in every weight (like Apple's
own apple.logo). Ultralight-S, Regular-S and Black-S therefore share one
outline, which keeps the template valid and interpolable.

Two layers, so hierarchical and palette rendering show the logo's two tones:
  layer 0 (primary)   mountain and swift
  layer 1 (secondary) glacier facet and lower-wing facet
In monochrome a small gap keeps the glacier facet readable; the wing facet sits
inside the swift's wing and simply merges with it.
"""
import os
import re
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "brand/sf-symbol"
NAME = "alpineswift"

# Logo geometry in the 1254 px frame of the original draft (same as the site).
MOUNTAIN = "M88 1095 L617 621 L1068 1050 L665 740 L567 925 L509 862 Z"
# The swift with the lower-wing facet cut out, so the two layers never overlap.
SWIFT = ("M647 118 C700 225 820 350 975 402 C1000 390 1030 376 1058 377 "
         "C1074 378 1084 386 1088 393 L1106 401 C1082 403 1061 412 1047 429 "
         "C1040 440 1036 452 1035 461 C1100 540 1150 680 1135 812 "
         "C1116 664 1062 562 988 503 L945 515 C870 545 800 585 737 628 L823 533 L678 546 "
         "C740 530 800 510 850 487 L875 463 C760 380 660 255 647 118 Z")
WING = "M1135 812 C1115 690 1050 582 945 515 L988 503 C1062 562 1116 664 1135 812 Z"

# Glacier facet: the triangle A-B-C shares the edge A-B with the mountain's
# ridge. Its A-B edge is pulled back by GAP so it reads as its own face.
A, B, C = (665, 740), (1068, 1050), (722, 900)
GAP = float(os.environ.get("SF_GAP", 26))  # in logo units (~2 pt at 100 pt)


def facet():
    if GAP <= 0:
        return f"M{A[0]} {A[1]} L{B[0]} {B[1]} L{C[0]} {C[1]} Z"
    ab = (B[0] - A[0], B[1] - A[1])
    ln = (ab[0] ** 2 + ab[1] ** 2) ** .5
    n = (-ab[1] / ln, ab[0] / ln)  # unit normal of A-B
    if (C[0] - A[0]) * n[0] + (C[1] - A[1]) * n[1] < 0:
        n = (-n[0], -n[1])  # point it towards C
    h = (C[0] - A[0]) * n[0] + (C[1] - A[1]) * n[1]  # height of C above A-B
    t = GAP / h  # slide A and B towards C by this fraction
    a2 = (A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t)
    b2 = (B[0] + (C[0] - B[0]) * t, B[1] + (C[1] - B[1]) * t)
    return f"M{a2[0]:.3f} {a2[1]:.3f} L{b2[0]:.3f} {b2[1]:.3f} L{C[0]} {C[1]} Z"


LAYERS = [  # (layer index, path) in paint order
    (0, MOUNTAIN), (0, SWIFT), (1, facet()), (1, WING),
]

# Template metrics at 100 pt, small scale (as exported by the SF Symbols app).
BASELINE = 696
CAP_HEIGHT = 70.459
GLYPH_HEIGHT = 88  # a pictorial mark: taller than a capital, like mountain.2 or bird
MARGIN = 3
COLUMNS = {"Ultralight-S": 559.711, "Regular-S": 1449.84, "Black-S": 2933.4}

num = re.compile(r"-?\d+(?:\.\d+)?")


def pairs(d):
    v = [float(x) for x in num.findall(d)]
    return list(zip(v[0::2], v[1::2]))


def cubic_extrema(d):
    """All anchor points plus samples along each cubic, for a tight bounding box."""
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


allpts = [p for _, d in LAYERS for p in cubic_extrema(d)]
minx, maxx = min(p[0] for p in allpts), max(p[0] for p in allpts)
miny, maxy = min(p[1] for p in allpts), max(p[1] for p in allpts)
scale = GLYPH_HEIGHT / (maxy - miny)
width = (maxx - minx) * scale
top = -(CAP_HEIGHT + GLYPH_HEIGHT) / 2  # centre the glyph on the cap height


def fmt(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def place(d):
    """Map logo coordinates to the symbol's local frame (x from the left margin, y up from baseline)."""
    out = []
    for cmd, args in re.findall(r"([MLCZ])([^MLCZ]*)", d):
        coords = " ".join(f"{fmt(MARGIN + (x - minx) * scale)} {fmt(top + (y - miny) * scale)}" for x, y in pairs(args))
        out.append(cmd + coords)
    return "".join(out)


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

placed = [(layer, place(d)) for layer, d in LAYERS]
glyph = "\n".join(f'   <path class="{CLASSES[l]}" d="{d}"/>' for l, d in placed)

notes = "\n".join(
    f'  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:middle;" transform="matrix(1 0 0 1 {x} 322)">{label}</text>'
    for label, x in [("Ultralight", 559.711), ("Thin", 856.422), ("Light", 1153.13), ("Regular", 1449.84),
                     ("Medium", 1746.56), ("Semibold", 2043.27), ("Bold", 2339.98), ("Heavy", 2636.69),
                     ("Black", 2933.4)])


def guide(id_, x1, x2, y1, y2, color="#27AAE1"):
    return (f'  <line id="{id_}" style="fill:none;stroke:{color};opacity:1;stroke-width:0.5;" '
            f'x1="{fmt(x1)}" x2="{fmt(x2)}" y1="{fmt(y1)}" y2="{fmt(y2)}"/>')


guides = []
for s, dy in (("S", 0), ("M", 430), ("L", 860)):
    guides.append(guide(f"Baseline-{s}", 263, 3036, BASELINE + dy, BASELINE + dy))
    guides.append(guide(f"Capline-{s}", 263, 3036, BASELINE + dy - CAP_HEIGHT, BASELINE + dy - CAP_HEIGHT))
symbols = []
for wid, col in COLUMNS.items():
    left = col - (width + 2 * MARGIN) / 2
    right = left + width + 2 * MARGIN
    guides.append(guide(f"left-margin-{wid}", left, left, 600.785, 720.121, "#00AEEF"))
    guides.append(guide(f"right-margin-{wid}", right, right, 600.785, 720.121, "#00AEEF"))
    symbols.append(f'  <g id="{wid}" transform="matrix(1 0 0 1 {fmt(left)} {BASELINE})">\n{glyph}\n  </g>')
symbols.reverse()

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
  <text id="descriptive-name" style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:end;" transform="matrix(1 0 0 1 3036 1969)">{NAME}</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;text-anchor:end;" transform="matrix(1 0 0 1 3036 1987)">Typeset at 100 points</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;" transform="matrix(1 0 0 1 263 726)">Small</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;" transform="matrix(1 0 0 1 263 1156)">Medium</text>
  <text style="stroke:none;fill:black;font-family:sans-serif;font-size:13;" transform="matrix(1 0 0 1 263 1586)">Large</text>
 </g>
 <g id="Guides">
{chr(10).join(guides)}
 </g>
 <g id="Symbols">
{chr(10).join(symbols)}
 </g>
</svg>
"""

symbolset = os.path.join(OUT, f"{NAME}.symbolset")
os.makedirs(symbolset, exist_ok=True)
for path in (os.path.join(OUT, f"{NAME}.svg"), os.path.join(symbolset, f"{NAME}.svg")):
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
with open(os.path.join(symbolset, "Contents.json"), "w", encoding="utf-8") as f:
    f.write('{\n  "info" : {\n    "author" : "xcode",\n    "version" : 1\n  },\n  "symbols" : [\n'
            f'    {{\n      "filename" : "{NAME}.svg",\n      "idiom" : "universal"\n    }}\n  ]\n}}\n')
print(f"glyph {fmt(width)} x {GLYPH_HEIGHT} pt at 100 pt, gap {GAP}; wrote {OUT}/{NAME}.svg and {symbolset}")
