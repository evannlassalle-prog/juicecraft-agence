# Technique, conversation 2 : configuration, code, intégrations et procédures

Ce fichier décrit l'état au 2026-10-14. Le site actuel (Stripe) a été construit dans une autre conversation : seules ses traces visibles d'ici sont décrites (§2).

## 1. Dépôts GitHub (compte `evannlassalle-prog`)
| Dépôt | Visibilité | Rôle | Créé |
|---|---|---|---|
| `juicecraft-site` | privé | site de production (Netlify publie la branche `main`) | 09/10 (par l'utilisateur ; premier contenu poussé par Claude) |
| `juicecraft-agence` | privé | dossier de référence de l'agence : contexte, marque, vidéos, documents | 14/10 (par l'utilisateur ; contenu poussé par Claude) |
| `juicecraft-automatisation` | ? | générateur de sites et pipeline (cité dans le README du site) | autre conversation, non vu ici |

Une session cloud ne peut pas créer de dépôt (refus de la plateforme) : l'utilisateur crée le dépôt vide, Claude le rattache (`add_repo`, accès en écriture) puis le remplit.

Commits signés par Claude : pied de message « Co-Authored-By: Claude … » + « Claude-Session: https://claude.ai/code/session_01L4uY6HcMT5UJbU2LVbtLDe ».

