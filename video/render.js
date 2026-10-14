// usage: node render.js stills W H outdir t1,t2,...   |   node render.js seq W H outdir fps sub [t0] [t1]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'), fs = require('fs');
const [mode, W, H, out, a, b, c, d] = process.argv.slice(2);
(async () => {
  const br = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--font-render-hinting=none', '--disable-lcd-text'] });
  const pg = await br.newPage({ viewport: { width: +W, height: +H }, deviceScaleFactor: 1 });
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto('file://' + path.join(__dirname, process.env.VIDEO_HTML || 'video.html') + `?w=${W}&h=${H}` + (process.env.AD_URL ? '&url=' + encodeURIComponent(process.env.AD_URL) : ''), { waitUntil: 'networkidle' });
  await pg.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  fs.mkdirSync(out, { recursive: true });
  const shot = async (t, file) => { await pg.evaluate(t => window.seek(t), t); await pg.screenshot({ path: file, type: 'png', clip: { x: 0, y: 0, width: +W, height: +H } }); };
  const t0 = Date.now();
  if (mode === 'stills') {
    for (const t of a.split(',').map(Number)) await shot(t, path.join(out, `t${t.toFixed(3)}.png`));
  } else {
    const fps = +a, sub = +b, from = c ? +c : 0, to = d ? +d : 15;
    const i0 = Math.round(from * fps * sub), i1 = Math.round(to * fps * sub), n = i1 - i0;
    for (let i = i0; i < i1; i++) {
      const t = (i + .5) / (fps * sub);   // centred sub-frame samples
      const fpth = path.join(out, String(i).padStart(5, '0') + '.png');
      if (process.env.RESUME && fs.existsSync(fpth) && fs.statSync(fpth).mtimeMs > fs.statSync(path.join(__dirname, process.env.VIDEO_HTML || 'video.html')).mtimeMs) continue;
      await shot(t, fpth);
      if ((i - i0) % 200 === 0) console.log(i - i0, '/', n, ((Date.now() - t0) / 1000).toFixed(1) + 's');
    }
  }
  console.log('done in', ((Date.now() - t0) / 1000).toFixed(1), 's', errs.length ? 'ERRORS: ' + errs.join(' | ') : 'no errors');
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
