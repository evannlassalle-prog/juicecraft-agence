"""juicecraft : génère tout le kit de logos en SVG vectoriel (texte converti en tracés).
python3 build_logo.py  ->  ../svg/*.svg
"""
import math, os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "svg")
os.makedirs(OUT, exist_ok=True)

INK, PAPER, LIGHT = "#131116", "#F2F2EF", "#F3F1F5"
MANGO, ORANGE, BERRY, GRAPE = "#FFB21A", "#FF5A1F", "#EE2A7B", "#7B3FF2"
WORD_TRACK = -0.045     # em, identique au site
DROP_PATH = "M16 2.5S6.5 12.6 6.5 19.4a9.5 9.5 0 0 0 19 0C25.5 12.6 16 2.5 16 2.5Z"
HILITE = "M11.2 19.6c.2-2.6 1.6-5 3.1-6.8.4-.5-.2-1-.7-.7-2 1.8-3.6 4.5-3.8 7.3-.1 1 1.3 1.2 1.4.2Z"
DROP_BOX = (6.5, 2.5, 25.5, 28.9)       # emprise visible de la goutte dans son repère 32x32
DW, DH = DROP_BOX[2] - DROP_BOX[0], DROP_BOX[3] - DROP_BOX[1]


# ------------------------------------------------------------------ texte -> tracés
class Face:
    def __init__(self, ttf):
        self.tt = TTFont(os.path.join(HERE, ttf))
        self.upem = self.tt["head"].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        blob = hb.Blob.from_file_path(os.path.join(HERE, ttf))
        self.hbf = hb.Font(hb.Face(blob))

    def shape(self, text, size, track=0.0):
        """liste [(d, x, advance)] + largeur, bbox verticale. Origine = ligne de base, y vers le haut."""
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.hbf, buf, {"kern": True, "liga": False})
        s = size / self.upem
        x, out = 0.0, []
        n = len(buf.glyph_infos)
        for i, (inf, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            name = self.tt.getGlyphName(inf.codepoint)
            out.append((name, x + pos.x_offset * s, pos.x_advance * s))
            x += pos.x_advance * s + (track * size if i < n - 1 else 0)
        return out, x

    def path(self, name, x, y, size, rot=0.0):
        """tracé SVG d'un glyphe dont l'origine (ligne de base, début du glyphe) est posée en (x, y)."""
        s = size / self.upem
        c, si = math.cos(rot), math.sin(rot)
        xx, xy, yx, yy = s * c, s * si, s * si, -s * c        # glyphe (y vers le haut) -> SVG (y vers le bas), tourné de rot
        pen = SVGPathPen(self.gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        self.gs[name].draw(TransformPen(pen, (xx, xy, yx, yy, x, y)))
        return pen.getCommands()

    def bounds(self, name, x, size):
        s = size / self.upem
        bp = BoundsPen(self.gs); self.gs[name].draw(bp)
        if bp.bounds is None:
            return None
        x0, y0, x1, y1 = bp.bounds
        return (x + x0 * s, y0 * s, x + x1 * s, y1 * s)   # y vers le haut


MONA = Face("MonaSans-800-108.ttf")
MONA7 = Face("MonaSans-700-100.ttf")


def word(face, text, size, track, x0, base_y, fill):
    """mot complet en tracés ; renvoie (svg, bbox x0,y0,x1,y1 en coord. SVG)."""
    glyphs, adv = face.shape(text, size, track)
    parts, bx0, by0, bx1, by1 = [], 1e9, 1e9, -1e9, -1e9
    for name, gx, _ in glyphs:
        d = face.path(name, x0 + gx, base_y, size)
        if d:
            parts.append(d)
        b = face.bounds(name, x0 + gx, size)
        if b:
            bx0 = min(bx0, b[0]); bx1 = max(bx1, b[2])
            by0 = min(by0, base_y - b[3]); by1 = max(by1, base_y - b[1])
    svg = f'<path fill="{fill}" d="{" ".join(parts)}"/>'
    return svg, (bx0, by0, bx1, by1)


def word_glyphs(face, text, size, track, x0, base_y):
    """une liste de tracés par lettre (pour l'animation)."""
    glyphs, _ = face.shape(text, size, track)
    return [(face.path(n, x0 + gx, base_y, size), face.bounds(n, x0 + gx, size)) for n, gx, _ in glyphs]


# ------------------------------------------------------------------ goutte
def drop(x, y, h, mode="color", uid="a", rot=0.0):
    """goutte dont l'emprise visible a pour coin haut-gauche (x, y) et pour hauteur h.
    mode : 'color' (dégradé + reflet) | 'simple' (dégradé sans reflet) | '#hex' (aplat) | 'cut:#hex' (aplat, reflet évidé)
    renvoie (defs, svg, largeur)"""
    k = h / DH
    tx, ty = x - DROP_BOX[0] * k, y - DROP_BOX[1] * k
    g = f'<g transform="translate({tx:.3f} {ty:.3f}) scale({k:.5f})">'
    defs = ""
    if mode in ("color", "simple"):
        defs = (f'<linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MANGO}"/>'
                f'<stop offset=".45" stop-color="{ORANGE}"/><stop offset="1" stop-color="{BERRY}"/></linearGradient>')
        body = f'<path fill="url(#g{uid})" d="{DROP_PATH}"/>'
        if mode == "color":
            body += f'<path fill="#fff" fill-opacity=".8" d="{HILITE}"/>'
    elif mode.startswith("cut:"):
        col = mode[4:]
        defs = (f'<mask id="m{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="32" height="32"><rect width="32" height="32" fill="#fff"/>'
                f'<path fill="#000" d="{HILITE}"/></mask>')
        body = f'<path fill="{col}" mask="url(#m{uid})" d="{DROP_PATH}"/>'
    else:
        body = f'<path fill="{mode}" d="{DROP_PATH}"/>'
    return defs, g + body + "</g>", DW * k


def svg_doc(w, h, defs, body, title, bg=None):
    r = f'<rect width="{w:.1f}" height="{h:.1f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title><defs>{defs}</defs>{r}{body}</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


# ------------------------------------------------------------------ LOGO PRINCIPAL (horizontal)
F = 300.0   # corps du mot, en unités SVG
PAD = 0.32 * F


def primary(word_fill, drop_mode, bg=None, uid="p"):
    glyphs, adv = MONA.shape("juicecraft", F, WORD_TRACK)
    # hauteur du mot (ascendante de f/t jusqu'à la descente du j)
    ys0, ys1 = 1e9, -1e9
    for n, gx, _ in glyphs:
        b = MONA.bounds(n, gx, F)
        if b:
            ys0 = min(ys0, -b[3]); ys1 = max(ys1, -b[1])      # y SVG (bas = positif)
    wh = ys1 - ys0
    dh = wh * 1.14
    gap = dh * 0.17
    x_drop, y_top = PAD, PAD
    defs, dsvg, dwid = drop(x_drop, y_top, dh, drop_mode, uid)
    base_y = y_top + (dh - wh) / 2 - ys0
    wsvg, bb = word(MONA, "juicecraft", F, WORD_TRACK, x_drop + dwid + gap, base_y, word_fill)
    W = bb[2] + PAD
    H = y_top + dh + PAD
    return svg_doc(W, H, defs, dsvg + wsvg, "juicecraft", bg), (W, H, dwid, dh, wh)


p_color, meta = primary(INK, "color")
save("juicecraft_logo-principal_couleur.svg", p_color)
save("juicecraft_logo-principal_fond-sombre.svg", primary(LIGHT, "color")[0])
save("juicecraft_logo-principal_noir.svg", primary(INK, f"cut:{INK}")[0])
save("juicecraft_logo-principal_blanc.svg", primary("#FFFFFF", "cut:#FFFFFF")[0])
save("juicecraft_logo-principal_sur-fond-encre.svg", primary(LIGHT, "color", bg=INK)[0])

# ------------------------------------------------------------------ LOGO SECONDAIRE
# (a) empilé : goutte au-dessus du mot
def stacked(word_fill, drop_mode, bg=None, tagline=None, uid="s"):
    glyphs, adv = MONA.shape("juicecraft", F, WORD_TRACK)
    ys0, ys1 = 1e9, -1e9
    for n, gx, _ in glyphs:
        b = MONA.bounds(n, gx, F)
        if b:
            ys0 = min(ys0, -b[3]); ys1 = max(ys1, -b[1])
    wh = ys1 - ys0
    wsvg0, bb0 = word(MONA, "juicecraft", F, WORD_TRACK, 0, 0, word_fill)
    ww = bb0[2] - bb0[0]
    dh = wh * 1.75
    W = ww + 2 * PAD
    cx = W / 2
    defs, dsvg, dwid = drop(cx - DW * dh / DH / 2, PAD, dh, drop_mode, uid)
    base_y = PAD + dh + dh * 0.16 - ys0
    wsvg, bb = word(MONA, "juicecraft", F, WORD_TRACK, PAD - bb0[0], base_y, word_fill)
    H = base_y + ys1 + PAD
    extra = ""
    if tagline:
        t_size = F * 0.115
        tsvg, tb = word(MONA7, tagline, t_size, 0.34, 0, 0, word_fill)
        tw = tb[2] - tb[0]
        tsvg, tb = word(MONA7, tagline, t_size, 0.34, cx - tw / 2 - tb[0], base_y + ys1 + F * 0.26, word_fill)
        extra = tsvg
        H = base_y + ys1 + F * 0.26 + t_size * 0.2 + PAD
    return svg_doc(W, H, defs, dsvg + wsvg + extra, "juicecraft", bg)


save("juicecraft_logo-secondaire_empile_couleur.svg", stacked(INK, "color"))
save("juicecraft_logo-secondaire_empile_fond-sombre.svg", stacked(LIGHT, "color"))
save("juicecraft_logo-secondaire_empile_noir.svg", stacked(INK, f"cut:{INK}"))
save("juicecraft_logo-secondaire_empile_blanc.svg", stacked("#FFFFFF", "cut:#FFFFFF"))
save("juicecraft_logo-secondaire_empile_signature.svg", stacked(INK, "color", tagline="SITES SUR MESURE"))

# (b) mot seul
def wordmark_fixed(fill, bg=None):
    # recale proprement : y de la ligne de base calculé depuis la bbox
    glyphs, adv = MONA.shape("juicecraft", F, WORD_TRACK)
    ys0, ys1, xs0, xs1 = 1e9, -1e9, 1e9, -1e9
    for n, gx, _ in glyphs:
        b = MONA.bounds(n, gx, F)
        if b:
            ys0 = min(ys0, -b[3]); ys1 = max(ys1, -b[1]); xs0 = min(xs0, b[0]); xs1 = max(xs1, b[2])
    wsvg, _ = word(MONA, "juicecraft", F, WORD_TRACK, PAD - xs0, PAD - ys0, fill)
    return svg_doc(xs1 - xs0 + 2 * PAD, ys1 - ys0 + 2 * PAD, "", wsvg, "juicecraft", bg)


save("juicecraft_logo-secondaire_mot-seul_noir.svg", wordmark_fixed(INK))
save("juicecraft_logo-secondaire_mot-seul_blanc.svg", wordmark_fixed("#FFFFFF"))


# (c) badge circulaire (merch, autocollant, contenu)
def badge(bg_fill, ring_fill, text_fill, drop_mode, uid="b"):
    R = 500.0
    cx = cy = R
    top_txt, bot_txt = "JUICECRAFT", "DES SITES QUI ONT DU JUS"
    # bande de texte [r_in, r_out], même corps en haut et en bas
    r_in = R * 0.655
    # corps choisi pour que la phrase du bas occupe ~190° de l'arc extérieur
    cap = 0.70                                               # hauteur de capitale / corps (Mona Sans)
    unit, adv_b = MONA7.shape(bot_txt, 100, 0.16)[0], MONA7.shape(bot_txt, 100, 0.16)[1]
    size = 100 * (math.radians(212) * (r_in + 0.0)) / adv_b
    size = min(size, R * 0.175)
    capH = cap * size
    r_out = r_in + capH
    parts = []

    def arc(txt, r_base, centre_angle, clockwise):
        glyphs, adv = MONA7.shape(txt, size, 0.16)
        for name, gx, ga in glyphs:
            s_mid = gx + ga / 2 - adv / 2                       # position le long du texte, centrée
            if clockwise:                                       # haut : lecture horaire, haut des lettres vers l'extérieur
                th = centre_angle + s_mid / r_base
                rot = th + math.pi / 2
            else:                                               # bas : lecture anti-horaire, haut des lettres vers le centre
                th = centre_angle - s_mid / r_base
                rot = th - math.pi / 2
            px, py = cx + r_base * math.cos(th), cy + r_base * math.sin(th)
            ox, oy = px - (ga / 2) * math.cos(rot), py - (ga / 2) * math.sin(rot)
            d = MONA7.path(name, ox, oy, size, rot)
            if d:
                parts.append(d)

    arc(top_txt, r_in, -math.pi / 2, True)
    arc(bot_txt, r_out, math.pi / 2, False)
    # séparateurs : petites gouttes à 9 h et 3 h
    seps, sdefs = "", ""
    for k, ang in enumerate((math.pi, 0.0)):
        sh = capH * 1.05
        px, py = cx + (r_in + capH / 2) * math.cos(ang), cy + (r_in + capH / 2) * math.sin(ang)
        d_defs, d_svg, dw = drop(px - DW * sh / DH / 2, py - sh / 2, sh, drop_mode if drop_mode.startswith("cut") else "simple", f"{uid}s{k}")
        sdefs += d_defs; seps += d_svg
    ring = f'<circle cx="{cx}" cy="{cy}" r="{R * 0.955:.1f}" fill="none" stroke="{ring_fill}" stroke-width="{R * 0.012:.1f}"/>'
    ring_in = f'<circle cx="{cx}" cy="{cy}" r="{r_in - capH * 0.35:.1f}" fill="none" stroke="{ring_fill}" stroke-width="{R * 0.012:.1f}"/>'
    dh = (r_in - capH * 0.35) * 1.18
    defs, dsvg, dwid = drop(cx - DW * dh / DH / 2, cy - dh / 2 + dh * 0.02, dh, drop_mode, uid)
    body = ((f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{bg_fill}"/>' if bg_fill != "none" else "") + ring + ring_in +
            f'<path fill="{text_fill}" d="{" ".join(parts)}"/>' + seps + dsvg)
    return svg_doc(2 * R, 2 * R, defs + sdefs, body, "juicecraft badge")


save("juicecraft_logo-secondaire_badge_encre.svg", badge(INK, "#4A4552", LIGHT, "color"))
save("juicecraft_logo-secondaire_badge_clair.svg", badge(PAPER, "#C9C7C2", INK, "color"))
save("juicecraft_logo-secondaire_badge_blanc.svg", badge("none", "#FFFFFF", "#FFFFFF", "cut:#FFFFFF"))

# ------------------------------------------------------------------ LOGO ICÔNE
def icon_only(mode, pad_ratio=0.14, bg=None, uid="i"):
    dh = 600.0
    pad = dh * pad_ratio
    dwid = DW * dh / DH
    defs, dsvg, _ = drop(pad, pad, dh, mode, uid)
    return svg_doc(dwid + 2 * pad, dh + 2 * pad, defs, dsvg, "juicecraft icône", bg)


save("juicecraft_logo-icone_couleur.svg", icon_only("color"))
save("juicecraft_logo-icone_noir.svg", icon_only(f"cut:{INK}"))
save("juicecraft_logo-icone_blanc.svg", icon_only("cut:#FFFFFF"))


def app_icon(kind, size=1024, small=False, uid="a"):
    """pastille carrée (photo de profil, icône d'app). small=True : goutte simplifiée et plus grande (16-48 px)."""
    r = size * 0.225
    dh = size * (0.64 if small else 0.56)
    dwid = DW * dh / DH
    x, y = (size - dwid) / 2, (size - dh) / 2 + (size * 0.012)
    if kind == "encre":
        bg = f'<rect width="{size}" height="{size}" rx="{r}" fill="{INK}"/>'
        defs, ds, _ = drop(x, y, dh, "simple" if small else "color", uid)
    elif kind == "clair":
        bg = f'<rect width="{size}" height="{size}" rx="{r}" fill="{PAPER}"/>'
        defs, ds, _ = drop(x, y, dh, "simple" if small else "color", uid)
    else:  # dégradé
        defs = (f'<linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{MANGO}"/>'
                f'<stop offset=".5" stop-color="{ORANGE}"/><stop offset="1" stop-color="{BERRY}"/></linearGradient>')
        bg = f'<rect width="{size}" height="{size}" rx="{r}" fill="url(#bg{uid})"/>'
        d2, ds, _ = drop(x, y, dh, f"cut:{'#FFFFFF'}" if not small else "#FFFFFF", uid)
        defs += d2
    return svg_doc(size, size, defs, bg + ds, "juicecraft icône d'application")


save("juicecraft_logo-icone_pastille_encre.svg", app_icon("encre"))
save("juicecraft_logo-icone_pastille_clair.svg", app_icon("clair"))
save("juicecraft_logo-icone_pastille_degrade.svg", app_icon("degrade"))
save("juicecraft_logo-icone_favicon-simplifie.svg", app_icon("encre", small=True))
save("juicecraft_logo-icone_favicon-simplifie-degrade.svg", app_icon("degrade", small=True))

print("SVG générés :", len(os.listdir(OUT)))
meta_w, meta_h, dwid, dh, wh = meta
print(f"principal {meta_w:.0f}x{meta_h:.0f}  goutte {dwid:.0f}x{dh:.0f}  mot h={wh:.0f}")
