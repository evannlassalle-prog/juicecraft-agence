# Délégation juicecraft (validée par le propriétaire le 2026-10-09)

## Niveau 1 : autonome, avec compte rendu
Lectures, tests (parcours d'achat, prix, plans d'abonnement), rapports hebdomadaires, brouillons,
corrections de texte et de référencement, mise à jour du site dans le zip (livrables/juicecraft-site.zip).

## Niveau 2 : seulement après accord explicite
Changements de prix, publication, activation ou suppression de produits,
envoi d'e-mails à des clients, codes de réduction, changement d'hébergement.

## Niveau 3 : jamais seul
Remboursements, litiges, conditions générales, décisions de prix ou de TVA,
tout ce qui touche un client mécontent.

## Périmètre confié
Site (zip), boutique Shopify, e-mails, vidéos, dans le cadre des 3 niveaux ci-dessus.
Lecture retenue du message du 2026-10-09 : ces quatre domaines sont le périmètre délégué.
Dans tous les cas, publier en ligne, envoyer un e-mail à un client et changer un prix restent soumis à accord (niveau 2).

## Décisions du propriétaire du 2026-10-10
- TVA : franchise en base. Mention : « TVA non applicable, art. 293 B du CGI ». Le mot « TTC » n'apparaît plus nulle part (site, Shopify, vidéos, e-mails).
- Maintenance : incluse dans les trois offres (hébergement, maintenance, assistance), comme décrit dans les fiches Shopify : Essentielle jusqu'à 5 pages, Premium jusqu'à 10 pages, Sur mesure avec 2 h de modifications par mois (au-delà sur devis).
- Identité pour les mentions légales : nom juicecraft ; statut NA ; SIRET NA ; adresse Frévent (62) France ; contact = adresse e-mail OVH (adresse exacte à fournir, jamais l'adresse personnelle) ; médiateur NA ; clientèle plutôt professionnelle, particuliers acceptés.
  Points bloquants relevés (niveau 3, à traiter avec un professionnel) : statut et SIRET « NA » sont incompatibles avec la franchise en base (art. 293 B) et avec la vente professionnelle ; adresse complète requise ; médiateur de la consommation obligatoire si des particuliers achètent.
- Prix de base Shopify = prix mensuel affiché (49 / 89 / 149 €), jamais le prix annuel : sinon Appstle affiche un faux prix barré. Les prix des plans Appstle sont fixes (type PRICE) et ne dépendent pas du prix de base.
- Thème : une règle CSS (snippets/price-styles.liquid) masque le prix barré qu'Appstle injecte à côté du prix d'abonnement. Thème brouillon 206430765390, à publier par le propriétaire. Si une vraie promotion avec prix barré est un jour voulue, retirer cette règle.

## Décisions du propriétaire du 2026-10-11
- Contact public : evannlassalle@gmail.com (choix du propriétaire, remplace « e-mail OVH »).
- Adresse à afficher : 62270 Conchy-sur-Canche, France (rue non fournie ; la rue figure déjà dans la politique de confidentialité Shopify).
- SIRET : immatriculation en cours.
- Clientèle : professionnels et particuliers, priorité aux professionnels. Conséquence : rétractation de 14 jours et médiateur de la consommation obligatoires.
- Mise en place : à imposer à l'achat (premier paiement = mise en place + première échéance). Méthode à arrêter : les plans d'abonnement appartiennent à Appstle (non modifiables par l'API du connecteur).
- Publication du site : accord donné par « Publié » ; le push sur main a été refusé par le contrôle de permissions de la session, confirmation explicite demandée.

## Hébergement (migré le 2026-10-09)
Site servi par Netlify (projet sparkling-bubblegum-b2d478), relié au dépôt GitHub privé evannlassalle-prog/juicecraft-site (branche main, déploiement automatique).
DNS resté chez OVH (ne pas passer à Netlify DNS : MX et SPF OVH) : A juicecraft.fr = 75.2.60.5, CNAME www vers sparkling-bubblegum-b2d478.netlify.app.
Ancien hébergement OVH conservé comme secours (A 51.91.236.255). Publier = pousser sur main, seulement après accord (niveau 2).

## Règles de sécurité
Aucun mot de passe ni code de confirmation dans la conversation. Accès par connecteurs (révocables) uniquement.

## Grille de référence (prix nets, TVA non applicable), à comparer au site et à Shopify
| Offre | Mise en place | Mensuel (12 cycles min.) | Annuel | Prix de base Shopify |
| Essentielle | 290 € | 49 € | 490 € | 49 € |
| Premium | 590 € | 89 € | 890 € | 89 € |
| Sur mesure | dès 1 690 € (devis) | 149 € | 1 490 € | 149 € |
Boutique : juicecraft-store.myshopify.com (produits essentielle, 🔵-premium-⭐, sur-mesure, mise-en-place-*).
Plans Appstle attendus : Mensuel MIN_CYCLES=12 ; Annuel MIN_CYCLES=NULL.
