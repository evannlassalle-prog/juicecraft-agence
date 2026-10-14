// usage: node render_anim.js <svg> <out_dir> <W> <H> <logoWidthRatio> <bg|transparent> [fps] [dur]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [svgName, outDir, W, H, ratio, bg, fps = '60', dur = '3.6'] = process.argv.slice(2);
(async () => {
  const svg = fs.readFileSync(path.join(__dirname, '..', 'animation', svgName), 'utf8');
  const vb = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const lw = Math.round(+W * +ratio), lh = Math.round(lw * vb[2] / vb[1]);
  const inner = svg.replace(/<svg ([^>]*?)width="[\d.]+" height="[\d.]+"/, `<svg $1width="${lw}" height="${lh}"`);
  const html = `<style>html,body{margin:0;width:${W}px;height:${H}px;background:${bg === 'transparent' ? 'transparent' : bg};overflow:hidden}svg{position:absolute;left:${Math.round((+W - lw) / 2)}px;top:${Math.round((+H - lh) / 2)}px;overflow:visible}</style>${inner}`;
  fs.writeFileSync(path.join(__dirname, '_a.html'), html);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +W, height: +H } });
  await p.goto('file://' + path.join(__dirname, '_a.html'));
  fs.rmSync(outDir, { recursive: true, force: true }); fs.mkdirSync(outDir, { recursive: true });
  const n = Math.round(+fps * +dur);
  for (let i = 0; i < n; i++) {
    const t = (i + .5) / +fps;
    await p.evaluate(t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; }), t);
    await p.screenshot({ path: path.join(outDir, String(i).padStart(4, '0') + '.png'), omitBackground: bg === 'transparent' });
  }
  await b.close(); console.log(svgName, n, 'frames');
})();
