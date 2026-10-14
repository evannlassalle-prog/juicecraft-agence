p='video.html'; s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    assert n==cnt, f"count={n} for: {old[:110]}"
    s=s.replace(old,new)

# ---------- layout constants
rep("lines: [\"Des sites sur mesure qui ont du <b class='grad' style='font-weight:inherit'>jus</b>.\"]","lines: [\"Studio de création de sites internet.\"]")
rep("lines: [\"Des sites sur mesure\", \"qui ont du <b class='grad' style='font-weight:inherit'>jus</b>.\"]","lines: [\"Studio de création\", \"de sites internet.\"]")
rep('fr4: { cx: W / 2, cy: H * .615, w: 940 * U, h: 820 * U },','fr4: { cx: W / 2, cy: H * .53, w: 940 * U, h: 760 * U },')
rep('dev: { cx: W * .7, cy: H * .515, scr: 900 * U, ph: 250 * U },','dev: { cx: W * .67, cy: H * .515, scr: 880 * U, ph: 245 * U },')
rep('dev: { cx: W * .53, cy: H * .66, scr: 860 * U, ph: 250 * U },','dev: { cx: W * .45, cy: H * .55, scr: 780 * U, ph: 240 * U },')
rep('h5: { x: 90 * U, top: H * .11, fs: 112 * U },','h5: { x: 90 * U, top: H * .14, fs: 112 * U },')
rep('const LAND = W / H > 1.2;','const LAND = W / H > 1.2;\nif (W / H <= 1.2) document.body.classList.add("port");')

# ---------- labels / kickers
rep('const LABELS = [["Sur", "<span class=\'grad\'>mesure.</span>"],','const LABELS = [["À votre", "<span class=\'grad\'>image.</span>"],')
rep('const KICK = ["01 — Design", "02 — Responsive", "03 — Performance", "04 — Sécurité", "05 — Référencement"];','const KICK = ["01 — Identité", "02 — Mobile", "03 — Performance", "04 — Sécurité", "05 — Référencement"];')

# ---------- lineAnim: selectable exit ease
rep('''  const ki = tin === null ? 1 : E.outExpo(P(t, tin, tin + din));
  const ko = tout === null ? 0 : E.inExpo(P(t, tout, tout + dout));''','''  const oe = opt.outEase || E.inExpo;
  const ki = tin === null ? 1 : E.outExpo(P(t, tin, tin + din));
  const ko = tout === null ? 0 : oe(P(t, tout, tout + dout));''')

# ---------- shader
rep('const N = 28;','const N = 40;')
rep("float spec=pow(max(dot(reflect(-L,n),vec3(0.,0.,1.)),0.),38.);","float spec=pow(max(dot(reflect(-L,n),vec3(0.,0.,1.)),0.),38.); spec*=1.-smoothstep(3.,8.,f);")

# ---------- flood radius / centre
rep('const floodR1 = t => t < 3.0 ? RC * E.inCubic(P(t, 2.66, 3.0)) : RC * (1 - E.inOutCubic(P(t, 3.45, 3.98)));',
'''const R0 = Math.hypot(W, H) * .55;
const floodR1 = t => t < 3.0 ? RC * E.inCubic(P(t, 2.66, 3.0)) : t < 3.48 ? lerp(RC, R0, E.inOutSine(P(t, 3.0, 3.48))) : R0 * (1 - E.inOutSine(P(t, 3.48, 3.94)));
const floodC = t => t < 3.5 ? H / 2 : lerp(H / 2, H * 1.28, E.inCubic(P(t, 3.5, 3.96)));
const WR = LAND ? H * .3 : W * .34;
const waveP = t => { const k = E.inOutCubic(P(t, 9.9, 10.46)); return LAND ? lerp(-WR - 40 * U, W + WR + 40 * U, k) : lerp(H + WR + 40 * U, -WR - 40 * U, k); };''')
rep('vx: side * (650 + r() * 900), vy: -520 + r() * 640','vx: side * (240 + r() * 520), vy: -(520 + r() * 760)')
rep('for (let i = 0; i < 14; i++) { const side = i % 2','for (let i = 0; i < 12; i++) { const side = i % 2')

