#!/usr/bin/env python3
# Usage: npm i lucide-react && python3 scripts/make_assets.py assets
#   (or set LUCIDE_ICONS to a lucide-react dist/esm/icons folder)
"""Generate Divan's SVG assets: logo, banner, agent icons, team chart, loop diagram.
Glyphs come from Lucide (ISC licence); everything else is drawn here."""
import json, os, re, sys

LUCIDE = os.environ.get("LUCIDE_ICONS", "node_modules/lucide-react/dist/esm/icons")
OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(f"{OUT}/icons", exist_ok=True)

FONT = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
NAVY, NAVY2, INK, MUTED, LINE, PAPER = "#0F172A", "#1E293B", "#0F172A", "#475569", "#CBD5E1", "#F8FAFC"
GOLD, BLUE = "#EAB308", "#3B82F6"

AGENTS = [  # id, glyph, colour, title, human role
    ("spec-writer",      "file-check",       "#3B82F6", "spec-writer",      "Product manager"),
    ("architect",        "drafting-compass", "#6366F1", "architect",        "Tech lead"),
    ("builder",          "code-xml",         "#0EA5E9", "builder",          "Developer"),
    ("reviewer",         "scan-search",      "#14B8A6", "reviewer",         "QA · independent"),
    ("security-checker", "shield-check",     "#F59E0B", "security-checker", "Security &amp; privacy"),
    ("feature-engineer", "brain-circuit",    "#A855F7", "feature-engineer", "ML · only if a model"),
    ("release-docs",     "rocket",           "#22C55E", "release-docs",     "Release &amp; docs"),
]
OWNER = ("owner", "crown", GOLD)


def glyph(name):
    """Return the inner SVG elements of a Lucide icon (24×24 grid)."""
    src = open(f"{LUCIDE}/{name}.mjs").read()
    body = re.search(r"const __iconNode = (\[.*?\n\]);", src, re.S).group(1)
    body = re.sub(r"(\w+):", r'"\1":', body)            # quote object keys
    nodes = json.loads(body)
    parts = []
    for tag, attrs in nodes:
        attrs = {k: v for k, v in attrs.items() if k != "key"}
        parts.append(f"<{tag} " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>")
    return "".join(parts)


def tile(x, y, size, colour, gname, radius=None, stroke="#FFFFFF"):
    """A rounded coloured square with a white Lucide glyph centred in it."""
    r = radius if radius is not None else size * 0.24
    s = size * 0.56 / 24                                   # glyph scale
    gx, gy = x + size * 0.22, y + size * 0.22
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" fill="{colour}"/>'
            f'<g transform="translate({gx} {gy}) scale({s})" fill="none" stroke="{stroke}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{glyph(gname)}</g>')


def svg(w, h, inner, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{inner}</svg>\n')


def write(name, content):
    open(f"{OUT}/{name}", "w").write(content)
    print("wrote", name)


def mark(cx, cy, scale=1.0):
    """The Divan mark: one gold circle (the owner) above an arc of seven departments."""
    import math
    parts = []
    R = 46 * scale
    for i, (_, _, colour, *_rest) in enumerate(AGENTS):
        a = math.radians(200 + i * (140 / 6))              # arc from 200° to 340°
        x = cx + R * math.cos(a) - 7 * scale
        y = cy - R * math.sin(a) - 7 * scale - 4 * scale
        parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{14*scale:.2f}" height="{14*scale:.2f}" '
                     f'rx="{4*scale:.2f}" fill="{colour}"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy - 14*scale:.2f}" r="{15*scale:.2f}" fill="{GOLD}"/>')
    return "".join(parts)


# ---------------------------------------------------------------- icons
for aid, g, colour, *_ in AGENTS + [OWNER]:
    write(f"icons/{aid}.svg", svg(64, 64, tile(0, 0, 64, colour, g), aid))

