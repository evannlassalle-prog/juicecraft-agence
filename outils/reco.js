// lecture seule : prix affichés dans « You may also like » et les cartes produit de chaque fiche
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const BASE = 'https://juicecraft-store.myshopify.com';
const PAGES = [['essentielle', '/products/essentielle'], ['premium', '/products/%F0%9F%94%B5-premium-%E2%AD%90'], ['mesure', '/products/sur-mesure']];
const theme = process.argv[2];
(async () => {
  const br = await chromium.launch();
  for (const [key, p] of PAGES) {
    const pg = await (await br.newContext({ viewport: { width: 1366, height: 900 }, locale: 'fr-FR' })).newPage();
    await pg.goto(BASE + p + (theme ? '?preview_theme_id=' + theme : ''), { waitUntil: 'load', timeout: 90000 });
    await pg.waitForTimeout(3500);
    const h = await pg.$('text=/you may also like/i');
    if (h) { await h.scrollIntoViewIfNeeded(); await pg.waitForTimeout(2500); }
    const cards = await pg.evaluate(() => [...document.querySelectorAll('product-recommendations product-card, product-recommendations .product-card, product-recommendations li')]
      .map(e => ({ txt: e.innerText.replace(/\s+/g, ' ').trim(), struck: [...e.querySelectorAll('[style*="line-through"], s, del, .compare-at-price')].filter(x => x.getBoundingClientRect().width > 0).map(x => x.textContent.trim()) }))
      .filter(c => c.txt));
    console.log(key, JSON.stringify(cards));
    await pg.context().close();
  }
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