# ---------- frame geometry
rep('if (t < 4.9) return A;\n  if (t < 6.0) return mixR(A, B4, E.inOutExpo(P(t, 4.9, 5.32)));','if (t < 4.88) return A;\n  if (t < 6.0) return mixR(A, B4, E.inOutCubic(P(t, 4.88, 5.4)));')
rep('  return { cx: B4.cx, cy: B4.cy, w, h };\n}','  let cx = B4.cx;\n  if (LAND) { cx = lerp(B4.cx, W * .6, kp); if (t >= 7.0) cx = lerp(W * .6, B4.cx, kb); }\n  return { cx, cy: B4.cy, w, h };\n}')
s=s.replace('P(t, 10.0, 10.6)','P(t, 10.1, 10.7)')

# ---------- measure()
rep('''  M.d6x = (W - M.lock.w) / 2 + G.s6.d / 2; M.d6y = G.s6.cy;
''','')
rep('''  M.url = { w: $("url6").offsetWidth, h: $("url6").offsetHeight };''','''  M.url = { w: $("url6").offsetWidth, h: $("url6").offsetHeight };
  M.legal = { w: $("legal6").offsetWidth, h: $("legal6").offsetHeight };
  M.lockShift = .11 * G.s6.d;
  const stackH = M.lock.h + 34 * U + M.tag6.h + 54 * U + M.cta.h + 44 * U + (URLTXT ? M.url.h : M.sub.h) + 26 * U + M.legal.h;
  G.s6.cy = (H - stackH) * .45 + M.lock.h / 2;
  M.d6x = (W - M.lock.w) / 2 - M.lockShift + G.s6.d / 2; M.d6y = G.s6.cy;
  const sd = $("sadrop"); t1.appendChild(sd);
  const jr = $("jus1").getBoundingClientRect(), tr = t1.getBoundingClientRect();
  M.sad = { x: jr.left - tr.left + jr.width * .16, y: jr.top - tr.top + jr.height * .72 };''')

# ---------- S1
rep('''    const ex = E.inExpo(P(t, 2.0, 2.32));
    if (LAND) t1.style.transform = `translate(${G.t1.x - ex * W * .55}px,${G.t1.cy - M.t1h / 2}px)`;
    else t1.style.transform = `translate(${G.t1.x}px,${G.t1.top - ex * H * .45}px)`;
    t1.style.opacity = 1 - P(t, 2.1, 2.32);''','''    const ex = E.inCubic(P(t, 1.95, 2.2));
    if (LAND) t1.style.transform = `translate(${G.t1.x - ex * W * .5}px,${G.t1.cy - M.t1h / 2}px)`;
    else t1.style.transform = `translate(${G.t1.x}px,${G.t1.top - ex * H * .45}px)`;
    t1.style.opacity = 1 - P(t, 2.08, 2.2);''')
rep('j.style.color = "#ABA7B0";','j.style.color = "#8A8692";')
rep('"wght" ${lerp(420, 230, E.outCubic(P(t, 1.0, 1.5)))}','"wght" ${lerp(420, 300, E.outCubic(P(t, 1.0, 1.5)))}')
i0=s.index('    const sd = $("sadrop"), dk = P(t, 1.45, 2.05);')
i1=s.index('    // card', i0)
s=s[:i0]+'''    const sd = $("sadrop"), dk = P(t, 1.45, 1.97);
    const grow = cl(dk / .12), fall = E.inQuad(dk) * G.t1.fs * 1.2;
    sd.style.transform = `translate(${M.sad.x}px,${M.sad.y + fall}px) scale(${grow * (1 + .12 * Math.sin(Math.min(1, dk * 2) * Math.PI))},${grow * (1 + .5 * dk)})`;
    sd.style.opacity = dk <= 0 ? 0 : 1 - P(t, 1.82, 1.97);
'''+s[i1:]
rep('vis(oldEl, t < 2.72);','vis(oldEl, t < 2.5);')

