import json, re
p='video30.html'; s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old); assert n==cnt, f"count={n}: {old[:100]}"; s=s.replace(old,new)

conc=json.load(open('concepts.json',encoding='utf-8'))
ccss=re.sub(r'transition:[^;}]*;?','',conc['css']); ccss=re.sub(r'animation:[^;}]*;?','',ccss)

# ================= CSS =================
css = ccss + r'''
:root{--f-display:var(--fd);--f-body:var(--fb);--f-mono:var(--fm);--f-serif:var(--fs)}
.cp{background:#F2F2EF}
.cp .cs{position:absolute;left:0;right:0;top:0;min-height:100%;font-size:2.9cqw}
#chips7{display:none;margin-top:3rem}
.cr7{display:flex;flex-wrap:wrap;gap:1rem}
.cr7 span{padding:.9rem 1.8rem;border-radius:99px;border:1px solid rgba(19,17,22,.16);font:500 2.1rem/1 var(--fm);color:#65616C;background:rgba(251,251,249,.75)}
.cr7 span.on{background:#131116;color:#F3F1F5;border-color:#131116}
#cn7{font:500 2rem/1.2 var(--fm);color:#8A8790;letter-spacing:.05em;white-space:nowrap}
/* S8 méthode */
#s8{background:#131116;color:#F3F1F5}
.gl8{position:absolute;inset:0;background:radial-gradient(55% 60% at 82% 18%,rgba(255,90,31,.2),transparent 70%),radial-gradient(50% 50% at 8% 92%,rgba(123,63,242,.18),transparent 70%)}
.lkick.dk{color:#A29EAA}
#s8h{color:#F3F1F5}
.st8{position:absolute;left:0;top:0;display:flex;align-items:center;gap:2.4rem;white-space:nowrap}
.nd8{display:grid;place-items:center;width:6.4rem;height:6.4rem;border-radius:50%;font:500 2.2rem/1 var(--fm);border:.28rem solid #3A3542;color:#A29EAA;background:#131116;flex:none;position:relative;z-index:2}
.st8.on .nd8{background:linear-gradient(135deg,#FFB21A,#FF5A1F 55%,#EE2A7B);border-color:transparent;color:#131116}
.tx8 b{display:block;font:800 6.2rem/1 var(--fd);letter-spacing:-.045em;font-stretch:94%;color:#F3F1F5}
.tx8 small{display:block;margin-top:.7rem;font:500 2.1rem/1.2 var(--fm);color:#A29EAA;letter-spacing:.02em}
.tube8{position:absolute;left:0;top:0;width:1.2rem;border-radius:99px;background:#2B2731;overflow:hidden;z-index:1}
.tube8 span{position:absolute;inset:0;background:linear-gradient(180deg,#FFB21A,#FF5A1F 40%,#EE2A7B 75%,#7B3FF2);transform-origin:50% 0;transform:scaleY(0);border-radius:inherit}
#s8ok{position:absolute;left:0;top:0;display:flex;align-items:center;gap:1.2rem;padding:1.5rem 2.4rem 1.5rem 1.8rem;border-radius:99px;background:#1FA971;color:#fff;font:600 2.8rem/1 var(--fb);white-space:nowrap;transform-origin:0 50%}
#s8ok svg{width:3rem;height:3rem}
/* S9 offres */
@property --ang{syntax:"<angle>";initial-value:0deg;inherits:true}
.pl9{position:absolute;left:0;top:0;display:flex;flex-direction:column;gap:1.8rem;padding:3.4rem 3.2rem;border-radius:3rem;background:#FBFBF9;border:1px solid rgba(19,17,22,.1);box-shadow:0 .2rem .4rem rgba(19,17,22,.05),0 3rem 6rem -2rem rgba(19,17,22,.28);color:#131116}
.pl9.feat{background:#1C1A21;color:#F3F1F5;border-color:transparent;isolation:isolate}
.pl9.feat::before{content:"";position:absolute;inset:-.35rem;border-radius:3.35rem;padding:.35rem;background:conic-gradient(from var(--ang),#FFB21A,#FF5A1F,#EE2A7B,#7B3FF2,#FFB21A);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;z-index:-1}
.hd9{display:grid;gap:1rem}
.pk9{font:500 2rem/1 var(--fm);letter-spacing:.12em;text-transform:uppercase;color:#65616C}
.pl9.feat .pk9{color:#A29EAA}
.pt9{font:800 6.4rem/1 var(--fd);letter-spacing:-.045em;font-stretch:94%}
.pp9{font:700 3.2rem/1 var(--fd);letter-spacing:-.03em;background:linear-gradient(100deg,#FFB21A,#FF5A1F 50%,#EE2A7B);-webkit-background-clip:text;background-clip:text;color:transparent;width:max-content}
.pl9 ul{list-style:none;margin:0;padding:0;display:grid;gap:1.1rem;font:500 2.5rem/1.25 var(--fb)}
.pl9 li{display:flex;gap:1rem}
.pl9 li::before{content:"✓";color:#FF5A1F;font-weight:700;flex:none}
.rc9{position:absolute;right:2.6rem;top:-1.5rem;padding:.8rem 1.6rem;border-radius:99px;background:linear-gradient(100deg,#FFB21A,#FF5A1F);color:#131116;font:600 1.8rem/1 var(--fm);letter-spacing:.06em;text-transform:uppercase}
.pl9.p{flex-direction:row;align-items:center;gap:2.4rem;padding:2.4rem 3rem}
.pl9.p .hd9{flex:none;width:40%}
.pl9.p .pt9{font-size:5.4rem}
.pl9.p ul{flex:1;font-size:2.2rem;gap:.8rem}
#s9note{position:absolute;left:0;top:0;display:flex;align-items:center;gap:1.4rem;font:600 3.2rem/1 var(--fb);color:#131116;white-space:nowrap}
#s9note i{display:grid;place-items:center;width:4.4rem;height:4.4rem;border-radius:50%;background:#1FA971;color:#fff;font-style:normal;font-size:2.4rem}
'''
rep('/* ---------- finishing ---------- */', css + '\n/* ---------- finishing ---------- */')

