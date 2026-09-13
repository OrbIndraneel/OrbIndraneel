import os
from PIL import Image, ImageEnhance
import html

im_orig = Image.open('source-prepped.png').convert('L')

configs = [
    ('cand0_default', 0.92, 1.0, 1.65, 0.60),
    ('cand1_balanced', 1.05, 1.0, 1.55, 0.62),
    ('cand2_contrasted', 1.15, 1.0, 1.45, 0.58),
    ('cand3_defined', 1.25, 1.0, 1.35, 0.55),
    ('cand4_soft', 0.95, 1.05, 1.75, 0.65),
]

COLS, ROWS, CELL_W, CELL_H = 100, 53, 8, 15
RAMP = ' .`:-=+*cs#%@'
PAD, TITLEBAR_H, STATUS_H = 20, 30, 30
ART_W, ART_H = COLS * CELL_W, ROWS * CELL_H
CANVAS_W, CANVAS_H = ART_W + PAD * 2, TITLEBAR_H + ART_H + STATUS_H + PAD
BG, BG2, FRAME, TITLE_TEXT, INK = '#0d1117', '#111722', '#30363d', '#7d8590', '#c9d1d9'
art_top = TITLEBAR_H + PAD * 0.35
font_size = CELL_H * 0.86

for name, cont, bri, gam, wf in configs:
    im = ImageEnhance.Brightness(im_orig).enhance(bri)
    im = ImageEnhance.Contrast(im).enhance(cont)
    im = im.resize((COLS, ROWS), Image.LANCZOS)
    px = im.load()
    rows_txt = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            lum = px[x, y] / 255.0
            lum = pow(lum, gam)
            if lum >= wf:
                chars.append(' ')
                continue
            idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
            idx = max(0, min(len(RAMP) - 1, idx))
            chars.append(RAMP[idx])
        rows_txt.append(''.join(chars))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="{BG}"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
        f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">OrbIndraneel@github: ~$ ./portrait.sh ({name})</text>'
    ]
    for ry, line in enumerate(rows_txt):
        y = art_top + ry * CELL_H + CELL_H * 0.74
        safe = html.escape(line)
        parts.append(f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>')
    parts.append('</svg>')
    out_svg = f'test_{name}.svg'
    with open(out_svg, 'w', encoding='utf-8') as f:
        f.write(''.join(parts))
    print(f'Wrote {out_svg}')
