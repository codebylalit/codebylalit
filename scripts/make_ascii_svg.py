import os
import sys
from PIL import Image, ImageDraw

RAMP = " .`:-=+*cs#%@"  # Bright (sparse) -> Dark (dense)

def create_sample_avatar_image(filename="source-prepped.png", width=200, height=200):
    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)
    draw.ellipse((60, 35, 140, 115), fill=40)
    draw.ellipse((30, 125, 170, 230), fill=40)
    draw.ellipse((75, 55, 90, 70), fill=210)
    draw.ellipse((110, 55, 125, 70), fill=210)
    img.save(filename)
    print(f"Generated default sample avatar image at '{filename}'")

def image_to_ascii(img_path: str, target_width: int = 80):
    if not os.path.exists(img_path):
        create_sample_avatar_image(img_path)

    try:
        img = Image.open(img_path).convert("L")
    except Exception as e:
        raise ValueError(f"Could not open image at '{img_path}': {e}")

    w, h = img.size
    aspect_ratio = h / float(w)
    target_height = max(10, int(target_width * aspect_ratio * 0.52))

    resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    pixels = resized.load()

    ascii_rows = []
    for y in range(target_height):
        row_str = ""
        for x in range(target_width):
            pixel_val = pixels[x, y]
            ramp_idx = int((pixel_val / 255.0) * (len(RAMP) - 1))
            row_str += RAMP[ramp_idx]
        ascii_rows.append(row_str)

    return ascii_rows

def generate_ascii_svg(rows, output_path="avi-ascii.svg"):
    char_w = 7.1
    char_h = 13.0
    padding_x = 22
    padding_y = 30

    num_cols = max(len(r) for r in rows)
    width = int(num_cols * char_w + (padding_x * 2))
    height = int(len(rows) * char_h + (padding_y * 2))

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <defs>',
        '    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#0f172a" />',
        '      <stop offset="50%" stop-color="#0b0f19" />',
        '      <stop offset="100%" stop-color="#05070f" />',
        '    </linearGradient>',
        '    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8" />',
        '      <stop offset="50%" stop-color="#a78bfa" stop-opacity="0.3" />',
        '      <stop offset="100%" stop-color="#ec4899" stop-opacity="0.6" />',
        '    </linearGradient>',
        '  </defs>',
        '  <style>',
        '    .outer-shell { fill: url(#bgGrad); stroke: url(#borderGrad); stroke-width: 1.5px; rx: 12px; }',
        '    .ascii-text { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; fill: #94a3b8; white-space: pre; }',
        '  </style>',
        '  <rect width="100%" height="100%" class="outer-shell" />',
        '  <defs>',
    ]

    for i in range(len(rows)):
        delay = i * 0.035
        y_top = padding_y + (i * char_h) - 10
        svg.append(f'    <clipPath id="clip-row-{i}">')
        svg.append(f'      <rect x="0" y="{y_top:.1f}" height="{char_h + 2}" width="{width}">')
        svg.append(f'        <animate attributeName="width" from="0" to="{width}" dur="0.25s" begin="{delay:.3f}s" fill="freeze" />')
        svg.append(f'      </rect>')
        svg.append(f'    </clipPath>')

    svg.append('  </defs>')

    for i, row in enumerate(rows):
        y_pos = padding_y + (i * char_h)
        escaped_row = row.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg.append(f'  <text x="{padding_x}" y="{y_pos:.1f}" class="ascii-text" clip-path="url(#clip-row-{i})">{escaped_row}</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"ASCII SVG generated at '{output_path}' ({width}x{height}px)")

if __name__ == "__main__":
    img_file = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "avi-ascii.svg"
    rows = image_to_ascii(img_file)
    generate_ascii_svg(rows, out_file)