# ---------- S3
rep('const w3 = $("w3"), on3 = t >= 3.0 && t < 3.6; vis(w3, on3);','const w3 = $("w3"), on3 = t >= 3.0 && t < 3.64; vis(w3, on3);')
rep('const k = E.outExpo(P(t, 3.0, 3.45)), ko = E.inCubic(P(t, 3.34, 3.5));','const k = E.outExpo(P(t, 3.0, 3.45)), ko = E.inCubic(P(t, 3.46, 3.62));')
rep('scale(${lerp(1.3, 1, k) * (1 - .12 * ko)})','scale(${lerp(LAND ? 1.3 : 1.08, 1, k) * (1 - .12 * ko)})')
rep('fl.style.opacity = t >= 3.0 && t < 3.16 ? .55 * (1 - P(t, 3.0, 3.16)) : t >= 13.0 && t < 13.14 ? .16 * (1 - P(t, 13.0, 13.14)) : 0;','fl.style.opacity = t >= 3.0 && t < 3.14 ? .4 * (1 - P(t, 3.0, 3.14)) : 0;')
rep('const s34 = $("s34"), on34 = t >= 3.45 && t < 10.02; vis(s34, on34);','''const s34 = $("s34"), on34 = t >= 3.5 && t < 10.5; vis(s34, on34);
  const wv = t >= 9.9 && t < 10.5, wp = waveP(t);
  s34.style.clipPath = wv ? (LAND ? `polygon(${wp}px 0,100% 0,100% 100%,${wp}px 100%)` : `polygon(0 0,100% 0,100% ${wp}px,0 ${wp}px)`) : "none";''')
rep('const ke = E.outExpo(P(t, 3.5, 4.2));\n    const push = .03 * E.inOutCubic(P(t, 4.15, 4.9)) * (1 - E.inOutExpo(P(t, 4.9, 5.32)));','''const ke = E.outExpo(P(t, 3.56, 4.26));
    const push = .04 * E.inOutCubic(P(t, 4.15, 4.9)) * (1 - E.inOutCubic(P(t, 4.88, 5.4)));
    const drift = lerp(-4, 2, E.inOutSine(P(t, 3.8, 4.9))) * (1 - E.inOutCubic(P(t, 4.88, 5.4)));''')
rep('rotateX(${(1 - ke) * 28}deg) scale(','rotateX(${(1 - ke) * 28}deg) rotateY(${drift}deg) scale(')
rep('vis(fr, t >= 3.5);','vis(fr, t >= 3.56);')
rep('const PN = [[3.5, 5.0], [5.0, 6.0],','const PN = [[3.56, 5.08], [5.08, 6.0],')
rep('urlt.innerHTML = t >= 9.0 ? "recherche · menuisier sur mesure" : sec ? "<b>https://</b>votre-site.fr" : "votre-site.fr";','urlt.innerHTML = t < 5.08 ? (URLTXT || "juicecraft") : t >= 9.0 ? (t >= 9.58 ? "recherche · menuisier sur mesure" : "recherche") : sec ? "<b>https://</b>votre-site.fr" : "votre-site.fr";')
rep('$("sr1").style.setProperty("--ring", E.outCubic(P(t, 9.66, 9.86)));\n','')
rep('[["sr1", 9.6], ["sr2", 9.66], ["sr3", 9.72]]','[["sr1", 9.6], ["sr2", 9.68], ["sr3", 9.76]]')

