"""Animated left panel for header.svg: 7 scenes that cross-fade in a loop.

Network -> Cyber -> Automotive -> Full-Stack -> Hardware -> Cloud -> Mobile
Each scene is drawn in local coordinates (0..W, 0..H) and translated into the panel.
"""
BG, PANEL2 = "#0b0e17", "#161a29"
CYAN, BLUE, PINK, GREEN, YEL, RED = "#7dcfff", "#7aa2f7", "#bb9af7", "#9ece6a", "#e0af68", "#f7768e"
DIM, TXT = "#565f89", "#c0caf5"

SCENE_T = 4          # seconds per scene
W, H = 350, 400      # panel size


def css(n):
    total = SCENE_T * n
    win = 100 / n
    return f"""
    .sc {{ opacity: 0; animation: show {total}s linear infinite both; }}
    .sc.only {{ opacity: 1; animation: none; }}
    @keyframes show {{
      0% {{ opacity: 0; }} {win*0.1:.2f}% {{ opacity: 1; }}
      {win*0.9:.2f}% {{ opacity: 1; }} {win:.2f}% {{ opacity: 0; }} 100% {{ opacity: 0; }}
    }}
    .spin {{ animation: spin 1s linear infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    .clk {{ animation: clk 1.2s linear infinite; }}
    @keyframes clk {{ to {{ stroke-dashoffset: -40; }} }}
    .road {{ animation: road .6s linear infinite; }}
    @keyframes road {{ to {{ stroke-dashoffset: 28; }} }}
    """


# ───────── primitives ─────────
def path(d, color, w=1.6, op=.55, dash=None, cls=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    c = f' class="{cls}"' if cls else ""
    return f'<path d="{d}" stroke="{color}" stroke-opacity="{op}" stroke-width="{w}" fill="none"{da}{c}/>'


def packet(d, color, dur, delay=0, r=3.5, bounce=True, fade_end=False):
    kp = 'keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"' if bounce else ""
    fade = (f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.85;.95;1" '
            f'dur="{dur}s" begin="-{delay}s" repeatCount="indefinite"/>') if fade_end else ""
    return (f'<circle r="{r}" fill="{color}" filter="url(#glow)">'
            f'<animateMotion path="{d}" dur="{dur}s" begin="-{delay}s" repeatCount="indefinite" {kp}/>{fade}</circle>')


def wire(d, color, dur, delay=0, dash=None, **kw):
    return path(d, color, dash=dash) + packet(d, color, dur, delay, **kw)


def box(x, y, w, h, color, label, fs=11, rx=5, fill=PANEL2):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{color}" stroke-width="1.5"/>'
            f'<text x="{x + w/2}" y="{y + h/2 + fs*.36:.1f}" text-anchor="middle" font-size="{fs}" fill="{color}">{label}</text>')


def txt(x, y, s, color, fs=11, anchor="middle", bold=False):
    b = ' font-weight="700"' if bold else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{color}"{b}>{s}</text>'


def blink(delay, dur=1.6):
    return (f'<animate attributeName="opacity" values="1;.3;1" dur="{dur}s" begin="{delay}s" '
            f'repeatCount="indefinite"/>')


