#!/usr/bin/env python3
"""Generate the editable 1200 × 630 social-card composition using existing branding.

Run from the repository root: python3 scripts/generate_social_card.py
Open /brand/social-card.html at a 1200 × 630 browser viewport, wait for fonts,
then save a viewport JPEG to assets/img/social/alpine-swift-v1.jpg.
The generated HTML is a design source, not the image referenced by social tags.
"""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parent.parent
WIDTH, HEIGHT, STEP = 1200, 630, 8


def hash_value(x, y):
    # Same seeded terrain noise as the homepage; JavaScript's 32-bit arithmetic.
    h = ((x * 374761393) + (y * 668265263)) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h ^ (h >> 16)) / 4294967296


def noise(x, y):
    xi, yi = math.floor(x), math.floor(y)
    xf, yf = x - xi, y - yi
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    a, b = hash_value(xi, yi), hash_value(xi + 1, yi)
    c, d = hash_value(xi, yi + 1), hash_value(xi + 1, yi + 1)
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v


def terrain(u, v):
    aspect = WIDTH / HEIGHT
    px, py = (u - .78) * aspect, v - .46
    return (
        .92 * math.exp(-(px * px * 1.3 + py * py) / .06)
        + .5 * math.exp(-((px + .42) ** 2 + (py - .12) ** 2) / .045)
        + .38 * math.exp(-((px - .3) ** 2 + (py + .2) ** 2) / .03)
        + .24 * math.exp(-((px + .95) ** 2 + (py + .22) ** 2) / .08)
        + .16 * noise(u * 4 * aspect, v * 4)
        + .07 * noise(u * 10 * aspect, v * 10)
        + .09 * (1 - abs(noise(u * 7 * aspect, v * 7) * 2 - 1))
        * math.exp(-(px * px + py * py) / .15)
    )


# Marching squares, using the same edge table as assets/js/site.js.
SEG = [[], [3, 2], [2, 1], [3, 1], [0, 1], [3, 0, 2, 1], [0, 2],
       [3, 0], [3, 0], [0, 2], [3, 1, 0, 2], [0, 1], [3, 1],
       [2, 1], [3, 2], []]
cols, rows = math.ceil(WIDTH / STEP) + 1, math.ceil(HEIGHT / STEP) + 1
field = [[terrain(x * STEP / WIDTH, y * STEP / HEIGHT)
          for x in range(cols)] for y in range(rows)]
paths = []
for level in range(1, 25):
    threshold = level * .05
    segments = []
    for y in range(rows - 1):
        for x in range(cols - 1):
            a, b = field[y][x], field[y][x + 1]
            c, d = field[y + 1][x + 1], field[y + 1][x]
            case = ((a > threshold) * 8 + (b > threshold) * 4
                    + (c > threshold) * 2 + (d > threshold))
            edges = SEG[case]
            if not edges:
                continue
            x0, y0 = x * STEP, y * STEP

            def edge(e):
                if e == 0:
                    return x0 + STEP * (threshold - a) / (b - a), y0
                if e == 1:
                    return x0 + STEP, y0 + STEP * (threshold - b) / (c - b)
                if e == 2:
                    return x0 + STEP * (threshold - d) / (c - d), y0 + STEP
                return x0, y0 + STEP * (threshold - a) / (d - a)

            for i in range(0, len(edges), 2):
                p, q = edge(edges[i]), edge(edges[i + 1])
                segments.append(f'M{p[0]:.1f},{p[1]:.1f}L{q[0]:.1f},{q[1]:.1f}')
    color = '#14F0DC' if threshold > .76 else '#AA8CFF'
    opacity = '.55' if level % 5 == 0 else '.25'
    stroke = '1.8' if level % 5 == 0 else '1'
    paths.append(f'<path d="{"".join(segments)}" stroke="{color}" '
                 f'stroke-opacity="{opacity}" stroke-width="{stroke}"/>')

html = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1200">
<meta name="robots" content="noindex">
<title>Alpine Swift · Social card source</title>
<style>
@font-face { font-family: Archivo; src: url('/assets/fonts/archivo-var.woff2'); font-weight: 400 900; font-stretch: 62% 125%; }
@font-face { font-family: Onest; src: url('/assets/fonts/onest-var.woff2'); font-weight: 400 700; }
@font-face { font-family: Mono; src: url('/assets/fonts/spline-sans-mono-var.woff2'); font-weight: 400 600; }
* { box-sizing: border-box; }
html, body { margin: 0; width: 1200px; height: 630px; overflow: hidden; }
body { background: #0A0420; color: #EEEAFB; -webkit-font-smoothing: antialiased; }
main { position: relative; width: 1200px; height: 630px; isolation: isolate; }
.terrain { position: absolute; inset: 0; z-index: -2; }
.shade { position: absolute; inset: 0; z-index: -1; background: linear-gradient(90deg, #0A0420 0%, rgba(10,4,32,.95) 30%, rgba(10,4,32,.65) 58%, rgba(10,4,32,.08) 100%); }
.brand { position: absolute; top: 60px; left: 64px; font: 850 29px Archivo, sans-serif; font-stretch: 125%; letter-spacing: .015em; text-transform: uppercase; }
.brand em { color: #14F0DC; font-style: normal; }
h1 { position: absolute; left: 64px; top: 183px; margin: 0; font: 830 64px/.99 Archivo, sans-serif; font-stretch: 115%; letter-spacing: -.025em; }
h1 em { color: #14F0DC; font-style: normal; }
.platforms { position: absolute; left: 67px; top: 368px; margin: 0; font: 400 25px Onest, sans-serif; color: #C1B9DD; }
.mark { position: absolute; width: 270px; height: 252px; object-fit: contain; right: 65px; top: 178px; }
footer { position: absolute; left: 64px; right: 64px; bottom: 52px; display: flex; justify-content: space-between; align-items: end; padding-top: 22px; border-top: 1px solid rgba(238,234,251,.2); }
.domain { font: 500 19px Mono, monospace; color: #EEEAFB; }
.signature { font: 400 18px Onest, sans-serif; color: #C1B9DD; }
</style>
</head>
<body>
<main aria-label="Alpine Swift: Native apps. Alpine precision.">
<svg class="terrain" width="1200" height="630" viewBox="0 0 1200 630" fill="none" aria-hidden="true">
__CONTOURS__
</svg>
<div class="shade"></div>
<div class="brand">Alpine <em>Swift</em></div>
<h1>Native apps.<br><em>Alpine</em> precision.</h1>
<p class="platforms">iPhone · iPad · Mac</p>
<img class="mark" src="/brand/alpine-swift-mark-white.svg" width="270" height="252" alt="Alpine Swift’s bird and mountain logo">
<footer><span class="domain">alpineswift.dev</span><span class="signature">Independent app studio · Peter Hildel</span></footer>
</main>
</body>
</html>
'''.replace('__CONTOURS__', '\n'.join(paths))
output = ROOT / 'brand' / 'social-card.html'
output.write_text(html)
print(f'Generated {output.relative_to(ROOT)}')
