import os
import sys
import json

# Ultra high-end Glowing Emerald/Indigo Palette
PALETTE = ["#1e293b", "#064e3b", "#047857", "#10b981", "#34d399", "#6ee7b7"]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: Contributions dataset '{json_path}' not found. Run fetch_contributions.py first.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {"count": 0, "date": "N/A"})

    width = 860
    height = 180
    box_size = 11
    gap = 3
    start_x = 35
    start_y = 38

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <defs>',
        '    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#0f172a" />',
        '      <stop offset="50%" stop-color="#0b0f19" />',
        '      <stop offset="100%" stop-color="#05070f" />',
        '    </linearGradient>',
        '    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#34d399" stop-opacity="0.8" />',
        '      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.3" />',
        '      <stop offset="100%" stop-color="#a78bfa" stop-opacity="0.6" />',
        '    </linearGradient>',
        '  </defs>',
        '  <style>',
        '    .outer-shell { fill: url(#bgGrad); stroke: url(#borderGrad); stroke-width: 1.5px; rx: 12px; }',
        '    .sub-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #94a3b8; }',
        '    .label-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 10px; fill: #64748b; }',
        '    .stat-val { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #38bdf8; font-weight: 700; }',
        '    .accent { fill: #34d399; font-weight: 700; }',
        '    @keyframes popIn {',
        '      0% { transform: scale(0); opacity: 0; }',
        '      70% { transform: scale(1.2); opacity: 0.9; }',
        '      100% { transform: scale(1); opacity: 1; }',
        '    }',
        '    .day-box { animation: popIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform-box: fill-box; transform-origin: center; }',
        '  </style>',
        '  <rect width="100%" height="100%" class="outer-shell" />',
        f'  <text x="35" y="24" class="sub-text">⚡ Live Contribution Activity (<tspan class="stat-val">{total:,}</tspan> contributions in 365 days)</text>',
    ]

    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for label, r_idx in day_labels:
        y_pos = start_y + r_idx * (box_size + gap) + 9
        svg.append(f'  <text x="10" y="{y_pos}" class="label-text">{label}</text>')

    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        x = start_x + col * (box_size + gap)
        y = start_y + row * (box_size + gap)

        level = min(max(0, day.get("level", 0)), len(PALETTE) - 1)
        color = PALETTE[level]
        delay = (col + row) * 0.01

        svg.append(f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2.5" fill="{color}" class="day-box" style="animation-delay: {delay:.3f}s;" />')

    footer_y = 160
    svg.append(f'  <text x="35" y="{footer_y}" class="sub-text">Current Streak: <tspan class="stat-val">{current_streak} days</tspan> | Longest: <tspan class="stat-val">{longest_streak} days</tspan> | Peak Day: <tspan class="accent">{best_day["count"]} commits ({best_day["date"]})</tspan></text>')

    legend_start_x = 730
    svg.append(f'  <text x="{legend_start_x - 30}" y="{footer_y}" class="label-text">Less</text>')
    for i, col_val in enumerate(PALETTE):
        lx = legend_start_x + i * (10 + 3)
        svg.append(f'  <rect x="{lx}" y="{footer_y - 9}" width="10" height="10" rx="2" fill="{col_val}" />')
    svg.append(f'  <text x="{legend_start_x + len(PALETTE) * 13 + 4}" y="{footer_y}" class="label-text">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Heatmap SVG generated at '{output_path}' ({width}x{height}px)")

if __name__ == "__main__":
    j_path = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap_svg(j_path, o_path)