# ───────── scenes ─────────
def s_network():
    o = []
    cx = W / 2
    # cloud
    o.append(f'<path transform="translate({cx},78)" d="M-38 10 a14 14 0 0 1 4 -27 a20 20 0 0 1 36 -6 '
             f'a16 16 0 0 1 30 10 a12 12 0 0 1 -2 23 z" fill="{PANEL2}" stroke="{PINK}" stroke-width="1.6"/>')
    o.append(txt(cx, 82, "Internet", PINK, 12))
    r1, s1, s2 = (cx, 150), (cx - 85, 225), (cx + 85, 225)
    hosts = [(s1[0] - 42, 300, "PC-A", PINK), (s1[0] + 38, 300, "PC-B", PINK),
             (s2[0] - 38, 300, "SRV", GREEN), (s2[0] + 42, 300, "PC-C", PINK)]
    o.append(wire(f"M{cx} 90 L{cx} 136", PINK, 2.2, dash="4 4"))
    o.append(wire(f"M{cx-18} 162 L{s1[0]} 213", CYAN, 2.6, .3))
    o.append(wire(f"M{cx+18} 162 L{s2[0]} 213", CYAN, 2.9, .8))
    o.append(wire(f"M{s1[0]+34} 225 L{s2[0]-34} 225", YEL, 3.4, .4, dash="4 4"))
    for i, (hx, hy, _, _) in enumerate(hosts):
        sw = s1 if i < 2 else s2
        o.append(wire(f"M{sw[0]} 237 L{hx} {hy-14}", BLUE, 2 + i * .3, i * .35))
    # router
    o.append(f'<g transform="translate({cx},{r1[1]})">'
             f'<rect x="-30" y="-6" width="60" height="12" fill="{PANEL2}"/>'
             f'<ellipse cx="0" cy="6" rx="30" ry="10" fill="{PANEL2}" stroke="{CYAN}" stroke-width="1.6"/>'
             f'<rect x="-29" y="-6" width="58" height="12" fill="{PANEL2}"/>'
             f'<path d="M-30 -6 v12 M30 -6 v12" stroke="{CYAN}" stroke-width="1.6"/>'
             f'<ellipse cx="0" cy="-6" rx="30" ry="10" fill="{PANEL2}" stroke="{CYAN}" stroke-width="1.6"/>'
             f'<path d="M-14 -9 l8 3 M14 -3 l-8 -3 M-4 -12 l3 6 M4 0 l-3 -6" stroke="{CYAN}" stroke-width="1.6" stroke-linecap="round"/>'
             f'</g>')
    o.append(txt(cx + 46, r1[1] + 4, "R1", CYAN, 12, "start"))
    for (sx, sy), lab in ((s1, "VLAN 10"), (s2, "VLAN 20")):
        o.append(f'<rect x="{sx-34}" y="{sy-12}" width="68" height="24" rx="4" fill="{PANEL2}" stroke="{BLUE}" stroke-width="1.6"/>')
        for k in range(6):
            o.append(f'<rect x="{sx-26+k*9}" y="{sy+2}" width="5" height="4" rx="1" fill="{GREEN}">{blink(k*.2)}</rect>')
        o.append(f'<path d="M{sx-20} {sy-5} h14 l-3 -3 M{sx+20} {sy-2} h-14 l3 3" stroke="{BLUE}" stroke-width="1.4" fill="none"/>')
        o.append(txt(sx, sy - 18, lab, BLUE, 11))
    for hx, hy, lab, col in hosts:
        o.append(f'<rect x="{hx-16}" y="{hy-14}" width="32" height="22" rx="3" fill="{PANEL2}" stroke="{col}" stroke-width="1.5"/>'
                 f'<rect x="{hx-11}" y="{hy-9}" width="22" height="12" rx="1" fill="{col}" fill-opacity=".2"/>'
                 f'<path d="M{hx-8} {hy+12} h16 M{hx} {hy+8} v4" stroke="{col}" stroke-width="1.5"/>')
        o.append(txt(hx, hy + 28, lab, col, 10))
    return o, "NETWORKING", CYAN, "OSPF · VLANs · GNS3 automation"


