const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
// [fichier svg, largeur px, dossier, nom de sortie]
const jobs = [];
const add = (svg, w, out) => jobs.push([svg, w, out]);
const lock = ['principal_couleur','principal_fond-sombre','principal_noir','principal_blanc','secondaire_empile_couleur','secondaire_empile_fond-sombre','secondaire_empile_noir','secondaire_empile_blanc','secondaire_empile_signature','secondaire_mot-seul_noir','secondaire_mot-seul_blanc'];
lock.forEach(n => { add(`juicecraft_logo-${n}.svg`, 3000, `png/juicecraft_logo-${n}_3000px.png`); add(`juicecraft_logo-${n}.svg`, 800, `png/juicecraft_logo-${n}_800px.png`); });
['principal_sur-fond-encre'].forEach(n => { add(`juicecraft_logo-${n}.svg`, 3000, `png/juicecraft_logo-${n}_3000px.png`); });
['secondaire_badge_encre','secondaire_badge_clair','secondaire_badge_blanc'].forEach(n => { add(`juicecraft_logo-${n}.svg`, 2000, `png/juicecraft_logo-${n}_2000px.png`); add(`juicecraft_logo-${n}.svg`, 600, `png/juicecraft_logo-${n}_600px.png`); });
['icone_couleur','icone_noir','icone_blanc'].forEach(n => { add(`juicecraft_logo-${n}.svg`, 1024, `png/juicecraft_logo-${n}_1024px.png`); add(`juicecraft_logo-${n}.svg`, 256, `png/juicecraft_logo-${n}_256px.png`); });
['icone_pastille_encre','icone_pastille_clair','icone_pastille_degrade'].forEach(n => { add(`juicecraft_logo-${n}.svg`, 1024, `png/juicecraft_logo-${n}_1024px.png`); add(`juicecraft_logo-${n}.svg`, 400, `png/juicecraft_logo-${n}_400px.png`); });
// pack favicon (version simplifiée pour les petites tailles)
[16, 32, 48, 64, 96].forEach(w => add('juicecraft_logo-icone_favicon-simplifie.svg', w, `favicon/favicon-${w}x${w}.png`));
[180].forEach(w => add('juicecraft_logo-icone_pastille_encre.svg', w, `favicon/apple-touch-icon.png`));
[192, 512].forEach(w => add('juicecraft_logo-icone_pastille_encre.svg', w, `favicon/icon-${w}.png`));
add('juicecraft_logo-icone_pastille_encre.svg', 1080, 'png/photo-de-profil_1080px.png');
['essentielle','premium','sur-mesure'].forEach(k => {
  add(`juicecraft_offre-${k}_embleme.svg`, 2000, `png/juicecraft_offre-${k}_embleme_2000px.png`);
  add(`juicecraft_offre-${k}_embleme.svg`, 600, `png/juicecraft_offre-${k}_embleme_600px.png`);
  add(`juicecraft_offre-${k}_logo-horizontal.svg`, 3000, `png/juicecraft_offre-${k}_logo-horizontal_3000px.png`);
  add(`juicecraft_offre-${k}_logo-horizontal_fond-sombre.svg`, 3000, `png/juicecraft_offre-${k}_logo-horizontal_fond-sombre_3000px.png`);
});

(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  for (const [svg, w, out] of jobs) {
    const file = path.join(root, 'svg', svg);
    const m = fs.readFileSync(file, 'utf8').match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const h = Math.round(w * m[2] / m[1]);
    await p.setViewportSize({ width: w, height: h });
    fs.writeFileSync(path.join(__dirname, '_x.html'), `<style>html,body{margin:0;background:transparent}img{display:block;width:${w}px;height:${h}px}</style><img src="file://${file}">`);
    await p.goto('file://' + path.join(__dirname, '_x.html'));
    await p.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
    fs.mkdirSync(path.dirname(path.join(root, out)), { recursive: true });
    await p.screenshot({ path: path.join(root, out), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }
  await b.close(); console.log(jobs.length, 'images');
})();
