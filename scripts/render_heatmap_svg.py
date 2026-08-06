import os
import sys
import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

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
    height = 175
    box_size = 11
    gap = 3
    start_x = 35
    start_y = 35

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 8px; }',
        '    .sub-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #8b949e; }',
        '    .label-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 10px; fill: #6e7681; }',
        '    .stat-val { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #a78bfa; font-weight: 600; }',
        '    .accent { fill: #7ee787; font-weight: 600; }',
        '    @keyframes popIn {',
        '      0% { transform: scale(0); opacity: 0; }',
        '      70% { transform: scale(1.18); opacity: 0.9; }',
        '      100% { transform: scale(1); opacity: 1; }',
        '    }',
        '    .day-box { animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; opacity: 0; transform-box: fill-box; transform-origin: center; }',
        '  </style>',
        '  <rect width="100%" height="100%" class="bg" />',
        f'  <text x="35" y="22" class="sub-text">Contribution Heatmap (<tspan class="stat-val">{total:,}</tspan> contributions in past year)</text>',
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
        delay = (col + row) * 0.011

        svg.append(f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" class="day-box" style="animation-delay: {delay:.3f}s;" />')

    footer_y = 156
    svg.append(f'  <text x="35" y="{footer_y}" class="sub-text">Current Streak: <tspan class="stat-val">{current_streak} days</tspan> | Longest: <tspan class="stat-val">{longest_streak} days</tspan> | Best Day: <tspan class="accent">{best_day["count"]} ({best_day["date"]})</tspan></text>')

    legend_start_x = 730
    svg.append(f'  <text x="{legend_start_x - 30}" y="{footer_y}" class="label-text">Less</text>')
    for i, col_val in enumerate(PALETTE):
        lx = legend_start_x + i * (10 + 3)
        svg.append(f'  <rect x="{lx}" y="{footer_y - 9}" width="10" height="10" rx="2" fill="{col_val}" />')
    svg.append(f'  <text x="{legend_start_x + len(PALETTE) * 13 + 4}" y="{footer_y}" class="label-text">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Heatmap SVG saved to '{output_path}' ({width}x{height}px)")

if __name__ == "__main__":
    j_path = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    o_path = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    render_heatmap_svg(j_path, o_path)