# ---------- badges
i0=s.index('    const BD = [["bd1", 4.25')
i1=s.index('    // caption', i0)
s=s[:i0]+'''    const BD = LAND ? [["bd1", 4.25, -.04, .22, "l"], ["bd2", 4.5, .97, -.05, "r"], ["bd3", 4.75, .98, .8, "r"]]
      : [["bd1", 4.25, .05, -.15, "l"], ["bd2", 4.5, .6, -.15, "l"], ["bd3", 4.75, .3, .96, "l"]];
    const bs = LAND ? 1.28 : 1.1;
    BD.forEach(([id, a, fx, fy2, side], i) => {
      const e = $(id), mb = M.badges[i];
      const k = E.outBack(P(t, a, a + .32), 2.0), ko = E.inCubic(P(t, 4.92, 5.08));
      let L = R.cx - R.w / 2 + R.w * fx - (side === "l" ? mb.w * bs * .35 : mb.w * bs * .7);
      let T = R.cy - R.h / 2 + R.h * fy2 + Math.sin(t * 2.4 + i) * 6 * U;
      L = LAND ? cl(L, 40 * U, W - mb.w * bs - 40 * U) : cl(L, 40 * U, W * .86 - mb.w * bs);
      if (!LAND) T = Math.min(T, H * .74 - mb.h * bs);
      e.style.transform = `translate(${L + (bs - 1) * mb.w / 2}px,${T + (bs - 1) * mb.h / 2}px) scale(${Math.max(0, k) * bs * (1 - .3 * ko)})`;
      e.style.opacity = P(t, a, a + .1) * (1 - ko);
      vis(e, t >= a && t < 5.1);
    });
'''+s[i1:]
rep('cap3L.forEach((s, i) => lineAnim(s, t, 3.62 + i * .07, 4.86 + i * .04));','cap3L.forEach((s, i) => lineAnim(s, t, 3.62 + i * .07, (LAND ? 4.86 : 4.62) + i * .04, { dout: .26 }));')

# ---------- labels
i0=s.index('    const LT = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0];')
i1=s.index('    const kIdx', i0)
s=s[:i0]+'''    const LT = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0];
    const bi = Math.min(4, Math.max(0, Math.floor(t - 5.0)));
    const labH = lerp(bi > 0 ? M.lab[bi - 1].h : M.lab[0].h, M.lab[bi].h, E.inOutCubic(P(t, LT[bi] - .08, LT[bi] + .24)));
    if (LAND) lab.style.transform = `translate(${G.lab.x}px,${G.lab.cy - (labH + M.labk + 60 * U) / 2}px)`;
    else lab.style.transform = `translate(${G.lab.x}px,${G.lab.top}px)`;
    $("labs").style.cssText = `position:relative;height:${labH}px;margin:${26 * U}px 0 ${30 * U}px`;
    labEls.forEach((el, i) => {
      el.style.top = "0px";
      labBlocks[i].forEach((s, j) => lineAnim(s, t, LT[i] + .04 + j * .06, i < 4 ? LT[i + 1] - .3 + j * .03 : null, { din: .5, dout: .22, outEase: E.inOutCubic }));
    });
'''+s[i1:]
rep('''const kIdx = Math.min(4, Math.max(0, Math.floor(t - 5.0)));''','''const kIdx = Math.min(4, Math.max(0, Math.floor(t - 5.05)));''')
rep('const kph = t - LT[kIdx]; lk.style.opacity = t < 5.0 ? 0 : cl(kph / .18) * (kIdx < 4 ? 1 - P(t, LT[kIdx + 1] - .12, LT[kIdx + 1]) : 1);','const kph = t - (LT[kIdx] + .05); lk.style.opacity = t < 5.05 ? 0 : cl(kph / .18) * (kIdx < 4 ? 1 - P(t, LT[kIdx + 1] - .1, LT[kIdx + 1]) : 1);')
rep('ro.textContent = t < 6.17 ? "1440 px" : t < 6.46 ? "768 px" : "390 px";','ro.textContent = t < 6.17 ? "1440\\u00a0px" : t < 6.46 ? "768\\u00a0px" : "390\\u00a0px";')

# ---------- S5
rep('const s5 = $("s5"), on5 = t >= 9.98 && t < 12.66; vis(s5, on5);','''const s5 = $("s5"), on5 = t >= 9.9 && t < 12.9; vis(s5, on5);
  s5.style.clipPath = wv ? (LAND ? `polygon(0 0,${wp}px 0,${wp}px 100%,0 100%)` : `polygon(0 ${wp}px,100% ${wp}px,100% 100%,0 100%)`) : "none";''')
