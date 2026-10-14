# juicecraft : contexte pour Claude

Studio de création de sites internet (marque juicecraft, propriétaire francophone, Pas-de-Calais).
Ce dépôt privé est le dossier de référence de l'agence, partagé entre les deux PC du propriétaire.
Mis en place le 2026-10-14 ; état décrit ci-dessous à cette date.

## Façon de travailler
- Répondre en français, directement, sans flatterie. Corriger les prémisses fausses. Donner un niveau de confiance quand c'est incertain.
- Finir chaque problème concret par des actions ordonnées et la façon de vérifier.
- Ne jamais écrire la tournure « ce n'est pas X, c'est Y ».
- Ne jamais demander ni écrire de mot de passe, jeton ou code de confirmation. Accès par connecteurs révocables seulement.

## Délégation (détail dans DELEGATION.md)
- Niveau 1, autonome avec compte rendu : lectures, tests, rapports, brouillons, corrections de texte et de référencement, mise à jour du site dans le zip.
- Niveau 2, après accord explicite : prix, publication (site, thème), activation ou suppression de produits, e-mails aux clients, codes de réduction, hébergement et DNS.
- Niveau 3, jamais seul : remboursements, litiges, CGV et textes juridiques, décisions de prix ou de TVA, client mécontent.

## Décisions du propriétaire
- TVA : franchise en base. Mention « TVA non applicable, art. 293 B du CGI ». Le mot « TTC » ne doit apparaître nulle part.
- Les trois offres incluent hébergement, maintenance (mises à jour, sauvegardes quotidiennes, surveillance) et assistance.
- Contact public : evannlassalle@gmail.com. Adresse affichée : 62270 Conchy-sur-Canche, France.
- SIRET : immatriculation en cours (au 2026-10-11). Ne pas ouvrir les ventes avant le numéro.
- Clientèle : professionnels et particuliers, priorité aux professionnels (rétractation de 14 jours et médiateur obligatoires).
- Mise en place : à imposer à l'achat (méthode à arrêter, voir « En attente »).

## Grille de prix (prix nets)
| Offre | Mise en place | Mensuel (engagement 12 mois) | Annuel | Pages |
|---|---|---|---|---|
| Essentielle | 290 € | 49 € | 490 € | jusqu'à 5 |
| Premium | 590 € | 89 € | 890 € | jusqu'à 10 |
| Sur mesure | dès 1 690 € (acompte, devis) | 149 € | 1 490 € | sur mesure |

## Où sont les choses
- Site vitrine en ligne : https://juicecraft.fr, servi par Netlify depuis le dépôt GitHub `evannlassalle-prog/juicecraft-site` (branche main = production ; tout le contenu de ce dépôt est public).
- Source du site : `index.html` ici. Construction : `python3 build_deploy.py <clé Web3Forms>` produit `deploy/index.html` (la clé est publique côté navigateur, elle figure dans `deploy/index.html`). Publier = copier `deploy/index.html` dans `juicecraft-site` et pousser sur main, après accord.
- Liens Shopify des boutons « Choisir cette offre » : `shop.json`.
- DNS chez OVH : A juicecraft.fr = 75.2.60.5, CNAME www vers sparkling-bubblegum-b2d478.netlify.app. Ne pas passer à Netlify DNS (MX et SPF OVH à garder).
- Boutique : juicecraft-store.myshopify.com, abonnements Appstle. Plans : mensuel MIN_CYCLES=12, annuel sans minimum. Prix des plans fixes (type PRICE), prix de base des produits = prix mensuel (49 / 89 / 149) pour éviter un faux prix barré. Les plans appartiennent à Appstle : modifiables seulement dans Appstle.
- Thème Shopify : en ligne « juicecraft - correction page produit (brouillon) ». Brouillon prêt « juicecraft - sans prix barré Appstle (brouillon) » : règle CSS dans `snippets/price-styles.liquid` qui masque le prix barré injecté par Appstle. Publication par le propriétaire uniquement.
- Vidéos : sources dans `video/` (`video30.html` = pub 30 s, `video.html` = 15 s), rendu `node render.js`, encodage `encode30.sh`, son dans `video/audio/`. Versions web dans `livrables/`. Les masters (130 Mo) sont trop lourds pour Git : voir README.
- Marque : `logo/` (SVG, PNG, animations, planche de marque).
- Documents : `docs/` (audit du 2026-10-10, brouillon des mentions légales). Outils de contrôle en lecture seule : `outils/`.
- Contrôle hebdomadaire : routine « Contrôle hebdomadaire juicecraft », lundi 7 h 57 (Paris), lecture seule.

## En attente (au 2026-10-14)
1. Publier le site corrigé (franchise, maintenance) : prêt dans `deploy/index.html`, pas encore en ligne (juicecraft.fr affiche encore « TTC »).
2. Publier le thème brouillon « sans prix barré Appstle ».
3. SIRET, médiateur de la consommation, adresse complète, puis pages légales (mentions, CGV, rétractation, confidentialité, annulation) avec un professionnel.
4. Imposer la mise en place : réglage Appstle « prix de la première commande » s'il existe, sinon ajout automatique par le thème.
5. Engagement de 12 mois à afficher (texte Appstle « annulez à tout moment » à remplacer).
6. Réglages Shopify : TVA non collectée, mention TVA sur la confirmation de commande, case marketing non présélectionnée, bandeau cookies.
Liste complète : `docs/checklist-ouverture.md`.