# ================= HTML =================
panels=''.join(f'        <div class="pn cp" id="pn{6+i}">{h}</div>\n' for i,h in enumerate(conc['html']))
rep('        <div class="wipe" id="wipe"></div>', panels + '        <div class="wipe" id="wipe"></div>')
rep('<div class="segs" id="segs"><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i></div>',
    '<div class="segs" id="segs"><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i></div>\n      <div id="chips7"><div class="cr7"><span>Menuiserie</span><span>Boutique</span><span>Cabinet</span><span>Restaurant</span></div></div>')
rep('    <div id="ro" class="abs">1440 px</div>','    <div id="ro" class="abs">1440 px</div>\n    <div id="cn7" class="abs" style="visibility:hidden">Concepts de démonstration · aucun client réel</div>')
scenes='''  <!-- S8 méthode -->
  <div id="s8" class="layer" style="z-index:3;visibility:hidden">
    <div class="gl8"></div>
    <div id="s8k" class="lkick dk" style="position:absolute;left:0;top:0">07 — Méthode</div>
    <div id="s8h" class="kt"><div class="ln"><span>De l’idée à la</span></div><div class="ln"><span><b class="grad" style="font-weight:inherit">mise en ligne.</b></span></div></div>
    <div id="s8ok"><svg viewBox="0 0 20 20"><use href="#chk"/></svg>Site en ligne</div>
  </div>
  <!-- S9 offres -->
  <div id="s9" class="layer" style="z-index:3;visibility:hidden">
    <div id="s9k" class="lkick" style="position:absolute;left:0;top:0">08 — Offres</div>
    <div id="s9h" class="kt"><div class="ln"><span>Des offres <b class="grad" style="font-weight:inherit">claires.</b></span></div></div>
    <div class="pl9" id="pl1"><div class="hd9"><span class="pk9">Site vitrine</span><b class="pt9">Essentielle</b><span class="pp9">Sur devis</span></div><ul><li>Design moderne et professionnel</li><li>Responsive, du mobile à l’ordinateur</li><li>Formulaire de contact, bases SEO</li></ul></div>
    <div class="pl9 feat" id="pl2"><span class="rc9">Recommandée</span><div class="hd9"><span class="pk9">Site vitrine</span><b class="pt9">Premium</b><span class="pp9">Sur devis</span></div><ul><li>Animations et micro-interactions</li><li>Vitesse optimisée, SEO renforcé</li><li>Accompagnement après livraison</li></ul></div>
    <div class="pl9" id="pl3"><div class="hd9"><span class="pk9">Projet spécifique</span><b class="pt9">Sur mesure</b><span class="pp9">Sur devis</span></div><ul><li>Conçu pour votre besoin</li><li>E-commerce, réservation, espace client</li><li>Chiffrage détaillé, poste par poste</li></ul></div>
    <div id="s9note"><i>✓</i>Devis détaillé avant tout paiement.</div>
  </div>

  <!-- S1: hook -->'''