## 2. Site de production (état observé le 14/10, construit dans l'autre conversation)
- `juicecraft-site` : dossier `public/` (accueil, `commande/`, `questionnaire/`, `suivi/`, `cgv/`, `mentions-legales/`, `confidentialite/`, `realisations/`, 5 pages « site-internet-<métier> », `robots.txt`, `sitemap.xml`, `llms.txt`), `netlify/functions/` (API, webhook Stripe, tâche `relances` horaire), `netlify/lib/messages.mjs` (e-mails), `outils/pages-metiers.mjs`, `outils/dev.mjs`, `tests/` (20 tests, `npm.cmd test`).
- **Prix et offres** : `public/commande/offres.js` (source unique). Au 14/10 : Essentielle création 890 €, 49 €/mois ou 490 €/an, 5 pages, 1 modification/mois ; Premium création 2 490 €, 89 € ou 890 €, 8 pages, 3 modifications/mois ; engagement 12 mois ; 2 tours de corrections ; validation automatique à J+15 ; contact `contact@juicecraft.fr` ; mention TVA « TVA non applicable, art. 293 B du CGI ».
- Variables Netlify listées par le README (valeurs jamais vues ni demandées) : `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `RESEND_API_KEY`, `EMAIL_EXPEDITEUR`, `EMAIL_REPONSE`, `EMAIL_NOTIFICATIONS`, `ADMIN_TOKEN`, `GITHUB_DISPATCH_TOKEN`, `GITHUB_DEPOT`.
- Vérifié en ligne le 14/10 : HTTP 200, aucun « TTC », mention 293 B présente, `/mentions-legales/`, `/cgv/`, `/confidentialite/` et `/commande/` en 200, aucun lien `myshopify`.
- Règle : toujours faire `git fetch` avant de modifier ; publier (push sur `main`) seulement après un accord explicite. Le 14/10, un push de Claude a été refusé faute d'être à jour : c'est ce qui a évité d'écraser 20 commits.

## 3. Hébergement, domaine et DNS
- Domaine `juicecraft.fr` acheté chez OVHcloud le 08/10, avec un hébergement gratuit `hosting-free-100m` (cluster129, identifiant FTP `juicecc`, dossier `www`), conservé en secours.
- **Netlify** : site `sparkling-bubblegum-b2d478` (`sparkling-bubblegum-b2d478.netlify.app`), relié au dépôt `juicecraft-site`, branche `main`. Le domaine principal `juicecraft.fr` et `www` y sont attachés, avec un certificat Let's Encrypt automatique.
- **Zone DNS restée chez OVH** (serveurs `ns200.anycast.me` / `dns200.anycast.me`, DNSSEC correct) :
  - `juicecraft.fr` A `75.2.60.5` (Netlify), AAAA supprimé ;
  - `www` CNAME `sparkling-bubblegum-b2d478.netlify.app.` (A et TXT `3|welcome` supprimés pour lever l'erreur « CNAME and other data ») ;
  - **à ne pas toucher** : MX `mx1/mx2/mx3.mail.ovh.net`, SPF `v=spf1 include:mx.ovh.com -all`, TXT `1|www.juicecraft.fr` ;
  - ne jamais passer à « Netlify DNS » (perte des MX et du SPF).
- **Retour arrière d'urgence** : A `juicecraft.fr` et A `www` = `51.91.236.255` (AAAA `2001:41d0:301::29`), puis supprimer le CNAME `www`.
- DMARC absent (constat d'audit).
- Échéance NIS2 : valider l'e-mail du titulaire avant le 22/11/2026.
- Netlify injecte un commentaire et un script `/.netlify/scripts/hud`, ainsi qu'un badge « Powered by Netlify » (constat d'audit).
- `_headers` du premier site : `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: SAMEORIGIN`, `Permissions-Policy: camera=(), microphone=(), geolocation=()` ; HSTS fourni par Netlify.

## 4. Premier site vitrine (archivé : `juicecraft-agence/archives/site-vitrine-2026-10-10/`)
- Page unique HTML/CSS/JS sans construction préalable ; WebGL pour le jus du hero ; IntersectionObserver pour les apparitions au défilement (la timeline de défilement a été abandonnée, car des sections restaient invisibles).
- `build_deploy.py` : `python3 build_deploy.py <clé Web3Forms>` produit `deploy/index.html`.
  - Il retire `<title>` et la description, injecte la clé dans `const WEB3FORMS_KEY = "";` et `const SHOP = {…}` depuis `shop.json`.
  - Il ajoute aussi le favicon `logo/favicon/favicon.svg` et les balises meta et og.
- `shop.json` : liens Shopify des 3 offres (obsolètes).
- Formulaire : envoi JSON vers Web3Forms, champ piège `botcheck`, mode démo si la clé est vide, clé `405f2edc-13c8-41a6-9d39-20234ec9be36` (publique par conception, régénérable chez Web3Forms en cas de spam).
- Boutons : `<a … data-offer="…" data-plan="essentielle|premium|mesure">Choisir cette offre</a>`, réécrits en lien Shopify si l'URL est en https.
- Version du 10/10 jamais publiée : franchise, « Maintenance incluse » (3 lignes fixes `.mt-row.inc` et « Évolutions » à bascule), plafonds 5/10 pages, configurateur « De 2 à 5 pages » / « De 6 à 10 pages ».

## 5. Boutique Shopify (abandonnée le 14/10)
- Boutique `juicecraft-store.myshopify.com`, plan Basic, EUR, fuseau Europe/Paris, `taxesIncluded: true`.
- Produits, tous **archivés** le 14/10 (titres au 14/10) :
  - Product/16127471354190 « ESSENTIELLE — Abonnement maintenance », variante 61108150141262 ;
  - Product/16127495995726 « PREMIUM — Abonnement maintenance », variante 61108252180814 ;
  - Product/16127510774094 « SUR MESURE — Abonnement maintenance », variante 61108309360974 ;
  - Product/16132776755534, 16132777017678 et 16132777115982 : mises en place (290 / 590 / 1 690 €), variantes 61143346938190, 61143347233102 et 61143347331406.
- Plans Appstle (propriété de l'application Appstle, non modifiables par l'API du connecteur) : ajustement de type PRICE fixe ; mensuel 49/89/149 avec `MIN_CYCLES=12`, annuel 490/890/1 490 sans minimum. Leçon : la valeur saisie dans Appstle (« politique d'annulation ») s'ajoute à la commande initiale, donc saisir 11 pour obtenir 12.
- Thèmes :
  - 206367555918 « juicecraft - correction page produit (brouillon) » (en ligne) ;
  - 206194049358 « juicecraft » (ancien) ;
  - 206430765390 « juicecraft - sans prix barré Appstle (brouillon) » (jamais publié), avec règle CSS dans `snippets/price-styles.liquid` : `.appstle_subscription_final_price ~ .price[data-appstle-price-modified='true'] { display: none !important; }`.
- Écritures de thème : seulement sur un thème non publié (`themeDuplicate` puis `themeFilesUpsert`) ; la publication est réservée au propriétaire.
- Commande : #1001, test, 49 €, payée, 0 € de taxe. Un seul client.
- Données exposées relevées : la politique de confidentialité et les réglages de la boutique contenaient le Gmail personnel et l'adresse postale complète.
- Fermeture : à faire par le propriétaire, dans l'ordre : désinstaller Appstle, désactiver les paiements, puis Paramètres → Forfait → Désactiver la boutique.

## 6. Vidéos publicitaires
- Sources : `juicecraft-agence/video/`.
  - `video.html` (15 s) et `video30.html` (30 s) : chronologie déterministe `seek(t)` dans le HTML.
  - Sauvegardes : `video30.bak_prix.html`, `video30.bak_ttc.html`.
- Rendu : `node render.js stills W H dossier t1,t2…` ou `node render.js seq W H dossier 60 2 [t0] [t1]`.
  - Playwright + Chromium SwiftShader, 60 i/s × 2 sous-images = 120 index/s.
  - Variables d'environnement `VIDEO_HTML`, `AD_URL=juicecraft.fr`, `RESUME=1` (ignore les images plus récentes que le HTML).
- Encodage : `./encode30.sh <dossier> 60 2 audio/soundtrack30.wav out/<nom>`.
  - `tmix` sur 2 sous-images, lanczos, bt709.
  - Master en CRF 15 (preset slow), version web en CRF 20 avec maxrate 14M.
- Scripts : `redo30_franchise.sh` (re-rendu de 22,0 à 25,5 s, 3 segments par format), `redo30.sh`, `final30.sh`, `add_url.sh` (changer l'adresse affichée), `patch2.py` et `patch30.py`.
- Son : `audio/make_audio.py` et `make_audio30.py` (synthèse numpy/scipy, 120 BPM, −14 LUFS), `cues.json` et `cues30.json`, `stems/`.
- Scènes de la 30 s : 0–10 s identique à la 15 s ; 10–16 réalisations fictives ; 16–22 méthode ; 22–25,5 offres (S9) ; 25–30 site réel et carte finale.
- Livrables (`livrables/`) : `juicecraft_pub_30s_{16x9,9x16}.mp4` (≈14 Mo), `juicecraft_pub_{16x9,9x16}.mp4` (15 s, ≈8 Mo).
  - Masters 30 s dans `livrables/masters-morceaux/` : 3 morceaux par fichier, `SHA256.txt`, recollage avec `copy /b` sous Windows ou `cat` ailleurs.
  - SHA-256 : 16:9 `09342cc9…74b2`, 9:16 `e6ce0f59…ec33`.
- **Contenu actuel de S9** (périmé) : 49 / 89 / 149 €/mois, « + 290 € » et « + 590 € de mise en place », « + mise en place dès 1 690 € », pastille « Prix clairs, sans TVA à ajouter. », ligne légale TVA et engagement.

## 7. Marque (`juicecraft-agence/logo/`)
- `svg/` : 32 fichiers.
  - principal (couleur, fond sombre, noir, blanc, sur fond encre) ;
  - secondaire (empilé, signature, mot seul, badge) ;
  - icône (couleur, noir, blanc, 3 pastilles, 2 favicons simplifiés) ;
  - 3 offres × (emblème, logo horizontal, logo horizontal fond sombre).
- `png/`, `favicon/` (ico, svg, PNG 16 à 512, apple-touch-icon, icon-192 et 512), `animation/` (MP4, GIF, WebM alpha, ProRes 4444 de 32 à 36 Mo, SVG animés).
- Planche de marque PNG et PDF, `LISEZ-MOI.txt`.
- `_src/` : `build_logo.py`, `build_anim.py`, `build_offres.py` (fontTools + uharfbuzz : texte vectorisé, Mona Sans en instances statiques), `export_png.js` (Playwright), `make_videos.sh`.

## 8. Contrôle et outils (`juicecraft-agence/outils/`)
- Scripts Playwright en lecture seule (vérification prix et barre d'ajout rapide, choix annuel, recommandations, HTML de la barre, comparaison thème en ligne et brouillon, contrôle local du site). Ils visent l'ancienne boutique Shopify et l'ancien site, donc ils sont devenus inutiles sauf `sitecheck.js` à adapter.
- Audit du 10/10 : `docs/rapport-audit-juicecraft-2026-10-10.md`, `docs/audit-2026-10-10-resultats.json` (115 constats, champs : zone, id, titre, gravité, niveau, statut, preuve, recommandation…).
- Routine hebdomadaire `trig_01SFGQNhiU8b94xsz6bP6xzv` : prompt dans `sources/routine-controle-hebdomadaire.txt`, à mettre à jour ou supprimer.

## 9. Limites de l'environnement rencontrées (utile pour reprendre)
- Conteneur cloud éphémère : tout ce qui n'est pas poussé sur GitHub ou envoyé peut disparaître.
- 4 CPU, donc au plus 2 agents de workflow en parallèle.
- Les redémarrages tuent les tâches de fond (relancer avec `setsid nohup` et la logique `RESUME`).
- Envoi de fichiers à l'utilisateur limité à 30 Mo ; GitHub refuse les fichiers de plus de 100 Mo.
- Proxy HTTPS de la session : le certificat est réémis (« Anthropic »), le vrai certificat est invisible. Pas de FTP, pas de `dig` (utiliser `https://dns.google/resolve`).
- Web3Forms bloque l'IP de la session.
- Le contrôle de permissions automatique a refusé :
  - un ajout au panier sur la boutique réelle ;
  - une publication en production jugée insuffisamment demandée ;
  - une recherche web ;
  - deux simples lectures de fichiers (refus manifestement erronés).
- Le connecteur Shopify est refusé aux tâches planifiées par l'organisation.
- Le CLI `gh` n'est pas authentifié.