def s_cyber():
    o = []
    # WAN / LAN zones
    o.append(txt(52, 76, "WAN", RED, 12, bold=True))
    o.append(txt(298, 76, "LAN", GREEN, 12, bold=True))
    # firewall wall
    for r in range(9):
        y = 92 + r * 22
        off = 0 if r % 2 == 0 else 6
        for c in range(2):
            o.append(f'<rect x="{150 + off + c*22}" y="{y}" width="20" height="20" rx="2" '
                     f'fill="{RED}" fill-opacity=".14" stroke="{RED}" stroke-opacity=".7"/>')
    # shield on top of the wall
    o.append(f'<path d="M175 50 l26 9 v14 c0 16 -12 25 -26 30 c-14 -5 -26 -14 -26 -30 v-14 z" '
             f'fill="{BG}" stroke="{CYAN}" stroke-width="1.8"/>')
    o.append(f'<rect x="166" y="72" width="18" height="13" rx="2" fill="{CYAN}" fill-opacity=".25" stroke="{CYAN}" stroke-width="1.4"/>'
             f'<path d="M169 72 v-5 a6 6 0 0 1 12 0 v5" stroke="{CYAN}" stroke-width="1.6" fill="none"/>')
    lanes = [110, 146, 182, 218, 254, 290]
    for i, y in enumerate(lanes):
        o.append(path(f"M30 {y} L320 {y}", DIM, 1, .35, "2 5"))
        if i % 2 == 0:   # allowed traffic passes through
            o.append(packet(f"M30 {y} L320 {y}", GREEN, 2.6, i * .3, bounce=False))
        else:            # malicious traffic dropped at the wall
            o.append(packet(f"M30 {y} L150 {y}", RED, 1.8, i * .25, bounce=False, fade_end=True))
            o.append(f'<text x="138" y="{y+4}" text-anchor="middle" font-size="12" fill="{RED}" font-weight="700" opacity="0">✕'
                     f'<animate attributeName="opacity" values="0;0;1;0" keyTimes="0;.8;.9;1" dur="1.8s" '
                     f'begin="-{i*.25}s" repeatCount="indefinite"/></text>')
    o.append(txt(260, 322, "permit tcp any eq 443", GREEN, 10))
    o.append(txt(100, 322, "deny ip any any log", RED, 10))
    return o, "CYBERSECURITY", RED, "ACLs · firewalls · secure coding"


def s_automotive():
    o = []
    # car body
    o.append(f'<path d="M40 160 L62 128 Q92 96 140 94 L218 94 Q252 98 280 126 L314 136 Q328 142 322 160 Z" '
             f'fill="{PANEL2}" stroke="{YEL}" stroke-width="1.8"/>')
    o.append(f'<path d="M100 126 Q118 104 145 104 L170 104 L170 126 Z M180 104 L214 104 Q236 108 256 126 L180 126 Z" '
             f'fill="{CYAN}" fill-opacity=".12" stroke="{CYAN}" stroke-opacity=".6"/>')
    for wx in (98, 264):
        o.append(f'<circle cx="{wx}" cy="162" r="17" fill="{BG}" stroke="{YEL}" stroke-width="2"/>')
        o.append(f'<g class="spin"><circle cx="{wx}" cy="162" r="9" fill="none" stroke="{DIM}" stroke-width="1.4"/>'
                 f'<path d="M{wx-9} 162 h18 M{wx} 153 v18" stroke="{YEL}" stroke-width="1.6"/></g>')
    o.append(path("M20 184 L330 184", DIM, 2, .7, "14 14", "road"))
    # CAN bus
    o.append(path("M30 258 L320 258", YEL, 2, .8))
    o.append(path("M30 266 L320 266", PINK, 2, .8))
    o.append(txt(30, 284, "CAN_H", YEL, 9, "start"))
    o.append(txt(30, 296, "CAN_L", PINK, 9, "start"))
    ecus = [(42, "ECU"), (112, "ABS"), (182, "ENG"), (252, "IVI")]
    for i, (x, lab) in enumerate(ecus):
        o.append(box(x, 208, 56, 26, YEL if i != 3 else CYAN, lab, 11))
        o.append(path(f"M{x+28} 234 L{x+28} 258", YEL, 1.4, .8))
        o.append(f'<circle cx="{x+46}" cy="214" r="2.5" fill="{GREEN}">{blink(i*.3, 1)}</circle>')
    for i in range(3):
        d = "M30 262 L320 262" if i % 2 == 0 else "M320 262 L30 262"
        o.append(f'<rect x="-9" y="-5" width="18" height="10" rx="2" fill="{YEL}" filter="url(#glow)">'
                 f'<animateMotion path="{d}" dur="2.4s" begin="-{i*.8}s" repeatCount="indefinite"/></rect>')
    o.append(txt(W/2, 322, "ID 0x1A4 · DLC 8 · 500 kbit/s", DIM, 10))
    return o, "AUTOMOTIVE", YEL, "ECUs · CAN bus · RTOS"