rep('const sc1 = E.inOutCubic(P(t, 10.35, 11.2)) * 1050 + E.inOutCubic(P(t, 11.45, 12.35)) * 1500;','const sc1 = 1100 + E.inOutCubic(P(t, 10.45, 11.2)) * 850 + E.inOutCubic(P(t, 11.45, 12.35)) * 1150;')
rep('const sc2 = E.inOutCubic(P(t, 10.45, 12.35)) * 2300;','const sc2 = 960 + E.inOutCubic(P(t, 10.5, 12.35)) * 1700;')
rep('lineAnim(sp, t, 10.06 + i * .08, null, { din: .6 })','lineAnim(sp, t, 10.16 + i * .08, null, { din: .6 })')
rep('rb.style.transform = `scaleX(${cur === 0 ? E.outExpo(P(t, 10.3, 10.7)) : 1})`;','rb.style.transform = `scaleX(${cur === 0 ? E.outExpo(P(t, 10.4, 10.8)) : 1})`;')

# ---------- S6
i0=s.index('  const ink = $("ink6")')
i1=s.index('  const s6 = $("s6")', i0)
s=s[:i0]+'''  const ink = $("ink6"), onI = t >= 12.3; vis(ink, onI);
  if (onI) {
    const pr = E.inOutCubic(P(t, 12.3, 12.82)), base = lerp(-110 * U, H + 150 * U, pr), pts = [];
    for (let i = 0; i <= 40; i++) { const x = i / 40 * W; const dr = (Math.sin(i * 1.37) * .5 + .5) * (Math.sin(i * .53 + 1) * .5 + .5) * 120 * U * Math.sin(Math.min(1, pr * 1.02) * Math.PI * .98 + .01); pts.push(`${x.toFixed(1)}px ${(base + dr).toFixed(1)}px`); }
    ink.style.clipPath = `polygon(0 0,100% 0,${pts.reverse().join(",")})`;
  }
'''+s[i1:]
rep('const lk = $("lock6"); lk.style.transform = `translate(${(W - M.lock.w) / 2}px,${G.s6.cy - M.lock.h / 2}px)`;','const lk = $("lock6"); lk.style.transform = `translate(${(W - M.lock.w) / 2 - M.lockShift}px,${G.s6.cy - M.lock.h / 2}px)`;')
rep('gk = E.outCubic(P(t, 13.0, 13.8))','gk = lerp(.4 * E.outCubic(P(t, 12.7, 13.0)), 1, E.outCubic(P(t, 13.0, 13.8)))')
rep('const sub = $("sub6"), ks = E.outExpo(P(t, 14.0, 14.5));','const sub = $("sub6"), ks = E.outExpo(P(t, 13.9, 14.35));')
rep('const syy = cy6 + M.cta.h + (URLTXT ? 40 : 46) * U;','''const syy = cy6 + M.cta.h + 44 * U;
    const lg = $("legal6"), kl = E.outExpo(P(t, 14.0, 14.45));
    lg.style.transform = `translate(${(W - M.legal.w) / 2}px,${syy + (URLTXT ? M.url.h : M.sub.h) + 26 * U + (1 - kl) * 12 * U}px)`; lg.style.opacity = kl * .95;''')

