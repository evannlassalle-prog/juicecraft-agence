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
- Clientèle : professionnels et particuliers, priorité aux professionnels (rétractation de 14 jours et médiateur obligatoires).
- SIRET : en cours d'attribution (au 2026-10-14). Ne pas ouvrir les ventes avant le numéro.

## Source de vérité (depuis le 2026-10-12)
Le site, la commande et les prix vivent dans le dépôt `evannlassalle-prog/juicecraft-site` (dossier `public/`, fonctions Netlify, tests ; voir son README). Les prix, pages incluses et délais sont dans `public/commande/offres.js` : toujours les lire là, jamais les recopier ici.
- Commande et paiement : Stripe sur juicecraft.fr/commande (Essentielle et Premium). Sur mesure : sur devis, par le formulaire.
- Au 2026-10-14 : Essentielle création 890 €, maintenance 49 €/mois ou 490 €/an, 5 pages ; Premium création 2 490 €, 89 €/mois ou 890 €/an, 8 pages. Engagement 12 mois.
- Contact affiché sur le site : contact@juicecraft.fr.
- Pages légales en ligne (brouillon) : /mentions-legales, /cgv, /confidentialite.
- Générateur de sites et pipeline : dépôt `juicecraft-automatisation`.
- Publication : pousser sur main de `juicecraft-site` = production Netlify, seulement après accord. Toujours partir de la dernière version de main (fetch avant toute modification).

## Ce que contient ce dossier
- `DELEGATION.md`, `docs/` (audit du 2026-10-10, brouillon des mentions légales, liste avant ouverture), `outils/` (contrôles en lecture seule de la boutique Shopify).
- `logo/` : marque (SVG, PNG, animations, planche).
- `video/` : sources et scripts des pubs (`video30.html` = 30 s, `video.html` = 15 s), bande-son ; versions web dans `livrables/`, masters 30 s découpés dans `livrables/masters-morceaux/`. Les vidéos affichent l'ancienne grille (mise en place 290 / 590 / dès 1 690 €) : à refaire si les prix de création ont changé.
- `archives/site-vitrine-2026-10-10/` : ancienne version mono-page du site et liens Shopify, remplacée par `juicecraft-site`. Ne plus l'utiliser.

## Ancienne boutique Shopify (abandonnée le 2026-10-14)
juicecraft-store.myshopify.com : les 6 produits sont archivés (plus rien à vendre, pages produits en 404). Une seule commande, de test (#1001). Fermeture définitive de la boutique et désinstallation d'Appstle : par le propriétaire dans l'administration Shopify. Ne plus rien y modifier.

## En attente (au 2026-10-14)
1. Fermer la boutique Shopify (désinstaller Appstle, puis désactiver la boutique) : action du propriétaire.
2. Vidéos : vérifier si les prix affichés correspondent encore à `offres.js`.
3. Contrôle du lundi : mettre à jour sa grille (il contrôle encore Shopify et l'ancien site).
4. SIRET, médiateur de la consommation, relecture des pages légales par un professionnel.
Liste générale : `docs/checklist-ouverture.md` (rédigée avant le passage à Stripe : à revoir).