def s_fullstack():
    o = []
    # browser
    o.append(f'<rect x="70" y="62" width="210" height="88" rx="8" fill="{PANEL2}" stroke="{GREEN}" stroke-width="1.6"/>')
    o.append(f'<path d="M70 80 h210" stroke="{GREEN}" stroke-opacity=".6"/>')
    for k, c in enumerate((RED, YEL, GREEN)):
        o.append(f'<circle cx="{82+k*10}" cy="71" r="3" fill="{c}"/>')
    o.append(txt(200, 75, "clarity-gym.app", DIM, 9))
    for k, (w, c) in enumerate(((120, GREEN), (160, DIM), (90, DIM))):
        o.append(f'<rect x="84" y="{92+k*16}" width="{w}" height="8" rx="4" fill="{c}" fill-opacity=".5">'
                 f'<animate attributeName="width" values="0;{w};{w}" keyTimes="0;.4;1" dur="2s" begin="{k*.25}s" repeatCount="indefinite"/></rect>')
    o.append(txt(262, 142, "Vue 3", GREEN, 10, "end"))
    # API
    o.append(box(110, 186, 130, 34, CYAN, "Go API :8080", 12))
    # DB cylinder
    o.append(f'<path d="M120 260 v40 a55 12 0 0 0 110 0 v-40" fill="{PANEL2}" stroke="{BLUE}" stroke-width="1.6"/>')
    o.append(f'<ellipse cx="175" cy="260" rx="55" ry="12" fill="{PANEL2}" stroke="{BLUE}" stroke-width="1.6"/>')
    o.append(f'<path d="M120 278 a55 12 0 0 0 110 0" fill="none" stroke="{BLUE}" stroke-opacity=".5"/>')
    o.append(txt(175, 300, "PostgreSQL", BLUE, 11))
    o.append(wire("M175 150 L175 186", GREEN, 1.6))
    o.append(wire("M175 220 L175 248", CYAN, 1.6, .4))
    o.append(txt(186, 172, "GET /api/members", DIM, 9, "start"))
    o.append(txt(186, 238, "SELECT …", DIM, 9, "start"))
    # JWT token
    o.append(f'<g><rect x="262" y="194" width="44" height="18" rx="9" fill="{PINK}" fill-opacity=".15" stroke="{PINK}"/>'
             f'<text x="284" y="207" text-anchor="middle" font-size="10" fill="{PINK}">JWT</text>{blink(0, 1.4)}</g>')
    return o, "FULL-STACK", GREEN, "Vue 3 · Go · PostgreSQL"


