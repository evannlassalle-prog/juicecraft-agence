import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
old = '#s9legal span{white-space:nowrap}\n'
assert s.count(old) == 1
s = s.replace(old, old + '.port #s9legal div{flex-direction:column;row-gap:.2rem}\n')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
