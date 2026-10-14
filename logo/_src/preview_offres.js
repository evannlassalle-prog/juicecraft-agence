const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, '..', 'svg');
  const fl = fs.readdirSync(dir).filter(f => f.startsWith('juicecraft_offre-')).sort();
  const emb = fl.filter(f => f.includes('embleme')), hz = fl.filter(f => f.endsWith('logo-horizontal.svg')), hd = fl.filter(f => f.includes('fond-sombre'));
  const row = (arr, bg, h) => `<div style="display:flex;gap:16px;background:${bg};padding:24px;justify-content:center;align-items:center">${arr.map(f => `<img src="file://${dir}/${f}" style="height:${h}px">`).join('')}</div>`;
  const html = `<body style="margin:0;background:#ddd">${row(emb, '#E9E8E4', 360)}${row(hz, '#F2F2EF', 150)}${row(hd, '#17151B', 150)}</body>`;
  fs.writeFileSync(path.join(__dirname, 'po.html'), html);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1700, height: 900 } });
  await p.goto('file://' + path.join(__dirname, 'po.html')); await p.waitForTimeout(500);
  await p.screenshot({ path: path.join(__dirname, 'po.png'), fullPage: true }); await b.close();
})();