# ---------------------------------------------------------------- logo
logo = (f'<rect width="128" height="128" rx="28" fill="{NAVY}"/>' + mark(64, 56, 1.0))
write("logo.svg", svg(128, 128, logo, "Divan logo"))

# ---------------------------------------------------------------- banner
tiles = "".join(tile(560 + i * 92, 236, 64, c, g) for i, (_, g, c, *_r) in enumerate(AGENTS))
banner = (
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
    f'<stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="#172554"/></linearGradient></defs>'
    '<rect width="1280" height="360" rx="24" fill="url(#bg)"/>'
    f'<rect x="64" y="72" width="216" height="216" rx="48" fill="{NAVY2}"/>' + mark(172, 163, 1.75) +
    f'<text x="560" y="140" font-family="{FONT}" font-size="88" font-weight="800" fill="#FFFFFF">Divan</text>'
    f'<text x="562" y="188" font-family="{FONT}" font-size="26" fill="#CBD5E1">A product team of AI agents —</text>'
    f'<text x="562" y="222" font-family="{FONT}" font-size="26" fill="#CBD5E1">built around one human who decides.</text>'
    + tiles
)
# The tagline sits above the tiles; move tiles lower for breathing room.
banner = banner.replace('y="236"', 'y="258"')
write("banner.svg", svg(1280, 360, banner, "Divan — a product team of AI agents, built around one human who decides"))

# ---------------------------------------------------------------- team chart
W, H = 1280, 520
team = [f'<rect width="{W}" height="{H}" rx="24" fill="{PAPER}" stroke="{LINE}"/>',
        f'<text x="{W/2}" y="56" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">The Divan: seven departments, one decision-maker</text>']
ox = W / 2 - 40
team.append(tile(ox, 92, 80, GOLD, "crown", stroke=NAVY))
team.append(f'<text x="{W/2}" y="200" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{INK}">You — the owner</text>')
team.append(f'<text x="{W/2}" y="226" text-anchor="middle" font-family="{FONT}" font-size="16" fill="{MUTED}">decide what to build, what to cut, when it is good enough</text>')
# connectors
cols = [W / 2 - 3 * 176 - 40 + i * 176 for i in range(7)]
team.append(f'<path d="M{W/2} 240 V270 M{cols[0]+40} 270 H{cols[-1]+40}" stroke="{LINE}" stroke-width="3" fill="none"/>')
for i, (aid, g, colour, title, role) in enumerate(AGENTS):
    x = cols[i]
    team.append(f'<path d="M{x+40} 270 V300" stroke="{LINE}" stroke-width="3"/>')
    team.append(tile(x, 300, 80, colour, g))
    team.append(f'<text x="{x+40}" y="412" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="700" fill="{INK}">{title}</text>')
    team.append(f'<text x="{x+40}" y="438" text-anchor="middle" font-family="{FONT}" font-size="15" fill="{MUTED}">{role}</text>')
team.append(f'<text x="{W/2}" y="490" text-anchor="middle" font-family="{FONT}" font-size="15" fill="{MUTED}">Agents execute. Only the builder edits product code. Reviewer and security only report.</text>')
write("team.svg", svg(W, H, "".join(team), "Divan team: the owner above seven specialised agents"))

# ---------------------------------------------------------------- loop diagram
W, H = 1280, 560
L = [f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
     f'<path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/></marker></defs>',
     f'<rect width="{W}" height="{H}" rx="24" fill="{PAPER}" stroke="{LINE}"/>',
     f'<text x="{W/2}" y="54" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">The feature loop — agents execute, you decide at three gates</text>']


def step(x, y, colour, g, label, sub):
    return (tile(x, y, 64, colour, g) +
            f'<text x="{x+32}" y="{y+90}" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="{INK}">{label}</text>'
            f'<text x="{x+32}" y="{y+112}" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{MUTED}">{sub}</text>')