rep('  <!-- S1: hook -->',scenes)

# ================= JS: data =================
rep("""["<span class='grad'>Visible.</span>"]];""","""["<span class='grad'>Visible.</span>"], ["Pour chaque", "<span class='grad'>métier.</span>"]];""")
rep('"05 — Référencement"];','"05 — Référencement", "06 — Réalisations"];')

# ================= JS: waves + helpers (after waveP) =================
helpers = r'''
/* ---------- 30 s edit: scenes inserted between the proofs and the real site ---------- */
let TT = 0, LATE = false;
const LATE0 = 24.9, XSHIFT = 15;
const EXB = [], EXF = [];
const waveAxis = (T, t0, rev) => { const k = E.inOutCubic(P(T, t0, t0 + .56)); const a = -WR - 40 * U, b = (LAND ? W : H) + WR + 40 * U; return LAND ? (rev ? lerp(b, a, k) : lerp(a, b, k)) : (rev ? lerp(a, b, k) : lerp(b, a, k)); };
const sideOf = (rev, isNew) => LAND ? (rev ? (isNew ? "R" : "L") : (isNew ? "L" : "R")) : (rev ? (isNew ? "T" : "B") : (isNew ? "B" : "T"));
const polyFor = (side, p) => side === "L" ? `polygon(0 0,${p}px 0,${p}px 100%,0 100%)` : side === "R" ? `polygon(${p}px 0,100% 0,100% 100%,${p}px 100%)` : side === "T" ? `polygon(0 0,100% 0,100% ${p}px,0 ${p}px)` : `polygon(0 ${p}px,100% ${p}px,100% 100%,0 ${p}px)`.replace(`0 ${p}px)`, "0 100%)");
function waveBlobs(p, T, out) {
  for (let i = -1; i <= 9; i++) { const jit = Math.sin(i * 2.1 + T * 7) * (LAND ? H : W) * .02;
    out.push(LAND ? { x: p + jit, y: H * i / 8, r: WR, c: ANC[(i + 8) % 8] } : { x: W * i / 8, y: p + jit, r: WR, c: ANC[(i + 8) % 8] }); }
  for (let i = 0; i < 5; i++) out.push(LAND ? { x: p - W * .07 * (1 + i % 3), y: H * (.1 + .2 * i), r: H * .15, c: ANC[(i * 3) % 8] } : { x: W * (.1 + .2 * i), y: p + H * .035 * (1 + i % 3), r: W * .16, c: ANC[(i * 3) % 8] });
}
const CONC = [["pn6", 10.0, "ardoise-menuiserie.fr"], ["pn7", 11.5, "maison-ondine.fr"], ["pn8", 13.0, "valles-avocats.fr"], ["pn9", 14.5, "comptoir-sauvage.fr"]];
const S8ROWS = [["01", "Échange", "Compte rendu et devis détaillé"], ["02", "Conception", "Maquettes à valider"], ["03", "Création", "Lien de prévisualisation"], ["04", "Validation", "Version finale validée"], ["05", "Mise en ligne", "Site en ligne et prise en main"]];
const STEP8 = [16.7, 17.65, 18.6, 19.55, 20.5];
const X8 = {}, X9 = {};

function initExtra() {
  const s8 = $("s8"), s9 = $("s9");
  s8.style.visibility = s9.style.visibility = "visible";
  // ----- S8
  const h8 = $("s8h"), k8 = $("s8k");
  h8.style.fontSize = (LAND ? 104 : 108) * U + "px"; h8.style.fontStretch = "90%";
  const h8h = h8.offsetHeight;
  const rows = S8ROWS.map(([n, name, sub]) => { const d = document.createElement("div"); d.className = "st8"; d.innerHTML = `<span class="nd8">${n}</span><div class="tx8"><b>${name}</b><small>${sub}</small></div>`; s8.appendChild(d); return d; });
  const tube = document.createElement("div"); tube.className = "tube8"; tube.innerHTML = "<span></span>"; s8.appendChild(tube);
  const pitch = (LAND ? 150 : 140) * U, nd = 64 * U, x0 = LAND ? W * .53 : 90 * U;
  const y0 = LAND ? (H - (4 * pitch + nd)) / 2 : .075 * H + 56 * U + h8h + 90 * U;
  const hx = LAND ? 140 * U : 90 * U, hy = LAND ? (H - h8h) / 2 + 24 * U : .075 * H + 56 * U;
  Object.assign(X8, { h8, k8, rows, tube, pitch, nd, x0, y0, hx, hy, h8L: [...h8.querySelectorAll(".ln>span")], ok: $("s8ok") });
  k8.style.transform = `translate(${hx}px,${hy - 60 * U}px)`;
  h8.style.transform = `translate(${hx}px,${hy}px)`;
  tube.style.width = 12 * U + "px"; tube.style.height = 4 * pitch + "px";
  tube.style.transform = `translate(${x0 + nd / 2 - 6 * U}px,${y0 + nd / 2}px)`;
  X8.okW = X8.ok.offsetWidth; X8.okH = X8.ok.offsetHeight;
  // ----- S9
  const h9 = $("s9h"), k9 = $("s9k"), plans = [$("pl1"), $("pl2"), $("pl3")], note = $("s9note");
  h9.style.fontSize = (LAND ? 96 : 100) * U + "px"; h9.style.fontStretch = "90%";
  const h9h = h9.offsetHeight;
  let cw, ch, gap, xs, ys, tx, ty;
  if (LAND) { cw = 470 * U; ch = 500 * U; gap = 28 * U; const tot = 3 * cw + 2 * gap; tx = (W - tot) / 2; ty = (H - ch) / 2 + 60 * U; xs = [0, 1, 2].map(i => tx + i * (cw + gap)); ys = [ty, ty, ty]; }
  else { cw = 880 * U; ch = 250 * U; gap = 22 * U; tx = (W - cw) / 2; ty = .21 * H; xs = [tx, tx, tx]; ys = [0, 1, 2].map(i => ty + i * (ch + gap)); }
  plans.forEach((e, i) => { e.style.width = cw + "px"; e.style.height = ch + "px"; e.classList.toggle("p", !LAND); });
  const totW = LAND ? 3 * cw + 2 * gap : cw, totH = LAND ? ch : 3 * ch + 2 * gap;
  Object.assign(X9, { h9, k9, plans, xs, ys, cw, ch, note, noteW: note.offsetWidth, h9L: [...h9.querySelectorAll(".ln>span")],
    hx: tx, hy: ty - h9h - (LAND ? 70 : 60) * U, noteY: ty + totH + (LAND ? 50 : 44) * U, cards: { cx: tx + totW / 2, cy: ty + totH / 2, w: totW + 120 * U, h: totH + 120 * U } });
  k9.style.transform = `translate(${X9.hx}px,${X9.hy - 56 * U}px)`;
  h9.style.transform = `translate(${X9.hx}px,${X9.hy}px)`;
  s8.style.visibility = s9.style.visibility = "hidden";
}

function extraBlobs(T) {
  [[15.9, false], [21.9, true]].forEach(([t0, rev]) => { if (T >= t0 && T < t0 + .6) waveBlobs(waveAxis(T, t0, rev), T, EXF); });
  if (T >= 22.0 && T < 25.0) hug(X9.cards, .8 * E.outCubic(P(T, 22.0, 22.7)) * (1 - E.inCubic(P(T, 24.7, 24.95))), T, EXB);
}

function s7Dom(T) {
  const fbh = $("fbody").clientHeight;
  let cur = 0;
  CONC.forEach(([id, t0, dom], i) => {
    const el = $(id), tn = i < 3 ? CONC[i + 1][1] : 99;
    if (T >= t0) cur = i;
    const ki = E.outExpo(P(T, t0, t0 + .45)), ko = i < 3 ? E.inOutCubic(P(T, tn, tn + .45)) : 0;
    el.style.visibility = (T >= t0 && T < tn + .5) ? "inherit" : "hidden";
    el.style.zIndex = 10 + i;
    el.style.transform = `translateX(${(1 - ki) * 100 - ko * 32}%)`;
    el.style.filter = ko > 0 ? `brightness(${1 - .35 * ko})` : "none";
    const cs = el.firstElementChild, maxs = Math.max(0, cs.offsetHeight - fbh);
    cs.style.transform = `translateY(${-maxs * E.inOutCubic(P(T, t0 + .35, t0 + 1.4))}px)`;
  });
  const p5 = $("pn5"), ko5 = E.inOutCubic(P(T, 10.0, 10.45));
  p5.style.transform = `translateX(${-ko5 * 32}%)`; p5.style.filter = ko5 > 0 ? `brightness(${1 - .35 * ko5})` : "none"; p5.style.visibility = T >= 10.5 ? "hidden" : "inherit";
  if (T >= 10.0) { $("url").classList.remove("secure"); $("urlt").textContent = CONC[cur][2]; }
  const chips = $("chips7"), on7 = T >= 10.0;
  $("segs").style.display = on7 ? "none" : ""; chips.style.display = on7 ? "block" : "none";
  chips.style.opacity = P(T, 10.14, 10.4);
  [...chips.querySelectorAll("span")].forEach((c, i) => c.classList.toggle("on", i === cur));
  const R = frameRect(9.86), cn = $("cn7"), k = P(T, 10.3, 10.6);
  cn.style.visibility = "inherit"; cn.style.opacity = k * (1 - P(T, 15.8, 16.0));
  cn.style.transform = `translate(${R.cx - cn.offsetWidth / 2}px,${R.cy + R.h / 2 + 26 * U}px)`;
}

function s8Dom(T) {
  const X = X8;
  X.k8.style.opacity = P(T, 16.1, 16.4);
  X.h8L.forEach((sp, i) => lineAnim(sp, T, 16.12 + i * .08, null, { din: .6 }));
  X.rows.forEach((r, i) => {
    const ta = STEP8[i], appear = E.outExpo(P(T, 16.3 + i * .06, 16.8 + i * .06)), active = T >= ta;
    const isCur = active && (i === 4 || T < STEP8[i + 1]);
    r.classList.toggle("on", active);
    r.style.opacity = (T < ta ? .3 : isCur ? 1 : .62) * appear;
    r.firstElementChild.style.transform = `scale(${active ? 1 + .16 * Math.sin(P(T, ta, ta + .38) * Math.PI) : 1})`;
    r.style.transform = `translate(${X.x0}px,${X.y0 + i * X.pitch + (1 - appear) * 44 * U}px)`;
  });
  X.tube.style.opacity = E.outExpo(P(T, 16.4, 16.8));
  X.tube.firstElementChild.style.transform = `scaleY(${P(T, STEP8[0], STEP8[4])})`;
  const kk = E.outBack(P(T, 21.4, 21.72), 1.8), ok = X.ok;
  ok.style.opacity = P(T, 21.4, 21.5);
  ok.style.transform = `translate(${X.x0}px,${X.y0 + 4 * X.pitch + X.nd + 44 * U}px) scale(${Math.max(0, kk)})`;
}

function s9Dom(T) {
  const X = X9, TP = [22.2, 22.5, 22.8];
  X.k9.style.opacity = P(T, 21.95, 22.2);
  X.h9L.forEach((sp, i) => lineAnim(sp, T, 22.0 + i * .08, null, { din: .55 }));
  X.plans.forEach((e, i) => {
    const k = E.outBack(P(T, TP[i], TP[i] + .5), 1.6), pulse = i === 1 && T > 23.2 ? 1 + .012 * Math.sin((T - 23.2) * 3.4) : 1;
    e.style.opacity = P(T, TP[i], TP[i] + .12);
    e.style.transform = `translate(${X.xs[i]}px,${X.ys[i] + (1 - k) * 70 * U}px) scale(${(.92 + .08 * k) * pulse})`;
    if (i === 1) e.style.setProperty("--ang", (((T - 22.5) * 70) % 360 + 360) % 360 + "deg");
  });
  const kn = E.outExpo(P(T, 23.5, 23.9));
  X.note.style.opacity = kn;
  X.note.style.transform = `translate(${(W - X.noteW) / 2}px,${X.noteY + (1 - kn) * 18 * U}px)`;
}

function extraDom(T) {
  const s34 = $("s34"), s8 = $("s8"), s9 = $("s9");
  if (T >= 9.7 && T < 16.5) s7Dom(T);
  else { for (const [id] of CONC) $(id).style.visibility = "hidden"; $("cn7").style.visibility = "hidden"; $("chips7").style.display = "none"; if (T < 9.7) $("segs").style.display = ""; }
  if (T >= 16.5) s34.style.visibility = "hidden";
  const p1 = waveAxis(T, 15.9, false), p2 = waveAxis(T, 21.9, true), p3 = waveAxis(T, LATE0, false);
  const w1 = T >= 15.9 && T < 16.5, w2 = T >= 21.9 && T < 22.5, w3 = T >= LATE0 && T < 25.5;
  if (w1) s34.style.clipPath = polyFor(sideOf(false, false), p1);
  s8.style.visibility = (T >= 15.9 && T < 22.5) ? "visible" : "hidden";
  s8.style.clipPath = w1 ? polyFor(sideOf(false, true), p1) : w2 ? polyFor(sideOf(true, false), p2) : "none";
  s9.style.visibility = (T >= 21.9 && T < 25.5) ? "visible" : "hidden";
  s9.style.clipPath = w2 ? polyFor(sideOf(true, true), p2) : w3 ? polyFor(sideOf(false, false), p3) : "none";
  if (s8.style.visibility === "visible") s8Dom(T);
  if (s9.style.visibility === "visible") s9Dom(T);
}
'''
rep('// S2 droplets', helpers + '\n// S2 droplets')

