import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)
rep('#s9legal{position:absolute;left:0;top:0;display:flex;flex-wrap:wrap;justify-content:center;column-gap:2.4rem;row-gap:.4rem;text-align:center;font:500 1.8rem/1.3 var(--fm);letter-spacing:.03em;color:#6A6672}\n'
    '#s9legal span{white-space:nowrap}\n',
    '#s9legal{position:absolute;left:0;top:0;display:flex;justify-content:center}\n'
    '#s9legal div{display:flex;flex-wrap:wrap;justify-content:center;column-gap:2.4rem;row-gap:.4rem;text-align:center;padding:.9rem 2.2rem;border-radius:1.6rem;background:rgba(251,251,249,.93);font:500 1.8rem/1.3 var(--fm);letter-spacing:.03em;color:#5E5A66}\n'
    '#s9legal span{white-space:nowrap}\n')
rep('<div id="s9legal"><span>TVA non applicable, art. 293 B du CGI.</span><span>Abonnement mensuel : engagement de 12 mois.</span></div>',
    '<div id="s9legal"><div><span>TVA non applicable, art. 293 B du CGI.</span><span>Abonnement mensuel : engagement de 12 mois.</span></div></div>')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
