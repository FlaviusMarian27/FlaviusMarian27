"""Generates every SVG in assets/ for the networking-themed GitHub profile.

Run:  python3 gen_assets.py
Edit the DATA section below, re-run, commit the assets/ folder.
"""
import os
import textwrap
import sys
import scenes
from xml.sax.saxutils import escape as esc

os.makedirs("assets/projects", exist_ok=True)

# ───────────────────────── theme (Tokyo Night) ─────────────────────────
BG, PANEL, PANEL2 = "#0b0e17", "#11141f", "#161a29"
CYAN, BLUE, PINK, GREEN, YEL, RED = "#7dcfff", "#7aa2f7", "#bb9af7", "#9ece6a", "#e0af68", "#f7768e"
DIM, TXT = "#565f89", "#c0caf5"
FONT = "Consolas,'JetBrains Mono','DejaVu Sans Mono','Courier New',monospace"
CW = 0.6  # monospace char width as fraction of font-size


def svg_open(w, h, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="gh" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <filter id="glow" x="-10%" y="-30%" width="120%" height="160%">
    <feGaussianBlur stdDeviation="4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <style>
    text {{ font-family: {FONT}; }}
    .k {{ fill: {CYAN}; }} .v {{ fill: {TXT}; }} .d {{ fill: {DIM}; }} .p {{ fill: {PINK}; }}
    .gr {{ fill: {GREEN}; }} .y {{ fill: {YEL}; }} .b {{ fill: {BLUE}; }}
    .bold {{ font-weight: 700; }}
    .cur {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .led {{ animation: led 1.6s ease-in-out infinite; }}
    @keyframes led {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    {extra_css}
  </style>
</defs>
'''


def frame(w, h, rx=16):
    return (f'<rect width="{w}" height="{h}" rx="{rx + 4}" fill="{BG}"/>\n'
            f'<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="{rx}" fill="{PANEL}" '
            f'stroke="url(#g)" stroke-width="2" filter="url(#glow)"/>\n')


def save(path, parts):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n</svg>")


def chip(x, y, label, color, fs=12):
    w = len(label) * fs * CW + 18
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{color}" fill-opacity=".12" '
            f'stroke="{color}" stroke-opacity=".55"/>'
            f'<text x="{x + w/2:.1f}" y="{y + 15}" text-anchor="middle" font-size="{fs}" fill="{color}">{esc(label)}</text>'), w


# ───────────────────────── icons ─────────────────────────
def router(x, y, label):
    return f'''<g transform="translate({x},{y})">
  <ellipse cx="0" cy="6" rx="30" ry="10" fill="{PANEL2}" stroke="{CYAN}" stroke-width="1.6"/>
  <rect x="-30" y="-6" width="60" height="12" fill="{PANEL2}"/>
  <line x1="-30" y1="-6" x2="-30" y2="6" stroke="{CYAN}" stroke-width="1.6"/>
  <line x1="30" y1="-6" x2="30" y2="6" stroke="{CYAN}" stroke-width="1.6"/>
  <ellipse cx="0" cy="-6" rx="30" ry="10" fill="{PANEL2}" stroke="{CYAN}" stroke-width="1.6"/>
  <path d="M-14 -9 l8 3 M14 -3 l-8 -3 M-4 -12 l3 6 M4 0 l-3 -6" stroke="{CYAN}" stroke-width="1.6" stroke-linecap="round"/>
  <text y="32" text-anchor="middle" font-size="12" class="k">{label}</text>
</g>'''


def switch(x, y, label, color=BLUE):
    leds = "".join(f'<rect x="{-26 + i*9}" y="3" width="5" height="4" rx="1" fill="{GREEN}" class="led" '
                   f'style="animation-delay:{i*0.2:.1f}s"/>' for i in range(6))
    return f'''<g transform="translate({x},{y})">
  <rect x="-34" y="-12" width="68" height="24" rx="4" fill="{PANEL2}" stroke="{color}" stroke-width="1.6"/>
  <path d="M-20 -5 h14 l-3 -3 M20 -2 h-14 l3 3" stroke="{color}" stroke-width="1.4" fill="none" stroke-linecap="round"/>
  {leds}
  <text y="30" text-anchor="middle" font-size="12" class="b">{label}</text>
</g>'''


def host(x, y, label, color=PINK):
    return f'''<g transform="translate({x},{y})">
  <rect x="-16" y="-14" width="32" height="22" rx="3" fill="{PANEL2}" stroke="{color}" stroke-width="1.5"/>
  <rect x="-11" y="-9" width="22" height="12" rx="1" fill="{color}" fill-opacity=".18"/>
  <path d="M-8 12 h16 M0 8 v4" stroke="{color}" stroke-width="1.5"/>
  <text y="28" text-anchor="middle" font-size="11" fill="{color}">{label}</text>
</g>'''


def cloud(x, y):
    return f'''<g transform="translate({x},{y})">
  <path d="M-38 10 a14 14 0 0 1 4 -27 a20 20 0 0 1 36 -6 a16 16 0 0 1 30 10 a12 12 0 0 1 -2 23 z"
        fill="{PANEL2}" stroke="{PINK}" stroke-width="1.6"/>
  <text y="4" text-anchor="middle" font-size="12" class="p">Internet</text>
</g>'''


def link(pid, d, color, dur, delay=0, dashed=False):
    dash = ' stroke-dasharray="4 4"' if dashed else ""
    return f'''<path id="{pid}" d="{d}" stroke="{color}" stroke-opacity=".55" stroke-width="1.6" fill="none"{dash}/>
<circle r="3.5" fill="{color}" filter="url(#glow)">
  <animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear">
    <mpath href="#{pid}"/>
  </animateMotion>
</circle>'''


# ───────────────────────── 1. header ─────────────────────────
def header(only=None, out="assets/header.svg"):
    W, H = 1000, 500
    o = [svg_open(W, H, scenes.css(len(scenes.SCENES))), frame(W, H)]
    for i, c in enumerate([RED, YEL, GREEN]):
        o.append(f'<circle cx="{34 + i*20}" cy="34" r="6" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="39" text-anchor="middle" class="d" font-size="14">ssh flavius@R1-UPT — console 115200</text>')
    o.append(f'<line x1="22" y1="56" x2="{W-22}" y2="56" stroke="{DIM}" stroke-opacity=".35"/>')

    o.extend(scenes.build(30, 74, only))

    # IOS-style info
    x0, y0, lh, fs, COLS = 410, 94, 22.2, 15, 52
    L = []

    def kv(k, v):
        L.append(f'<tspan class="k">{esc(k)}</tspan><tspan class="d"> {"."*max(2, COLS-len(k)-len(v)-2)} </tspan>'
                 f'<tspan class="v">{esc(v)}</tspan>')

    def hd(t):
        pad = "─" * ((COLS - len(t) - 2) // 2)
        L.append(f'<tspan class="d">{pad} </tspan><tspan class="y bold">{t}</tspan><tspan class="d"> {pad}</tspan>')

    L.append(f'<tspan class="p bold">R1-UPT</tspan><tspan class="d">#</tspan><tspan class="v"> show version</tspan>')
    kv("hostname", "Flavius-Andrei Marian")
    kv("location", "Timișoara, Romania")
    kv("site", "Politehnica Timișoara · AC")
    kv("program", "Software Engineering · Year 4")
    kv("thesis", "Network automation · GNS3 + Python")
    kv("focus", "Routing · Switching · Automation")
    kv("stack.net", "Cisco IOS · GNS3 · Packet Tracer")
    kv("stack.code", "Python · C · Go · Java")
    kv("training", "Cisco NetAcad CCNA · Linux Ess.")
    L.append("")
    hd("show cdp neighbors")
    kv("mail", "flavius.marian@student.upt.ro")
    kv("linkedin", "in/flavius-andrei-marian")
    kv("github", "@FlaviusMarian27")

    o.append(f'<g font-size="{fs}" xml:space="preserve">')
    for i, l in enumerate(L):
        o.append(f'<text x="{x0}" y="{y0 + i*lh:.1f}">{l}</text>')
    yl = y0 + len(L) * lh + 8
    o.append(f'<text x="{x0}" y="{yl:.1f}"><tspan class="p bold">R1-UPT</tspan><tspan class="d">#</tspan> '
             f'<tspan class="cur gr">█</tspan></text></g>')
    # port LEDs bottom-right
    for i in range(8):
        col = GREEN if i not in (5,) else YEL
        o.append(f'<rect x="{W - 250 + i*28}" y="{H - 42}" width="20" height="12" rx="2" fill="{col}" '
                 f'class="led" style="animation-delay:{i*.18:.2f}s"/>')
    o.append(f'<text x="{W - 250}" y="{H - 50}" font-size="10" class="d">Gi0/1 ─────────────── Gi0/8</text>')
    save(out, o)


# ───────────────────────── 2. section titles ─────────────────────────
def section(name, prompt_cmd, title):
    W, H = 1000, 64
    o = [svg_open(W, H)]
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{PANEL}" stroke="url(#gh)" stroke-opacity=".7"/>')
    o.append(f'<text x="22" y="40" font-size="20"><tspan class="p bold">R1-UPT</tspan><tspan class="d">#</tspan>'
             f'<tspan class="v"> {esc(prompt_cmd)}</tspan></text>')
    tw = len(title) * 18 * CW
    o.append(f'<text x="{W-24}" y="40" font-size="18" text-anchor="end" class="k bold">{esc(title)}</text>')
    start = 22 + (len("R1-UPT# ") + len(prompt_cmd)) * 20 * CW + 20
    end = W - 24 - tw - 20
    o.append(link(f"s_{name}", f"M{start:.0f} 33 L{end:.0f} 33", BLUE, 4, dashed=True))
    save(f"assets/section-{name}.svg", o)


# ───────────────────────── 3. deep dive ─────────────────────────
DEEP = [
    ("Gi0/1", "Networking", CYAN,
     "Enterprise topologies in Cisco Packet Tracer and GNS3: VLANs, routing, addressing plans. "
     "My thesis automates GNS3 labs with Python, so configs are generated and tested instead of typed by hand."),
    ("Gi0/2", "System Programming", BLUE,
     "OS work in C on Linux: process synchronization, memory management, multithreading. "
     "The kind of code where an off-by-one in a mutex ruins your whole afternoon."),
    ("Gi0/3", "Low-Level & Hardware", PINK,
     "An 8086 microprocessor system built from scratch in x86 Assembly and ALU modules modeled in SystemC. "
     "Writing Assembly taught me more about CPUs than any lecture."),
    ("Gi0/4", "Full-Stack", GREEN,
     "Clarity Gym: Vue 3 + Go + PostgreSQL with JWT auth, bcrypt and three roles. "
     "Rewritten from an earlier Node.js + MongoDB version once I outgrew the stack."),
]


def deepdive():
    W, H = 1000, 420
    o = [svg_open(W, H), frame(W, H)]
    pw, ph, gap = 470, 186, 20
    for i, (port, title, col, body) in enumerate(DEEP):
        x = 20 + (i % 2) * (pw + gap)
        y = 20 + (i // 2) * (ph + gap)
        o.append(f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="12" fill="{BG}" stroke="{col}" stroke-opacity=".5"/>')
        o.append(f'<rect x="{x}" y="{y+18}" width="4" height="30" rx="2" fill="{col}"/>')
        o.append(f'<circle cx="{x + pw - 24}" cy="{y + 33}" r="5" fill="{GREEN}" class="led"/>')
        o.append(f'<text x="{x + pw - 36}" y="{y + 37}" text-anchor="end" font-size="11" class="d">{port} up/up</text>')
        o.append(f'<text x="{x + 22}" y="{y + 40}" font-size="19" fill="{col}" class="bold">{esc(title)}</text>')
        for j, line in enumerate(textwrap.wrap(body, 47)):
            o.append(f'<text x="{x + 22}" y="{y + 80 + j*24}" font-size="14.5" class="v">{esc(line)}</text>')
    save("assets/deepdive.svg", o)


# ───────────────────────── 4. project cards ─────────────────────────
# (slug, name, repo, year, category, description, tech)
PROJECTS = [
    ("network-sim", "Enterprise Network Simulation", "Cisco-Enterprise-Network-Simulation", 2026, "NETWORKING",
     "Enterprise network topology designed and simulated in Cisco Packet Tracer.",
     ["Cisco IOS", "Packet Tracer"]),
    ("exploding-kittens", "Exploding Kittens · LAN", "ExplodingKittens", 2025, "NETWORKING",
     "Multiplayer card game played over LAN, terminal UI built with ncurses.",
     ["C", "Sockets", "ncurses"]),
    ("system-monitor", "System Monitor", "System-Monitor", 2026, "SYSTEMS",
     "Dedicated system for monitoring computer resources.",
     ["C", "Python", "Linux"]),
    ("os-core", "Operating Systems Core", "OperatingSystems", 2025, "SYSTEMS",
     "Process synchronization, memory management and multithreading in C.",
     ["C", "POSIX", "Linux"]),
    ("clarity-gym", "Clarity Gym", "Clarity-Gym", 2026, "FULL-STACK",
     "Gym management platform with JWT auth, bcrypt and client / trainer / admin roles.",
     ["Vue 3", "Go", "PostgreSQL", "JWT"]),
    ("gym-manager", "Gym Manager Web App", "GymManagerWeb", 2025, "FULL-STACK",
     "First version of the gym platform, before the move to Vue + Go.",
     ["Node.js", "MongoDB", "JavaScript"]),
    ("8086", "8086 Microprocessor System", "Microsistem-cu-microprocesor-8086", 2025, "LOW-LEVEL",
     "Microprocessor system built from scratch around the Intel 8086.",
     ["x86 Assembly", "8086"]),
    ("systemc-alu", "SystemC ALU Modules", "SystemC-ALU-Modules", 2025, "LOW-LEVEL",
     "ALU hardware modules described and simulated in SystemC.",
     ["C++", "SystemC"]),
    ("mp3-windows", "MP3/MP4 Converter · Windows", "MP3-MP4-Windows", 2026, "APPS",
     "Desktop media converter with a PySide6 GUI for Windows.",
     ["Python", "PySide6"]),
    ("mp3-linux", "MP3/MP4 Converter · Linux", "MP3_converter", 2026, "APPS",
     "The same converter, packaged for Linux desktops.",
     ["Python", "PySide6", "Linux"]),
    ("tictactoe", "TicTacToe SFML", "TicTacToe", 2026, "APPS",
     "Classic game with a graphical interface, written to practice OOP in C++.",
     ["C++", "SFML"]),
    ("portfolio", "Personal Portfolio", "Flavius-Project", 2025, "WEB",
     "Personal website hosted on GitHub Pages.",
     ["HTML", "CSS", "JavaScript"]),
]
CAT_COLOR = {"NETWORKING": CYAN, "SYSTEMS": BLUE, "FULL-STACK": GREEN, "LOW-LEVEL": PINK, "APPS": YEL, "WEB": YEL}


def project_card(idx, p):
    slug, name, repo, year, cat, desc, tech = p
    col = CAT_COLOR[cat]
    W, H = 1000, 116
    o = [svg_open(W, H)]
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{PANEL}" stroke="{col}" stroke-opacity=".55"/>')
    # port block on the left
    o.append(f'<rect x="16" y="16" width="84" height="84" rx="10" fill="{BG}" stroke="{col}" stroke-opacity=".6"/>')
    o.append(f'<rect x="38" y="36" width="40" height="30" rx="3" fill="none" stroke="{col}" stroke-width="1.6"/>')
    o.append(f'<path d="M46 66 v-8 h24 v8" fill="none" stroke="{col}" stroke-width="1.4"/>')
    for k in range(4):
        o.append(f'<line x1="{48 + k*7}" y1="44" x2="{48 + k*7}" y2="52" stroke="{col}" stroke-width="1.4"/>')
    o.append(f'<circle cx="34" cy="30" r="3.5" fill="{GREEN}" class="led" style="animation-delay:{idx*.13:.2f}s"/>')
    o.append(f'<text x="58" y="88" text-anchor="middle" font-size="11" fill="{col}">Gi0/{idx+1}</text>')
    # text
    o.append(f'<text x="122" y="44" font-size="20" class="v bold">{esc(name)}</text>')
    o.append(f'<text x="122" y="70" font-size="13.5" fill="#a9b1d6">{esc(desc)}</text>')
    x = 122.0
    for t in tech:
        s, w = chip(x, 80, t, col)
        o.append(s)
        x += w + 8
    # right side
    c, cw_ = chip(0, 0, cat, col, 11)
    catw = len(cat) * 11 * CW + 18
    o.append(chip(W - 24 - catw, 18, cat, col, 11)[0])
    o.append(f'<text x="{W-24}" y="72" text-anchor="end" font-size="13" class="d">{year}</text>')
    o.append(f'<text x="{W-24}" y="98" text-anchor="end" font-size="13" class="k">view repo →</text>')
    save(f"assets/projects/{slug}.svg", o)


# ───────────────────────── 5. focus as routing table ─────────────────────────
FOCUS = [
    ("C", "10.0.1.0/24", "Networking", "routing, switching, automation with Python", CYAN),
    ("C", "10.0.2.0/24", "Operating Systems", "kernel internals, memory, scheduling", BLUE),
    ("O", "10.0.3.0/24", "Cybersecurity", "network security, secure coding", PINK),
    ("O", "10.0.4.0/24", "Automotive", "ECUs, RTOS, in-vehicle networks", YEL),
    ("S", "10.0.5.0/24", "Edge AI", "small ML models on constrained hardware", GREEN),
]


def focus():
    W, H = 1000, 70 + len(FOCUS) * 38 + 40
    o = [svg_open(W, H), frame(W, H)]
    o.append(f'<text x="30" y="44" font-size="13" class="d" xml:space="preserve">Codes: C - connected (now), '
             f'O - OSPF (learning), S - static (next)</text>')
    o.append(f'<line x1="30" y1="60" x2="{W-30}" y2="60" stroke="{DIM}" stroke-opacity=".35"/>')
    for i, (code, net, name, what, col) in enumerate(FOCUS):
        y = 92 + i * 38
        o.append(f'<text x="30" y="{y}" font-size="16" xml:space="preserve">'
                 f'<tspan fill="{col}" class="bold">{code}</tspan>'
                 f'<tspan class="d">   {net}   via   </tspan>'
                 f'<tspan fill="{col}" class="bold">{esc(name):<18}</tspan>'
                 f'<tspan class="v"> {esc(what)}</tspan></text>')
    o.append(f'<text x="30" y="{H-24}" font-size="14" xml:space="preserve"><tspan class="p bold">R1-UPT</tspan>'
             f'<tspan class="d">#</tspan> <tspan class="cur gr">█</tspan></text>')
    save("assets/focus.svg", o)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        for i in range(len(scenes.SCENES)):
            header(i, f"{sys.argv[2]}/scene{i}.svg")
        sys.exit()
    header()
    for n, cmd, t in [("deepdive", "show tech-support", "Technical Deep Dive"),
                      ("projects", "show interfaces status", "Project Portfolio"),
                      ("stack", "show inventory", "Tech Stack"),
                      ("stats", "show interfaces counters", "GitHub Stats"),
                      ("focus", "show ip route", "Current Focus"),
                      ("contact", "show cdp neighbors detail", "Contact")]:
        section(n, cmd, t)
    deepdive()
    for i, p in enumerate(PROJECTS):
        project_card(i, p)
    focus()
    print("assets generated")