# ---------- liquid scenes (press, wave) — replace old blocks
i0=s.index('  if (t >= 2.36 && t < 3.0) {')
i1=s.index('  if (t >= 9.8 && t < 10.34) {')
i2=s.index('  if (t >= 12.5 && t < 13.7) {')
press='''  if (t >= 2.36 && t < 3.0) {
    const half = Math.min(M.card.w * (LAND ? 1.12 : 1) * .5, W * .4);
    DROPS.forEach(d => { const t0 = 2.4 + d.d; if (t < t0) return; const dt = t - t0, gpx = 2400 * U;
      BF.push({ x: W / 2 + d.side * half * .9 + d.vx * U * dt, y: H / 2 + d.vy * U * dt + .5 * gpx * dt * dt, r: d.r0 * U * E.outCubic(P(t, t0, t0 + .08)) * (1 - .45 * P(t, t0, 3.0)), c: d.c }); });
    const env = E.outCubic(P(t, 2.38, 2.6)) * (1 - E.inCubic(P(t, 2.72, 2.9)));
    const spread = half * (.7 + .5 * E.outExpo(P(t, 2.38, 2.74)));
    for (let i = 0; i < 17; i++) { const u = (i - 8) / 8; BF.push({ x: W / 2 + u * spread, y: H / 2 + Math.sin(i * 1.9 + t * 11) * 5 * U, r: 50 * U * env * (.8 + .3 * Math.sin(i * 2.3 + t * 9)), c: [C.orange, C.berry, C.mango, C.peach][i % 4] }); }
    flood(t, W / 2, floodC(t), floodR1(t), BF);
  }
'''
wave='''  if (t >= 9.9 && t < 10.5) {
    const p = waveP(t);
    for (let i = -1; i <= 9; i++) { const jit = Math.sin(i * 2.1 + t * 7) * (LAND ? H : W) * .02;
      BF.push(LAND ? { x: p + jit, y: H * i / 8, r: WR, c: ANC[(i + 8) % 8] } : { x: W * i / 8, y: p + jit, r: WR, c: ANC[(i + 8) % 8] }); }
    for (let i = 0; i < 5; i++) BF.push(LAND ? { x: p - W * .07 * (1 + i % 3), y: H * (.1 + .2 * i), r: H * .15, c: ANC[(i * 3) % 8] } : { x: W * (.1 + .2 * i), y: p + H * .035 * (1 + i % 3), r: W * .16, c: ANC[(i * 3) % 8] });
  }
'''
rest=s[i1:i2]
end_old=rest.index('\n  }\n')+5
between=rest[end_old:]
s=s[:i0]+press+wave+between+s[i2:]

rep('if (t >= 3.0 && t < 3.98) flood(t, W / 2, H / 2, floodR1(t), BB);','if (t >= 3.0 && t < 4.0) flood(t, W / 2, floodC(t), floodR1(t), BB);')
rep('if (t >= 10.25 && t < 12.64) hug(lapRect(t), .6 * E.outCubic(P(t, 10.25, 10.8)), t, BB);','if (t >= 10.42 && t < 12.85) hug(lapRect(t), .6 * E.outCubic(P(t, 10.42, 10.95)), t, BB);')
rep('const s = E.outCubic(P(t, 3.55, 4.15))','const s = E.outCubic(P(t, 3.6, 4.2))')

# drop fall + splash
rep('''    if (t < 12.97) { const k = E.inQuad(P(t, 12.55, 12.97)); const y = lerp(-90 * U, yI, k); const st = 1 + 2.2 * k;
      BF.push({ x: x0, y, r: 44 * U, c: C.orange }); BF.push({ x: x0, y: y - 34 * U * st, r: 24 * U, c: C.mango }); BF.push({ x: x0, y: y - 62 * U * st, r: 12 * U, c: C.gold }); }''','''    if (t < 12.97) { const k = E.inQuad(P(t, 12.5, 12.97)); const y = lerp(H * .05, yI, k); const st = 1 + .55 * k, g = E.outCubic(P(t, 12.5, 12.62));
      BF.push({ x: x0, y, r: 62 * U * g, c: C.orange }); BF.push({ x: x0, y: y - 30 * U * st, r: 42 * U * g, c: C.peach }); BF.push({ x: x0, y: y - 54 * U * st, r: 26 * U * g, c: C.mango }); BF.push({ x: x0, y: y - 80 * U * st, r: 14 * U * g, c: C.gold }); }''')
rep('BF.push({ x: x0 + c.vx * U * dt, y: yI + c.vy * U * dt + .5 * g * dt * dt, r: c.r0 * U * (1 - P(t, 13.15, 13.62)), c: c.c });','BF.push({ x: x0 + Math.sign(c.vx) * 24 * U + c.vx * U * dt, y: yI + c.vy * U * dt + .5 * g * dt * dt, r: c.r0 * U * E.outCubic(P(t, 12.97, 13.05)) * (1 - P(t, 13.15, 13.62)), c: c.c });')
open(p,'w',encoding='utf-8').write(s); print('patch2 ok')
