"""SVG animé du logo (CSS keyframes) : goutte qui tombe, s'écrase, éclabousse, puis le mot se lève."""
import math, os, random
import build_logo as L

HERE = L.HERE
OUT = os.path.join(HERE, "..", "animation")
os.makedirs(OUT, exist_ok=True)
T_TOTAL = 3.6


def build(word_fill, with_word=True, name="x"):
    glyphs, adv = L.MONA.shape("juicecraft", L.F, L.WORD_TRACK)
    ys0, ys1 = 1e9, -1e9
    for n, gx, _ in glyphs:
        b = L.MONA.bounds(n, gx, L.F)
        if b:
            ys0 = min(ys0, -b[3]); ys1 = max(ys1, -b[1])
    wh = ys1 - ys0
    dh = wh * 1.14
    gap = dh * 0.17
    PAD = L.PAD
    if with_word:
        defs, dsvg, dwid = L.drop(PAD, PAD, dh, "color", "an")
        base_y = PAD + (dh - wh) / 2 - ys0
        letters = L.word_glyphs(L.MONA, "juicecraft", L.F, L.WORD_TRACK, PAD + dwid + gap, base_y)
        W = max(b[2] for _, b in letters if b) + PAD
        H = PAD * 2 + dh
        dcx = PAD + dwid / 2
    else:
        pad = dh * 0.5
        defs, dsvg, dwid = L.drop(pad, pad, dh, "color", "an")
        letters = []
        W = dwid + 2 * pad
        H = dh + 2 * pad
        dcx = pad + dwid / 2
        PAD = pad
    d_bottom = PAD + dh
    # gouttelettes d'éclaboussure
    rnd = random.Random(7)
    drops_svg, css = "", ""
    n = 9
    for i in range(n):
        side = -1 if i % 2 == 0 else 1
        k = i // 2
        ang = math.radians(rnd.uniform(28, 74))
        sp = dh * rnd.uniform(0.8, 1.45)
        vx = side * math.cos(ang) * sp * (0.9 + 0.12 * k)
        vy = math.sin(ang) * sp * 0.95
        r = dh * rnd.uniform(0.05, 0.095)
        fall = dh * rnd.uniform(0.25, 0.45)
        col = ("#FFB21A", "#FF5A1F", "#EE2A7B", "#FF7A2E")[i % 4]
        dur = rnd.uniform(0.75, 0.95)
        delay = 0.5 + rnd.uniform(0, 0.05)
        drops_svg += (f'<g class="sx" style="--vx:{vx:.1f}px;--d:{delay:.3f}s;--t:{dur:.3f}s">'
                      f'<g class="sy" style="--vy:{vy:.1f}px;--fall:{fall:.1f}px;--d:{delay:.3f}s;--t:{dur:.3f}s">'
                      f'<circle cx="{dcx:.1f}" cy="{d_bottom - r:.1f}" r="{r:.1f}" fill="{col}"/></g></g>')
    fall_from = -(H + dh * 0.6)
    style = f"""
  .df{{transform-box:fill-box;transform-origin:50% 100%;animation:fall .5s cubic-bezier(.55,0,.85,.45) both}}
  .ds{{transform-box:fill-box;transform-origin:50% 100%;animation:squash .75s linear .5s forwards}}
  @keyframes fall{{0%{{transform:translateY({fall_from:.0f}px) scale(.9,1.14)}}100%{{transform:translateY(0) scale(.92,1.12)}}}}
  @keyframes squash{{0%{{transform:scale(1.34,.66);animation-timing-function:cubic-bezier(.2,.8,.3,1)}}
    38%{{transform:scale(.92,1.1);animation-timing-function:cubic-bezier(.3,0,.4,1)}}
    70%{{transform:scale(1.03,.97);animation-timing-function:ease-out}}100%{{transform:scale(1,1)}}}}
  .sx{{opacity:0;animation:sx var(--t) linear var(--d) both}}
  .sy{{animation:sy var(--t) linear var(--d) both}}
  @keyframes sx{{0%{{transform:translateX(0);opacity:0}}3%{{opacity:1}}85%{{opacity:1}}100%{{transform:translateX(var(--vx));opacity:0}}}}
  @keyframes sy{{0%{{transform:translateY(0);animation-timing-function:cubic-bezier(.2,.7,.4,1)}}
    42%{{transform:translateY(calc(var(--vy) * -1));animation-timing-function:cubic-bezier(.6,0,.9,.6)}}100%{{transform:translateY(var(--fall))}}}}
  .L{{transform-box:fill-box;opacity:0;animation:rise .85s cubic-bezier(.16,1,.3,1) calc(.62s + var(--i) * .042s) both}}
  @keyframes rise{{0%{{transform:translateY(.55em) scale(1,1.12);opacity:0}}20%{{opacity:1}}100%{{transform:none;opacity:1}}}}
  @media (prefers-reduced-motion:reduce){{.df,.ds,.sx,.sy,.L{{animation:none!important;opacity:1!important;transform:none!important}}.sx{{opacity:0!important}}}}
"""
    letters_svg = "".join(f'<path class="L" style="--i:{i}" fill="{word_fill}" d="{d}"/>' for i, (d, b) in enumerate(letters) if d)
    body = f'<g class="df"><g class="ds">{dsvg}</g></g>{drops_svg}{letters_svg}'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-label="juicecraft">'
           f'<title>juicecraft</title><defs>{defs}</defs><style>{style}</style>{body}</svg>\n')
    return svg, (W, H)


for fname, fill, word in (("juicecraft_logo-anime_fond-clair.svg", L.INK, True),
                          ("juicecraft_logo-anime_fond-sombre.svg", L.LIGHT, True),
                          ("juicecraft_logo-anime_icone.svg", L.INK, False)):
    svg, wh = build(fill, word)
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(svg)
    print(fname, [round(v) for v in wh])
