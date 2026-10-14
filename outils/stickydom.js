// lecture seule : relève le HTML du prix dans la barre d'ajout rapide et dans la zone de prix principale
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const br = await chromium.launch();
  const pg = await (await br.newContext({ viewport: { width: 1366, height: 900 }, locale: 'fr-FR' })).newPage();
  await pg.goto('https://juicecraft-store.myshopify.com/products/essentielle', { waitUntil: 'load', timeout: 90000 });
  await pg.waitForTimeout(4000);
  await pg.evaluate(() => window.scrollTo(0, 1600));
  await pg.waitForTimeout(1500);
  const r = await pg.evaluate(() => ({
    sticky: (document.querySelector('.sticky-add-to-cart__price') || {}).outerHTML,
    main: [...document.querySelectorAll('product-price')].map(e => e.outerHTML.slice(0, 900)),
    appstle: [...document.querySelectorAll('[class*="appstle"], [id*="appstle"]')].slice(0, 6).map(e => e.tagName + '#' + e.id + '.' + e.className),
  }));
  console.log(JSON.stringify(r, null, 1));
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