# ================= core edits =================
rep('function seek(t) {\n  lastSeek = t;','function seekCore(t) {\n  lastSeek = t;')
rep('on34 = t >= 3.5 && t < 10.5; vis(s34, on34);','on34 = t >= 3.5 && t < 10.5 && !LATE; vis(s34, on34);')
rep('const fy = t > 5.3 ? Math.sin(t * 1.7) * 4 * U : 0;','const fy = TT > 5.3 ? Math.sin(TT * 1.7) * 4 * U : 0;')
i0=s.index('    // labels\n    const lab = $("lab")'); i1=s.index('    // readout')
s=s[:i0]+'''    // labels (driven by the real timeline TT so they can run past the frozen S4 core)
    const lab = $("lab"); vis(lab, TT >= 4.98);
    const LT = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 16.0];
    const bi = Math.min(5, Math.max(0, Math.floor(TT - 5.0)));
    const labH = lerp(bi > 0 ? M.lab[bi - 1].h : M.lab[0].h, M.lab[bi].h, E.inOutCubic(P(TT, LT[bi] - .08, LT[bi] + .24)));
    if (LAND) lab.style.transform = `translate(${G.lab.x}px,${G.lab.cy - (labH + M.labk + 60 * U) / 2}px)`;
    else lab.style.transform = `translate(${G.lab.x}px,${G.lab.top}px)`;
    $("labs").style.cssText = `position:relative;height:${labH}px;margin:${26 * U}px 0 ${30 * U}px`;
    labEls.forEach((el, i) => {
      el.style.top = "0px";
      labBlocks[i].forEach((s, j) => lineAnim(s, TT, LT[i] + .04 + j * .06, i < 5 ? LT[i + 1] - .3 + j * .03 : null, { din: .5, dout: .22, outEase: E.inOutCubic }));
    });
    const kIdx = Math.min(5, Math.max(0, Math.floor(TT - 5.05)));
    const lk = $("labk"); lk.textContent = KICK[kIdx];
    const kph = TT - (LT[kIdx] + .05); lk.style.opacity = TT < 5.05 ? 0 : cl(kph / .18) * (kIdx < 5 ? 1 - P(TT, LT[kIdx + 1] - .1, LT[kIdx + 1]) : 1);
    segB.forEach((b, i) => b.style.transform = `scaleX(${P(TT, LT[i], LT[i + 1])})`);
    $("segs").style.opacity = P(TT, 5.0, 5.2);
'''+s[i1:]
rep('''  if (t >= 3.5 && t < 9.96) {
    const s = E.outCubic(P(t, 3.6, 4.2)) * lerp(1, .64, E.inOutCubic(P(t, 4.9, 5.32))) * (1 - E.inCubic(P(t, 9.8, 9.95)));
    hug(frameRect(t), s, t, BB);
  }''','''  if (TT >= 3.5 && TT < 16.5 && !LATE) {
    const s = E.outCubic(P(TT, 3.6, 4.2)) * lerp(1, .64, E.inOutCubic(P(TT, 4.9, 5.32))) * (1 - E.inCubic(P(TT, 15.9, 16.2)));
    hug(frameRect(Math.min(TT, 9.86)), s, TT, BB);
  }''')
