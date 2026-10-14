"""Les trois logos d'offres : Essentielle (1), Premium (2), Sur mesure (3)."""
import math, os
import build_logo as L

OUT = os.path.join(L.HERE, "..", "svg")
R = 500.0
CX = CY = R

OFFERS = [
    dict(key="essentielle", name="ESSENTIELLE", tier=1, stops=("#FFC93C", "#FF8A1F"), disc="#F6F1E7",
         text=L.INK, off="#E2DAC8", tag="Essentielle"),
    dict(key="premium", name="PREMIUM", tier=2, stops=("#FF7A2E", "#EE2A7B"), disc=L.INK,
         text=L.LIGHT, off="#3B3643", tag="Premium"),
    dict(key="sur-mesure", name="SUR MESURE", tier=3, stops=("#EE2A7B", "#7B3FF2"), disc="#0D0B11",
         text=L.LIGHT, off="#3B3643", tag="Sur mesure", accent="#FFD36B"),
]
SPARK = "M0 -1C.1 -.34 .34 -.1 1 0C.34 .1 .1 .34 0 1C-.1 .34 -.34 .1 -1 0C-.34 -.1 -.1 -.34 0 -1Z"


def grad(gid, stops, vertical=False):
    x2, y2 = ("0", "1") if vertical else ("1", "1")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{stops[0]}"/>'
            f'<stop offset="1" stop-color="{stops[1]}"/></linearGradient>')


def drop_g(x, y, h, fill, hilite=True, opacity=1.0):
    k = h / L.DH
    tx, ty = x - L.DROP_BOX[0] * k, y - L.DROP_BOX[1] * k
    body = f'<path fill="{fill}" d="{L.DROP_PATH}"/>'
    if hilite:
        body += f'<path fill="#fff" fill-opacity=".8" d="{L.HILITE}"/>'
    return f'<g opacity="{opacity}" transform="translate({tx:.3f} {ty:.3f}) scale({k:.5f})">{body}</g>', L.DW * k


def ring_text(face, txt, size, track, r_base, centre, clockwise):
    glyphs, adv = face.shape(txt, size, track)
    parts = []
    for name, gx, ga in glyphs:
        s_mid = gx + ga / 2 - adv / 2
        th = centre + (s_mid if clockwise else -s_mid) / r_base
        rot = th + math.pi / 2 if clockwise else th - math.pi / 2
        px, py = CX + r_base * math.cos(th), CY + r_base * math.sin(th)
        ox, oy = px - (ga / 2) * math.cos(rot), py - (ga / 2) * math.sin(rot)
        d = face.path(name, ox, oy, size, rot)
        if d:
            parts.append(d)
    return " ".join(parts)


def sparkle(x, y, r, fill):
    return f'<path fill="{fill}" transform="translate({x:.1f} {y:.1f}) scale({r:.1f})" d="{SPARK}"/>'


def emblem(o):
    gid, rid = f"g_{o['key']}", f"r_{o['key']}"
    defs = grad(gid, o["stops"]) + grad(rid, o["stops"], vertical=True)
    t = o["tier"]
    fillg = f"url(#{gid})"
    body = f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="{o["disc"]}"/>'
    # anneaux : de plus en plus riches
    body += f'<circle cx="{CX}" cy="{CY}" r="{R * 0.945}" fill="none" stroke="url(#{rid})" stroke-width="{R * (0.028 if t == 1 else 0.034)}"/>'
    if t >= 2:
        body += f'<circle cx="{CX}" cy="{CY}" r="{R * 0.885}" fill="none" stroke="{o["stops"][0]}" stroke-opacity=".55" stroke-width="{R * 0.008}"/>'
    if t >= 3:
        body += (f'<circle cx="{CX}" cy="{CY}" r="{R * 0.915}" fill="none" stroke="{o["accent"]}" stroke-opacity=".9" '
                 f'stroke-width="{R * 0.01}" stroke-dasharray="{R * 0.012} {R * 0.03}" stroke-linecap="round"/>')
    # texte en arc : JUICECRAFT en haut, nom de l'offre en bas
    size = R * 0.118
    r_in = R * 0.665
    capH = 0.70 * size
    r_out = r_in + capH
    top = ring_text(L.MONA7, "JUICECRAFT", size, 0.20, r_in, -math.pi / 2, True)
    bot = ring_text(L.MONA7, o["name"], size, 0.20, r_out, math.pi / 2, False)
    body += f'<path fill="{o["text"]}" fill-opacity=".92" d="{top}"/>'
    body += f'<path fill="{fillg}" d="{bot}"/>'
    # petites gouttes séparatrices à 9 h et 3 h
    for ang in (math.pi, 0.0):
        px, py = CX + (r_in + capH / 2) * math.cos(ang), CY + (r_in + capH / 2) * math.sin(ang)
        sh = capH * 1.15
        g, _ = drop_g(px - L.DW * sh / L.DH / 2, py - sh / 2, sh, fillg, hilite=False)
        body += g
    body += f'<circle cx="{CX}" cy="{CY}" r="{r_in - capH * 0.45:.1f}" fill="none" stroke="{o["text"]}" stroke-opacity=".16" stroke-width="{R * 0.008}"/>'
    # halo derrière la goutte (premium et au-dessus)
    if t >= 2:
        body += (f'<defs><radialGradient id="h_{o["key"]}"><stop offset="0" stop-color="{o["stops"][1]}" stop-opacity="{.42 if t == 2 else .55}"/>'
                 f'<stop offset="1" stop-color="{o["stops"][1]}" stop-opacity="0"/></radialGradient></defs>'
                 f'<circle cx="{CX}" cy="{CY - R * 0.05}" r="{R * 0.42}" fill="url(#h_{o["key"]})"/>')
    # goutte centrale
    dh = R * 0.50
    g, dw = drop_g(CX - L.DW * dh / L.DH / 2, CY - dh * 0.62, dh, fillg)
    body += g
    # étincelles
    if t == 2:
        body += sparkle(CX + dw * 0.78, CY - dh * 0.5, R * 0.065, "#FFD36B" if False else o["stops"][0])
    if t == 3:
        body += sparkle(CX + dw * 0.80, CY - dh * 0.55, R * 0.085, o["accent"])
        body += sparkle(CX - dw * 0.86, CY - dh * 0.28, R * 0.05, o["accent"])
        body += sparkle(CX + dw * 1.02, CY - dh * 0.14, R * 0.035, o["accent"])
    # rangée de trois gouttes : le niveau de l'offre (1, 2 ou 3 remplies)
    ph = R * 0.1
    gap = ph * 1.05
    total = 3 * (L.DW * ph / L.DH) + 2 * gap
    x0 = CX - total / 2
    for i in range(3):
        on = i < t
        pg, pw = drop_g(x0 + i * (L.DW * ph / L.DH + gap), CY + R * 0.205, ph,
                        fillg if on else o["off"], hilite=False)
        body += pg
    return defs, body


