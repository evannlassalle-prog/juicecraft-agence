const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, '..', 'svg');
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg')).sort();
  const cell = f => {
    const dark = /fond-sombre|blanc|badge_blanc/.test(f) && !/badge_clair/.test(f);
    return `<div class="c" style="background:${dark ? '#1A181F' : (/pastille|badge_encre|sur-fond-encre/.test(f) ? '#E9E8E4' : '#F2F2EF')}"><img src="file://${dir}/${f}"><small>${f.replace('juicecraft_logo-','').replace('.svg','')}</small></div>`;
  };
  const html = `<style>body{margin:0;background:#ccc;font:12px sans-serif}.g{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:8px}.c{display:grid;place-items:center;height:260px;position:relative;border-radius:8px}img{max-width:88%;max-height:170px}small{position:absolute;bottom:6px;left:8px;color:#888}</style><div class="g">${files.map(cell).join('')}</div>`;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1700, height: 1000 } });
  fs.writeFileSync(path.join(__dirname,'preview.html'), html); await p.goto('file://'+path.join(__dirname,'preview.html')); await p.waitForTimeout(800);
  await p.screenshot({ path: path.join(__dirname, 'preview.png'), fullPage: true });
  await b.close();
})();