def gate(cx, cy, letter, sub):
    return (f'<rect x="{cx-30}" y="{cy-30}" width="60" height="60" rx="10" transform="rotate(45 {cx} {cy})" fill="{GOLD}"/>'
            f'<text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="{FONT}" font-size="24" font-weight="800" fill="{NAVY}">{letter}</text>'
            f'<text x="{cx}" y="{cy+66}" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="{INK}">Gate {letter}</text>'
            f'<text x="{cx}" y="{cy+88}" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{MUTED}">{sub}</text>')


def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{MUTED}" stroke-width="2.5" fill="none" marker-end="url(#ar)"/>'


A = {a[0]: a for a in AGENTS}
y1 = 110   # row 1 tiles top
# Row 1: Idea → spec-writer → Gate A → architect → Gate B → builder
L.append(f'<rect x="60" y="{y1+8}" width="110" height="48" rx="24" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>'
         f'<text x="115" y="{y1+39}" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="{INK}">Idea</text>')
L.append(arrow(176, y1+32, 236, y1+32))
L.append(step(244, y1, A["spec-writer"][2], A["spec-writer"][1], "spec-writer", "feature card"))
L.append(arrow(316, y1+32, 400, y1+32))
L.append(gate(450, y1+32, "A", "you approve scope"))
L.append(arrow(500, y1+32, 584, y1+32))
L.append(step(592, y1, A["architect"][2], A["architect"][1], "architect", "design · 3 variants"))
L.append(arrow(664, y1+32, 748, y1+32))
L.append(gate(798, y1+32, "B", "you pick the design"))
L.append(arrow(848, y1+32, 932, y1+32))
L.append(step(940, y1, A["builder"][2], A["builder"][1], "builder", "one task at a time"))
# down to row 2
y2 = 340
L.append(f'<path d="M972 {y1+124} V{y2-40} H1100 V{y2-6}" stroke="{MUTED}" stroke-width="2.5" fill="none" marker-end="url(#ar)"/>')
# Row 2 (right to left): reviewer → security → release-docs → Gate C → Released
L.append(step(1068, y2, A["reviewer"][2], A["reviewer"][1], "reviewer", "independent check"))
# rework loop reviewer → builder
L.append(f'<path d="M1140 {y2+20} C1210 {y2-40}, 1210 {y1+40}, 1010 {y1+32}" stroke="{A["reviewer"][2]}" stroke-width="2.5" stroke-dasharray="7 6" fill="none" marker-end="url(#ar)"/>'
         f'<text x="1214" y="{(y1+y2)/2+30}" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{A["reviewer"][2]}" font-weight="700">fix</text>'
         f'<text x="1214" y="{(y1+y2)/2+48}" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{MUTED}">max 3</text>')
L.append(arrow(1060, y2+32, 984, y2+32))
L.append(step(912, y2, A["security-checker"][2], A["security-checker"][1], "security-checker", "promises kept"))
L.append(arrow(904, y2+32, 828, y2+32))
L.append(step(756, y2, A["release-docs"][2], A["release-docs"][1], "release-docs", "prepares, never ships"))
L.append(arrow(748, y2+32, 660, y2+32))
L.append(gate(610, y2+32, "C", "you merge and ship"))
L.append(arrow(560, y2+32, 470, y2+32))
L.append(f'<rect x="300" y="{y2+8}" width="164" height="48" rx="24" fill="{A["release-docs"][2]}"/>'
         f'<text x="382" y="{y2+39}" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#FFFFFF">Released</text>')
L.append(arrow(294, y2+32, 210, y2+32))
L.append(f'<rect x="56" y="{y2-4}" width="148" height="72" rx="14" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>'
         f'<text x="130" y="{y2+26}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="{INK}">Signal vs target</text>'
         f'<text x="130" y="{y2+48}" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{MUTED}">keep · iterate · remove</text>')
write("loop.svg", svg(W, H, "".join(L), "The Divan feature loop with three owner gates"))