rep('  drawB(BB, t); drawF(BF, t);','  EXB.forEach(b => BB.push(b)); EXF.forEach(b => BF.push(b));\n  const tl = LATE ? t : TT;\n  drawB(BB, tl); drawF(BF, tl);')
rep('const f = Math.round(t * 60), r = rng(f * 7919 + 13);','const f = Math.round((LATE ? t : TT) * 60), r = rng(f * 7919 + 13);')
rep('  const dark = t >= 12.5;','  const dark = (LATE && t >= 12.5) || (TT >= 15.9 && TT < 22.4);')
rep('window.READY = false;','''function seek(T) {
  TT = T; LATE = T >= LATE0;
  const tc = LATE ? T - XSHIFT : Math.min(T, 9.86);
  EXB.length = 0; EXF.length = 0;
  extraBlobs(T);
  seekCore(tc);
  extraDom(T);
}

window.READY = false;''')
rep('''  measure();
  ["s1", "s34", "s5", "s6", "w3", "lab", "fr"].forEach(id => $(id).style.visibility = "");''','''  measure();
  ["s1", "s34", "s5", "s6", "w3", "lab", "fr"].forEach(id => $(id).style.visibility = "");
  initExtra();''')
open(p,'w',encoding='utf-8').write(s); print('video30 patched', len(s))