def svg(w, h, defs, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title><defs>{defs}</defs>{body}</svg>\n')


def save(name, content):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(content)


for o in OFFERS:
    defs, body = emblem(o)
    save(f"juicecraft_offre-{o['key']}_emblème.svg".replace("è", "e"), svg(2 * R, 2 * R, defs, body, f"juicecraft {o['tag']}"))

    # lockup horizontal : emblème + juicecraft + nom de l'offre en couleur
    F = 300.0
    glyphs, adv = L.MONA.shape("juicecraft", F, L.WORD_TRACK)
    ys0, ys1, xs0, xs1 = 1e9, -1e9, 1e9, -1e9
    for n, gx, _ in glyphs:
        b = L.MONA.bounds(n, gx, F)
        if b:
            ys0 = min(ys0, -b[3]); ys1 = max(ys1, -b[1]); xs0 = min(xs0, b[0]); xs1 = max(xs1, b[2])
    wh = ys1 - ys0
    tag_size = F * 0.40
    tg, tadv = L.MONA7.shape(o["name"], tag_size, 0.26)
    ty0, ty1 = 1e9, -1e9
    for n, gx, _ in tg:
        b = L.MONA7.bounds(n, gx, tag_size)
        if b:
            ty0 = min(ty0, -b[3]); ty1 = max(ty1, -b[1])
    th = ty1 - ty0
    block = wh + F * 0.20 + th
    pad = 2 * R * 0.0 + 60
    emb_h = 2 * R
    ex = pad
    top = pad + (emb_h - block) / 2
    wx = ex + 2 * R + 110
    wsvg = "".join(f'<path d="{L.MONA.path(n, wx - xs0 + gx, top - ys0, F)}"/>' for n, gx, _ in glyphs if L.MONA.path(n, 0, 0, F))
    tx0 = wx - 0
    tsvg = "".join(f'<path d="{L.MONA7.path(n, tx0 + gx, top + wh + F * 0.20 - ty0, tag_size)}"/>' for n, gx, _ in tg if L.MONA7.path(n, 0, 0, tag_size))
    W = wx + (xs1 - xs0) + pad
    Hh = emb_h + 2 * pad
    lock_defs = defs
    lock_body = (f'<g transform="translate({ex} {pad})">{body}</g>'
                 f'<g fill="{L.INK}">{wsvg}</g><g fill="url(#g_{o["key"]})">{tsvg}</g>')
    save(f"juicecraft_offre-{o['key']}_logo-horizontal.svg", svg(W, Hh, lock_defs, lock_body, f"juicecraft {o['tag']}"))
    dark_body = (f'<g transform="translate({ex} {pad})">{body}</g>'
                 f'<g fill="{L.LIGHT}">{wsvg}</g><g fill="url(#g_{o["key"]})">{tsvg}</g>')
    save(f"juicecraft_offre-{o['key']}_logo-horizontal_fond-sombre.svg", svg(W, Hh, lock_defs, dark_body, f"juicecraft {o['tag']}"))
print("offres :", [f for f in os.listdir(OUT) if "offre" in f])
