// lecture seule : compare l'accueil et le catalogue entre le thème en ligne et le thème brouillon
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const BASE = 'https://juicecraft-store.myshopify.com';
const theme = process.argv[2];
(async () => {
  const br = await chromium.launch();
  for (const p of ['/', '/collections/all']) {
    const res = {};
    for (const [label, q] of [['live', ''], ['brouillon', '?preview_theme_id=' + theme]]) {
      const pg = await (await br.newContext({ viewport: { width: 1366, height: 900 }, locale: 'fr-FR' })).newPage();
      const errs = []; pg.on('pageerror', e => errs.push(e.message));
      const r = await pg.goto(BASE + p + q, { waitUntil: 'load', timeout: 90000 });
      await pg.waitForTimeout(3000);
      res[label] = { status: r.status(), prices: await pg.evaluate(() => [...document.querySelectorAll('.price')].filter(e => e.getBoundingClientRect().width > 0).map(e => e.textContent.replace(/\s+/g, ' ').trim()).slice(0, 14)), height: await pg.evaluate(() => document.documentElement.scrollHeight), errs };
      await pg.context().close();
    }
    console.log(p, JSON.stringify(res));
  }
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
