// contrôle local du site construit : fichier local, requêtes externes bloquées, aucun envoi de formulaire
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [file, out] = process.argv.slice(2);
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const br = await chromium.launch();
  const errs = [];
  for (const [label, vw, vh] of [['desktop', 1440, 900], ['mobile', 390, 844]]) {
    const ctx = await br.newContext({ viewport: { width: vw, height: vh }, locale: 'fr-FR' });
    const pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push(label + ' pageerror: ' + e.message));
    pg.on('console', m => { if (m.type() === 'error' && !/fonts\.g|net::ERR/.test(m.text())) errs.push(label + ' console: ' + m.text()); });
    await pg.route(/^https?:\/\//, r => r.abort());
    await pg.goto('file://' + file, { waitUntil: 'load' });
    const H = await pg.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += 500) { await pg.evaluate(y => window.scrollTo(0, y), y); await pg.waitForTimeout(120); }
    await pg.waitForTimeout(600);
    const txt = await pg.evaluate(() => document.body.innerText);
    const checks = {
      'aucun TTC': !/\bTTC\b|toutes taxes comprises/i.test(txt),
      'mention TVA': /TVA non applicable, art\. 293 B du CGI/.test(txt),
      'maintenance incluse': /Maintenance incluse/.test(txt) && !/Maintenance possible/.test(txt),
      'pages 5 et 10': /Jusqu'à 5 pages/.test(txt) && /Jusqu'à 10 pages/.test(txt),
    };
    console.log(label, JSON.stringify(checks));
    const off = await pg.$('#offres'); await off.scrollIntoViewIfNeeded(); await pg.waitForTimeout(900);
    await off.screenshot({ path: path.join(out, `${label}_offres.png`) });
    const mt = await pg.$('.t-maint'); await mt.scrollIntoViewIfNeeded(); await pg.waitForTimeout(900);
    await mt.screenshot({ path: path.join(out, `${label}_maintenance.png`) });
    if (label === 'desktop') {
      const state = () => pg.evaluate(() => [...document.querySelectorAll('.mt-row')].map(e => e.className + '|' + e.getAttribute('aria-pressed')));
      const before = await state();
      await pg.click('.mt-row.inc >> nth=0', { force: true });
      await pg.click('button.mt-row');
      const after = await state();
      console.log('lignes maintenance avant', JSON.stringify(before));
      console.log('lignes maintenance après', JSON.stringify(after));
      for (const q of ['#q1', '#q4', '#q6']) { const b = await pg.$(q); if ((await b.getAttribute('aria-expanded')) !== 'true') await b.click(); await pg.waitForTimeout(500); }
      const faq = await pg.$('#faq-list'); await faq.scrollIntoViewIfNeeded(); await pg.waitForTimeout(800);
      await faq.screenshot({ path: path.join(out, 'desktop_faq.png') });
      for (const a of ['#a1', '#a4', '#a6']) console.log('FAQ ' + a + ' :', await pg.evaluate(s => document.querySelector(s).innerText, a));
      const cfg = await pg.$('#cfg-body'); await cfg.scrollIntoViewIfNeeded(); await pg.waitForTimeout(700);
      await pg.click('.opt[data-v="present"]'); await pg.waitForTimeout(500);
      console.log('config tailles :', await pg.evaluate(() => [...document.querySelectorAll('.opt small')].map(e => e.textContent).join(' | ')));
      await pg.click('.opt[data-v="many"]'); await pg.waitForTimeout(500);
      await pg.click('.opt[data-v="local"]'); await pg.waitForTimeout(700);
      console.log('config résultat :', await pg.evaluate(() => document.querySelector('.cfg-res').innerText.replace(/\n+/g, ' / ')));
    }
    await ctx.close();
  }
  console.log(errs.length ? 'ERREURS: ' + errs.join(' | ') : 'aucune erreur JS');
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
