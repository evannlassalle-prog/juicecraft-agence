const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2400, height: 1400 } });
  await p.goto('file://' + path.join(__dirname, 'board.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1200);
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  await p.screenshot({ path: path.join(__dirname, '..', 'juicecraft_planche-de-marque.png'), fullPage: true });
  await p.pdf({ path: path.join(__dirname, '..', 'juicecraft_planche-de-marque.pdf'), width: '2400px', height: h + 'px', printBackground: true });
  console.log('height', h); await b.close();
})();
