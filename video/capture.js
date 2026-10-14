const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const dir = process.argv[2];
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--enable-unsafe-swiftshader'] });
  const shoot = async (vp, dpr, file, clipH, hover) => {
    const p = await b.newPage({ viewport: vp, deviceScaleFactor: dpr });
    await p.goto('file://' + dir + '/site.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    if (hover) await p.addStyleTag({ content: '.badge,.switch,.demo-cap{visibility:hidden!important}' });
    await p.waitForTimeout(2600);
    if (hover) { await p.mouse.move(hover[0], hover[1]); await p.waitForTimeout(1200); }
    if (clipH) await p.screenshot({ path: file, type: 'jpeg', quality: 93, fullPage: true, clip: { x: 0, y: 0, width: vp.width, height: clipH } });
    else await p.screenshot({ path: file, type: 'jpeg', quality: 93 });
    await p.close();
  };
  await shoot({ width: 1440, height: 900 }, 2, dir + '/desk_hero.jpg', 0, [520, 760]);
  await shoot({ width: 1440, height: 900 }, 1.5, dir + '/desk_long.jpg', 4700, [520, 760]);
  await shoot({ width: 390, height: 844 }, 2, dir + '/mob_long.jpg', 4200);
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