def s_hardware():
    o = []
    # clock signal
    sq = "M30 82 " + " ".join(f"h10 v-14 h10 v14" for _ in range(14))
    o.append(path(sq, CYAN, 1.6, .9, "160 0"))
    o.append(f'<path d="{sq}" stroke="{CYAN}" stroke-width="2.2" fill="none" stroke-dasharray="12 28" class="clk" filter="url(#glow)"/>')
    o.append(txt(320, 62, "CLK", CYAN, 10, "end"))
    # chip
    cx, cy, s = 175, 200, 110
    x0, y0 = cx - s / 2, cy - s / 2
    for k in range(7):
        p = x0 + 12 + k * 14
        for d in (f"M{p} {y0} v-12", f"M{p} {y0+s} v12", f"M{x0} {y0+12+k*14} h-12", f"M{x0+s} {y0+12+k*14} h12"):
            o.append(path(d, PINK, 2.4, .9))
    traces = [
        f"M{x0+12} {y0-12} V108 H40", f"M{x0+96} {y0-12} V108 H310",
        f"M{x0-12} {y0+40} H60 V250 H30", f"M{x0+s+12} {y0+40} H290 V250 H320",
        f"M{x0+26} {y0+s+12} V300 H50", f"M{x0+82} {y0+s+12} V300 H300",
        f"M{x0+54} {y0+s+12} V320",
    ]
    for i, d in enumerate(traces):
        o.append(path(d, BLUE, 1.4, .5))
        o.append(packet(d, CYAN if i % 2 else PINK, 1.8 + (i % 3) * .4, i * .25, r=2.8, bounce=False))
    o.append(f'<rect x="{x0}" y="{y0}" width="{s}" height="{s}" rx="8" fill="{PANEL2}" stroke="{PINK}" stroke-width="2"/>')
    o.append(f'<circle cx="{x0+14}" cy="{y0+14}" r="4" fill="none" stroke="{DIM}"/>')
    o.append(txt(cx, cy - 4, "8086", PINK, 22, bold=True))
    o.append(txt(cx, cy + 16, "ALU · SystemC", DIM, 10))
    return o, "HARDWARE", PINK, "x86 Assembly · SystemC · ALUs"


def s_cloud():
    o = []
    o.append(f'<path transform="translate(175,102) scale(1.9)" d="M-38 10 a14 14 0 0 1 4 -27 a20 20 0 0 1 36 -6 '
             f'a16 16 0 0 1 30 10 a12 12 0 0 1 -2 23 z" fill="{PANEL2}" stroke="{BLUE}" stroke-width="1"/>')
    o.append(txt(175, 96, "CLOUD", BLUE, 14, bold=True))
    o.append(txt(175, 114, "k8s · storage · inference", DIM, 9))
    # racks inside cloud
    for k in range(3):
        o.append(f'<rect x="{147+k*20}" y="122" width="14" height="8" rx="1" fill="{BLUE}" fill-opacity=".35">{blink(k*.3, 1.2)}</rect>')
    nodes = [(70, 270), (175, 290), (280, 270)]
    for i, (nx, ny) in enumerate(nodes):
        d = f"M{nx} {ny-18} Q{(nx+175)/2} {200} 175 {150}"
        o.append(path(d, CYAN, 1.4, .5, "4 4"))
        o.append(packet(d, CYAN, 1.9 + i * .3, i * .4, bounce=False))
        o.append(packet(f"M175 150 Q{(nx+175)/2} 200 {nx} {ny-18}", PINK, 2.4 + i * .2, .9 + i * .3, r=2.6, bounce=False))
        o.append(f'<rect x="{nx-28}" y="{ny-18}" width="56" height="36" rx="6" fill="{PANEL2}" stroke="{CYAN}" stroke-width="1.5"/>')
        # tiny neural net glyph
        for a in (-12, 0, 12):
            o.append(f'<circle cx="{nx-12}" cy="{ny+a/2-2}" r="2" fill="{CYAN}"/>')
            o.append(f'<circle cx="{nx+12}" cy="{ny+a/2-2}" r="2" fill="{PINK}"/>')
            for b in (-12, 0, 12):
                o.append(f'<path d="M{nx-12} {ny+a/2-2} L{nx+12} {ny+b/2-2}" stroke="{DIM}" stroke-width=".6"/>')
        o.append(txt(nx, ny + 32, f"edge-{i+1}", CYAN, 10))
    return o, "CLOUD &amp; EDGE", BLUE, "edge nodes · small ML models"


