// lecture seule : choisit « Abonnement Annuel » dans le sélecteur de la fiche (aucun ajout au panier), relève les prix affichés
// usage : node annual.js <outdir> <label> [previewThemeId]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [out, label, theme] = process.argv.slice(2);
const BASE = 'https://juicecraft-store.myshopify.com';
const PAGES = [['essentielle', '/products/essentielle'], ['premium', '/products/%F0%9F%94%B5-premium-%E2%AD%90'], ['mesure', '/products/sur-mesure']];
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const br = await chromium.launch();
  for (const [key, p] of PAGES) {
    const ctx = await br.newContext({ viewport: { width: 1366, height: 900 }, locale: 'fr-FR' });
    const pg = await ctx.newPage();
    try {
      await pg.goto(BASE + p + (theme ? '?preview_theme_id=' + theme : ''), { waitUntil: 'load', timeout: 90000 });
      await pg.waitForTimeout(4000);
      const sel = await pg.$('select');
      const res = { key, hasSelect: !!sel };
      const snap = async (tag) => {
        res[tag] = await pg.evaluate(() => {
          const t = e => e ? e.innerText.replace(/\s+/g, ' ').trim() : null;
          const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).display !== 'none'; };
          const struck = [...document.querySelectorAll('[style*="line-through"], s, del, .compare-at-price')].filter(vis).map(e => e.textContent.replace(/\s+/g, ' ').trim()).filter(Boolean);
          return { main: t(document.querySelector('product-price')), sticky: t(document.querySelector('.sticky-add-to-cart__price')), widget: t(document.querySelector('[class*="appstle"][class*="widget"], #appstle_subscription_widget0')) && t(document.querySelector('[class*="appstle"][class*="widget"], #appstle_subscription_widget0')).slice(0, 160), struckVisible: struck };
        });
      };
      await snap('mensuel');
      if (sel) {
        const opts = await sel.$$eval('option', o => o.map(x => x.textContent.trim()));
        res.options = opts;
        const idx = opts.findIndex(o => /annuel/i.test(o));
        if (idx >= 0) { await sel.selectOption({ index: idx }); await pg.waitForTimeout(2500); await snap('annuel'); }
      }
      await pg.screenshot({ path: path.join(out, `${label}_${key}_annuel.png`) });
      console.log(JSON.stringify(res));
    } catch (e) { console.log(key, 'erreur', String(e).slice(0, 160)); }
    await ctx.close();
  }
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
