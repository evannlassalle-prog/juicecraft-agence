import sys, pathlib
p = pathlib.Path(sys.argv[1])
s = p.read_text(encoding='utf-8')
def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:90])
    s = s.replace(old, new)

CHK = '<li><svg><use href="#chk"/></svg>'

# A. chapeau de la section Offres
rep("Trois offres à prix affichés, toutes taxes comprises. La mise en place du site est payée une fois.",
    "Trois offres à prix affichés, TVA non applicable (art. 293 B du CGI). La mise en place du site est payée une fois.")

# B. blocs de prix : plus de TTC
rep('<div class="price"><b>49 €<span>/mois TTC</span></b><small>ou 490 € TTC par an<br>+ 290 € TTC de mise en place</small></div>',
    '<div class="price"><b>49 €<span>/mois</span></b><small>ou 490 € par an<br>+ 290 € de mise en place</small></div>')
rep('<div class="price"><b>89 €<span>/mois TTC</span></b><small>ou 890 € TTC par an<br>+ 590 € TTC de mise en place</small></div>',
    '<div class="price"><b>89 €<span>/mois</span></b><small>ou 890 € par an<br>+ 590 € de mise en place</small></div>')
rep('<div class="price"><b>149 €<span>/mois TTC</span></b><small>ou 1 490 € TTC par an<br>Mise en place dès 1 690 € TTC, sur devis</small></div>',
    '<div class="price"><b>149 €<span>/mois</span></b><small>ou 1 490 € par an<br>Mise en place dès 1 690 €, sur devis</small></div>')

# C. contenu des offres aligné sur les descriptions Shopify (pages, hébergement, maintenance, assistance)
rep(CHK + 'Design moderne et professionnel</li>',
    CHK + "Jusqu'à 5 pages</li>\n          " + CHK + 'Design moderne et professionnel</li>')
rep(CHK + 'Mise en ligne</li>\n        </ul>',
    CHK + 'Mise en ligne</li>\n          ' + CHK + 'Hébergement, maintenance et assistance inclus</li>\n        </ul>')
rep(CHK + 'Tout ce qui est inclus dans Essentielle</li>',
    CHK + 'Tout ce qui est inclus dans Essentielle</li>\n          ' + CHK + "Jusqu'à 10 pages</li>")
rep(CHK + 'Accompagnement après livraison</li>\n        </ul>',
    CHK + 'Accompagnement après livraison</li>\n          ' + CHK + 'Modifications régulières et assistance prioritaire</li>\n        </ul>')
rep(CHK + 'Conception entièrement adaptée à votre besoin</li>',
    CHK + 'Tout le contenu de Premium</li>\n          ' + CHK + 'Conception entièrement adaptée à votre besoin</li>')
rep(CHK + 'Modifications incluses : 2 h par mois, au-delà sur devis</li>',
    CHK + 'Maintenance renforcée et accompagnement personnalisé</li>\n          ' + CHK + 'Modifications incluses : 2 h par mois, au-delà sur devis</li>')

# D. note sous les offres
rep('<p class="plans-note">Tous les prix sont TTC. À la commande,',
    '<p class="plans-note">Prix nets : TVA non applicable, art. 293 B du CGI. À la commande,')

# E. FAQ
rep("Prix toutes taxes comprises. Essentielle : 290 € de mise en place, puis 49 €/mois (12 mois d'engagement) ou 490 € par an. Premium : 590 € de mise en place, puis 89 €/mois ou 890 € par an. Sur mesure : mise en place dès 1 690 € sur devis, puis 149 €/mois ou 1 490 € par an. Pour un besoin",
    "TVA non applicable, art. 293 B du CGI. Essentielle : 290 € de mise en place, puis 49 €/mois ou 490 € par an. Premium : 590 € de mise en place, puis 89 €/mois ou 890 € par an. Sur mesure : mise en place dès 1 690 € sur devis, puis 149 €/mois ou 1 490 € par an. L'abonnement mensuel engage sur 12 mois ; l'abonnement annuel offre 2 mois. L'abonnement comprend l'hébergement, la maintenance et l'assistance. Pour un besoin")
rep("Oui. L'étape Validation prévoit des allers-retours ; le nombre de tours inclus est précisé dans l'offre et dans les CGV.",
    "Oui. L'étape Validation prévoit des allers-retours avant la mise en ligne. Ensuite, les modifications sont incluses selon l'offre : corrections et petites modifications (Essentielle), modifications régulières (Premium), 2 h par mois (Sur mesure, au-delà sur devis).")
rep("Nous restons disponibles. Selon l'offre, un accompagnement après livraison est inclus, et une maintenance peut être mise en place selon vos besoins.",
    "Nous restons disponibles. Les trois offres incluent l'hébergement, la maintenance et l'assistance. Premium ajoute une assistance prioritaire, Sur mesure une maintenance renforcée et un accompagnement personnalisé.")

# F. tuile maintenance : incluse dans les trois offres (trois lignes fixes, « Évolutions » sur demande)
rep('<div class="tx"><h3>Maintenance possible</h3><p>Une intervention ultérieure reste possible selon vos besoins : mises à jour, sauvegardes, évolutions. Activez, désactivez, c\'est vous qui choisissez.</p></div>',
    '<div class="tx"><h3>Maintenance incluse</h3><p>Mises à jour, sauvegardes et surveillance sont comprises dans les trois offres. Les évolutions se font sur demande.</p></div>')
rep('<button class="mt-row" aria-pressed="true"><span><b>Mises à jour</b><small>Régulières</small></span><span class="tg"></span></button>',
    '<div class="mt-row inc"><span><b>Mises à jour</b><small>Régulières</small></span><span class="tg" aria-hidden="true"></span></div>')
rep('<button class="mt-row" aria-pressed="true"><span><b>Sauvegardes</b><small>Quotidiennes</small></span><span class="tg"></span></button>',
    '<div class="mt-row inc"><span><b>Sauvegardes</b><small>Quotidiennes</small></span><span class="tg" aria-hidden="true"></span></div>')
rep('<button class="mt-row" aria-pressed="true"><span><b>Surveillance</b><small>Site disponible</small></span><span class="tg"></span></button>',
    '<div class="mt-row inc"><span><b>Surveillance</b><small>Site disponible</small></span><span class="tg" aria-hidden="true"></span></div>')
rep('.mt-row[aria-pressed="true"] .tg{background:var(--leaf)}\n.mt-row[aria-pressed="true"] .tg::after{transform:translateX(17px)}\n',
    '.mt-row[aria-pressed="true"] .tg,.mt-row.inc .tg{background:var(--leaf)}\n.mt-row[aria-pressed="true"] .tg::after,.mt-row.inc .tg::after{transform:translateX(17px)}\n')
rep('$$(".mt-row").forEach(b => b.addEventListener(',
    '$$("button.mt-row").forEach(b => b.addEventListener(')

# G. configurateur : tailles alignées sur les plafonds de pages (5 et 10), prix sans TTC
rep('["few", "Quelques pages", "De 2 à 6 pages"]', '["few", "Quelques pages", "De 2 à 5 pages"]')
rep('["many", "Un site complet", "7 pages ou plus"]', '["many", "Un site complet", "De 6 à 10 pages"]')
rep("à partir de 149 € par mois TTC, mise en place sur devis.",
    "à partir de 149 € par mois (TVA non applicable), mise en place dès 1 690 € sur devis.")

p.write_text(s, encoding='utf-8')
print('site patché :', p)
