import os
import sys

def generate_info_card(output_path="info-card.svg"):
    is_static = os.getenv("STATIC") == "1"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 350" width="490" height="350">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 8px; }}
    .title-bar {{ fill: #161b22; stroke: #30363d; stroke-width: 1px; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .text-title {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #8b949e; font-weight: 600; }}
    .key {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #a78bfa; font-weight: 600; }}
    .val {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #c9d1d9; }}
    .accent {{ fill: #7ee787; font-weight: 600; }}

    @keyframes slideIn {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .line {{ animation: {"none" if is_static else "slideIn 0.35s ease-out forwards"}; opacity: {"1" if is_static else "0"}; }}
  </style>

  <rect width="100%" height="100%" class="bg" />
  <path d="M 0 8 A 8 8 0 0 1 8 0 L 482 0 A 8 8 0 0 1 490 8 L 490 32 L 0 32 Z" class="title-bar" />

  <!-- Window Controls -->
  <circle cx="20" cy="16" r="5" class="dot-red" />
  <circle cx="36" cy="16" r="5" class="dot-yellow" />
  <circle cx="52" cy="16" r="5" class="dot-green" />
  <text x="245" y="20" text-anchor="middle" class="text-title">neofetch --codebylalit</text>

  <!-- Info Lines -->
  <g transform="translate(25, 65)">
    <g class="line" style="animation-delay: 0.10s;">
      <text x="0" y="0" class="key">User</text><text x="110" y="0" class="val">Lalit Namdev (@codebylalit)</text>
    </g>
    <g class="line" style="animation-delay: 0.22s;" transform="translate(0, 30)">
      <text x="0" y="0" class="key">Role</text><text x="110" y="0" class="val">Frontend Developer &amp; Micro-SaaS Maker</text>
    </g>
    <g class="line" style="animation-delay: 0.34s;" transform="translate(0, 60)">
      <text x="0" y="0" class="key">Stack</text><text x="110" y="0" class="val">React, React Native, TypeScript, Next.js</text>
    </g>
    <g class="line" style="animation-delay: 0.46s;" transform="translate(0, 90)">
      <text x="0" y="0" class="key">Focus</text><text x="110" y="0" class="val">AI-Powered Web Apps &amp; Mobile Products</text>
    </g>
    <g class="line" style="animation-delay: 0.58s;" transform="translate(0, 120)">
      <text x="0" y="0" class="key">Highlights</text><text x="110" y="0" class="val accent">🏆 Top 50 Finalist @ Odoo Hackathon</text>
    </g>
    <g class="line" style="animation-delay: 0.70s;" transform="translate(0, 150)">
      <text x="0" y="0" class="key">Builds</text><text x="110" y="0" class="val">Skooty, Invoicelly, NenoBanana, Hashly</text>
    </g>
    <g class="line" style="animation-delay: 0.82s;" transform="translate(0, 180)">
      <text x="0" y="0" class="key">Location</text><text x="110" y="0" class="val">Ahmedabad, India 🇮🇳 (UTC+05:30)</text>
    </g>
  </g>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Info Card SVG saved to '{output_path}'")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "info-card.svg"
    generate_info_card(out_file)
