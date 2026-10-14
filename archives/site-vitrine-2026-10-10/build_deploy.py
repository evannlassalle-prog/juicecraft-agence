"""Build deploy/index.html (standalone page for any static host) from index.html.
usage: python3 build_deploy.py [WEB3FORMS_ACCESS_KEY]"""
import re, sys, pathlib
root = pathlib.Path(__file__).parent
src = (root / "index.html").read_text(encoding="utf-8")
key = sys.argv[1].strip() if len(sys.argv) > 1 else ""
if key and not re.fullmatch(r"[0-9a-fA-F-]{20,64}", key):
    sys.exit("Clé Web3Forms invalide : elle ressemble à 1a2b3c4d-....")
body = re.sub(r"^<title>.*?</title>\s*", "", src, count=1, flags=re.S)
body = re.sub(r'^<meta name="description"[^>]*>\s*', "", body, count=1)
import json
shop = {"essentielle": "", "premium": "", "mesure": ""}
sp = root / "shop.json"
if sp.exists():
    shop.update({k: v.strip() for k, v in json.loads(sp.read_text(encoding="utf-8")).items() if k in shop})
for k, v in shop.items():
    if v and not re.fullmatch(r"https://[^\s\"<>]+", v):
        sys.exit(f"Adresse Shopify invalide pour {k} : elle doit commencer par https://")
body = body.replace('const SHOP = { "essentielle": "", "premium": "", "mesure": "" };', "const SHOP = " + json.dumps(shop, ensure_ascii=False) + ";", 1)
body = body.replace('const WEB3FORMS_KEY = "";', f'const WEB3FORMS_KEY = "{key}";', 1)
desc = "juicecraft conçoit des sites internet sur mesure, rapides et soignés pour les artisans, commerces, cabinets et entreprises."
import urllib.parse
_fav = (root / "logo" / "favicon" / "favicon.svg").read_text(encoding="utf-8").strip()
icon = "data:image/svg+xml," + urllib.parse.quote(_fav, safe="/:=,;()' ")
head = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>juicecraft · Création de sites internet sur mesure</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F2F2EF">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="juicecraft · Des sites qui ont du jus">
<meta property="og:description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="{icon}">
<style>:root{{color-scheme:light}}body{{margin:0}}</style>
</head>
<body>
"""
out = root / "deploy" / "index.html"
out.write_text(head + body + "\n</body>\n</html>\n", encoding="utf-8")
print(out, "| clé Web3Forms :", "renseignée" if key else "vide (mode démonstration)")