def s_mobile():
    o = []
    px, py, pw, ph = 118, 58, 114, 230
    o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="20" fill="{PANEL2}" stroke="{PINK}" stroke-width="2"/>')
    o.append(f'<rect x="{px+40}" y="{py+8}" width="34" height="8" rx="4" fill="{BG}"/>')
    o.append(f'<rect x="{px+8}" y="{py+24}" width="{pw-16}" height="{ph-50}" rx="8" fill="{BG}"/>')
    o.append(txt(px + 16, py + 42, "My app", PINK, 11, "start", True))
    cols = (CYAN, GREEN, YEL, BLUE)
    for k in range(4):
        y = py + 52 + k * 38
        o.append(f'<g opacity="0"><rect x="{px+16}" y="{y}" width="{pw-32}" height="30" rx="6" fill="{cols[k]}" fill-opacity=".15" stroke="{cols[k]}" stroke-opacity=".7"/>'
                 f'<circle cx="{px+30}" cy="{y+15}" r="7" fill="{cols[k]}" fill-opacity=".6"/>'
                 f'<rect x="{px+42}" y="{y+9}" width="44" height="5" rx="2" fill="{TXT}" fill-opacity=".6"/>'
                 f'<rect x="{px+42}" y="{y+18}" width="28" height="4" rx="2" fill="{DIM}"/>'
                 f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{k*.15:.2f};{k*.15+.12:.2f};.92;1" dur="4s" repeatCount="indefinite"/></g>')
    for k in range(3):
        o.append(f'<circle cx="{px+37+k*20}" cy="{py+ph-14}" r="3" fill="{PINK if k == 0 else DIM}"/>')
    # signal waves
    for k in range(3):
        r = 14 + k * 12
        o.append(f'<path d="M{270 - r*.7:.1f} {96 - r*.7:.1f} A{r} {r} 0 0 1 {270 + r*.7:.1f} {96 - r*.7:.1f}" stroke="{CYAN}" '
                 f'stroke-width="2" fill="none" stroke-linecap="round">'
                 f'<animate attributeName="opacity" values=".1;1;.1" dur="1.5s" begin="{k*.25}s" repeatCount="indefinite"/></path>')
    o.append(f'<circle cx="270" cy="96" r="3" fill="{CYAN}"/>')
    o.append(wire("M232 160 L300 160 L300 250", CYAN, 2.2, dash="3 4"))
    o.append(box(270, 252, 60, 26, CYAN, "REST", 11))
    o.append(path("M118 200 L60 200 L60 250", GREEN, 1.4, .5, "3 4"))
    o.append(box(30, 252, 60, 26, GREEN, "SQLite", 10))
    return o, "MOBILE", PINK, "mobile app design · REST APIs"


SCENES = [s_network, s_cyber, s_automotive, s_fullstack, s_hardware, s_cloud, s_mobile]


def build(bx, by, only=None):
    n = len(SCENES)
    o = [f'<g transform="translate({bx},{by})">',
         f'<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="url(#g)" stroke-opacity=".6"/>',
         '<g fill="#1f2335">' + "".join(f'<circle cx="{x}" cy="{y}" r="1"/>'
                                        for x in range(15, W, 20) for y in range(15, H, 20)) + "</g>"]
    seg = (W - 40 - (n - 1) * 6) / n
    for i, fn in enumerate(SCENES):
        if only is not None and i != only:
            continue
        body, name, col, caption = fn()
        cls = "sc only" if only is not None else "sc"
        o.append(f'<g class="{cls}" style="animation-delay:{i*SCENE_T}s">')
        o.append(txt(16, 26, f"[{i+1:02}/{n:02}] {name}", col, 12, "start", True))
        o.append(f'<circle cx="{W-56}" cy="22" r="3.5" fill="{GREEN}">{blink(0, 1)}</circle>')
        o.append(txt(W - 16, 26, "live", GREEN, 11, "end"))
        o.extend(body)
        o.append(txt(W / 2, 352, caption, TXT, 12))
        o.append(f'<rect x="{20 + i*(seg+6):.1f}" y="372" width="{seg:.1f}" height="5" rx="2.5" fill="{col}" filter="url(#glow)"/>')
        o.append("</g>")
    # progress track (under the active segment)
    o.insert(3, "".join(f'<rect x="{20 + i*(seg+6):.1f}" y="372" width="{seg:.1f}" height="5" rx="2.5" fill="#1f2335"/>'
                        for i in range(n)))
    o.append("</g>")
    return o
