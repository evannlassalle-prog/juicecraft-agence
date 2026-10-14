import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)

# 1. CSS : "/mois" hors du texte à dégradé (l'opacité d'un enfant rendait le texte invisible)
rep('.pp9{font:700 3.2rem/1 var(--fd);letter-spacing:-.03em;background:linear-gradient(100deg,#FFB21A,#FF5A1F 50%,#EE2A7B);-webkit-background-clip:text;background-clip:text;color:transparent;width:max-content}\n'
    '.pp9 em{font-style:normal;font-size:.55em;font-weight:600;letter-spacing:0;margin-left:.25em;opacity:.9}\n',
    '.pp9{font:700 3.2rem/1 var(--fd);letter-spacing:-.03em;display:flex;align-items:baseline;gap:.3em;width:max-content}\n'
    '.pp9 .v9{background:linear-gradient(100deg,#FFB21A,#FF5A1F 50%,#EE2A7B);-webkit-background-clip:text;background-clip:text;color:transparent}\n'
    '.pp9 em{font-style:normal;font-size:.58em;font-weight:600;letter-spacing:0;color:#65616C}\n'
    '.pl9.feat .pp9 em{color:#A29EAA}\n')

# 2. CSS : mention légale en petit
rep('#s9note i{display:grid;place-items:center;width:4.4rem;height:4.4rem;border-radius:50%;background:#1FA971;color:#fff;font-style:normal;font-size:2.4rem}\n',
    '#s9note i{display:grid;place-items:center;width:4.4rem;height:4.4rem;border-radius:50%;background:#1FA971;color:#fff;font-style:normal;font-size:2.4rem}\n'
    '#s9legal{position:absolute;left:0;top:0;display:flex;flex-wrap:wrap;justify-content:center;column-gap:2.4rem;row-gap:.4rem;text-align:center;font:500 1.8rem/1.3 var(--fm);letter-spacing:.03em;color:#6A6672}\n'
    '#s9legal span{white-space:nowrap}\n')

# 3. Marquage : prix sans TTC, mise en place Sur mesure "dès 1 690 €"
rep('<span class="pp9">49 €<em>/mois</em></span><small class="ps9">TTC · + 290 € de mise en place</small>',
    '<span class="pp9"><span class="v9">49 €</span><em>/mois</em></span><small class="ps9">+ 290 € de mise en place</small>')
rep('<span class="pp9">89 €<em>/mois</em></span><small class="ps9">TTC · + 590 € de mise en place</small>',
    '<span class="pp9"><span class="v9">89 €</span><em>/mois</em></span><small class="ps9">+ 590 € de mise en place</small>')
rep('<span class="pp9">149 €<em>/mois</em></span><small class="ps9">TTC · mise en place sur devis</small>',
    '<span class="pp9"><span class="v9">149 €</span><em>/mois</em></span><small class="ps9">+ mise en place dès 1 690 €</small>')
rep('<div id="s9note"><i>✓</i>Prix clairs, affichés TTC.</div>\n',
    '<div id="s9note"><i>✓</i>Prix clairs, sans TVA à ajouter.</div>\n'
    '    <div id="s9legal"><span>TVA non applicable, art. 293 B du CGI.</span><span>Abonnement mensuel : engagement de 12 mois.</span></div>\n')

# 4. Mise en page : mention légale sous la pastille
rep('const h9 = $("s9h"), k9 = $("s9k"), plans = [$("pl1"), $("pl2"), $("pl3")], note = $("s9note");',
    'const h9 = $("s9h"), k9 = $("s9k"), plans = [$("pl1"), $("pl2"), $("pl3")], note = $("s9note"), legal9 = $("s9legal");\n'
    '  legal9.style.width = (W - 2 * 90 * U) + "px";')
rep('note, noteW: note.offsetWidth, h9L:',
    'note, noteW: note.offsetWidth, noteH: note.offsetHeight, legal: legal9, legalW: W - 2 * 90 * U, h9L:')

# 5. Animation : la mention apparaît juste après la pastille
rep('  X.note.style.transform = `translate(${(W - X.noteW) / 2}px,${X.noteY + (1 - kn) * 18 * U}px)`;\n}',
    '  X.note.style.transform = `translate(${(W - X.noteW) / 2}px,${X.noteY + (1 - kn) * 18 * U}px)`;\n'
    '  const kl = E.outExpo(P(T, 23.75, 24.15));\n'
    '  X.legal.style.opacity = kl;\n'
    '  X.legal.style.transform = `translate(${(W - X.legalW) / 2}px,${X.noteY + X.noteH + 22 * U + (1 - kl) * 12 * U}px)`;\n}')

open(p, 'w', encoding='utf-8').write(s)
print('patched', p)
