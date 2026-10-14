// usage: node storefront.js <outdir> <label>   — lecture seule : ouvre les 3 fiches produit, relève les prix affichés, ne passe jamais commande
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [out, label] = process.argv.slice(2);
const BASE = 'https://juicecraft-store.myshopify.com';
const PAGES = [
  ['essentielle', '/products/essentielle'],
  ['premium', '/products/%F0%9F%94%B5-premium-%E2%AD%90'],
  ['mesure', '/products/sur-mesure'],
];
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const br = await chromium.launch();
  const ctx = await br.newContext({ viewport: { width: 1366, height: 900 }, locale: 'fr-FR' });
  const res = {};
  for (const [key, p] of PAGES) {
    const pg = await ctx.newPage();
    try {
      await pg.goto(BASE + p, { waitUntil: 'load', timeout: 90000 });
      await pg.waitForTimeout(3500);
      // Cookie banner éventuel : on ne clique sur rien.
      const info = await pg.evaluate(() => {
        const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
        const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch (e) { return null; } }).filter(Boolean);
        const offers = [];
        const walk = o => { if (!o || typeof o !== 'object') return; if (o.offers) [].concat(o.offers).forEach(f => offers.push({ price: f.price, cur: f.priceCurrency })); Object.values(o).forEach(walk); };
        ld.forEach(walk);
        const strike = [...document.querySelectorAll('s, del, [class*="compare"], [class*="was"], [class*="strike"]')].filter(vis).map(e => e.textContent.replace(/\s+/g, ' ').trim()).filter(t => /€/.test(t)).slice(0, 12);
        const widget = (document.querySelector('[class*="appstle"], #appstle_subscription_widget0, [id*="appstle"]') || {}).innerText || '';
        const h = [...document.querySelectorAll('h1,h2,h3,h4,p,span')].find(e => /you may also like/i.test(e.textContent) && e.children.length === 0);
        let reco = null;
        if (h) { const sec = h.closest('section') || h.parentElement; reco = (sec.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 700); }
        return { title: document.title, offers, strike, widget: widget.replace(/\s+/g, ' ').slice(0, 300), reco, hasReco: !!h };
      });
      await pg.screenshot({ path: path.join(out, `${label}_${key}_haut.png`) });
      await pg.evaluate(() => window.scrollTo(0, 1600));
      await pg.waitForTimeout(1200);
      const sticky = await pg.evaluate(() => [...document.querySelectorAll('body *')].filter(e => { const s = getComputedStyle(e); return (s.position === 'fixed' || s.position === 'sticky') && /€/.test(e.innerText || '') && e.getBoundingClientRect().height > 0; }).map(e => (e.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 160)).slice(0, 5));
      await pg.screenshot({ path: path.join(out, `${label}_${key}_scroll.png`) });
      const h2 = await pg.$('text=/you may also like/i');
      if (h2) { await h2.scrollIntoViewIfNeeded(); await pg.waitForTimeout(1500); await pg.screenshot({ path: path.join(out, `${label}_${key}_reco.png`) }); }
      res[key] = { ...info, sticky };
    } catch (e) { res[key] = { error: String(e).slice(0, 200) }; }
    await pg.close();
  }
  // Pages catalogue
  const pg = await ctx.newPage();
  try {
    await pg.goto(BASE + '/collections/all', { waitUntil: 'load', timeout: 90000 });
    await pg.waitForTimeout(2500);
    res.catalogue = await pg.evaluate(() => [...document.querySelectorAll('a[href*="/products/"]')].map(a => (a.closest('li, .card-wrapper, .grid__item, article') || a).innerText.replace(/\s+/g, ' ').trim()).filter(t => /€/.test(t)).filter((t, i, a) => a.indexOf(t) === i).slice(0, 12));
    await pg.screenshot({ path: path.join(out, `${label}_catalogue.png`), fullPage: false });
  } catch (e) { res.catalogue = String(e).slice(0, 200); }
  await pg.close();
  fs.writeFileSync(path.join(out, `${label}.json`), JSON.stringify(res, null, 2));
  console.log(JSON.stringify(res, null, 1));
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
