# Audit complet juicecraft — rapport du 10 octobre 2026

Périmètre : site https://juicecraft.fr, boutique Shopify (juicecraft-store.myshopify.com), abonnements Appstle, DNS et e-mail, dépôt GitHub, vidéos livrées. Audit en lecture seule : rien n'a été modifié, aucun message envoyé, aucune commande passée, aucune saisie sur la page de paiement.

## 1. Verdict

Le site et la boutique fonctionnent. En revanche, ils ne sont pas prêts pour une vente annoncée officiellement. Quatre points bloquent : aucune base juridique publiée (CGV, mentions légales, rétractation, résiliation), une TVA qui n'apparaît nulle part alors que tout est affiché « TTC », un engagement de 12 mois invisible côté boutique et contredit par le texte « annulez à tout moment », et des prix trompeurs dans la boutique (faux prix barrés, prix de base incohérents).

Chiffres : 12 agents (6 auditeurs, 6 contradicteurs indépendants), 484 appels d'outils, environ 1,5 million de jetons, 65 minutes. Résultat brut : 115 constats (2 critiques, 27 élevés, 42 moyens, 44 faibles). Beaucoup sont des doublons vus depuis plusieurs zones : regroupés, ils forment 13 sujets (section 3). 99 constats ont été confirmés par un second agent, 16 ont été ajoutés par les contradicteurs (non contre-vérifiés), aucun n'a été réfuté. Les contradicteurs ont corrigé la gravité de 13 constats et le niveau de 4. 4 contrôles annoncés « OK » par un auditeur se sont révélés faux. 119 contrôles ont réussi. 59 points n'ont pas pu être vérifiés (annexe C).

Niveaux : 1 = je corrige seul avec compte rendu ; 2 = exige votre accord explicite (publication, prix, produits, réglages d'applications, DNS) ; 3 = ne se décide jamais seul (juridique, TVA, remboursements, litiges).

## 2. Ce qui est bon (vérifié)

- Prix : le site, Shopify, les plans Appstle et la grille de référence concordent. Annuel = 10 mensualités. MIN_CYCLES=12 sur les trois plans mensuels, vide sur les annuels. La page en ligne est identique au dépôt et au dossier de déploiement (hors script Netlify).
- Parcours d'achat : 12 scénarios (offre x périodicité x appareil) donnent les bons prix et les bons totaux (339 / 780, 679 / 1 480, 1 839 / 3 180 €). Un abonnement sans plan est refusé (erreur 422). Aucune règle de quantité parasite. La page de paiement est en français et sans champ de livraison.
- DNS et e-mail : A, CNAME www, MX, SPF et DNSSEC corrects, aucun reste vers l'ancien serveur OVH pour l'apex et www. Redirections http vers https et www vers domaine nu. HSTS et quatre en-têtes de sécurité actifs. Aucun cookie sur le site.
- Performance et stabilité : environ 308 Ko pour 14 requêtes, chargement complet en 1,1 à 1,5 s, aucune erreur JavaScript. La page ne bouge plus au repos (30 s mesurées) et le titre garde 3 lignes pour les 7 mots rotatifs. CLS 0,044 (ordinateur) et 0,012 (mobile). Avec « réduire les animations », tout s'arrête.
- Accessibilité de base : navigation complète au clavier, focus visible, FAQ et formulaire utilisables, validation du formulaire sans envoi. axe-core ne remonte que des contrastes et un ordre de titres.
- Dépôt : aucun secret ni donnée personnelle dans le dépôt, le HTML publié et les fichiers de travail.
- Rédaction : aucune faute d'orthographe ni de grammaire trouvée dans le texte du site.

## 3. Les 13 sujets, regroupés et classés

Légende « Vérifié par moi » : j'ai refait le contrôle moi-même après l'audit.

### S1. Aucune base juridique publiée — critique, niveau 3
Constat : sur le site, « Mentions légales », « Confidentialité » et « CGV » sont du texte non cliquable ; /mentions-legales, /cgv et /confidentialite répondent 404 ; la FAQ renvoie aux CGV pour le nombre de tours de modifications. Aucun SIRET, statut, adresse, e-mail, téléphone, hébergeur ni médiateur n'apparaît. Côté boutique, seule /policies/privacy-policy existe (modèle Shopify générique, téléphone vide, sans Web3Forms ni Netlify ni Appstle) ; conditions de vente, remboursement et rétractation, mentions et coordonnées répondent 404. Le formulaire de contact n'a ni information RGPD ni lien de confidentialité. Rétractation, médiateur de la consommation, résiliation en ligne et distinction professionnels / particuliers ne figurent nulle part.
Vérifié par moi : oui (404, texte du pied de page).
Action : vous, avec un professionnel du droit ou votre expert-comptable. Je prépare la liste des informations à réunir et l'emplacement des liens (pied de page, fiches, panier, paiement). Je ne rédige pas de texte juridique seul.
Constats sources : PRIX-11, LEGAL-01, LEGAL-02, LEGAL-03, LEGAL-06, LEGAL-07, LEGAL-08, LEGAL-09, LEGAL-17, ACHAT-02, ACHAT-15, ACHAT-M1, ACCES-12, ACCES-M2, SEO-10, SEO-25, INFRA-M1, INFRA-M2.

### S2. TVA et mention « TTC » — élevé, niveau 3
Constat : aucune ligne de TVA au panier ni au paiement (« Total 339,00 € » sans « dont TVA »). La commande test #1001 a 0 de taxe et aucune ligne de taxe. La boutique est réglée « taxes incluses ». Le site, les descriptions et les vidéos affichent « TTC ». Votre régime réel est inconnu.
Si vous êtes en franchise en base : « TTC » est inexact, la mention à porter est « TVA non applicable, art. 293 B du CGI ». Si la TVA à 20 % s'applique : la collecte n'est pas configurée dans Shopify (Paramètres, Taxes et droits).
Action : vous confirmez votre régime (comptable). Ensuite j'harmonise tous les textes. La grille de prix ne change pas ; votre marge nette change (environ 17 % de moins par vente si la TVA s'applique).
Constats sources : ACHAT-05, LEGAL-16, ACHAT-11 et le faux « OK » sur la TVA.

### S3. Engagement de 12 mois invisible et contredit — élevé, niveaux 2 et 3
Constat : le bloc d'abonnement d'Appstle affiche « Modifiez ou annulez votre abonnement à tout moment ». Ni les fiches, ni le panier, ni la page de paiement ne mentionnent l'engagement de 12 mois (seul le code technique MIN_CYCLES=12 le porte). La « politique de résiliation » ouverte depuis le paiement est le texte Shopify par défaut, en anglais, qui dit aussi « à tout moment ». Le paiement affiche « 49,00 € par période de mois » et « 490,00 € par période de an ». Un client peut donc croire qu'il peut partir à tout moment alors que l'engagement est de 12 mois : risque de contestation.
Action : (a) texte du bloc d'abonnement dans Appstle (niveau 2) ; (b) ajout de l'engagement, de « /mois » et de « TTC » en tête des descriptions (texte, que je peux faire après votre accord de principe) ; (c) politique d'abonnement en français dans Shopify (niveau 3, avec S1) ; (d) noms des plans plus explicites (« mensuel, engagement 12 mois »).
Constats sources : ACHAT-01, ACHAT-03, ACHAT-09, ACHAT-17, LEGAL-04, LEGAL-05, PRIX-02, PRIX-M1, PRIX-M3.

### S4. Prix trompeurs dans la boutique — élevé, niveau 2
Constat : (a) sous « You may also like », chaque carte affiche le prix de l'abonnement courant à la place de son vrai prix et barre le vrai prix : « Mise en place — ESSENTIELLE 49 € barré 290 € », « PREMIUM 49 € barré 89 € ». (b) La barre d'ajout rapide affiche « 49 € barré 490 € » (fausse promotion de 90 %) et « 89 € barré 89 € ». (c) Les prix de base sont incohérents : Essentielle 490 €, Premium 89 €, Sur mesure 149 € (catalogue, données structurées et og:price). J'avais fixé 890 et 1 490 € le 9 octobre : ces deux valeurs ont été modifiées depuis, sans que je sache par qui.
Vérifié par moi : oui pour les prix de base (lecture publique des produits). Le reste a été relu par un second agent.
Action recommandée : base = prix mensuel pour les trois offres (49, 89, 149 €), masquer le prix barré dans le réglage d'affichage d'Appstle, retirer « You may also like » des fiches. À contrôler ensuite en navigation privée. Prix de base : décision de prix, donc votre accord.
Constats sources : PRIX-01, PRIX-03, PRIX-M2, SEO-18, SEO-19, SEO-M2, ACHAT-08, LEGAL-M1.

### S5. « Mise en place obligatoire » non imposée — élevé, niveau 2
Constat : un abonnement s'achète seul (panier de 49 € constaté), et la mise en place s'achète seule (290 € sans abonnement). Les trois produits de mise en place sont visibles et achetables depuis le catalogue. Pour Sur mesure, le site dit « prix et contenu confirmés avant tout paiement », alors que l'acompte de 1 690 € et la première mensualité se paient directement (panier de 1 839 € constaté).
Options : (1) imposer l'association (règle de panier ou lot, à étudier avec Appstle) ; (2) laisser l'achat séparé et surveiller les commandes sans mise en place ; (3) retirer les produits du catalogue public. Pour Sur mesure, reformuler le texte ou réserver l'achat aux clients ayant accepté un devis.
Constats sources : PRIX-09, PRIX-10, ACHAT-06, ACHAT-M2, LEGAL-15, LEGAL-M2.

### S6. Consentement, cookies et polices — moyen, niveau 2 (avis juridique : niveau 3)
Constat : la case « Envoyez-moi des nouvelles et des offres par e-mail » est pré-cochée au paiement sur tous les paniers testés. La boutique dépose _shopify_analytics et _shopify_marketing dès la première visite, sans bandeau constaté (test fait depuis un réseau non français : à reconfirmer). Le site charge ses polices depuis Google Fonts : l'adresse IP de chaque visiteur part vers Google avant tout consentement.
Vérifié par moi : oui pour Google Fonts (balises vers fonts.googleapis.com et fonts.gstatic.com).
Action : décocher la case par défaut (Shopify, Paramètres, Paiement) ; contrôler le bandeau de consentement (Paramètres, Confidentialité des clients) depuis une connexion française ; héberger les polices sur le site (je prépare le correctif, publication avec votre accord).
Constats sources : ACHAT-04, LEGAL-10, LEGAL-11, LEGAL-12, INFRA-02, ACCES-M3.

### S7. Badge « Powered by Netlify » sur votre site — moyen, niveau 2
Constat : Netlify injecte un script (/.netlify/scripts/hud) et un badge fixe en bas à droite de chaque page, qui recouvre des boutons. Un clic ouvre une carte « Build your own site with Netlify » (constructeur IA). Pour un studio dont le métier est de créer des sites, c'est gênant. Le script n'émet ni requête ni cookie.
Vérifié par moi : oui (capture de la page en ligne : badge visible en bas à droite).
Action : réglage dans Netlify (Project configuration, General, option du badge : nom exact à vérifier dans l'interface ; je ne sais pas si l'offre gratuite permet de le retirer).
Constats sources : SEO-M1, ACCES-M1, ACCES-02, INFRA-03, LEGAL-M3.

### S8. Vidéos : une erreur de ma part et d'anciens fichiers — élevé, niveaux 1 et 2
Constat : dans les deux vidéos de 30 s livrées le 9 octobre, « /mois » n'apparaît pas à l'image : on lit « 49 € », « 89 € », « 149 € » suivis de « TTC · + 290 € de mise en place ». Je vous avais écrit « 49, 89 et 149 € /mois TTC » : c'était faux pour les vidéos, et je ne l'avais pas vu en contrôlant mes images fixes. Cause probable (non testée) : le texte « /mois » hérite d'une couleur transparente. Les anciens masters du 8 octobre (« Sur devis », « Devis détaillé avant tout paiement ») subsistent dans livrables/masters/ sous des noms proches. L'archive livrables/juicecraft-site.zip ne contient pas _headers (elle est obsolète depuis le passage à Netlify).
Action : je corrige le rendu et je ré-encode les deux vidéos, après votre réponse sur la TVA (le mot « TTC » peut changer). J'archive les anciens masters (après accord).
Constats sources : PRIX-04, PRIX-05, INFRA-11.

### S9. Promesses et textes qui se contredisent — moyen, niveau 2 (décision du propriétaire)
Constat : (a) la maintenance est incluse selon l'introduction des offres et la boutique, optionnelle selon la section « Maintenance possible » et la FAQ. (b) La boutique promet « Jusqu'à 5 pages » et « Jusqu'à 10 pages », l'hébergement, l'assistance prioritaire, les intégrations ; le site non. (c) Le configurateur recommande Essentielle pour « 2 à 6 pages » alors qu'elle s'arrête à 5, et « 7 pages ou plus » mène à Premium qui s'arrête à 10. (d) La FAQ promet un « nombre de tours de modifications précisé dans l'offre » : il ne l'est nulle part. (e) « Réalisations » désigne des concepts fictifs. (f) « Sauvegardes quotidiennes », « Surveillance », « 2 h de modifications par mois » : leur réalité est à confirmer.
Action : vous confirmez ce qui est réellement fourni ; ensuite j'aligne site et boutique.
Constats sources : PRIX-06, PRIX-07, PRIX-08, PRIX-12, SEO-12, SEO-13, SEO-14, LEGAL-13, LEGAL-14, LEGAL-18.

### S10. Référencement technique du site — moyen à faible, niveau 2 (préparable en brouillon)
Constat : ni robots.txt ni sitemap.xml (404) ; pas de balise canonical (Netlify ajoute un en-tête Link canonical pour le doublon netlify.app) ; pas d'image de partage (og:image), d'og:url ni de balises Twitter ; pas de données structurées JSON-LD ; pas de favicon.ico, apple-touch-icon ni manifest ; page 404 de Netlify en anglais ; liens vers la boutique posés seulement par JavaScript ; titres h1 et h4 à corriger ; aucune espace insécable avant ? ! : ; ; redirection www en deux sauts ; README.md servi publiquement.
Vérifié par moi : oui pour robots.txt, sitemap.xml, og:image, canonical, JSON-LD (absents) et README.md (HTTP 200).
Action : je prépare le lot dans une branche du dépôt avec aperçu ; publication avec votre accord.
Constats sources : SEO-01 à SEO-09, SEO-11, SEO-15, SEO-16, SEO-17, SEO-06, INFRA-06, INFRA-07, INFRA-M3.

### S11. Accessibilité — moyen à faible, niveau 2 (préparable en brouillon)
Constat : animations automatiques sans bouton de pause (mot rotatif, démo du héros, marquee, bulles) ; légende de la démo illisible sur la bulle colorée ; contrastes insuffisants (titres d'étapes à 2,34:1, étiquettes « Livrable » à 3,0:1, texte indicatif des champs à 4,11:1) ; menu mobile sans piège de focus ; erreurs du formulaire non liées aux champs ; le configurateur perd le focus à chaque réponse ; la section Services change de hauteur au changement d'onglet (mobile, tablette, 1 024 px) ; LCP et tâches longues dégradés par l'animation du héros (mesure sans GPU, indicative).
Action : je prépare les corrections dans la même branche que S10 ; publication avec votre accord.
Constats sources : ACCES-01, ACCES-03 à ACCES-11, ACCES-13.

### S12. Boutique : langue, marque et petits défauts — moyen à faible, niveau 1 et 2
Constat : textes restés en anglais (« You may also like », « Join our email list », « Disclosures », « Delivery every », page 404) ; pas de meta description sur l'accueil et le catalogue ; données structurées avec la marque « Ma boutique » et une catégorie « Informatique et technologie » par défaut ; vendeur « Ma boutique » sur les offres et « juicecraft » sur les mises en place ; images sans texte alternatif ; montants au format « €1.690,00 » et un jeton « {{amount_with_comma_separator}} » visible dans le filtre du catalogue ; accueil de la boutique avec une grande zone vide ; adresse du produit Premium contenant des émojis ; sélecteur de quantité qui permet d'acheter plusieurs abonnements ; sur connexion lente, le bouton d'achat est actif jusqu'à 25 s avant l'apparition du bloc d'abonnement et un clic affiche une page d'erreur.
Action : textes, vendeur, descriptions et alt : je peux les corriger (niveau 1) ; thème et réglages de monnaie : accord requis (niveau 2).
Constats sources : ACHAT-07, ACHAT-10, ACHAT-12 à ACHAT-14, ACHAT-16, PRIX-13 à PRIX-15, SEO-17, SEO-20 à SEO-24.

### S13. E-mail, DNS et sécurité — moyen à faible, niveau 2
Constat : aucun enregistrement DMARC (le domaine peut être usurpé par e-mail) ; MTA-STS et TLS-RPT absents ; pas de Content-Security-Policy ; la clé Web3Forms est publique sans restriction de domaine et l'anti-spam est côté navigateur seulement ; en cas d'échec d'envoi, le formulaire n'offre aucune autre adresse de contact ; quelques enregistrements DNS résiduels de l'ancien hébergement.
Action : DMARC en mode observation (p=none) à ajouter chez OVH avec une adresse de rapports de votre choix, après avoir vérifié les expéditeurs légitimes (Shopify, Appstle, Web3Forms) ; message d'échec du formulaire avec une adresse de contact dédiée.
Constats sources : INFRA-01, INFRA-04, INFRA-05, INFRA-08, INFRA-09, INFRA-10.

## 4. Décisions attendues de votre part

1. TVA : êtes-vous assujetti à la TVA (20 %) ou en franchise en base (art. 293 B) ? Cette réponse commande S2 et la rédaction « TTC » partout.
2. Identité pour les mentions légales : nom ou dénomination, statut, SIRET, adresse (ou domiciliation), e-mail et téléphone de contact, directeur de publication, médiateur de la consommation, clientèle visée (professionnels seulement ou aussi particuliers).
3. Promesses réelles : maintenance incluse ou non ; sauvegardes quotidiennes et surveillance réellement assurées ; plafonds de 5 et 10 pages ; 2 h de modifications par mois ; nombre de tours de modifications ; délai de réponse du support.
4. Prix de base Shopify : base = prix mensuel (49, 89, 149 €) pour les trois offres, avec masquage du prix barré. Accord ou autre choix.
5. Mise en place : imposée (règle de panier) ou achetable séparément avec surveillance ; Sur mesure : acompte direct ou sur devis.
6. Badge Netlify : accord pour le retirer si le réglage existe.
7. Lot de corrections du site (S10 + S11 + polices locales) : accord pour que je le prépare dans une branche avec aperçu, sans rien publier.

## 5. Plan d'action dans l'ordre

1. Vous répondez aux décisions 1 à 3 (elles bloquent la rédaction des textes). Pendant ce temps, je ne publie rien.
2. Boutique, avec Appstle (environ 30 minutes, niveau 2) : engagement dans le texte du bloc, masquage du prix barré, retrait de « You may also like », case marketing décochée, prix de base. Je vous guide pas à pas et je recontrôle en ligne.
3. Pages légales : vous les faites établir (S1) ; je prépare les emplacements et les liens.
4. Site : lot S10 + S11 + polices locales en branche, aperçu, vos retours, puis publication.
5. Vidéos : correction de « /mois », ré-encodage, envoi, archivage des anciens masters.
6. Netlify : badge. OVH : DMARC.
7. Surveillance : j'ajoute au contrôle du lundi les nouveaux points (pages légales en 200, badge absent, balises de partage, prix de base, absence de prix barré, case décochée).

Comment savoir que ça marche : après chaque lot, je relance les contrôles concernés et je vous donne preuve par preuve ; en fin de parcours, un nouvel audit complet doit tomber à zéro constat de niveau critique ou élevé.

## Annexe A. Les 115 constats détaillés
Tri : gravité puis niveau. « Statut » : confirmé = reproduit par un second agent ; sinon trouvé par le contradicteur et non contre-vérifié.
### PRIX-11 — CGV et mentions légales citées mais introuvables (site et boutique)
- Zone : Prix, offres et cohérence des contenus
- Gravité : critique | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Sur le site, « Mentions légales », « Confidentialité » et « CGV » sont des éléments de liste simples, sans lien. La FAQ renvoie aux CGV pour le nombre de tours de modifications. En boutique, /policies/refund-policy, /policies/terms-of-service, /policies/legal-notice et /policies/shipping-policy répondent 404 (seule /policies/privacy-policy répond 200), alors que le panier demande d'accepter la « politique de résiliation » d'un abonnement avec engagement de 12 mois.
- Attendu : CGV (engagement, résiliation, rétractation, mise en place) et mentions légales accessibles depuis le site et la boutique.
- Preuve : https://juicecraft.fr, HTML : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> ; curl -L https://juicecraft-store.myshopify.com/policies/refund-policy → 404, terms-of-service → 404, legal-notice → 404, privacy-policy → 200 ; texte du panier : « j'accepte la politique de résiliation ».
- Recommandation : Ne pas rédiger seul : le propriétaire fait établir CGV, mentions légales et politique de résiliation/rétractation (niveau 3), puis les publie et les relie dans le pied de page du site et dans les politiques Shopify. À noter dans les CGV : engagement de 12 mois, 2 mois offerts en annuel, mise en place, acompte Sur mesure, nombre de tours de modifications.
- Preuve du contradicteur : curl https://juicecraft.fr ligne 1258 : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> ; curl -o /dev/null -w %{http_code} sur https://juicecraft-store.myshopify.com/policies/refund-policy, /terms-of-service, /legal-notice, /shipping-policy, /contact-information, /subscription-policy, /cancellation-policy, /pages/cgv, /pages/mentions-legales = 404 ; /policies/privacy-policy = 200 ; pied de page boutique : bouton « Conditions générales et politiques » dont la fenêtre ne contient que « Politique de confidentialité » ; texte du panier : « j'accepte la politique de résiliation ».

### LEGAL-02 — Aucune CGV ni conditions de vente ; la boutique vend en ligne sans conditions, remboursement ni mentions publiées
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : critique | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : La FAQ du site renvoie aux CGV (« le nombre de tours inclus est précisé dans l'offre et dans les CGV ») mais elles n'existent pas. Sur Shopify, seule /policies/privacy-policy existe : terms-of-service, refund-policy, legal-notice, contact-information, shipping-policy et subscription-policy répondent 404. Le pied de page boutique affiche « Conditions générales et politiques » avec pour seul lien la politique de confidentialité, alors que cette politique invoque des « Conditions de service » inexistantes. La boutique accepte pourtant des abonnements et des paiements (checkout atteint avec 339,00 € au panier, sans rien saisir).
- Attendu : Des conditions générales de vente accessibles avant la commande (prix, durée, reconduction, résiliation, droit de rétractation et ses exceptions, médiateur, responsabilités, livrables, modifications incluses). Références : Code de la consommation, art. L221-5 (information précontractuelle des contrats à distance) https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053310511 ; art. L111-1. Obligation visant les consommateurs ; applicabilité aux clients uniquement professionnels : à faire valider.
- Preuve : GET https://juicecraft-store.myshopify.com/policies/terms-of-service = 404 ; /policies/refund-policy = 404 ; /policies/legal-notice = 404 ; /policies/contact-information = 404 ; /policies/shipping-policy = 404 ; /policies/subscription-policy = 404 ; /policies/privacy-policy = 200. graphql shop.shopPolicies = [PRIVACY_POLICY] uniquement. Texte FAQ du site : « …précisé dans l'offre et dans les CGV ». Pied de page boutique : « Conditions générales et politiques ».
- Recommandation : Le propriétaire fait rédiger ou valider les CGV (et le texte de politique de remboursement et de rétractation), puis les publie sur Shopify (Paramètres, Politiques) et sur juicecraft.fr/cgv avec lien depuis le pied de page, la fiche produit, le panier et le paiement. En attendant, retirer ou ne pas laisser croire à l'existence de « CGV » (FAQ). Aucun texte juridique n'est rédigé ici.
- Preuve du contradicteur : curl /policies/{terms-of-service,refund-policy,legal-notice,contact-information,shipping-policy,subscription-policy} et /pages/{mentions-legales,cgv} = 404 ; /policies/privacy-policy = 200. graphql_query shop.shopPolicies = [PRIVACY_POLICY] uniquement. Texte de la FAQ du site : « précisé dans l'offre et dans les CGV ». Pied de page boutique : seul lien 'Politique de confidentialité => /policies/privacy-policy'. Playwright : checkout atteint, total 339,00 €.

### ACHAT-01 — La politique de résiliation affichée au paiement est le texte Shopify anglais par défaut et contredit l'engagement de 12 mois
- Zone : Parcours d'achat et page de paiement
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Le lien « politique de résiliation » (paiement express, bouton « Annulations » en pied de page, et panier) ouvre une fenêtre intitulée « Annulations » entièrement en anglais (« Some items in our store may be offered to you as a subscription... »). Elle indique « If you want to cancel or change your subscription, you can do it at any time » et renvoie à « our returns policy ». Elle ne mentionne ni l'engagement de 12 mois du mensuel, ni le droit de rétractation, ni les modalités du renouvellement annuel.
- Attendu : Une politique de résiliation en français, cohérente avec l'offre : engagement 12 mois pour le mensuel, renouvellement et résiliation de l'annuel, délais et modalités.
- Preuve : Playwright : panier Essentielle mensuel -> /checkout -> clic sur le bouton « politique de résiliation » -> dialogue dont le texte commence par « Some items in our store may be offered to you as a subscription, a pre-order or try before you buy... You can do it at any time ... See our returns policy for more details on returns and refunds. » ; capture shots/cancel-dialog.png
- Recommandation : Faire rédiger/valider par le propriétaire (ou un juriste) une politique d'abonnement en français puis la renseigner dans Shopify (Paramètres > Politiques > Politique d'abonnement). Texte de base à valider : « Abonnement mensuel : engagement de 12 mois, facturé chaque mois ; la résiliation prend effet à l'issue de la période de 12 mois en cours. Abonnement annuel : facturé chaque année, renouvelé automatiquement, résiliable avant la date de renouvellement depuis le lien de votre e-mail de confirmation. » Ne pas publier sans accord du propriétaire (sujet juridique).
- Preuve du contradicteur : Playwright, panier Essentielle mensuel construit par l'interface, puis /checkout, clic sur « Annulations » : dialogue « Some items in our store may be offered to you as a subscription... If you want to cancel or change your subscription, you can do it at any time... See our returns policy... » (capture lue). GraphQL shop.shopPolicies ne renvoie que PRIVACY_POLICY. Pied de page du paiement : seulement « Politique de confidentialité » et « Annulations ».

### ACHAT-02 — Aucune politique de remboursement, ni conditions de vente (CGV), côté boutique : les pages renvoient 404
- Zone : Parcours d'achat et page de paiement
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Seule la politique de confidentialité existe. /policies/refund-policy et /policies/terms-of-service renvoient 404 (page 404 en anglais), alors que le texte de résiliation renvoie à « our returns policy ». Le pied de page de la boutique et du paiement ne propose que « Politique de confidentialité » (et « Annulations »). Aucun lien vers CGV, mentions légales ou rétractation sur le parcours de paiement.
- Attendu : Le parcours de paiement doit donner accès aux CGV, à la politique de remboursement/rétractation et aux mentions légales (les CGV et mentions existent sur juicecraft.fr).
- Preuve : curl https://juicecraft-store.myshopify.com/policies/refund-policy -> 404 ; /policies/terms-of-service -> 404 ; /policies/shipping-policy -> 404 ; /policies -> 404 ; GraphQL shop { shopPolicies } ne retourne que PRIVACY_POLICY ; pied de page /collections/all : seul lien « Politique de confidentialité »
- Recommandation : Créer dans Shopify (Paramètres > Politiques) la politique de remboursement et les conditions de service, en reprenant les CGV de juicecraft.fr après validation juridique, afin qu'elles apparaissent dans le pied de page du paiement. Décision à valider par le propriétaire (sujet juridique).
- Preuve du contradicteur : curl https://juicecraft-store.myshopify.com/policies/refund-policy -> 404, /policies/terms-of-service -> 404, /policies/shipping-policy -> 404, /policies/subscription-policy -> 404, /policies -> 404, /policies/privacy-policy -> 200. Liens a[href*=policies] de la page d'accueil boutique : seulement /policies/privacy-policy. GraphQL shopPolicies : un seul élément (PRIVACY_POLICY).

### ACHAT-05 — Aucune ligne de TVA/taxes affichée au panier et au paiement alors que les prix sont annoncés TTC
- Zone : Parcours d'achat et page de paiement
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : moyenne
- Constat : Le résumé de commande affiche seulement « Total EUR 339,00 € » sans « dont TVA ». Le panier indique « Droits de douane et taxes inclus » mais le sous-total récurrent précise « Ne comprend pas l'expédition, les taxes, les droits de douane ». La commande test #1001 a 0 de taxe et aucune ligne de taxe. Soit la TVA n'est pas configurée dans Shopify, soit l'activité relève d'une franchise de TVA et les libellés « TTC » sont à revoir.
- Attendu : Cohérence entre « TTC » annoncé et la TVA affichée/collectée (ou mention « TVA non applicable, art. 293 B du CGI » si franchise).
- Preuve : Checkouts ess-M, ess-A, mes-M : aucun libellé de taxe dans le résumé ; GraphQL orders(first:5) -> #1001 test=true taxesIncluded=true totalTaxSet=0.0 taxLines=[] ; shop.taxesIncluded=true ; descriptions produits : « 290 € TTC »
- Recommandation : Le propriétaire doit confirmer avec son comptable le régime de TVA. Si TVA 20 % applicable : activer la collecte de TVA France dans Shopify (Paramètres > Taxes et droits). Si franchise : retirer « TTC » des textes et ajouter « TVA non applicable, art. 293 B du CGI ».
- Preuve du contradicteur : Checkouts lus (Essentielle mensuel mobile, Sur mesure mensuel, Premium annuel) : lignes « Total 339,00 € », « 1 839,00 € », « 1 480,00 € » sans ligne de taxe ; seule ligne contenant « taxes » : « Ne comprend pas l'expédition, les taxes, les droits de douane ou toute réduction applicable ». GraphQL orders : #1001 test=true, taxesIncluded=true, totalTaxSet 0.0, taxLines []. shop.taxesIncluded=true. Panier : « Droits de douane et taxes inclus ».

### ACHAT-M1 — juicecraft.fr : « Mentions légales », « Confidentialité » et « CGV » du pied de page ne sont pas cliquables et aucun texte n'existe
- Zone : Parcours d'achat et page de paiement
- Gravité : élevé | Niveau : 3 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Dans le pied de page de juicecraft.fr, les trois éléments « Mentions légales », « Confidentialité » et « CGV » sont de simples éléments de liste sans lien ni action ; aucune page ni fenêtre ne s'ouvre. Aucun texte de CGV ou de mentions légales n'est présent sur le site, alors que la FAQ renvoie vers « les CGV » pour le nombre de modifications incluses. Côté boutique, aucune politique de remboursement ni CGV n'existe non plus (ACHAT-02). Le parcours complet, du site au paiement, ne donne donc accès à aucune CGV, aucune mention légale éditeur et aucune information sur le droit de rétractation. Cela contredit la prémisse d'ACHAT-02 (« les CGV et mentions existent sur juicecraft.fr »).
- Attendu : Pages ou fenêtres accessibles par ces liens, avec mentions légales de l'éditeur (identité, adresse, SIRET, hébergeur), CGV et informations sur la rétractation, et lien vers les CGV depuis le paiement.
- Preuve : Playwright sur https://juicecraft.fr/ : pour chaque li de .foot-legal (CGV, Mentions légales, Confidentialité) : hasA=false, cursor=none ; clic -> URL inchangée, aucun nouvel onglet, aucune boîte de dialogue ; aucun a[href] contenant legal|cgv|mention|confidential|privacy|terms. HTML ligne 1258 : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> ; le mot « CGV » n'apparaît que 2 fois (FAQ et pied de page) ; mêmes éléments dans /home/user/juicecraft-site/index.html. curl : https://juicecraft.fr/cgv, /mentions-legales, /mentions, /legal, /conditions-generales-de-vente, /confidentialite -> 404. Aucune occurrence de « TVA », « SIRET » ou « 293 » sur la page.
- Recommandation : Le propriétaire doit faire rédiger ou valider (juriste) les mentions légales, les CGV (engagement de 12 mois, résiliation, rétractation, remboursement) et la confidentialité, puis décider où les publier (pages du site et/ou politiques Shopify) et rendre les liens du pied de page actifs. Aucune publication sans son accord (sujet juridique). Zone proche d'un audit juridique distinct : à recouper avec lui.

### SEO-10 — Pied de page : Mentions légales, Confidentialité et CGV ne sont pas des liens et les pages n'existent pas
- Zone : Référencement, contenu et rédaction
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Les trois entrées sont de simples <li> de texte. Aucune page de mentions légales, de CGV ni de politique de confidentialité n'est accessible sur juicecraft.fr, alors que la FAQ renvoie aux « CGV » pour le nombre de tours de modifications et que le formulaire collecte nom et e-mail. Aucune coordonnée (e-mail, téléphone, adresse, identité de l'éditeur) n'apparaît sur le site. Risque de non-conformité (LCEN, RGPD, droit de la consommation) et perte de confiance.
- Attendu : Trois pages publiées et liées, avec l'identité de l'éditeur, l'hébergeur (Netlify), les CGV et la politique de confidentialité.
- Preuve : HTML : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> ; https://juicecraft.fr/mentions-legales, /cgv, /confidentialite -> HTTP/2 404.
- Recommandation : Le contenu juridique ne se décide pas seul : le propriétaire (ou un conseil) doit rédiger ou valider les textes. Une fois validés, publier les pages et transformer les <li> en <a href="/mentions-legales">, <a href="/confidentialite">, <a href="/cgv"> (niveau 2 pour la publication technique).
- Preuve du contradicteur : HTML : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> ; curl https://juicecraft.fr/mentions-legales, /cgv, /confidentialite -> 404 ; grep du texte visible (@, tél, siret, siren, adresse, RGPD) : aucune occurrence ; seule ligne de pied « © 2026 juicecraft. Tous droits réservés. ».

### SEO-25 — Boutique : pages légales Remboursement, Conditions d'utilisation et Mentions absentes
- Zone : Référencement, contenu et rédaction
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Seule la politique de confidentialité existe ; les politiques de remboursement et conditions de service renvoient 404. Le pied de page affiche « Conditions générales et politiques » ; pour une vente de services à distance à des consommateurs, l'absence de CGV, de politique de rétractation et de mentions du vendeur est un risque juridique et un frein à la confiance au moment du paiement.
- Attendu : Politiques publiées (remboursement, conditions de service, mentions légales/contact) accessibles depuis le pied de page et le paiement.
- Preuve : https://juicecraft-store.myshopify.com/policies/refund-policy -> HTTP/2 404 ; /policies/terms-of-service -> 404 ; /policies/legal-notice -> 404 ; /policies/privacy-policy -> 200.
- Recommandation : Décision du propriétaire (ou d'un juriste) : rédiger et publier ces politiques dans Admin > Paramètres > Politiques, puis relier au site (voir SEO-10). Ne pas utiliser de modèle générique sans validation.
- Preuve du contradicteur : curl -w '%{http_code}' https://juicecraft-store.myshopify.com/policies/refund-policy 404 ; /policies/terms-of-service 404 ; /policies/legal-notice 404 ; /policies/shipping-policy 404 ; /policies/privacy-policy 200.

### LEGAL-01 — Aucune page de mentions légales ; éditeur, statut, SIRET, TVA, hébergeur non identifiés sur le site
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Le pied de page affiche « Mentions légales », « Confidentialité » et « CGV » comme éléments de liste non cliquables (<li> sans lien). Les routes /mentions-legales, /cgv, /confidentialite, /politique-de-confidentialite, /cookies, /conditions répondent 404. Le site n'affiche ni nom ou dénomination de l'éditeur, ni statut juridique, ni SIRET/RCS, ni numéro de TVA, ni adresse, ni e-mail ou téléphone (seul le formulaire permet de contacter), ni directeur de publication, ni hébergeur (Netlify). Les seules coordonnées de l'exploitant sont dans la politique de confidentialité Shopify (adresse 9 rue de St Pol, 62270 Conchy sur Canche et e-mail evannlassalle@gmail.com), qui ne nomme pas le statut de l'entreprise ni son SIRET.
- Attendu : Une page de mentions légales accessible depuis le pied de page (lien cliquable) identifiant l'éditeur, l'hébergeur et le directeur de publication. Références officielles : loi n° 2004-575 du 21 juin 2004 (LCEN), article 1-1 (anciennement art. 6 III), https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000049568614 ; fiche economie.gouv.fr « Mentions sur votre site internet : les obligations à respecter ». La loi vise l'éditeur du site, professionnel ou non, avec un régime allégé pour l'éditeur non professionnel. Contenu exact selon le statut du propriétaire : à faire valider.
- Preuve : Pied de page : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul>. curl https://juicecraft.fr/mentions-legales = 404 ; /cgv = 404 ; /confidentialite = 404 ; /politique-de-confidentialite = 404 ; /cookies = 404 ; /conditions = 404. grep sur le HTML : aucun « SIRET », « SIREN », « RCS », « TVA », « mailto: », « tel: ».
- Recommandation : Le propriétaire fait valider (juriste, expert-comptable ou chambre consulaire) le contenu de la page, puis la publication : (1) créer /mentions-legales avec nom ou dénomination, forme et statut, SIRET, numéro de TVA ou mention de franchise en base, adresse (ou adresse de domiciliation), e-mail, directeur de la publication, hébergeur Netlify avec ses coordonnées relevées sur netlify.com ; (2) transformer les trois <li> en liens <a href> vers les pages. Brouillon à préparer sans le publier ; publication = accord explicite du propriétaire.
- Preuve du contradicteur : curl https://juicecraft.fr/{mentions-legales,cgv,confidentialite,politique-de-confidentialite,cookies,conditions,mentions,legal,privacy,cgu} = 404 (3633 octets). Playwright : footLegal = '<li>Mentions légales</li><li>Confidentialité</li><li>CGV</li>', liens légaux = [], mailto/tel = []. grep du HTML (200 132 octets) sans SIRET/SIREN/RCS/TVA/mailto:/tel:.

### LEGAL-03 — Droit de rétractation et exception pour prestation de service non mentionnés nulle part
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : moyenne
- Constat : Aucune occurrence de « rétractation », « 14 jours » ni d'exception pour service exécuté avant la fin du délai n'apparaît sur le site, les fiches produits, le panier ni le paiement. Les produits sont des services (type « Service ») dont la mise en place démarre après paiement ; aucune case de renonciation expresse n'est présentée.
- Attendu : Information précontractuelle claire sur l'existence du droit de rétractation de 14 jours ou sur les cas où il est exclu ou perdu, et, si le propriétaire démarre la prestation avant la fin du délai, recueil de l'accord préalable exprès et de la renonciation. Références : Code de la consommation art. L221-5, L221-18 et L221-28 (exception 1° : service pleinement exécuté avant la fin du délai avec accord préalable exprès et renonciation du consommateur) https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032226820/2016-09-28 ; fiche DGCCRF « E-commerce : les règles entre professionnels et consommateurs ». Visent les consommateurs ; l'art. L221-3 étend certaines protections aux petits professionnels (jusqu'à 5 salariés, objet hors du champ de l'activité principale) pour les contrats conclus hors établissement, mais son application à ces ventes en ligne est à faire valider.
- Preuve : grep -iE "rétractation|14 jours" sur https://juicecraft.fr/ (HTML complet) = 0 résultat ; textes /products/essentielle.js, premium, sur-mesure, mise-en-place-* : aucune mention ; texte du paiement (checkout_text) : aucune mention ; fenêtre « politique de résiliation » : aucune mention de rétractation.
- Recommandation : Le propriétaire fait valider avec un juriste la rédaction de la clause de rétractation (délai, formulaire type, exception L221-28 1° et mécanisme de renonciation) et décide s'il démarre la prestation avant 14 jours. Puis la faire figurer dans les CGV, sur les fiches produits et au paiement. Niveau 3 : aucune rédaction autonome.
- Preuve du contradicteur : grep -i 'rétractation|14 jours' sur home.html, site_text.txt, prod_essentielle.txt, prod_premium.txt, cart.txt, checkout.txt = 0 résultat ; descriptions .js des 6 produits sans occurrence. Légifrance L221-5 et L221-28 relus (LEGIARTI000053310511 et LEGIARTI000032226820).

### LEGAL-04 — La « politique de résiliation » affichée au paiement est un texte Shopify générique en anglais, contradictoire avec l'engagement de 12 mois
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Le lien « politique de résiliation » (panier et paiement) n'est pas une URL : c'est un bouton qui ouvre une fenêtre contenant le texte par défaut de Shopify, en anglais, qui indique « If you want to cancel or change your subscription, you can do it at any time » et renvoie à « our returns policy » (inexistante, 404). La fiche produit Essentielle (bloc Appstle) affiche aussi en français « Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. » Ces messages contredisent « L'abonnement mensuel engage sur 12 mois » du site et MIN_CYCLES=12 des plans mensuels.
- Attendu : Un texte de résiliation en français, cohérent avec le contrat réel (engagement 12 mois, reconduction, préavis, remboursement éventuel), sans promesse d'annulation à tout moment si elle n'existe pas. Les engagements contradictoires affichés au point de vente exposent à une contestation du client ; qualification juridique à faire valider.
- Preuve : Playwright : panier https://juicecraft-store.myshopify.com/cart contient <small id="shopify-buyer-consent" data-consent-type="subscription">… j'accepte la <span id="shopify-subscription-policy-button">politique de résiliation</span>…</small> ; sur /checkout, clic sur le bouton « Annulations » : fenêtre « Some items in our store may be offered to you as a subscription… If you want to cancel or change your subscription, you can do it at any time… See our returns policy… ». /policies/subscription-policy = 404. Fiche /products/essentielle (texte) : « Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. »
- Recommandation : Le propriétaire décide la règle de résiliation réelle (avec avis juridique), puis : renseigner une politique d'abonnement en français dans Shopify (Paramètres, Politiques, ou texte de résiliation) et remplacer le texte « annulez à tout moment » dans les réglages du widget Appstle (niveau 2 pour le réglage d'application, niveau 3 pour le fond juridique). Ne rien modifier sans accord.
- Preuve du contradicteur : Playwright /checkout : clic sur le bouton « Annulations », texte de la fenêtre commence par « Some items in our store may be offered to you as a subscription… If you want to cancel or change your subscription, you can do it at any time… See our returns policy… ». /policies/subscription-policy et /policies/refund-policy = 404. prod_essentielle.txt et prod_premium.txt ligne 25 : « Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. ». .js : option du plan mensuel '1MONTH1MONTHMIN_CYCLES=12…'.

### LEGAL-05 — L'engagement de 12 mois et la reconduction ne sont affichés ni sur les fiches produits ni au panier ni au paiement
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Le site mentionne l'engagement de 12 mois, mais le texte des fiches produits (essentielle, premium, sur-mesure), du panier et de la page de paiement ne contient ni « 12 mois », ni la reconduction, ni les modalités de résiliation. Le paiement indique seulement « 49,00 € par période de mois ». La reconduction à l'issue des 12 mois (mensuel) et du terme annuel n'est décrite nulle part.
- Attendu : Au moment de l'achat : durée minimale, reconduction, préavis et prix récurrent clairement présentés (information précontractuelle). Références : Code de la consommation art. L221-5 ; reconduction tacite : art. L215-1 et suivants pour les consommateurs, https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034072591/2024-01-04/ (contenu exact et application aux contrats avec professionnels : à faire valider).
- Preuve : Texte de /products/essentielle (Playwright, product_text.txt) : aucune occurrence de « 12 » ni « engagement » ; panier : « Abonnement Mensuel, Prix €49,00 » ; paiement : « Sous-total récurrent … 49,00 € par période de mois ». Plans Appstle : '1MONTH1MONTHMIN_CYCLES=12…' (libellé technique visible dans l'API, non lisible par l'acheteur).
- Recommandation : Le propriétaire valide la formulation puis, après accord (niveau 2 pour l'affichage, niveau 3 pour le fond), ajouter en tête de description des 3 offres une ligne du type « Abonnement mensuel : engagement de 12 mois (49 € TTC/mois) ; reconduction : [à faire valider] ; résiliation : [à faire valider] ». Texte exact à valider avant publication.
- Preuve du contradicteur : Descriptions .js essentielle, premium, sur-mesure : aucune occurrence de '12 mois', 'engag', 'résili', 'annul'. cart.txt : 'Abonnement Mensuel / Prix €49,00' sans durée. checkout.txt : '49,00 € par période de mois' ; aucune mention de 12 mois. Le site (site_text.txt lignes 367, 412, 423) annonce bien « 12 mois d'engagement ».

### LEGAL-09 — Formulaire de contact : aucune information RGPD au point de collecte ni lien de confidentialité
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Le formulaire collecte nom, e-mail, entreprise (facultatif), type de projet, offre envisagée et message libre, puis les envoie en JSON à https://api.web3forms.com/submit (clé publique 405f2edc-…) vers la boîte du propriétaire. La seule mention est « Vos informations servent uniquement à répondre à votre demande. » : sans identité du responsable, base légale, destinataire (Web3Forms), durée de conservation, droits ni lien vers une politique de confidentialité. Il n'existe pas de case de consentement (non obligatoirement requise pour répondre à une demande, à faire valider ; c'est l'information qui est exigée).
- Attendu : Une mention d'information à proximité du bouton d'envoi ou un lien vers la politique de confidentialité couvrant identité, finalité, base légale, destinataires, durée, droits (RGPD art. 13). La CNIL propose une mention type à adapter pour les formulaires de collecte : https://www.cnil.fr/fr/exemples-de-formulaire-de-collecte-de-donnees-caractere-personnel. Le lieu de traitement et le rôle de Web3Forms n'ont pas pu être sourcés.
- Preuve : HTML du formulaire (id="form") : champs name, email, company, type, offer, msg + case anti-spam botcheck ; script : fetch("https://api.web3forms.com/submit", { body: JSON.stringify({ access_key: WEB3FORMS_KEY, subject, from_name, name, email, entreprise, type_de_projet, offre, message }) }) ; texte : <p class="form-note">Vos informations servent uniquement à répondre à votre demande.</p>. Aucun envoi réel effectué lors de l'audit.
- Recommandation : Après validation juridique, ajouter sous le bouton une ligne d'information pointant vers la page de confidentialité du site (ex. : « Vos données sont utilisées pour répondre à votre demande, conservées [durée à valider] ; en savoir plus : lien Confidentialité »). Le propriétaire fait aussi vérifier le contrat et la localisation de traitement de Web3Forms avant de les citer. Niveau 3.
- Preuve du contradicteur : home.html ligne 1218 <form id="form">, ligne 1240 '<p class="form-note">Vos informations servent uniquement à répondre à votre demande.</p>' ; ligne 1817 WEB3FORMS_KEY = "405f2edc-13c8-41a6-9d39-20234ec9be36" ; ligne 1838 fetch("https://api.web3forms.com/submit"…). Playwright : hasPrivacyInForm = false (aucun <a> dans #form).

### ACCES-12 — Pied de page : « Mentions légales », « Confidentialité » et « CGV » sont du texte non cliquable
- Zone : Accessibilité, performance et robustesse
- Gravité : élevé | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : Dans la colonne « Informations » du pied de page, les trois entrées ne sont pas des liens (simples <li> sans <a>) et aucune page correspondante n'est référencée dans le HTML. Un visiteur ou un lecteur d'écran ne peut pas lire les mentions légales, la politique de confidentialité ni les CGV depuis le site, alors que le site collecte des demandes de contact et renvoie vers une boutique en ligne. Observation faite lors du contrôle visuel, hors du périmètre strict d'accessibilité.
- Attendu : Mentions légales et information sur les données personnelles accessibles depuis le site ; liens utilisables au clavier et au lecteur d'écran.
- Preuve : DOM du pied de page : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> ; aucun href contenant mentions, cgv ou confidentialité dans le HTML de https://juicecraft.fr/ ; essais https://juicecraft.fr/mentions-legales, /cgv, /confidentialite -> HTTP 404 (adresses devinées, à titre indicatif).
- Recommandation : Décision du propriétaire : rédiger les trois documents (contenu juridique à valider, ne pas improviser), les publier sur des pages dédiées, puis transformer les <li> en liens <a href="/mentions-legales"> etc.
- Preuve du contradicteur : HTML de https://juicecraft.fr/ : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> sans <a>. grep insensible à la casse de siret, siren, rcs, hébergeur, éditeur, rgpd, données personnelles : aucun résultat. curl : /mentions-legales, /cgv, /confidentialite, /politique-de-confidentialite, /conditions-generales-de-vente, /legal -> HTTP 404. https://juicecraft-store.myshopify.com/policies/privacy-policy -> HTTP 200 (texte français, dernière mise à jour 9 octobre 2026).

### ACCES-M2 — Boutique Shopify : pas de conditions de vente, de politique de remboursement ni de mentions légales publiées (hors périmètre strict, à rapprocher de la zone juridique)
- Zone : Accessibilité, performance et robustesse
- Gravité : élevé | Niveau : 3 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : moyenne
- Constat : Sur la boutique, seule la politique de confidentialité est publiée. Les pages de conditions de vente, de remboursement et de mentions légales renvoient HTTP 404, ce qui est le comportement de Shopify pour une politique vide. Le site vitrine ne relie à aucun de ces documents (ACCES-12), de sorte que ni le site ni la boutique ne donnent au client les conditions de vente et les informations de rétractation avant l'achat. Je n'ai pas ouvert la page de paiement pour vérifier le pied de page du checkout.
- Attendu : Conditions générales de vente, informations sur le droit de rétractation et mentions légales accessibles avant la commande ; politique de confidentialité reliée depuis le site.
- Preuve : curl -L sur https://juicecraft-store.myshopify.com/policies/terms-of-service -> 404 ; /policies/refund-policy -> 404 ; /policies/legal-notice -> 404 ; /policies/shipping-policy -> 404 ; /policies/contact-information -> 404 ; /policies/privacy-policy -> 200 (18 774 caractères de texte, « Dernière mise à jour : 9 octobre 2026 »).
- Recommandation : Décision du propriétaire, à valider juridiquement : rédiger et publier CGV, politique de remboursement/rétractation et mentions légales dans Shopify (Paramètres > Politiques), puis relier les trois entrées du pied de page du site (et la politique de confidentialité existante) vers ces pages. Ne pas improviser le contenu.

### INFRA-M1 — Aucune page légale sur le site : mentions légales, confidentialité et CGV affichées mais inexistantes, formulaire sans information RGPD
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : élevé | Niveau : 3 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Le pied de page affiche « Mentions légales », « Confidentialité » et « CGV » en simples textes, sans lien, et aucune de ces pages n'existe sur juicecraft.fr (404 partout). La FAQ renvoie pourtant à « dans les CGV ». Le formulaire collecte nom, e-mail, entreprise et description du projet et les envoie à api.web3forms.com, avec pour seule information « Vos informations servent uniquement à répondre à votre demande » (ni identité du responsable de traitement, ni destinataires, ni durée, ni droits, ni lien vers une politique de confidentialité). Côté Shopify, seule une politique de confidentialité modèle existe : aucune CGV (conditions de service), aucune politique de remboursement, aucune mention légale, alors que le site vend des abonnements en ligne via Shopify. La correction relève du juridique : texte à décider par le propriétaire, éventuellement avec un conseil.
- Attendu : Mentions légales (identité de l'éditeur, coordonnées, hébergeur), politique de confidentialité et CGV accessibles par des liens depuis le pied de page, et information sur le traitement des données à côté du formulaire.
- Preuve : /home/user/juicecraft-site/index.html l.1258 : <ul class="foot-legal"><li>Mentions légales</li><li>Confidentialité</li><li>CGV</li></ul> ; Playwright : .foot-legal li -> [{"t":"Mentions légales","a":false},{"t":"Confidentialité","a":false},{"t":"CGV","a":false}] (aucun lien) ; grep -c 'href="/' = 0 ; curl https://juicecraft.fr/mentions-legales et /cgv -> HTTP/2 404 ; l.1196 « dans les CGV » ; l.1240 <p class="form-note">Vos informations servent uniquement à répondre à votre demande.</p> ; Shopify graphql_query shop.shopPolicies -> un seul élément, type PRIVACY_POLICY ; https://juicecraft-store.myshopify.com/policies/terms-of-service, /refund-policy, /legal-notice -> 404 ; /policies/privacy-policy -> 200.
- Recommandation : Ne rien rédiger seul : le propriétaire décide de la rédaction des mentions légales, des CGV (y compris engagement de 12 mois, résiliation, rétractation pour les contenus et services numériques), de la politique de remboursement et de la politique de confidentialité, idéalement avec un avis juridique. Ensuite, avec accord (niveau 2), transformer les trois entrées du pied de page en liens vers de vraies pages, ajouter près du formulaire une phrase d'information avec lien, et lier aussi la politique Shopify à la boutique. En attendant, ne pas faire apparaître comme présentes des pages qui n'existent pas.

### PRIX-01 — Fausses indications de prix dans « You may also like » des pages offres
- Zone : Prix, offres et cohérence des contenus
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Sur la page ESSENTIELLE, la rubrique de recommandations affiche « Mise en place — ESSENTIELLE €49,00 (290,00 barré) », « Mise en place — PREMIUM €49,00 (590,00 barré) », « Mise en place — SUR MESURE (acompte) €49,00 (1.690,00 barré) » et « PREMIUM €49,00 (89,00 barré) ». Le prix d'abonnement du produit consulté (plan mensuel) est appliqué à tous les produits recommandés et le vrai prix est présenté comme un prix barré. Sur la page PREMIUM, le texte rendu montre le même schéma (« €89,00 » alterné avec 490/290/590/1.690).
- Attendu : Chaque carte affiche son propre prix réel (mise en place 290 €, 590 €, 1 690 €), sans prix barré trompeur.
- Preuve : Playwright https://juicecraft-store.myshopify.com/products/essentielle, capture /tmp/audit-prix/shot_ess_bottom.png ; /products/%F0%9F%94%B5-premium-%E2%AD%90 lu par texte (€89,00 / €490,00 / €89,00 / €290,00…). Les allocations Shopify ont compare_at_price=49000 pour le plan mensuel Essentielle (prix 4900), ce que le thème traite comme prix barré. Le panier /cart et les pages mise-en-place-* affichent les bons prix (€290,00, €590,00, €1.690,00). Capture Premium non obtenue (délai dépassé).
- Recommandation : Supprimer la rubrique « You may also like » des 3 pages offres, ou la désactiver pour les produits avec plan d'abonnement. À défaut, corriger le thème/le widget Appstle pour qu'il n'applique pas le plan de la page courante aux cartes. Corriger aussi le prix de base (voir PRIX-03) pour supprimer le compare_at artificiel. Vérifier ensuite visuellement les 3 pages.
- Preuve du contradicteur : Playwright /products/essentielle : texte de la section « 4 cartes » = « Mise en place — ESSENTIELLE | €49,00€290,00 | Mise en place — PREMIUM | €49,00€590,00 | SUR MESURE (acompte) | €49,00€1.690,00 | PREMIUM | €49,00€89,00 » ; capture /tmp/audit-prix-contra/ess_rec2.png et ess_rec.png (prix barrés visibles). /products/%F0%9F%94%B5-premium-%E2%AD%90 : « ESSENTIELLE €89,00€490,00 | Mise en place — ESSENTIELLE €89,00€290,00 | … PREMIUM €89,00€590,00 | SUR MESURE €89,00€1.690,00 ». /products/sur-mesure : « ESSENTIELLE €149,00€490,00 | MEP ESSENTIELLE €149,00€290,00 | … €149,00€1.690,00 » (capture sm_rec.png). Contre-épreuve curl sans JS : €290,00 / €590,00 / €1.690,00 / €89,00 corrects.

### PRIX-02 — Boutique : ni « /mois », ni « TTC » sur le prix de l'abonnement, ni les 12 mois d'engagement
- Zone : Prix, offres et cohérence des contenus
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Sur les pages produit des 3 offres, le prix d'abonnement s'affiche « €49,00 » (ou 89, 149) avec le menu « Abonnement Mensuel / Abonnement Annuel », sans « par mois », sans « TTC » et sans mention de l'engagement de 12 mois. Le texte rendu de la page ne contient ni « engag » ni « 12 mois » (le code MIN_CYCLES=12 n'existe que dans la valeur technique du plan). Le panier affiche « Prix €49,00 » et « Abonnement Mensuel » sans durée ; la fenêtre « Détails de l'abonnement » ne change pas le texte de la page. La mention TTC n'apparaît que dans la phrase sur la mise en place. Le site annonce, lui, « 12 mois d'engagement » et « 2 mois offerts ».
- Attendu : Le client voit avant de payer : montant mensuel TTC, engagement de 12 mois, alternative annuelle (2 mois offerts) et mise en place TTC, comme sur le site.
- Preuve : Playwright /products/essentielle : texte « €49,00 / Options d'achat / Abonnement / Fréquence de facturation / Abonnement Mensuel » ; regex /12\s*mois|engag/ = false après ouverture du popup ; /cart : « Prix €49,00 » ; GraphQL minCycles=12. Idem /products/%F0%9F%94%B5-premium-%E2%AD%90 (hasMois=false, eng=false) et /products/sur-mesure (eng=false).
- Recommandation : Ajouter en tête de chaque description (texte exact pour Essentielle) : « Abonnement mensuel : 49 € TTC par mois, engagement de 12 mois (588 € TTC sur 12 mois) ; ou abonnement annuel : 490 € TTC par an (2 mois offerts). Mise en place obligatoire : 290 € TTC, payée une seule fois. » Premium : 89 € / 1 068 € / 890 € / 590 €. Sur mesure : 149 € / 1 788 € / 1 490 € / acompte 1 690 € TTC. Renommer les plans : « Abonnement mensuel TTC (engagement 12 mois) » et « Abonnement annuel TTC (2 mois offerts) ». Faire valider la formulation d'engagement et de résiliation avec les CGV (voir PRIX-11).
- Preuve du contradicteur : Playwright /products/essentielle (capture ess_top.png) : « €49,00 / Options d'achat / Abonnement €49,00 / Fréquence de facturation / Abonnement Mensuel » ; /cart (panier jetable) : « ESSENTIELLE Abonnement Mensuel Prix €49,00 » ; GraphQL read-only sellingPlans : minCycles=12 pour les 3 plans mensuels. Après sélection du plan annuel, la page affiche « €490,00 » sans « /an ».

### PRIX-04 — Vidéos 30 s : prix « 49 € / 89 € / 149 € » sans « /mois » visible
- Zone : Prix, offres et cohérence des contenus
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Dans les deux vidéos 30 s livrées, les cartes d'offres montrent « 49 € », « 89 € », « 149 € » suivis de « TTC · + 290 € de mise en place ». Le « /mois » présent dans le code source (<em>/mois</em>) n'apparaît pas à l'image, y compris à 24,5 s (carte entièrement affichée). Un spectateur lit donc un prix unique de 49 € plus 290 €. L'engagement de 12 mois et le prix annuel ne sont pas mentionnés, et la carte Sur mesure dit « mise en place sur devis » sans « dès 1 690 € ».
- Attendu : « 49 €/mois TTC » lisible, ou mention équivalente (« par mois, engagement 12 mois »), et « dès 1 690 € » pour Sur mesure.
- Preuve : ffmpeg -ss 23.8 et 24.5 sur /home/user/juicecraft/livrables/juicecraft_pub_30s_16x9.mp4 (images /tmp/audit-prix/fr_16x9_23.8.png, fz_24.5.png) et sur juicecraft_pub_30s_9x16.mp4 (fr_9x16_23.8.png) : « 49 € », sans « /mois ». Source video30.html lignes 431-433 : <span class="pp9">49 €<em>/mois</em></span> ; CSS .pp9 avec background-clip:text et color:transparent.
- Recommandation : Corriger le rendu (cause probable, non testée : l'élément <em> hérite du texte transparent à fond dégradé ; lui donner une couleur propre ou mettre « /mois TTC » dans la ligne .ps9), ajouter « dès 1 690 € » sur Sur mesure, ré-encoder les deux vidéos et vérifier les images à 23,8 s. Ne pas diffuser les versions actuelles avant correction ; la publication reste soumise à accord.
- Preuve du contradicteur : ffmpeg -ss 24.5 -i /home/user/juicecraft/livrables/juicecraft_pub_30s_16x9.mp4 -frames:v 1 (/tmp/audit-prix-contra/f16_24.5.png) et idem 9x16 (f9_24.5.png) : « Essentielle 49 € / TTC · + 290 € de mise en place », « Premium 89 € / TTC · + 590 € de mise en place », « Sur mesure 149 € / TTC · mise en place sur devis », bandeau « Prix clairs, affichés TTC. » ; durée 30,000 s.

### PRIX-09 — Sur mesure : « prix confirmés avant tout paiement » mais l'acompte et la 1re mensualité se paient avant le devis
- Zone : Prix, offres et cohérence des contenus
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Le site affirme « Prix et contenu confirmés avant tout paiement » (section Contact) et, dans le configurateur, le même texte pour Sur mesure. Or la boutique permet de payer directement l'acompte de 1 690 € et la 1re mensualité ; le montant définitif n'est « confirmé par devis » qu'ensuite. Le panier de test Sur mesure mensuel + acompte atteint 1 839 € (183 900 centimes) sans devis préalable.
- Attendu : Soit le devis est validé avant le paiement, soit le texte indique que l'acompte précède le devis et ce qu'il couvre (et qu'il est remboursable si le devis n'est pas accepté, à valider juridiquement).
- Preuve : Texte rendu du site : « Prix et contenu confirmés avant tout paiement » ; /products/mise-en-place-sur-mesure-acompte.js : « Le montant définitif est confirmé par devis avant le début du travail » ; /products/sur-mesure.js ; panier test : total 183900 (mes-month).
- Recommandation : Décision du propriétaire, avec validation juridique du traitement de l'acompte (CGV). Option A : réserver le paiement Sur mesure aux clients ayant accepté un devis (lien non listé). Option B : reformuler sur le site et en boutique : « Pour Sur mesure, un acompte de 1 690 € TTC est payé à la commande ; le montant définitif de la mise en place est confirmé par devis avant le début du travail. »
- Preuve du contradicteur : Panier jetable (curl cookie jar) : POST /cart/add.js SUR MESURE mensuel (692928840014) + 61143347331406 → /cart.js total_price=183900 item_count=2 ; Playwright : checkout atteint, total « 1 839,00 € »-équivalent non saisi ; texte https://juicecraft.fr : « Prix et contenu confirmés avant tout paiement » ; /products/mise-en-place-sur-mesure-acompte.js : « Le montant définitif est confirmé par devis avant le début du travail ».

### PRIX-10 — Mise en place « obligatoire » mais non imposée au paiement
- Zone : Prix, offres et cohérence des contenus
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Les descriptions disent « Mise en place obligatoire », mais un abonnement peut être acheté seul : panier test avec Essentielle mensuel seul = 4 900 centimes (49 €), 1 article. Les produits de mise en place sont aussi vendus seuls (boutons « Ajouter » sur l'accueil et le catalogue). La note du site dit seulement que la page de l'offre « vous propose d'ajouter la mise en place », formulation facultative, contredisant « obligatoire ». Manque à gagner possible de 290 à 1 690 € par commande.
- Attendu : Mise en place réellement imposée avec l'abonnement (ou texte indiquant qu'elle est facultative).
- Preuve : curl avec cookie jar : POST /cart/add.js {id:61108150141262, selling_plan:692928774478} → 200, /cart.js total_price=4900 item_count=1 ; texte du site : « À la commande, la page de l'offre vous propose d'ajouter la mise en place au panier avant de payer. »
- Recommandation : Étudier avec Appstle/Shopify une règle de panier ou un lot (bundle) imposant l'achat conjoint ; en attendant, surveiller les commandes sans mise en place. Reformuler le site : « La mise en place est obligatoire : ajoutez-la au panier avant de payer. » Masquer les produits mise-en-place-* du catalogue public si possible.
- Preuve du contradicteur : curl cookie jar : POST /cart/add.js {id:61108150141262, selling_plan:692928774478} → /cart.js total_price=4900 item_count=1 ; graphql_query ordersCount=1, orders[0] : name #1001, test:true, lineItems [ESSENTIELLE, sellingPlan « Abonnement Mensuel », 49.0] ; capture /tmp/audit-prix-contra/ess_top.png : bouton « Payer avec PayPal » sous « Ajouter au panier ».

### PRIX-M1 — Infobulle « Modifiez ou annulez votre abonnement à tout moment » contredit l'engagement de 12 mois
- Zone : Prix, offres et cohérence des contenus
- Gravité : élevé | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Sur chaque page d'offre, le lien « Détails de l'abonnement » ouvre une infobulle qui promet « Gardez un contrôle total sur vos abonnements. Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. ». Cette promesse contredit l'engagement de 12 mois affiché sur le site (« 12 mois d'engagement en paiement mensuel ») et configuré dans Appstle (minCycles=12). La phrase est présente dans le code des 6 pages produit.
- Attendu : Aucune promesse d'annulation à tout moment sur un abonnement mensuel engagé 12 mois ; texte aligné sur les conditions d'engagement et de résiliation des CGV.
- Preuve : Playwright /products/essentielle, clic sur « Détails de l'abonnement » : infobulle visible (capture /tmp/audit-prix-contra/ess_popup.png) « Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. » ; curl : grep -c « annulez votre abonnement » = 1 sur essentielle, 🔵-premium-⭐, sur-mesure et les 3 pages mise-en-place-* ; graphql_query : minCycles 12.
- Recommandation : Après accord du propriétaire, remplacer ou masquer ce texte dans le thème ou les réglages de l'application d'abonnement (par exemple : « Abonnement mensuel avec engagement de 12 mois ; abonnement annuel sans reconduction tacite non précisée » à valider avec les CGV). Ne pas inventer les conditions de résiliation : à faire valider avec PRIX-11.

### PRIX-M3 — Page de paiement : aucune mention de l'engagement de 12 mois ni de TTC, libellé « par période de mois »
- Zone : Prix, offres et cohérence des contenus
- Gravité : élevé | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : La page de paiement Shopify (ouverte sans rien saisir, panier Essentielle mensuel + mise en place) affiche le total 339,00 € et « Sous-total récurrent : 49,00 € par période de mois », sans durée d'engagement, sans « TTC » ni ligne de taxe, avec la phrase générique « vous acceptez les futurs montants facturés indiqués sur cette page et la politique de résiliation ». L'engagement de 12 mois et le prix annuel ne sont donc annoncés ni à la caisse, ni dans le panier, ni sur la fiche produit ; la politique de résiliation citée n'existe pas parmi les pages testées (404).
- Attendu : À la caisse : montant mensuel TTC, durée de 12 mois d'engagement et accès à la politique de résiliation.
- Preuve : Playwright : ajout via /cart/add.js (panier jetable) puis /checkout (URL /checkouts/<jeton>) ; texte lu : « Résumé des coûts … 339,00 € … Sous-total récurrent … 49,00 € par période de mois » ; recherches engag, 12 mois, par mois = false ; rien saisi, page quittée sans commande ; curl /policies/subscription-policy et /policies/cancellation-policy = 404.
- Recommandation : Après accord du propriétaire : renseigner la politique de résiliation et de rétractation de la boutique (voir PRIX-11) ; ajouter dans le nom des plans Appstle « mensuel TTC, engagement 12 mois » et « annuel TTC » pour que le libellé de la caisse porte l'information ; contrôler la page de paiement après modification. La formulation de l'engagement se fait avec les CGV.

### ACHAT-03 — L'engagement de 12 mois du mensuel n'est annoncé ni sur la fiche produit ni au paiement ; le bloc affiche « annulez à tout moment »
- Zone : Parcours d'achat et page de paiement
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Sur la fiche, le bloc d'abonnement dit « Gardez un contrôle total sur vos abonnements. Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. » La description des trois offres ne mentionne aucun engagement. Le checkout affiche seulement « 49,00 € par période de mois » sans durée minimale. L'engagement (MIN_CYCLES=12) n'est indiqué que sur juicecraft.fr. Un client peut donc acheter le mensuel en croyant pouvoir arrêter à tout moment.
- Attendu : Mention claire et visible avant l'achat : « 12 mois d'engagement » pour le mensuel, cohérente avec la page d'accueil et avec le plan MIN_CYCLES=12.
- Preuve : Texte du bloc .appstle_sub_widget lu sur les 12 scénarios : « Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. » ; descriptions /products/essentielle.js, premium, sur-mesure : aucune occurrence de « engagement » ni « 12 mois » ; juicecraft.fr : « 12 mois d'engagement en paiement mensuel »
- Recommandation : Dans Appstle (réglage du widget, accord requis), remplacer le texte du tooltip par : « Abonnement mensuel : engagement de 12 mois, puis résiliable à tout moment. Abonnement annuel : renouvelé chaque année, résiliable avant l'échéance. » Ajouter en tête de description de chaque offre : « Abonnement mensuel avec engagement de 12 mois ; annuel = 10 mensualités (2 mois offerts). »
- Preuve du contradicteur : Texte .appstle_sub_widget lu sur /products/essentielle?selling_plan=692928774478 : « ...Modifiez ou annulez votre abonnement à tout moment, en fonction de vos besoins. ». grep -il -E 'engagement|12 mois' sur les 6 /products/<handle>.js : aucun fichier. Texte complet du checkout mobile (4 034 caractères) : motif engagement|12 mois absent. https://juicecraft.fr/ : « 49 €/mois (12 mois d'engagement) ». Plan : option « 1MONTH1MONTHMIN_CYCLES=12 ».

### ACHAT-04 — Case « Envoyez-moi des nouvelles et des offres par e-mail » pré-cochée au paiement
- Zone : Parcours d'achat et page de paiement
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Sur les 3 paniers testés, la case de consentement marketing est cochée par défaut. C'est la seule case du formulaire.
- Attendu : Un consentement marketing (RGPD/CNIL) doit être donné activement : case décochée par défaut.
- Preuve : Playwright, input[name=marketing_opt_in] checked=true sur essentielle-mensuel, essentielle-annuel, sur-mesure-mensuel (checkouts /fr-fr) ; capture shots/co-ess-M-desk.png
- Recommandation : Dans Shopify Paramètres > Paiement (Checkout) > Marketing par e-mail : ne pas présélectionner la case (« Ne pas présélectionner »). À appliquer avec l'accord du propriétaire.
- Preuve du contradicteur : Playwright : input[name=marketing_opt_in].checked === true sur checkouts Essentielle mensuel (ordinateur), Essentielle annuel, Sur mesure mensuel, Premium annuel, Essentielle mensuel (mobile 390 px) et mise en place seule ; libellé « Envoyez-moi des nouvelles et des offres par e-mail ».

### ACHAT-06 — La « mise en place obligatoire » n'est pas imposée : un abonnement seul passe jusqu'au paiement
- Zone : Parcours d'achat et page de paiement
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Rien n'empêche d'ajouter l'abonnement sans le produit de mise en place (290 à 1 690 € de revenu initial). Le panier avec un abonnement seul est accepté et mène à la page de paiement ; seul un lien dans la description rappelle la mise en place. Le message dit « ajoutez-la au panier avant de payer », sans contrôle.
- Attendu : Impossibilité de payer une offre sans sa mise en place, ou ajout automatique de la mise en place.
- Preuve : POST /cart/add.js {id:61108150141262, quantity:1, selling_plan:692928774478} -> 200 sans produit de mise en place ; navigation vers /checkout -> page /checkouts/cn/.../fr-fr atteinte (lk.js) ; le panier test montre 1 seule ligne ESSENTIELLE
- Recommandation : Mettre en place avec accord du propriétaire une règle côté boutique (Shopify Function de validation du panier ou ajout automatique de la mise en place via l'application d'abonnement/bundle) ; à défaut, rendre le message plus visible au-dessus du bouton : « La mise en place (290 € TTC) doit être ajoutée au panier avant de payer. »
- Preuve du contradicteur : POST /cart/add.js {id:61108150141262, quantity:1, selling_plan:692928774478} -> 200, cart total 4900 ; /checkout -> /checkouts/cn/<jeton>/fr-fr, résumé « ESSENTIELLE 49,00 € ; Total 49,00 € ; Sous-total récurrent 49,00 € par période de mois », une seule ligne. Position du lien de description sur /products/sur-mesure : ordinateur top=740 (bouton add top=542), mobile top=1124 (bouton top=913, innerHeight 844).

### SEO-18 — Prix de base des produits Premium et Sur mesure incohérent avec la règle « prix de base = annuel » (visible dans les données structurées)
- Zone : Référencement, contenu et rédaction
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : La grille prévoit que le prix de base Shopify des produits d'offre est le prix annuel. Essentielle est bien à 490,00 €, mais Premium est à 89,00 € (attendu 890 €) et Sur mesure à 149,00 € (attendu 1 490 €). Conséquences vérifiées : les fiches, le catalogue et l'accueil affichent « Premium €89,00 » et « Sur mesure €149,00 » ; le JSON-LD Product et og:price:amount publient 89,00 et 149,00 pour des offres dont l'annuel vaut 10 fois plus ; une fiche Premium/Sur mesure affichera donc un prix annuel incohérent avec Essentielle. Les plans Appstle portent bien les bons prix (8900/89000 et 14900/149000). Non vérifié : effet réel au paiement.
- Attendu : Premium 890,00 €, Sur mesure 1 490,00 € (comme Essentielle 490,00 €), ou à défaut des données structurées cohérentes.
- Preuve : https://juicecraft-store.myshopify.com/products.json : premium price "89.00", sur-mesure "149.00", essentielle "490.00" ; /products/essentielle.js : price 49000 ; og:price:amount « 89,00 » sur la fiche Premium et « 490,00 » sur Essentielle ; catalogue rendu : « PREMIUM €89,00 », « SUR MESURE €149,00 », « ESSENTIELLE €490,00 ».
- Recommandation : Après accord du propriétaire (prix = niveau 2), vérifier avec Appstle que le changement du prix de base à 890,00 € et 1 490,00 € ne modifie pas les plans, puis corriger les deux variantes. Contrôler ensuite le JSON-LD et le catalogue.
- Preuve du contradicteur : /products.json : essentielle 490.00, sur-mesure 149.00, 🔵-premium-⭐ 89.00 ; /products/<handle>.js : allocations premium price 8900 et 89000 (compare_at 8900), sur-mesure 14900 et 149000 ; texte rendu /collections/all : « ESSENTIELLE | €490,00 … PREMIUM | €89,00 … SUR MESURE | €149,00 » ; JSON-LD Premium offers.price "89.00", og:price:amount 89,00.

### SEO-19 — Cartes « You may also like » : prix de l'offre affiché à la place du prix du produit, avec le vrai prix barré
- Zone : Référencement, contenu et rédaction
- Gravité : élevé | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Sur la fiche Essentielle, la section de recommandations montre « Mise en place — ESSENTIELLE €49,00 ~~€290,00~~ », « Mise en place — PREMIUM €49,00 ~~€590,00~~ », « Mise en place — SUR MESURE (acompte) €49,00 ~~€1.690,00~~ » et « PREMIUM €49,00 ~~€89,00~~ ». Le prix de l'abonnement courant (49 €) est appliqué à tous les produits et le vrai prix est barré : promotion fictive de -83 % à -97 %, source de confusion et de pratique commerciale trompeuse, et de litiges à l'encaissement. Probablement dû à l'application d'abonnement dans la section de recommandations du thème.
- Attendu : Chaque carte affiche son prix réel, sans prix barré.
- Preuve : Playwright https://juicecraft-store.myshopify.com/products/essentielle, texte rendu de la section « You may also like » : « Mise en place — ESSENTIELLE €49,00€290,00 », « Mise en place — PREMIUM €49,00€590,00 », « Mise en place — SUR MESURE (acompte) €49,00€1.690,00 », « PREMIUM €49,00€89,00 ». Capture : prix barrés visibles. Le catalogue /collections/all affiche les prix corrects (€290,00, €590,00, €1.690,00).
- Recommandation : Le plus simple : supprimer ou masquer la section de recommandations des fiches produit (thème : Personnaliser > modèle Produit > retirer « Produits recommandés »). Sinon régler l'affichage des prix de l'application Appstle (réglages d'application = niveau 2). Vérifier ensuite dans une fenêtre privée.
- Preuve du contradicteur : Capture Playwright /products/essentielle (défilement jusqu'à « You may also like ») : cartes « Mise en place — ESSENTIELLE €49,00 ~~€290,00~~ », « Mise en place — PREMIUM €49,00 ~~€590,00~~ », « PREMIUM €49,00 ~~€89,00~~ » ; /collections/all : €290,00, €590,00, €1.690,00 sans barré.

### SEO-M2 — Fiches d'offre : barre d'ajout rapide avec faux prix barré (Essentielle 49 € barré 490 €, Premium 89 € barré 89 €)
- Zone : Référencement, contenu et rédaction
- Gravité : élevé | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Sur les fiches produit de la boutique, la barre d'ajout rapide qui apparaît au défilement affiche le prix de l'abonnement mensuel avec le prix de base barré : « ESSENTIELLE €49,00 ~~€490,00~~ » (promotion apparente de 90 % qui n'existe pas), « PREMIUM €89,00 ~~€89,00~~ » et « SUR MESURE €149,00 ~~€149,00~~ » (prix barré identique). L'élément barré est un « compare amount » de l'application d'abonnement. C'est le même mécanisme que SEO-19 mais sur la fiche elle-même, au moment de l'ajout au panier, donc plus exposé. Conséquence sur la correction de SEO-18 (prix de base à 890 € et 1 490 €) : par analogie avec Essentielle, les plans mensuels de Premium et Sur mesure afficheront alors aussi un faux prix barré (89 € barré 890 €, 149 € barré 1 490 €) ; ceci est une déduction à vérifier, non testée.
- Attendu : Prix mensuel affiché sans prix barré, ou compare amount désactivé dans l'application d'abonnement.
- Preuve : Playwright https://juicecraft-store.myshopify.com/products/essentielle : sticky-add-to-cart innerText « ESSENTIELLE €49,00€490,00 Ajouter au panier » ; éléments span.appstle_subscription_compare_amount « €490,00 » et « Original price €490,00 » ; capture d'écran : €49,00 suivi de €490,00 barré dans la barre du bas ; fiche Premium : <span class="price appstle_subscription_final_price">€89,00</span><span class="price" data-appstle-price-modified="true" style="text-decoration: line-through;"><bdi>€89,00</bdi></span> ; Sur mesure : « €149,00€149,00 » ; /products/essentielle.js : allocation mensuelle price 4900, compare_at_price 49000.
- Recommandation : Dans les réglages de l'application d'abonnement (affichage du prix de comparaison dans le widget et la barre d'ajout), désactiver l'affichage du prix barré, ou le limiter aux vraies réductions ; recontrôler en fenêtre privée sur les trois fiches, à faire avant ou avec la correction du prix de base de Premium et Sur mesure (SEO-18). Réglage d'application : niveau 2.

### LEGAL-06 — Résiliation en ligne : fonctionnalité d'accès direct non vérifiée, aucune indication sur le site ou la boutique
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 3 | Statut : confirmé | Confiance : moyenne
- Constat : Aucun lien ni bouton « résilier votre contrat » n'est visible sur le site, la boutique ou le paiement. La seule indication est dans le texte générique : « Your order confirmation emails have links to your order. You can manage your subscription from there. » Le portail Appstle n'a pas pu être contrôlé (nécessite une commande).
- Attendu : Pour un contrat conclu en ligne avec un consommateur, le professionnel met à disposition une fonctionnalité gratuite de résiliation par voie électronique, accessible directement et facilement, intitulée « résilier votre contrat » ou équivalent. Références : Code de la consommation art. L215-1-1 https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046190107 et décret n° 2023-417 du 31 mai 2023 (art. D215-1 et D215-2) https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000047613963. L'obligation vise le consommateur ; sa portée pour une clientèle exclusivement professionnelle est à faire valider.
- Preuve : Texte du site et de la boutique : aucune occurrence de « résilier votre contrat » ; fenêtre « Annulations » du paiement (anglais) : « You can manage your subscription from there » (liens de l'e-mail de confirmation).
- Recommandation : Le propriétaire fait valider si L215-1-1 s'applique à ses clients, puis vérifie dans Appstle (réglages du portail client) qu'un accès « Résilier votre contrat » est proposé depuis le site ou le compte. Test de bout en bout à faire sur une vraie commande de test avec accord (hors audit).
- Preuve du contradicteur : grep -i 'résili' : site_text.txt = 0 ; prod_*.txt = 0 (seul 'annulez … à tout moment') ; cart.txt ligne 39 'politique de résiliation' (simple libellé) ; checkout.txt = 'politique de résiliation' et 'Annulations' (bouton vers texte générique). Légifrance L215-1-1 (LEGIARTI000046190107) : en vigueur depuis le 1er juin 2023, obligation de fonctionnalité gratuite, vise le consommateur.

### LEGAL-07 — Pas de médiateur de la consommation indiqué
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 3 | Statut : confirmé | Confiance : moyenne
- Constat : Aucun médiateur de la consommation (nom, coordonnées, site) n'apparaît sur le site, les fiches produits, le paiement ni dans une CGV (inexistante).
- Attendu : Le professionnel garantit au consommateur le recours effectif à un médiateur et communique ses coordonnées de façon visible (site, CGV, bons de commande). Références : Code de la consommation art. L612-1 https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032224805 et L616-1 https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032224762 ; R616-1 ; page economie.gouv.fr « Vos principales obligations » (médiation). Vise les consommateurs ; applicabilité si la clientèle est uniquement professionnelle : à faire valider.
- Preuve : grep -iE "médiat|mediat" sur https://juicecraft.fr/ = 0 ; idem sur les textes des produits, du panier et du paiement.
- Recommandation : Le propriétaire choisit un médiateur référencé (adhésion préalable obligatoire, il ne faut pas citer un médiateur sans convention) puis fait ajouter ses coordonnées aux CGV et aux mentions. Niveau 3.
- Preuve du contradicteur : grep -n -i 'médiat' home.html : une seule ligne (1062) '<span>Médiation</span>' dans la démo Vallès & Associés ; aucune mention dans site_text.txt hors cette étiquette, ni dans les textes boutique, panier, paiement. Légifrance LEGIARTI000032224805 = L612-1 ; LEGIARTI000032224762 = L616-1.

### LEGAL-08 — Politique de confidentialité Shopify générique, incomplète et limitée à la boutique
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : La politique (lue en entier) est le modèle Shopify : (1) le champ téléphone est vide (« veuillez nous appeler au , nous envoyer un e-mail… ») ; (2) aucune base légale précise, aucune durée de conservation chiffrée (« dépend de différents facteurs ») ; (3) aucun sous-traitant propre à l'activité n'est nommé (Web3Forms, Netlify, Appstle, PayPal, Google Fonts) ; (4) elle parle de « sociétés affiliées/groupe de sociétés », « publicités personnalisées » et d'un droit de ne pas partager pour publicité ciblée, sans lien avec l'activité réelle ; (5) elle renvoie à des « Conditions de service » qui n'existent pas ; (6) la CNIL n'est pas nommée comme autorité de plainte ; (7) elle ne décrit pas les cookies ; (8) elle est rattachée à la boutique mais le « Confidentialité » du site n'est pas un lien. L'identité du responsable se limite à « juicecraft » sans statut ni SIRET.
- Attendu : Une information conforme aux articles 12 à 14 du RGPD : identité et coordonnées du responsable, finalités, base légale, destinataires, durée de conservation (ou critères), droits et moyen de les exercer, droit de réclamation auprès de la CNIL, transferts. Sources : https://www.cnil.fr/fr/conformite-rgpd-information-des-personnes-et-transparence ; https://www.cnil.fr/fr/informer-les-personnes. Adéquation de chaque rubrique : à faire valider.
- Preuve : GET https://juicecraft-store.myshopify.com/policies/privacy-policy = 200 ; extraits : « veuillez nous appeler au , nous envoyer un e-mail à l'adresseevannlassalle@gmail.com ou nous contacter à l'adresse 9 rue de St Pol, 62270 Conchy sur Canche, France » ; « La durée de conservation de vos informations personnelles dépend de différents facteurs » ; « En cas de contradiction entre nos Conditions de service et la présente Politique de confidentialité… » ; « Nous utilisons Shopify pour prendre en charge la publicité personnalisée… ».
- Recommandation : Le propriétaire fait adapter la politique (une version pour la boutique et une page /confidentialite pour juicecraft.fr, ou un texte commun) en indiquant : responsable et statut, finalités (réponse aux demandes, exécution du contrat, facturation, obligations légales), base légale, destinataires et sous-traitants réels (Shopify, Appstle, PayPal, Web3Forms, Netlify), durées chiffrées, droits, réclamation CNIL ; renseigner ou retirer la phrase du téléphone. Niveau 3 : texte juridique.
- Preuve du contradicteur : GET /policies/privacy-policy = 200 (260 416 octets). Texte extrait : 'veuillez nous appeler au , nous envoyer un e-mail…' ; 'base juridique'/'base légale' = 0 occurrence ; 'CNIL' = 0 ; 'Web3Forms','Netlify','Appstle','PayPal','Google' = 0 ; 'En cas de contradiction entre nos Conditions de service…' présent ; 'La durée de conservation… dépend de différents facteurs' ; 'publicité personnalisée' et 'groupe de sociétés' présents.

### LEGAL-17 — Distinction particuliers / professionnels non faite : le site vise les professionnels, la boutique vend à tous
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 3 | Statut : confirmé | Confiance : moyenne
- Constat : Le site s'adresse aux « professionnels, commerces, artisans et entreprises », mais le paiement est ouvert à tous les pays et à tout acheteur, sans question « particulier ou professionnel », sans champ entreprise/SIRET/TVA intracommunautaire, et sans mention de la clientèle visée. Les droits de rétractation, médiation et résiliation en ligne diffèrent selon que l'acheteur est un consommateur ou un professionnel.
- Attendu : Le propriétaire confirme la clientèle visée (professionnels uniquement ou aussi particuliers), puis les textes l'indiquent ; si B2B seulement, une mention en ce sens dans les CGV. L'application des textes consommateurs à un professionnel est à faire valider (art. L221-3 pour les petits professionnels).
- Preuve : Texte du paiement : champs Prénom, Nom, Adresse, Code postal, Ville, Téléphone, liste Pays (France par défaut, ~240 pays) ; aucun champ Société ni TVA. Site : « pour les professionnels, commerces, artisans et entreprises » ; shopsToCountries = ["FR"] (graphql).
- Recommandation : Décision du propriétaire (niveau 3) : préciser la cible dans les CGV et, si nécessaire, ajouter un champ société/TVA au paiement et la mention « vente réservée aux professionnels ».
- Preuve du contradicteur : Playwright /checkout : champs [email, marketing_opt_in, paiement carte/PayPal, countryCode, firstName, lastName, address1, address2, postalCode, city, phone optionnel] sans champ société/SIRET/TVA ; select countryCode : 238 options, valeur FR. graphql shop.shipsToCountries = ["FR"]. Site : 'professionnels, commerces, artisans et entreprises'.

### PRIX-03 — Prix de base Shopify : annuel pour Essentielle, mensuel pour Premium et Sur mesure
- Zone : Prix, offres et cohérence des contenus
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : La règle de référence veut que le prix de base des produits d'offre soit le prix annuel. Essentielle est à 490 € mais Premium est à 89 € et Sur mesure à 149 €. Résultat : l'accueil et le catalogue de la boutique listent « ESSENTIELLE €490,00 », « PREMIUM €89,00 », « SUR MESURE €149,00 » sans unité, et les données structurées de partage affichent og:price:amount 490,00 / 89,00 / 149,00. Les allocations de plan ont un compare_at_price égal au prix de base (Essentielle mensuel : prix 4900, compare_at 49000 ; Premium annuel : prix 89000, compare_at 8900).
- Attendu : Prix de base = prix annuel : 490 € (déjà), 890 € et 1 490 €, avec les plans à prix fixes inchangés.
- Preuve : /products/<handle>.js : price 49000 / 8900 / 14900 ; GraphQL priceRangeV2 490.0 / 89.0 / 149.0 ; https://juicecraft-store.myshopify.com/ et /collections/all : « €490,00 », « €89,00 », « €149,00 » ; og:price:amount 490,00 / 89,00 / 149,00.
- Recommandation : Après accord du propriétaire, passer le prix de la variante Premium à 890,00 € et Sur mesure à 1 490,00 €, puis rejouer les paniers de test (mensuel : 89 € / 149 € ; annuel : 890 € / 1 490 €) et vérifier que les plans Appstle conservent leurs prix fixes. Ajouter dans le titre ou la description d'accueil « dès 49 €/mois TTC ».
- Preuve du contradicteur : curl /products/<handle>.js : price 49000 / 8900 / 14900 ; selling_plan_allocations Essentielle mensuel price 4900 compare_at_price 49000 ; graphql_query products.priceRangeV2 : 490.0 / 89.0 / 149.0 ; curl https://juicecraft-store.myshopify.com/ : « ESSENTIELLE €490,00 … PREMIUM €89,00 … SUR MESURE €149,00 » ; /collections/all/products.json : 490.00 / 89.00 / 149.00.

### PRIX-06 — Promesses de contenu des offres différentes entre site et boutique
- Zone : Prix, offres et cohérence des contenus
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Présent seulement en boutique : « Jusqu'à 5 pages » (Essentielle) et « Jusqu'à 10 pages » (Premium) ; Essentielle : Hébergement, Maintenance technique, Corrections et petites modifications, Assistance ; Premium : Portfolio / galerie, Modifications régulières, Maintenance, Assistance prioritaire, « Design entièrement personnalisé » ; Sur mesure : Tout le contenu de Premium, Intégrations externes, Animations avancées, SEO avancé, Maintenance renforcée, Accompagnement personnalisé. Présent seulement sur le site : « E-commerce, réservation, espace client » (Sur mesure) et « Accompagnement après livraison » (Premium). Formulé différemment : Premium « Design premium avec animations » (site) contre « Design entièrement personnalisé » (boutique). Les cartes du site ne listent ni limites de pages, ni hébergement, ni maintenance, ni assistance, que seule l'introduction mentionne globalement. Identiques : « Modifications incluses : 2 h par mois, au-delà sur devis » (Sur mesure), bases SEO, mise en ligne, formulaire de contact, vitesse.
- Attendu : Une liste unique de promesses par offre, identique sur le site, la boutique, les méta-descriptions et les vidéos.
- Preuve : https://juicecraft.fr (section Offres) et /products/essentielle.js, /products/%F0%9F%94%B5-premium-%E2%AD%90.js, /products/sur-mesure.js (champ description) ; méta Premium « Design personnalisé, animations, SEO renforcé et assistance prioritaire » ; vidéo : « Accompagnement après livraison ».
- Recommandation : Faire trancher le propriétaire sur la liste de référence, puis aligner. Proposition : ajouter sur le site « Jusqu'à 5 pages », « Hébergement, maintenance technique et assistance inclus » (Essentielle) ; « Jusqu'à 10 pages », « Maintenance et assistance prioritaire » (Premium) ; et en boutique ajouter « E-commerce, réservation, espace client » à Sur mesure (si c'est inclus) ou le retirer du site. Aligner méta-descriptions et vidéos ensuite. Publication du site soumise à accord.
- Preuve du contradicteur : curl /products/essentielle.js, /products/%F0%9F%94%B5-premium-%E2%AD%90.js, /products/sur-mesure.js (champ description) comparés au texte des cartes de https://juicecraft.fr (section « Des offres claires pour démarrer ») : « Jusqu'à 5 pages », « Jusqu'à 10 pages », « Maintenance renforcée » absents du site ; « E-commerce, réservation, espace client » absent des descriptions Shopify.

### PRIX-07 — Configurateur : tailles de site incompatibles avec les plafonds de pages des offres
- Zone : Prix, offres et cohérence des contenus
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le configurateur propose « Quelques pages : De 2 à 6 pages » et « Un site complet : 7 pages ou plus ». Le code recommande Essentielle pour « quelques pages » (sauf priorité haut de gamme) alors que l'offre Essentielle est limitée à 5 pages en boutique ; « 7 pages ou plus » conduit à Premium, limité à 10 pages, sans renvoi vers Sur mesure au-delà.
- Attendu : Seuils du configurateur alignés sur les limites de pages des offres (5 et 10).
- Preuve : Code JS de juicecraft.fr : Q[1] (["few","Quelques pages","De 2 à 6 pages"], ["many","Un site complet","7 pages ou plus"]) et recommend() : « else if (s === "many" || p === "premium") … Premium », sinon Essentielle ; boutique : « Jusqu'à 5 pages », « Jusqu'à 10 pages ».
- Recommandation : Remplacer par « De 2 à 5 pages », « De 6 à 10 pages », et ajouter un cas « Plus de 10 pages » orienté vers Sur mesure ; ajuster recommend() en conséquence.
- Preuve du contradicteur : https://juicecraft.fr, script du configurateur : ["few","Quelques pages","De 2 à 6 pages"], ["many","Un site complet","7 pages ou plus"] ; recommend() : « else if (s === "many" || p === "premium") r = { … t: "Vitrine Premium" … } » ; /products/essentielle.js : « Jusqu'à 5 pages ».

### PRIX-08 — Le site se contredit sur la maintenance : incluse dans l'abonnement ou optionnelle
- Zone : Prix, offres et cohérence des contenus
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : L'introduction des offres dit : « L'abonnement couvre l'hébergement, la maintenance et l'assistance, avec 12 mois d'engagement ». La section Approche dit « Maintenance possible… Activez, désactivez, c'est vous qui choisissez », et la FAQ dit « une maintenance peut être mise en place selon vos besoins ». La boutique annonce la maintenance incluse (Essentielle « Maintenance technique », Premium « Maintenance », Sur mesure « Maintenance renforcée ») sur un engagement de 12 mois.
- Attendu : Un seul discours : maintenance incluse dans l'abonnement, ou optionnelle et facturée à part.
- Preuve : https://juicecraft.fr texte rendu : paragraphe de la section Offres ; carte « Maintenance possible / Une intervention ultérieure reste possible selon vos besoins… Activez, désactivez, c'est vous qui choisissez. » ; FAQ « Que se passe-t-il après la mise en ligne ? ».
- Recommandation : Si la maintenance est incluse (cohérent avec la boutique et les prix) : remplacer le titre par « Maintenance incluse » et le texte par « Mises à jour, sauvegardes et corrections techniques sont incluses dans votre abonnement ; les évolutions au-delà du forfait sont sur devis. » ; FAQ : « Pendant l'abonnement, l'hébergement, la maintenance et l'assistance sont inclus. »
- Preuve du contradicteur : /tmp/audit-prix-contra/live.html (curl https://juicecraft.fr) : « L'abonnement couvre l'hébergement, la maintenance et l'assistance, avec 12 mois d'engagement en paiement mensuel » ; ligne 979 « <h3>Maintenance possible</h3> … Activez, désactivez, c'est vous qui choisissez. » ; FAQ q6 « une maintenance peut être mise en place selon vos besoins ».

### PRIX-M2 — Barre d'achat de la page Essentielle : 49 € avec 490 € barré
- Zone : Prix, offres et cohérence des contenus
- Gravité : moyen | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Sur la page ESSENTIELLE, la barre d'ajout au panier qui s'affiche au défilement montre « €49,00 » suivi de « €490,00 » barré, ce qui suggère une réduction de 90 % alors que 490 € est le prix annuel et non un ancien prix. Cause : l'allocation du plan mensuel a compare_at_price = 49 000 pour un prix de 4 900. Sur Premium et Sur mesure, prix et prix de comparaison sont identiques (8 900 / 14 900), aucun barré visible.
- Attendu : Aucun prix barré sur les plans d'abonnement ; chaque prix affiché avec son unité.
- Preuve : Capture /tmp/audit-prix-contra/ess_rec.png (barre du bas : « ESSENTIELLE €49,00 ~~€490,00~~ Ajouter au panier ») ; Playwright texte de main : « ESSENTIELLE / €49,00€490,00 / Ajouter au panier » ; /products/essentielle.js : alloc 692928774478 price 4900 compare_at_price 49000 ; Premium « €89,00€89,00 » et Sur mesure « €149,00€149,00 » sans élément barré visible.
- Recommandation : Corriger en même temps que PRIX-03 (prix de base annuel de Premium et Sur mesure, et vérification de la valeur compare_at de chaque plan Essentielle) ; contrôler visuellement la barre collante et le bloc d'achat des 3 pages après modification.

### ACHAT-08 — Prix de base incohérent entre les produits : Essentielle 490 €, Premium 89 € et Sur mesure 149 € dans les listes
- Zone : Parcours d'achat et page de paiement
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : La grille de référence prévoit le prix annuel comme prix de base. Essentielle l'applique (490 €), mais Premium (89 €) et Sur mesure (149 €) ont le prix mensuel comme prix de base. Les cartes de la page d'accueil de la boutique, du catalogue et de « You may also like » affichent donc « €490,00 », « €89,00 », « €149,00 » sans unité (an/mois), ce qui prête à confusion.
- Attendu : Prix de base annuel pour les 3 offres (490 / 890 / 1 490 €) ou affichage explicite de la périodicité (« dès 89 €/mois »).
- Preuve : /collections/all/products.json : ESSENTIELLE 490.00, PREMIUM 89.00, SUR MESURE 149.00 ; /products/<handle>.js : price 49000, 8900, 14900 (les plans annuels valent 49000, 89000, 149000 via selling_plan_allocation) ; capture shots/pg-all-mob.png
- Recommandation : Après accord du propriétaire : passer le prix de base de PREMIUM à 890 € et de SUR MESURE à 1 490 € (les plans Appstle fixent déjà les prix 89/149 et 890/1 490), ou ajouter « dès … €/mois » aux cartes. Vérifier ensuite que le prix du plan mensuel reste 89 € et 149 €.
- Preuve du contradicteur : /collections/all/products.json : essentielle 490.00, 🔵-premium-⭐ 89.00, sur-mesure 149.00. /products/<handle>.js : price 49000, 8900, 14900 ; allocations de plans : [4900, 49000], [8900, 89000], [14900, 149000]. Page d'accueil boutique rendue : « ESSENTIELLE €490,00 ... PREMIUM €89,00 ... SUR MESURE €149,00 ».

### ACHAT-09 — « 490,00 € par période de an » : libellé du sous-total récurrent mal formé
- Zone : Parcours d'achat et page de paiement
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Au paiement, le sous-total récurrent affiche « 49,00 € par période de mois » et pour l'annuel « 490,00 € par période de an », formulations incorrectes en français. La même infobulle est utilisée sur mobile.
- Attendu : « 49,00 € par mois » et « 490,00 € par an ».
- Preuve : Checkout Essentielle annuel : « Sous-total récurrent ... 490,00 € par période de an » ; mensuel : « 49,00 € par période de mois » ; Sur mesure mensuel : « 149,00 € par période de mois » (co-ess-A-desk.json, co-ess-M-desk.json, co-mes-M-desk.json ; capture shots/co-ess-M-desk.png)
- Recommandation : Dans Shopify > Paramètres > Langues > Modifier les traductions du checkout (français), traduire la chaîne « par période de {interval} » en « par {interval} » ; si ce n'est pas modifiable, vérifier le libellé d'intervalle du plan Appstle (« mois » / « an »).
- Preuve du contradicteur : Checkout Essentielle mensuel : « 49,00 € par période de mois » ; Essentielle annuel : « 490,00 € par période de an » ; Sur mesure mensuel : « 149,00 € par période de mois » ; Premium annuel : « 890,00 € par période de an » ; mobile : « Sous-total récurrent 49,00 € par période de mois » (capture lue).

### ACHAT-12 — Connexion lente : le bouton d'achat est actif ~25 s avant le bloc d'abonnement, un clic affiche une page d'erreur Shopify
- Zone : Parcours d'achat et page de paiement
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Sur une connexion émulée à 400 kbit/s et 400 ms de latence (mobile), le bouton « Ajouter au panier » apparaît actif à ~5-7 s alors que le bloc d'abonnement (Appstle) n'apparaît qu'après plus de 30 s. Un clic avant son chargement envoie l'ajout sans plan de vente et affiche une page d'erreur plein écran.
- Attendu : Bouton désactivé tant que le bloc d'abonnement n'est pas chargé, ou message clair.
- Preuve : Playwright CDP : timings commit 533 ms, h1 ~4,9 s, widget 29,4 s ; slow2.js : bouton enabled dès 6,7 s, widget absent jusqu'à 30,7 s ; slow3.js : clic -> POST /cart/add -> 422 et page « Un problème est survenu. ... Erreur panier: La variante peut seulement être achetée avec un forfait de vente. » ; panier vide ; capture shots/slow-click.png
- Recommandation : Dans le thème, désactiver le bouton d'achat (disabled) par défaut sur les produits d'abonnement et l'activer quand .appstle_sub_widget est présent ; ou précharger le script Appstle. Accord du propriétaire requis (thème en ligne).
- Preuve du contradicteur : Playwright mobile avec CDP. Fast 3G (1,6 Mbit/s, 150 ms) : btnAt 1,5 s, widAt 7 s ; clic à 1,3-1,4 s -> POST /cart/add 422, corps « Erreur panier: La variante peut seulement être achetée avec un forfait de vente. », panier vide. Slow 3G (400 kbit/s, 400 ms) : bouton à 5,3 s, bloc absent, clic -> 422 à 7 s. Sans limitation : btnAt 0,8 s, widAt 2,8 s.

### ACHAT-M2 — La mise en place peut être achetée seule (sans abonnement) : l'association offre + mise en place n'est imposée dans aucun sens
- Zone : Parcours d'achat et page de paiement
- Gravité : moyen | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : En complément d'ACHAT-06 (abonnement sans mise en place), le produit de mise en place s'ajoute et se paie seul : 290 € payés sans aucun abonnement d'hébergement ni de maintenance. Les trois mises en place sont en outre proposées comme produits autonomes avec un bouton « Ajouter » dans le catalogue de la boutique et dans « You may also like » du panier, sans lien avec une offre.
- Attendu : Une mise en place toujours associée à une offre (ajout automatique ou validation du panier), ou retrait des mises en place du catalogue public.
- Preuve : POST /cart/add.js {id:61143346938190, quantity:1} -> 200, cart total 29000 ; /checkout -> /checkouts/cn/<jeton>/fr-fr, résumé « Mise en place — ESSENTIELLE 290,00 € ; Total 290,00 € », sans ligne d'abonnement ni sous-total récurrent. Accueil boutique et /cart : « Ajouter Mise en place — ESSENTIELLE €290,00 », « Ajouter Mise en place — PREMIUM €590,00 », « Ajouter Mise en place — SUR MESURE (acompte) €1.690,00 ». /products/mise-en-place-essentielle.js : requires_selling_plan=false.
- Recommandation : Avec l'accord du propriétaire : sortir les 3 mises en place du catalogue et des recommandations (collection ou canaux de vente), et traiter le couplage avec ACHAT-06 par une règle de validation de panier ou un ajout automatique.

### SEO-01 — Pas de robots.txt ni de sitemap.xml sur juicecraft.fr
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Les deux fichiers répondent 404 (page d'erreur HTML de Netlify). Les moteurs n'ont ni consigne d'exploration ni plan du site, alors que la FAQ promet « plan du site » parmi les fondations techniques du référencement incluses dans les offres.
- Attendu : /robots.txt et /sitemap.xml en 200, le sitemap déclaré dans robots.txt.
- Preuve : curl https://juicecraft.fr/robots.txt -> HTTP/2 404 ; curl https://juicecraft.fr/sitemap.xml -> HTTP/2 404 ; idem sur sparkling-bubblegum-b2d478.netlify.app. Le dépôt ne contient que README.md, _headers et index.html.
- Recommandation : Ajouter à la racine du dépôt (publication = niveau 2). robots.txt :
User-agent: *
Allow: /

Sitemap: https://juicecraft.fr/sitemap.xml

sitemap.xml :
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://juicecraft.fr/</loc>
    <lastmod>2026-10-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>

Puis soumettre le sitemap dans Google Search Console (propriétaire du domaine requis).
- Preuve du contradicteur : curl -s -o /dev/null -w '%{http_code}' https://juicecraft.fr/robots.txt -> 404 (text/html) ; /sitemap.xml -> 404 ; https://sparkling-bubblegum-b2d478.netlify.app/robots.txt -> HTTP/2 404 ; /home/user/juicecraft-site ne contient que README.md, _headers, index.html ; texte FAQ lu : « Les fondations techniques du référencement (structure, balises, vitesse, plan du site) sont incluses ».

### SEO-03 — Aperçu de partage incomplet : pas d'og:image, d'og:url ni de balises Twitter
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Open Graph limité à type, locale, title et description. Sans image, les partages LinkedIn, WhatsApp, Facebook, Slack affichent une carte sans visuel, ce qui réduit le clic pour un studio de création de sites dont l'image est la vitrine. og:title (« Des sites qui ont du jus ») diffère du title (« Création de sites internet sur mesure ») : acceptable mais à garder volontairement.
- Attendu : og:url, og:image (1200x630), og:site_name, twitter:card.
- Preuve : Head de https://juicecraft.fr/ : seules les balises og:type, og:locale, og:title, og:description ; 0 occurrence de og:image, og:url, twitter:. L'image 1200x630 n'existe pas encore (https://juicecraft.fr/og.png -> 404).
- Recommandation : Créer une image 1200x630 (logo goutte + « Des sites qui ont du jus »), la déposer à /og-image.png puis ajouter dans le head :
<meta property="og:url" content="https://juicecraft.fr/">
<meta property="og:site_name" content="juicecraft">
<meta property="og:image" content="https://juicecraft.fr/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="juicecraft, studio de création de sites internet">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="juicecraft · Des sites qui ont du jus">
<meta name="twitter:description" content="Sites internet sur mesure, rapides et soignés pour les artisans, commerces, cabinets et entreprises.">
<meta name="twitter:image" content="https://juicecraft.fr/og-image.png">
- Preuve du contradicteur : Parsing Python de https://juicecraft.fr/ : meta og: = og:type, og:locale, og:title « juicecraft · Des sites qui ont du jus », og:description ; compteurs « twitter » = 0 ; curl https://juicecraft.fr/og.png -> 404.

### SEO-06 — Page 404 générique de Netlify, en anglais, sans retour vers le site
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Une URL inexistante affiche « Page not found / Looks like you've followed a broken link… » avec lang="en", sans lien vers l'accueil, et renvoie vers un guide de support Netlify : perte de visiteurs et image peu soignée. Le code 404 est correct.
- Attendu : Page 404.html en français, aux couleurs du site, avec lien vers l'accueil.
- Preuve : curl https://juicecraft.fr/zzz-inexistante -> HTTP/2 404, <html lang="en">, <title>Page not found</title>.
- Recommandation : Ajouter un fichier 404.html à la racine du dépôt (Netlify le sert automatiquement avec le code 404). Contenu minimal :
<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page introuvable · juicecraft</title></head><body><main><h1>Cette page n'existe pas ou a été déplacée.</h1><p>Retournez à <a href="/">l'accueil de juicecraft</a> ou <a href="/#contact">écrivez-nous</a>.</p></main></body></html>
- Preuve du contradicteur : curl https://juicecraft.fr/zzz-inexistante : <html lang="en">, <title>Page not found</title>, 3 621 octets, seul href = answers.netlify.com/... ; code 404.

### SEO-12 — « Réalisations », « Voir nos réalisations » et « Notre travail en images » désignent des concepts fictifs
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le menu, le bouton du hero, le titre de section et le pied de page parlent de « réalisations » et de « notre travail », alors que le texte de la section précise que ce sont des « concepts de démonstration, fictifs » (badge « Concept fictif »). Titre et ancre ne correspondent pas au contenu : un visiteur qui ne lit que le menu croit voir des clients réels (risque de pratique commerciale trompeuse).
- Attendu : Libellés alignés sur le contenu.
- Preuve : Menu : « Réalisations » (#realisations) ; hero : « Voir nos réalisations » ; h2 « Notre travail en images. » ; lede : « Notre portfolio se construit. Voici des concepts de démonstration, fictifs, qui montrent notre approche. » ; cartes marquées « CONCEPT FICTIF ».
- Recommandation : Renommer : menu « Concepts » (ou « Démonstrations »), bouton « Voir nos concepts », h2 « Nos concepts de démonstration. », et conserver l'id #realisations ou le renommer #concepts en mettant à jour les liens. Revenir à « Réalisations » quand des projets clients réels existent.
- Preuve du contradicteur : Texte visible : « Voir nos réalisations », « Réalisations » (x4), h2 « Notre travail en images. », « Notre portfolio se construit. Voici des concepts de démonstration, fictifs, qui montrent notre approche. », « Concept fictif » (x4).

### SEO-13 — Contradiction sur la maintenance entre l'offre et la FAQ
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le texte des offres dit que l'abonnement « couvre l'hébergement, la maintenance et l'assistance », tandis que la FAQ dit qu'« une maintenance peut être mise en place selon vos besoins » et la section « Maintenance possible » que « une intervention ultérieure reste possible » (laisse entendre une option à part). La boutique indique « Maintenance technique » (Essentielle), « Maintenance » (Premium), « Maintenance renforcée » (Sur mesure). Un client ne sait pas si la maintenance est incluse ou payante.
- Attendu : Un seul message : ce qui est inclus dans l'abonnement et ce qui est sur devis.
- Preuve : Section #offres : « L'abonnement couvre l'hébergement, la maintenance et l'assistance » ; FAQ « Que se passe-t-il après la mise en ligne ? » : « une maintenance peut être mise en place selon vos besoins » ; section #approche : « Maintenance possible — Une intervention ultérieure reste possible selon vos besoins ».
- Recommandation : Harmoniser, par exemple. FAQ : « Nous restons disponibles. L'abonnement inclut l'hébergement, la maintenance technique et l'assistance ; les évolutions importantes font l'objet d'un devis. » Titre de carte : « Maintenance incluse » au lieu de « Maintenance possible », et préciser le périmètre exact. À faire valider par le propriétaire (contenu contractuel).
- Preuve du contradicteur : Texte visible #offres : « L'abonnement couvre l'hébergement, la maintenance et l'assistance » ; FAQ : « Nous restons disponibles. Selon l'offre, un accompagnement après livraison est inclus, et une maintenance peut être mise en place selon vos besoins. » ; carte #approche : « Maintenance possible ».

### SEO-14 — Contenu des offres différent entre le site et la boutique, renvoi à des CGV et à un nombre de tours qui ne sont écrits nulle part
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : La boutique précise des limites et inclusions absentes du site : Essentielle « Jusqu'à 5 pages », « Hébergement », « Maintenance technique » ; Premium « Jusqu'à 10 pages », « Portfolio / galerie », « Assistance prioritaire » ; Sur mesure « Tout le contenu de Premium », « Intégrations externes », « Maintenance renforcée ». Le site liste d'autres éléments (« Design moderne et professionnel », « Mise en ligne »). Le client découvre les limites de pages après avoir cliqué. De plus la FAQ dit que le nombre de tours de modifications est « précisé dans l'offre et dans les CGV » : il n'apparaît ni dans les offres du site ou de la boutique, ni dans des CGV (page absente).
- Attendu : Mêmes inclusions et mêmes limites sur le site et sur la fiche produit ; nombre de tours indiqué.
- Preuve : Site : liste Essentielle = 5 puces sans nombre de pages. /products/essentielle.js description : « Jusqu'à 5 pages » ; /products.json premium : « Jusqu'à 10 pages ». FAQ « Puis-je demander des modifications ? » : « le nombre de tours inclus est précisé dans l'offre et dans les CGV ». /cgv -> 404.
- Recommandation : Choisir une source de vérité (la fiche produit est la plus complète) et reporter sur le site : « Jusqu'à 5 pages » (Essentielle), « Jusqu'à 10 pages » (Premium), hébergement et maintenance. Indiquer le nombre de tours de modifications (valeur à fournir par le propriétaire) ou reformuler la FAQ : « le nombre de tours inclus vous est communiqué avant toute commande ».
- Preuve du contradicteur : grep 'pages' dans le texte du site : aucun « Jusqu'à N pages » ; capture Playwright fiche Essentielle : « Création du site / Jusqu'à 5 pages / … / Maintenance technique » ; JSON-LD Premium : « Jusqu'à 10 pages » ; FAQ : « le nombre de tours inclus est précisé dans l'offre et dans les CGV ».

### SEO-M1 — Badge « Powered by Netlify » injecté sur le site en production (promotion d'un concurrent, en anglais)
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Le HTML servi par juicecraft.fr contient une balise script ajoutée par Netlify qui n'existe pas dans le dépôt, laquelle affiche en bas à droite de chaque visiteur un badge « Powered by Netlify » ouvrant une fenêtre « Build your own site with Netlify » (champ pour décrire le site à construire). Pour un studio dont le métier est de vendre des sites, cela renvoie le visiteur vers une plateforme tierce, en anglais, sur la page d'accueil, et se superpose à la zone des commandes du bas de page (à 1280x800 il touche le sélecteur « Élégant / Audacieux / Minimal »). Le poids de page de 200 132 octets annoncé par le premier audit inclut cette injection.
- Attendu : Aucun badge ou script tiers promotionnel injecté par l'hébergeur sur le site de la marque ; HTML servi identique au fichier du dépôt.
- Preuve : diff entre https://juicecraft.fr/ et /home/user/juicecraft-site/index.html : unique ligne ajoutée « <script async src="/.netlify/scripts/hud?variant=public" data-nf-variant="public" data-netlify-site-id="953a3a52-…" data-app-host="app.netlify.com"></script> » (200 132 octets servis contre 199 948 dans le dépôt) ; Playwright 1280x800 : iframe#nl-badge-frame title « Powered by Netlify » à x=1079, y=736, 201x64 px, capture montrant le badge au-dessus de « Minimal » ; https://juicecraft.fr/.netlify/scripts/hud?variant=public -> 200, en-tête « the badge and owner toolbar Netlify injects on published sites », textes « Build your own site with Netlify », « Hide this badge ». Même injection sur sparkling-bubblegum-b2d478.netlify.app.
- Recommandation : Dans la console Netlify (projet sparkling-bubblegum-b2d478), chercher le réglage qui désactive le badge ou la barre injectée sur le site publié (nom exact du réglage à vérifier dans l'interface ; aucune modification faite ici), puis recontrôler que le HTML servi ne contient plus /.netlify/scripts/hud. Réglage d'hébergement : niveau 2, accord du propriétaire requis.

### LEGAL-10 — Case « Envoyez-moi des nouvelles et des offres par e-mail » pré-cochée au paiement
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Sur la page de paiement Shopify, la case marketing (name marketing_opt_in) est cochée par défaut. Un bloc « Join our email list – Get exclusive deals and early access to new products. » (en anglais, avec champ e-mail) figure aussi en pied des fiches produits.
- Attendu : Pas de case de consentement pré-cochée pour la prospection par e-mail. Source CNIL : https://www.cnil.fr/fr/la-prospection-commerciale-par-courrier-electronique : pour les consommateurs, consentement préalable par acte positif, case non pré-cochée ; pour les professionnels, pas de consentement systématique mais information et opposition simple. Le statut des acheteurs (particuliers ou professionnels) est à faire confirmer par le propriétaire.
- Preuve : Playwright sur /checkouts/cn/…/fr-fr : input[type=checkbox] name="marketing_opt_in" id="marketing_opt_in" checked=true, libellé « Envoyez-moi des nouvelles et des offres par e-mail ». Fiche produit : texte « Join our email list / Get exclusive deals and early access to new products. / E-mail ».
- Recommandation : Après accord du propriétaire (réglage Shopify, Paramètres, Paiement, Marketing : décocher par défaut ; traduire ou retirer le bloc newsletter en anglais ou y joindre une information). Niveau 2.
- Preuve du contradicteur : Playwright /checkouts/cn/…/fr-fr : input[name=marketing_opt_in] checked=true, libellé « Envoyez-moi des nouvelles et des offres par e-mail » (2 exécutions). Bloc « Join our email list / Get exclusive deals and early access to new products. » dans prod_essentielle.txt lignes 71-73. CNIL https://www.cnil.fr/fr/la-prospection-commerciale-par-courrier-electronique relue via WebFetch.

### LEGAL-11 — Cookies Shopify d'analyse et de marketing déposés dès la première visite, sans bandeau constaté
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : faible
- Constat : Au premier chargement de la boutique (contexte vierge, sans action), Shopify dépose _shopify_analytics et _shopify_marketing (365 jours), plus _shopify_essential, localization, cart_currency et _shop_app_essential (.shop.app). Aucun bandeau de consentement n'est visible (le texte de la page ne contient pas « cookie » ni « consent »). sessionStorage contient consentHeader, appstleSubscriptionConfig, wpm-ri-*, _shs_state ; la fiche produit charge aussi PayPal (localStorage __paypal…) et des scripts depuis ajax.googleapis.com, cdn.jsdelivr.net, cdnjs.cloudflare.com et subscription-admin.appstle.com. Le contrôle a été fait depuis un réseau qui n'est pas en France : le comportement pour un visiteur français n'est pas prouvé.
- Attendu : Les traceurs non essentiels (mesure d'audience hors exemption, marketing) ne se déposent qu'après consentement (article 82 de la loi Informatique et Libertés ; lignes directrices et recommandation CNIL : https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies/comment-mettre-mon-site-web-en-conformite). Le classement exact de chaque cookie Shopify et la réglementation applicable au regard du réglage Shopify « Confidentialité des clients » : à faire valider.
- Preuve : Playwright https://juicecraft-store.myshopify.com/ : cookies [localization 365d, cart_currency 14d, _shopify_essential 365d, _shopify_analytics 365d, _shopify_marketing 365d, _shop_app_essential@.shop.app 365d] ; sessionStorage consentHeader = « 3.AMPS_US_f_f_BEHZ*oHRSTKEb5JXth3WRQ » ; innerText sans « cookie » ; hôtes : shop.app, monorail-edge.shopifysvc.com, otlp-http-production.shopifysvc.com, subscription-admin.appstle.com, www.paypal.com, www.paypalobjects.com, ajax.googleapis.com, cdn.jsdelivr.net, cdnjs.cloudflare.com, extensions.shopifycdn.com.
- Recommandation : Le propriétaire vérifie dans Shopify (Paramètres, Confidentialité des clients) que la bannière de consentement est active pour l'UE/France, puis la teste depuis une connexion française. Niveau 2 (réglage).
- Preuve du contradicteur : Playwright https://juicecraft-store.myshopify.com/ : cookies [localization, cart_currency, _shopify_essential, _shopify_analytics (365 j), _shopify_marketing (365 j), _shop_app_essential@.shop.app] ; sessionStorage consentHeader = '3.AMPS_US_f_f_rXU0bxgbTvyDy6ieebj16Q' ; innerText sans 'cookie|consent' (false). graphql_query privacySettings { banner } = 'Access denied… read_privacy_settings'.

### LEGAL-13 — Bloc « Maintenance possible » : promesses (sauvegardes quotidiennes, surveillance, mises à jour régulières) et « Activez, désactivez » incompatibles avec l'abonnement affiché
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : La section « Accompagnement » affiche « Maintenance possible : Une intervention ultérieure reste possible selon vos besoins : mises à jour, sauvegardes, évolutions. Activez, désactivez, c'est vous qui choisissez. », avec « Mises à jour : Régulières », « Sauvegardes : Quotidiennes », « Surveillance : Site disponible », « Évolutions : Sur demande ». Or la section Offres dit que l'abonnement « couvre l'hébergement, la maintenance et l'assistance » avec engagement de 12 mois, donc la maintenance n'est ni optionnelle ni désactivable. La réalité technique (fréquence des sauvegardes, outil de surveillance, mises à jour) n'a pu être contrôlée.
- Attendu : Chaque promesse correspond à une prestation réellement fournie, mesurable et cohérente avec le contrat. Le propriétaire confirme sauvegardes quotidiennes, surveillance, périodicité des mises à jour et sa possibilité d'activer ou désactiver la maintenance ; sinon reformuler.
- Preuve : innerText du site : « Maintenance possible / Une intervention ultérieure reste possible selon vos besoins : mises à jour, sauvegardes, évolutions. Activez, désactivez, c'est vous qui choisissez. / Mises à jour Régulières / Sauvegardes Quotidiennes / Surveillance Site disponible / Évolutions Sur demande » ; section Offres : « L'abonnement couvre l'hébergement, la maintenance et l'assistance, avec 12 mois d'engagement ».
- Recommandation : Le propriétaire confirme la réalité de chaque ligne ; sinon proposer au niveau 2 une reformulation (ex. retirer « Activez, désactivez » et préciser la fréquence réelle, ou « sauvegardes régulières » si elles ne sont pas quotidiennes).
- Preuve du contradicteur : site_text.txt lignes 171-181 : 'Maintenance possible / … Activez, désactivez, c'est vous qui choisissez. / Mises à jour Régulières / Sauvegardes Quotidiennes / Surveillance Site disponible' ; ligne 367 : 'L'abonnement couvre l'hébergement, la maintenance et l'assistance, avec 12 mois d'engagement' ; ligne 443 (FAQ) : 'une maintenance peut être mise en place selon vos besoins'.

### LEGAL-14 — Contenus des offres différents entre le site et la boutique ; promesses à confirmer (pages, assistance prioritaire, 2 h par mois)
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Boutique Essentielle : « Jusqu'à 5 pages », « Hébergement », « Maintenance technique », « Corrections et petites modifications », « Assistance » ; le site liste « Design moderne et professionnel, Responsive, Formulaire de contact, Bases SEO, Mise en ligne » sans pages, hébergement ni maintenance dans la carte. Boutique Premium : « Jusqu'à 10 pages », « Modifications régulières », « Maintenance », « Assistance prioritaire », « Portfolio / galerie » ; le site écrit « Accompagnement après livraison » sans pages ni assistance prioritaire. Sur mesure : « 2 h par mois, au-delà sur devis » sur les deux, « Maintenance renforcée » seulement sur la boutique. Les limites (nombre de pages, définition d'« assistance prioritaire », « modifications régulières », délai de réponse) ne sont pas chiffrées.
- Attendu : Mêmes engagements, chiffrés et vérifiables, sur le site, la fiche produit et les CGV ; le propriétaire confirme qu'il tient chaque promesse (5 et 10 pages, assistance prioritaire avec délai, 2 h/mois, « modifications régulières »).
- Preuve : /products/essentielle.js description : « Jusqu'à 5 pages … Hébergement … Maintenance technique … Assistance » ; /products/%F0%9F%94%B5-premium-%E2%AD%90.js : « Jusqu'à 10 pages … Modifications régulières … Maintenance … Assistance prioritaire » ; /products/sur-mesure.js : « Maintenance renforcée … Modifications incluses : 2 h par mois, au-delà sur devis ». Cartes d'offres du site (innerText section Offres).
- Recommandation : Le propriétaire confirme les promesses et harmonise les textes (descriptions Shopify : niveau 1 après confirmation ; texte du site : niveau 2). Ajouter des limites chiffrées (délai de réponse de l'assistance, nombre de tours de corrections) à valider.
- Preuve du contradicteur : /products/essentielle.js : 'Jusqu'à 5 pages … Hébergement … Maintenance technique … Assistance' ; /products/%F0%9F%94%B5-premium-%E2%AD%90.js : 'Jusqu'à 10 pages … Modifications régulières … Maintenance … Assistance prioritaire' ; /products/sur-mesure.js : 'Maintenance renforcée … 2 h par mois'. site_text.txt lignes 367-406 : cartes d'offres sans nombre de pages ni assistance prioritaire.

### LEGAL-15 — Le site promet un délai et un prix « confirmés avant tout paiement », mais la boutique permet de payer sans échange préalable
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le site affirme « Délai communiqué avant tout engagement » et « Prix et contenu confirmés avant tout paiement » ; la FAQ dit « Le délai est communiqué lors de l'échange initial ». Les boutons « Choisir cette offre » mènent directement à la fiche produit où l'achat d'un abonnement, de la mise en place et de l'acompte sur mesure (1 690 €) est possible sans devis ni échange (paiement atteint avec 339,00 € au panier). Aucun délai de réalisation n'est indiqué sur la boutique.
- Attendu : Cohérence entre la promesse du site et le parcours réel d'achat ; indication du délai de livraison ou d'exécution avant la commande (information précontractuelle de L221-5 : à faire valider).
- Preuve : Site : « Délai communiqué avant tout engagement / Prix et contenu confirmés avant tout paiement » ; liens des boutons : https://juicecraft-store.myshopify.com/products/essentielle, …/%F0%9F%94%B5-premium-%E2%AD%90, …/sur-mesure ; Playwright : cart/add.js 200 puis /checkout atteint avec 339,00 € sans devis. Sur mesure : « Acompte de mise en place obligatoire (1 690 € TTC…) ».
- Recommandation : Le propriétaire choisit : soit reformuler ces deux promesses (ex. « délai indiqué dans la confirmation de commande »), soit conditionner l'achat à un échange. Niveau 2 pour le site.
- Preuve du contradicteur : home.html ligne 1806 const SHOP = {essentielle, premium, mesure → URLs juicecraft-store.myshopify.com/products/…} et ligne 1809 'a.href = u' ; site_text.txt lignes 451-452 'Délai communiqué avant tout engagement / Prix et contenu confirmés avant tout paiement' ; grep 'délai|livraison' sur prod_*.txt, cart.txt = 0 ; checkout atteint avec 339,00 € et 1 839,00 €.

### LEGAL-M1 — Prix de base affichés incohérents dans la boutique : Premium (89 €) et Sur mesure (149 €) apparaissent moins chers qu'Essentielle (490 €), sans « TTC » ni période
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Le prix de base Shopify d'Essentielle est le prix annuel (490 €), mais ceux de Premium et Sur mesure sont les prix mensuels (89 € et 149 €), contrairement à la grille de référence où le prix de base est le prix annuel (890 € et 1 490 €). Le catalogue, l'en-tête des fiches et les blocs « You may also like » affichent donc €490,00 / €89,00 / €149,00 sans « TTC » ni « /mois » ni « /an ». Un visiteur voit Premium (l'offre recommandée) moins chère qu'Essentielle. Le montant réellement facturé est correct, car l'achat sans forfait d'abonnement est refusé (422).
- Attendu : Prix affichés cohérents entre les trois offres et avec le site (49/89/149 €/mois TTC ou 490/890/1 490 € TTC par an), avec la période et la mention TTC, pour ne pas induire en erreur sur le prix (Code de la consommation L112-1, à faire valider).
- Preuve : curl https://juicecraft-store.myshopify.com/collections/all (HTML) : prix visibles 'ESSENTIELLE €490,00', 'PREMIUM €89,00', 'SUR MESURE €149,00'. /products/{essentielle,premium,sur-mesure}.js : price = 49000, 8900, 14900 ; allocations annuelles 49000, 89000, 149000. Playwright prod_premium.txt : '€89,00€89,00' en tête de fiche. POST /cart/add.js sans selling_plan sur les 3 variantes = 422.
- Recommandation : Le propriétaire décide d'aligner le prix de base des produits Premium et Sur mesure sur le prix annuel (890 € et 1 490 €) ou de masquer le prix dans les cartes, et d'ajouter TTC et période dans les titres ou descriptions. Changement de prix ou de produit : accord explicite requis (niveau 2). À contrôler avec l'audit des prix et de l'achat.

### LEGAL-M2 — « Mise en place obligatoire » annoncée sur les fiches mais non imposée par le panier : l'abonnement s'achète seul
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : moyenne
- Constat : Les fiches disent « Mise en place obligatoire (290 € TTC…) : ajoutez-la au panier avant de payer » et le site « Prix et contenu confirmés avant tout paiement », mais le panier accepte l'abonnement seul, sans les frais de mise en place. Seul l'ajout au panier a été testé : le passage du paiement avec l'abonnement seul n'a pas été essayé. Le mot « obligatoire » est donc une consigne de lecture, pas une règle du panier, avec un manque à gagner possible de 290 € à 1 690 € par commande et un contenu de commande qui peut différer de la promesse.
- Attendu : Soit le panier impose réellement la mise en place (offre groupée ou règle de panier), soit le texte ne dit pas « obligatoire » ; l'allégation doit correspondre à ce que la boutique applique.
- Preuve : POST https://juicecraft-store.myshopify.com/cart/add.js (curl, panier jetable) avec {id:61108150141262, selling_plan:692930576718} = 200, final_line_price 49000 ; idem {id:61108252180814, selling_plan:692930969934} = 89000 et {id:61108309360974, selling_plan:692930838862} = 149000, sans produit de mise en place. Texte : /products/essentielle.js description 'Mise en place obligatoire (290 € TTC, payée une seule fois) : ajoutez-la au panier avant de payer'.
- Recommandation : Le propriétaire choisit la règle (offre groupée, règle de panier, ou reformulation) et fait tester un parcours d'achat réel avec son accord. Modification du fonctionnement d'achat : niveau 2. À recouper avec l'audit de l'achat.

### ACCES-01 — Animations automatiques infinies sans possibilité de pause
- Zone : Accessibilité, performance et robustesse
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Plusieurs animations durent plus de 5 s sans fin et sans bouton de pause : mot rotatif du titre (changement toutes les 2,6 s), bascule automatique des 3 styles de la démo du héros (toutes les 3,6 s), marquee défilant sous le héros, bulles WebGL du héros en boucle, plus des animations CSS infinies (document.getAnimations() : 25 premières, presque toutes Infinity). Seule la préférence système prefers-reduced-motion les coupe.
- Attendu : WCAG 2.2.2 (niveau A) : tout contenu qui bouge automatiquement plus de 5 s doit pouvoir être mis en pause, arrêté ou masqué par l'utilisateur.
- Preuve : Code source : setInterval(..., 2600) pour la rotation du mot, setInterval(..., 3600) pour la démo, requestAnimationFrame pour le marquee et le canvas WebGL. Recherche des boutons dont le libellé contient pause/stop/arrêt : liste vide. Mesure : 25 animations en cours, iterations=Infinity.
- Recommandation : Ajouter un petit bouton « Mettre en pause les animations » (aria-pressed) visible dans l'en-tête ou près du héros ; au clic, appliquer la même logique que reduced-motion (clearInterval des deux timers, arrêt du marquee et du rendu WebGL, animation-play-state: paused sur les animations CSS infinies) et mémoriser le choix. À défaut, arrêter automatiquement la rotation du mot, la démo et le marquee après 5 s.
- Preuve du contradicteur : Lecture de https://juicecraft.fr/ : ligne 1490 setInterval(rotate, 2600), ligne 1491 setInterval(press, 7000), ligne 1520 setInterval(... 3600) pour la bascule des styles de démo, plus setInterval(addOne,1700) et setInterval(bookTick,1300). Recherche insensible à la casse de « pause » dans le HTML : aucun résultat. En reduced-motion (Playwright reducedMotion=reduce, 12 s) : titre figé « Votre commerce… », 0 animation CSS infinie en cours, #cur absent.

### ACCES-03 — Légende de la démo du héros illisible sur la bulle colorée
- Zone : Accessibilité, performance et robustesse
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : La phrase « Même contenu, trois identités. Choisissez la vôtre. » (mono 12 px, gris #65616c) est posée sur la bulle orange/rose/violette du héros et devient en grande partie illisible ; sur ordinateur la fin de la phrase se confond avec la bulle. Sur mobile, la phrase passe sur 2 lignes avec le même problème sur la bulle. Dans une moindre mesure, la fin des mots « soignés » du paragraphe d'introduction (ordinateur) passe sur le bord de la bulle.
- Attendu : Contraste texte/fond d'au moins 4,5:1 pour du texte de 12 px (WCAG 1.4.3).
- Preuve : Échantillon du fond derrière .demo-cap (texte rendu transparent, capture, ratio avec #65616c) : ordinateur 98 % des pixels < 4,5:1, médiane 1,79:1, minimum 1,0:1 ; mobile 40 % < 4,5:1, médiane 4,56:1, minimum 1,0:1. Paragraphe .lede (#65616c, 18,7 px) : médiane 5,0:1 mais 8 % des pixels < 4,5:1 sur ordinateur. Captures sec-desktop-top.png et demo-m-all.png.
- Recommandation : Soit placer .demo-cap sur une pastille opaque (background: rgba(242,242,239,.92); padding: 4px 10px; border-radius: 999px; color: #3b3842), soit la remonter au-dessus du commutateur de style en dehors de la zone de la bulle ; ne pas laisser le texte courant passer sous la bulle (z-index de la bulle sous le texte avec un fond pastille).
- Preuve du contradicteur : Capture https://juicecraft.fr/ 1440x900 (/tmp/audit-acces-contra/hero-desktop.png) : « Même contenu, trois identités. Choisissez la vôtre. » en partie confondue avec la bulle orange/violette. Capture mobile 390x844 (mob-hero-1.png) : « identités. Choisissez la » sur le bord violet de la bulle. Mesure par pixel du fond derrière .demo-cap (texte rendu transparent) : ordinateur médiane 3,77:1, minimum 1,0:1 ; mobile médiane 5,1:1, minimum 1,03:1. Sans WebGL (bulle absente) la légende est lisible.

### ACCES-04 — Titres des étapes de la méthode non actives trop pâles (2,34:1)
- Zone : Accessibilité, performance et robustesse
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Dans la section « De l'idée à la mise en ligne », les titres des étapes pas encore atteintes (Conception, Création, Validation, Mise en ligne dans l'état statique ; en défilement normal, les étapes à venir) sont en #a29ea7 sur #f2f2ef, soit 2,34:1, sous le seuil de 3:1 exigé pour un grand texte (38,4 px gras sur ordinateur, 25,6 px sur mobile).
- Attendu : Au moins 3:1 pour du grand texte, même pour un état « à venir » (le texte n'entre pas dans l'exception des composants inactifs).
- Preuve : axe-core color-contrast : « .step:nth-child(3) > h3 ... contrast of 2.34 (foreground color: #a29ea7, background color: #f2f2ef, font size: 28.8pt, font weight: bold). Expected 3:1 » ; mêmes valeurs pour .step:nth-child(4), (5), (6) ; reproduit sur ordinateur et mobile.
- Recommandation : Foncer la couleur des étapes à venir à #7a7680 ou plus foncé (contraste ≈ 4,1:1 sur #f2f2ef) ; si l'effet d'atténuation doit rester, le garder pour l'indicateur (pastille et trait) et laisser le titre à au moins #77737d.
- Preuve du contradicteur : Playwright + axe-core 4.14.0 (runOnly color-contrast) sur https://juicecraft.fr/ : « .step:nth-child(3|4|5|6) > h3 : 2.34 (foreground #a29ea7, background #f2f2ef, 28.8pt bold) Expected 3:1 » (ordinateur) et 19.2pt (mobile). CSS source : « .step:not(.on) h3{color:#A29EA7} » ; la classe .on est ajoutée par le script de défilement (stepLis.forEach ... s.classList.toggle("on", on)).

### ACCES-M1 — Le badge Netlify ouvre une carte qui invite les visiteurs à créer leur site avec un constructeur IA
- Zone : Accessibilité, performance et robustesse
- Gravité : moyen | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Un clic sur le badge « Powered by Netlify » ouvre une carte « Build your own site with Netlify — Describe what you want, and an AI agent designs, builds and deploys it in minutes. », avec un champ de description et un lien « Drop a site you already have », qui envoient le visiteur vers app.netlify.com. Sur le site d'un studio dont le métier est de créer des sites (offres de 49 à 149 € par mois), c'est une promotion directe d'une alternative pour ses propres prospects, sans rapport avec la marque juicecraft. La cause est un réglage Netlify par projet, pas le code du site.
- Attendu : Aucun message promotionnel tiers sur la page d'accueil d'un site commercial, en particulier un message qui détourne vers un service concurrent.
- Preuve : Playwright : clic sur #nl-badge dans l'iframe #nl-badge-frame de https://juicecraft.fr/ (rien saisi, rien envoyé) : texte de #nl-card = « Build your own site with Netlify | Describe what you want, and an AI agent designs, builds and deploys it in minutes. | OR | Drop a site you already have | Hide this badge » ; form.nl-prompt action = https://app.netlify.com/start. Script lu sur https://juicecraft.fr/.netlify/scripts/hud?variant=public (« the badge and owner toolbar Netlify injects on published sites »). Documentation https://docs.netlify.com/manage/projects/powered-by-netlify-badge/ : réglage « Project configuration > General > Powered by Netlify badge », activé par défaut pour les projets Free créés à partir du 19 août 2026, désactivable sans redéploiement.
- Recommandation : Avec l'accord du propriétaire, désactiver l'interrupteur « Powered by Netlify badge » dans Netlify (projet sparkling-bubblegum-b2d478, Project configuration > General), puis vérifier que la balise <script ... /.netlify/scripts/hud?variant=public> et l'iframe #nl-badge-frame ont disparu du HTML servi. Une fois fait, ACCES-02 est résolu par la même action.

### INFRA-01 — Aucune politique DMARC : le domaine peut être usurpé par e-mail
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Aucun enregistrement DMARC n'existe pour juicecraft.fr. Le SPF est strict (-all) et seul le DKIM n'a pas pu être confirmé (voir non_verifie), mais sans DMARC les destinataires n'ont aucune consigne ni aucun rapport sur les messages qui usurpent @juicecraft.fr.
- Attendu : Un enregistrement TXT _dmarc.juicecraft.fr valide, au minimum en p=none avec adresse de rapports (rua).
- Preuve : https://dns.google/resolve?name=_dmarc.juicecraft.fr&type=TXT -> Status 3 (NXDOMAIN, aucune réponse) ; https://cloudflare-dns.com/dns-query?name=_dmarc.juicecraft.fr&type=TXT (accept: application/dns-json) -> Status 3. Constaté le 9-10 octobre 2026.
- Recommandation : Après validation du propriétaire, ajouter chez OVH (zone DNS) un TXT : nom _dmarc, valeur exacte `v=DMARC1; p=none; rua=mailto:<adresse de rapports à choisir par le propriétaire>; fo=1` (adresse de rapports à confirmer, idéalement une boîte dédiée car les rapports sont nombreux). Observer les rapports 2 à 4 semaines, vérifier que SPF et DKIM sont alignés pour tous les expéditeurs légitimes (OVH, Shopify, Appstle...), puis passer à p=quarantine puis p=reject. Ne pas passer directement à p=reject.
- Preuve du contradicteur : https://dns.google/resolve?name=_dmarc.juicecraft.fr&type=TXT -> Status 3 (NXDOMAIN, SOA dns200.anycast.me. tech.ovh.net. 2091582533) ; https://cloudflare-dns.com/dns-query?name=_dmarc.juicecraft.fr&type=TXT (accept: application/dns-json) -> Status 3. Relevé le 10 octobre 2026.

### INFRA-02 — Polices chargées depuis Google Fonts (adresse IP des visiteurs transmise à Google)
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Chaque visite déclenche des requêtes vers fonts.googleapis.com et fonts.gstatic.com, avant tout consentement, ce qui transmet l'adresse IP du visiteur à un tiers. Cela contredit le profil d'un site sans cookie ni traceur et ajoute des connexions externes (performance).
- Attendu : Polices servies depuis juicecraft.fr (auto-hébergées) ou aucune ressource tierce non nécessaire.
- Preuve : Playwright/Chromium, chargement de https://juicecraft.fr/ : requêtes GET https://fonts.googleapis.com/css2?family=Mona+Sans:wdth,wght@75..125,200..900&family=Instrument+Sans... puis 5 fichiers https://fonts.gstatic.com/s/{instrumentsans,geistmono,monasans,instrumentserif x2}/...woff2. Le HTML contient les liens vers fonts.googleapis.com et fonts.gstatic.com (preconnect).
- Recommandation : Télécharger les familles Mona Sans, Instrument Sans, Instrument Serif et Geist Mono au format woff2, les déposer dans le dépôt (par exemple /fonts/), les déclarer par @font-face (font-display: swap) et supprimer les balises <link> vers Google. Des fichiers MonaSans.woff2 et GeistMono.woff2 existent déjà dans /home/user/juicecraft/logo/_src/ (à vérifier : variantes de graisse/largeur utilisées). Le correctif technique exige l'accord du propriétaire pour la publication ; l'appréciation juridique (RGPD, politique de confidentialité) relève du niveau 3 et n'a pas été évaluée ici.
- Preuve du contradicteur : Playwright, chargement de https://juicecraft.fr/ (networkidle) : hôtes contactés = ['juicecraft.fr','fonts.googleapis.com','fonts.gstatic.com'] ; cookies = [] ; grep dans /home/user/juicecraft-site/index.html : href="https://fonts.googleapis.com/css2?family=Mona+Sans...", href="https://fonts.gstatic.com", href="https://fonts.googleapis.com".

### INFRA-03 — Badge « Powered by Netlify » injecté et visible sur le site, absent du dépôt
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Netlify ajoute à la fin de la page (après </html>) un script qui affiche en bas à droite un bouton « Powered by Netlify » (iframe fixe, z-index maximal) qui invite les visiteurs à créer leur propre site. Il ne figure pas dans le dépôt, affiche une marque tierce sur le site d'un studio de création de sites, ajoute une requête de 34 481 octets (demandée 2 fois lors du chargement) et recouvre une partie du contenu. Aucun risque vie privée n'a été constaté (voir controles_ok).
- Attendu : HTML publié identique au dépôt, sans élément tiers non voulu (à confirmer avec le propriétaire s'il souhaite conserver le badge).
- Preuve : Ligne 1887 du HTML publié : <script async src="/.netlify/scripts/hud?variant=public" data-nf-variant="public" data-netlify-site-id="953a3a52-b9bb-46b6-91b3-4c35e0eb92d4" data-app-host="app.netlify.com"></script>, absente de /home/user/juicecraft-site/index.html. Capture Playwright (1280x800) : bouton « Powered by Netlify » visible en bas à droite (iframe #nl-badge-frame, 201x64 px à x=1079, y=736). Requêtes du script : 2 GET /.netlify/scripts/hud?variant=public. Doc officielle Netlify : « In the Netlify UI, go to your project and select Project configuration > General > Powered by Netlify badge » puis activer/désactiver, « The change takes effect on the next request. You don't need to redeploy » ; « on by default for projects on Free plans created on or after August 19, 2026 » (https://docs.netlify.com/manage/projects/powered-by-netlify-badge/ ; changelog https://www.netlify.com/changelog/2026-08-19-pre-launch-toolbar-and-powered-by-netlify-badge/). Le projet date du 9 octobre 2026, ce qui concorde avec un plan Free (déduction, plan non vérifié).
- Recommandation : Si le propriétaire ne veut pas du badge : dans l'interface Netlify, Project configuration > General > Powered by Netlify badge > désactiver > Save (effet immédiat, sans redéploiement, sans modifier le dépôt). Ne pas tenter de le masquer par CSS ou en retirant le script : ce serait contourné ou instable. Après le changement, relire le HTML publié (curl) pour confirmer la disparition de la ligne 1887.
- Preuve du contradicteur : curl -H 'accept-encoding: identity' https://juicecraft.fr/ (200 132 octets) ; diff avec /home/user/juicecraft-site/index.html : seule différence = ligne 1887 `<script async src="/.netlify/scripts/hud?variant=public" ... data-netlify-site-id="953a3a52-...">`. Playwright : #nl-badge-frame {x:1079,y:736,w:201,h:64}. Script hud.js : 34 481 octets, 0 occurrence de fetch/XMLHttpRequest/sendBeacon/document.cookie. WebFetch https://docs.netlify.com/manage/projects/powered-by-netlify-badge/ : « on by default for projects on Free plans created on or after August 19, 2026 » ; « You don't need to redeploy ».

### INFRA-05 — Échec d'envoi du formulaire sans autre moyen de contact sur le site
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : moyen | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Le formulaire est le seul canal de contact : aucune adresse e-mail ni téléphone n'apparaît dans le HTML. En cas d'échec (réseau, quota Web3Forms dépassé, service indisponible), le message affiché invite seulement à réessayer, sans alternative, et le fetch n'a pas de délai maximal. Un prospect (notamment pour l'offre sur mesure sur devis) peut être perdu sans que le propriétaire le sache.
- Attendu : Message d'erreur proposant une alternative (adresse de contact) et envoi bloqué avec un délai maximal.
- Preuve : index.html ligne ~1860 : alertBox.textContent = "La demande n'est pas partie. Vérifiez votre connexion et réessayez dans un instant." ; grep des adresses e-mail dans index.html : seulement camille@entreprise.fr et nom@domaine.fr (exemples) ; aucun tel: ni numéro. fetch("https://api.web3forms.com/submit", ...) sans AbortController.
- Recommandation : Remplacer le message par : « La demande n'est pas partie. Réessayez dans un instant ou écrivez-nous directement à <adresse de contact du propriétaire>. » (adresse à fournir et valider par le propriétaire ; ne pas utiliser l'adresse personnelle sans accord) et ajouter un délai maximal de 15 s au fetch (AbortController). Publication soumise à accord.
- Preuve du contradicteur : grep -n sur /home/user/juicecraft-site/index.html : adresses e-mail = camille@entreprise.fr (l.1221) et nom@domaine.fr (l.1830) seulement ; grep -c 'tel:' = 0 ; l.1856 alertBox.textContent = "La demande n'est pas partie. Vérifiez votre connexion et réessayez dans un instant." ; grep AbortController = aucun résultat.

### PRIX-05 — Anciens masters et captures avec « Sur devis » et « Devis détaillé avant tout paiement » encore livrés
- Zone : Prix, offres et cohérence des contenus
- Gravité : moyen | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Le dossier livrables/masters/ contient les masters 30 s du 8 octobre (16:9 et 9:16) qui affichent « Sur devis » sur les trois cartes d'offres et « Devis détaillé avant tout paiement. » ; une capture de travail ancienne video/shots/site.html contient aussi « Sur devis » et « devis détaillé ». Ils portent les mêmes noms de fichier que les versions à jour (juicecraft_pub_30s_*_master.mp4) mais un contenu et une taille différents (131 918 416 octets contre 132 047 959). Risque de diffuser par erreur l'ancien discours. La note de cues30.json et patch30.py citent aussi l'ancienne ligne (usage interne).
- Attendu : Seuls les fichiers à jour sont dans les livrables ; les anciens sont archivés ou clairement nommés.
- Preuve : ffmpeg -ss 23.8 sur /home/user/juicecraft/livrables/masters/juicecraft_pub_30s_16x9_master.mp4 (/tmp/audit-prix/old_133907.png) et ..._9x16_master.mp4 (old9.png) : « Sur devis », « Devis détaillé avant tout paiement. » ; ls -la : masters/ datés 2026-10-08 23:39 et 23:57, versions à jour du 2026-10-09 16:35 et 16:54 ; grep video/shots/site.html.
- Recommandation : Déplacer livrables/masters/juicecraft_pub_30s_*_master.mp4 vers un dossier d'archives nommé « ancien-prix-NE-PAS-DIFFUSER » (ou supprimer, après accord) et remplacer par les masters à jour. Les vidéos 15 s (juicecraft_pub_16x9.mp4 et 9x16) ne contiennent pas d'offre ni de prix.
- Preuve du contradicteur : ffmpeg -ss 23.8 sur livrables/masters/juicecraft_pub_30s_16x9_master.mp4 (old16_23.8.png) et ..._9x16_master.mp4 (old9_23.8.png) : « Sur devis » x3 et « Devis détaillé avant tout paiement. » ; ls -la : masters/ 131 918 416 et 132 142 697 octets (8 oct. 23:39 et 23:57) contre 132 047 959 et 132 279 855 octets pour les masters du dossier parent ; grep -il « Devis détaillé » video/shots/site.html patch30.py cues30.json video30.bak_prix.html : présents.

### ACHAT-10 — Textes restés en anglais dans la boutique et page 404
- Zone : Parcours d'achat et page de paiement
- Gravité : moyen | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Titre du panier « Cart », « You may also like », « View all », bouton du formulaire de contact « Submit », bloc pied de page « Join our email list / Get exclusive deals and early access to new products. » sur toutes les pages, et page 404 « Page not found / Continue shopping / Discover something new ». La fenêtre de résiliation est aussi en anglais (voir ACHAT-01).
- Attendu : Tout en français.
- Preuve : pages.js (ordinateur et mobile) : home, /collections/all, /cart, /pages/contact, /policies/refund-policy (404) ; textes relevés : « Join our email list », « You may also like », « View all », « Submit », « Page not found » ; captures shots/pg-cart-desk.png et shots/pg-contact-desk.png
- Recommandation : Dans l'éditeur du thème (Personnaliser > Paramètres des sections) : remplacer par « Inscrivez-vous à notre liste e-mail », « Vous aimerez aussi », « Tout voir », « Envoyer », « Page introuvable », « Continuer vos achats », « Découvrir de nouveaux produits » ; si le bloc newsletter n'est pas utilisé, le retirer (sinon case de consentement à prévoir).
- Preuve du contradicteur : Texte de /cart (Essentielle + mise en place) : « Cart 2 ... You may also like View all ... » ; pied de page de l'accueil boutique et de /policies/privacy-policy : « Join our email list Get exclusive deals and early access to new products. » ; curl /pages/contact : « Submit » présent, « Envoyer » absent ; curl /policies/refund-policy (404) : <h1>Page not found</h1>, « Continue shopping », « Discover something new ».

### ACHAT-11 — Prix sans périodicité ni « TTC » sur fiche, panier et paiement ; formats de montants différents entre boutique et paiement
- Zone : Parcours d'achat et page de paiement
- Gravité : moyen | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Fiche produit et panier affichent « €49,00 » sans « /mois » ni « TTC » ; seul le libellé du plan indique la périodicité. Le format varie : boutique « €1.490,00 » et « €339,00 EUR » (symbole avant, point des milliers) contre paiement « 1 839,00 € » (convention française). Le panier affiche « L'expédition est calculée lors du paiement » alors qu'il n'y a pas de livraison.
- Attendu : « 49 € TTC / mois », « 490 € TTC / an », format français « 1 490,00 € » partout, pas de mention d'expédition.
- Preuve : Fiches produit : prix « €49,00 » (capture shots/essentielle-Mensuel-desk-product.png) ; panier : « Total estimé €339,00 EUR | Droits de douane et taxes inclus. L'expédition est calculée lors du paiement » ; checkout : « 339,00 € »
- Recommandation : Paramètres > Général > Format de devise : HTML sans devise « {{amount_with_comma_separator}} € ». Ajouter « /mois TTC » / « /an TTC » sous le prix de la fiche (texte du bloc ou description) et masquer la mention d'expédition du panier.
- Preuve du contradicteur : Texte de /cart : « Total du panier €339,00 EUR ... Total estimé €339,00 EUR Droits de douane et taxes inclus. L'expédition est calculée lors du paiement. » ; fiche /products/essentielle : prix « €49,00 » ; accueil boutique : « €1.690,00 » ; checkout : « 339,00 € », « 1 839,00 € ».

### SEO-20 — Textes restés en anglais sur la boutique
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Plusieurs textes de la boutique sont en anglais : « You may also like » (fiches produit), « Join our email list » et « Get exclusive deals and early access to new products. » (pied de page de toutes les pages), « Submit » (bouton du formulaire /pages/contact), page 404 : « Page not found », « The link may be incorrect, or the page has been removed. », « Continue shopping », « Discover something new ». Le nom de l'option du plan d'abonnement est « Delivery every » (visible dans le panier, l'e-mail et l'espace client ; non vérifié visuellement). Le bandeau d'annonce « Bienvenue sur le shop de JUICECRAFT ! » mélange anglicisme et majuscules.
- Attendu : Boutique entièrement en français, marque écrite « juicecraft ».
- Preuve : Playwright /products/essentielle : « You may also like », « Join our email list », « Get exclusive deals and early access to new products. » ; /pages/contact : « Submit » ; /zzz-inconnu : « Page not found », « Continue shopping », « Discover something new » ; /products/essentielle.js : selling_plan options name « Delivery every » ; bandeau : « Bienvenue sur le shop de JUICECRAFT ! ».
- Recommandation : Dans Shopify admin > Boutique en ligne > Thèmes > Modifier le contenu par défaut du thème (langue française) ou Personnaliser : « You may also like » -> « Vous aimerez aussi » ; « Join our email list » -> « Recevez nos actualités » ; « Get exclusive deals and early access to new products. » -> « Offres exclusives et nouveautés en avant-première. » ; « Submit » -> « Envoyer » ; 404 : « Page introuvable. Le lien est peut-être incorrect ou la page a été supprimée. » / « Continuer vos achats » / « Découvrez nos offres ». Bandeau : « Bienvenue sur la boutique juicecraft ! ». Pour « Delivery every », renommer dans Appstle (réglage d'application : niveau 2) : « Fréquence de facturation ». Ajouter une case de consentement RGPD sous le champ e-mail du pied de page si la liste d'abonnés est utilisée (vérification juridique : niveau 3).
- Preuve du contradicteur : Playwright /products/essentielle : h3 « You may also like », h2 « Join our email list » ; /pages/contact : bouton « Submit » (curl) ; /zzz-inconnu : status 404, texte « Page not found | The link may be incorrect, or the page has been removed. | Continue shopping | Discover something new » ; /products/essentielle.js : options name 'Delivery every' ; bandeau « Bienvenue sur le shop de JUICECRAFT ! ».

### SEO-22 — Accueil, catalogue et contact de la boutique sans meta description, titres peu descriptifs
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : La page d'accueil a pour title « juicecraft » seul, aucune meta description, og:description = « juicecraft » (valeur de remplissage). Le catalogue a pour title « Produits – juicecraft » et la page contact « Contact – juicecraft », sans description non plus. Ces pages, dans le sitemap, apparaîtront avec un extrait automatique dans Google. Les fiches produit sont, elles, bien renseignées.
- Attendu : Title de 30 à 60 caractères et meta description de 70 à 160 caractères par page.
- Preuve : curl https://juicecraft-store.myshopify.com/ : <title>juicecraft</title>, pas de balise name="description", og:title="juicecraft", og:description="juicecraft" ; /collections/all : <title>Produits – juicecraft</title> sans description ; /pages/contact : <title>Contact – juicecraft</title>.
- Recommandation : Admin > Boutique en ligne > Préférences : Titre de la page d'accueil « juicecraft · Offres de création de site internet » ; Méta description : « Studio de création de sites internet sur mesure : offres Essentielle, Premium et Sur mesure à prix affichés TTC. Commandez en ligne ou demandez un devis. » (153 caractères). Collection « Tous les produits » : titre « Offres de création de site internet – juicecraft », description « Essentielle dès 49 €/mois, Premium dès 89 €/mois, Sur mesure dès 149 €/mois, TTC. Mise en place payée une fois. ». Page Contact : titre « Contact – juicecraft », description « Une question sur nos offres de création de sites internet ? Écrivez à juicecraft, nous répondons rapidement. ».
- Preuve du contradicteur : curl https://juicecraft-store.myshopify.com/ : <title>juicecraft</title>, regex meta name=description = [], <meta property="og:description" content="juicecraft"> ; /collections/all : <title>Produits – juicecraft</title>, pas de description ; /pages/contact : <title>Contact – juicecraft</title>, pas de description.

### SEO-23 — Données structurées produit : marque « Ma boutique » et catégorie « Informatique et technologie » héritées par défaut
- Zone : Référencement, contenu et rédaction
- Gravité : moyen | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Les trois offres déclarent le fournisseur « Ma boutique » (vendor) : le JSON-LD Product publie brand « Ma boutique », au lieu de « juicecraft » comme sur les produits « mise en place ». La catégorie de produit est « Informatique et technologie » pour les offres et « Service » pour les mises en place. Le nom du produit (« ESSENTIELLE », « PREMIUM », « SUR MESURE ») est tout en majuscules et sans mot décrivant l'offre dans le h1, alors que le title reprend « Création de site internet ».
- Attendu : brand = juicecraft ; noms de produits descriptifs et cohérents avec le site.
- Preuve : JSON-LD de /products/essentielle : "brand":{"@type":"Brand","name":"Ma boutique"},"category":"Informatique et technologie" ; /products/essentielle.js : "vendor":"Ma boutique" ; /products/mise-en-place-essentielle : brand « juicecraft », category « Service » ; h1 de la fiche : « ESSENTIELLE ».
- Recommandation : Modifier le fournisseur des trois produits d'offre en « juicecraft » (Admin > Produits > Fournisseur ; texte de produit = niveau 1). Un renommage du titre (par exemple « Offre Essentielle — site vitrine ») est plus visible : à proposer au propriétaire (niveau 2) avec cohérence « Mise en place — ESSENTIELLE » -> « Mise en place — Essentielle » (casse alignée sur le site).
- Preuve du contradicteur : /products.json : essentielle, 🔵-premium-⭐, sur-mesure vendor 'Ma boutique' ; mise-en-place-* vendor 'juicecraft' ; JSON-LD fiche Premium : "brand":{"@type":"Brand","name":"Ma boutique"},"category":"Informatique et technologie".

### LEGAL-16 — Mention TTC absente près des prix de la boutique, de l'abonnement au panier et au paiement
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : moyen | Niveau : 1 | Statut : confirmé | Confiance : moyenne
- Constat : Sur la boutique, les prix de l'abonnement s'affichent « €49,00 », « €490,00 », « €290,00 » sans « TTC » ni « /mois » dans la grille de prix ; la mention TTC n'existe que dans la description (« 290 € TTC »). Au paiement, le sous-total récurrent est suivi de « Ne comprend pas l'expédition, les taxes, les droits de douane ou toute réduction applicable », ce qui peut laisser croire que la TVA est en sus alors que Shopify affiche des prix toutes taxes comprises (taxesIncluded = true). Le panier mentionne « Droits de douane et taxes inclus. L'expédition est calculée lors du paiement. » (texte d'expédition inadapté à un service).
- Attendu : Prix affichés TTC de manière visible et cohérente avec le site ; textes sans ambiguïté sur les taxes. Référence : Code de la consommation art. L112-1 (prix TTC), à faire valider.
- Preuve : Texte /products/essentielle (Playwright) : « €49,00 », « Abonnement Mensuel » sans TTC ; panier : « Total estimé €339,00 EUR / Droits de douane et taxes inclus. L'expédition est calculée lors du paiement. » ; paiement : « 49,00 € par période de mois / Ne comprend pas l'expédition, les taxes… » ; graphql shop.taxesIncluded = true.
- Recommandation : Niveau 1 pour le texte de boutique : ajouter « TTC » aux descriptions et au titre (« 49 € TTC/mois »). Le libellé « Ne comprend pas … les taxes » du paiement est un texte Shopify à vérifier dans les réglages de taxes (niveau 2).
- Preuve du contradicteur : prod_essentielle.txt : '€49,00' sans TTC, 'Mise en place obligatoire (290 € TTC…)' seulement dans la description ; grep -c TTC : cart.txt 0, checkout.txt 0, shop_home.txt 0 ; checkout.txt lignes 314-315 'Sous-total récurrent / Ne comprend pas l'expédition, les taxes, les droits de douane ou toute réduction applicable' ; cart.txt : 'Droits de douane et taxes inclus. L'expédition est calculée lors du paiement.' ; graphql shop.taxesIncluded = true.

### ACHAT-15 — Politique de confidentialité : téléphone vide et espace manquant dans la rubrique Contact
- Zone : Parcours d'achat et page de paiement
- Gravité : faible | Niveau : 3 | Statut : confirmé | Confiance : haute
- Constat : La rubrique Contact indique « veuillez nous appeler au , nous envoyer un e-mail à l'adresseevannlassalle@gmail.com ou nous contacter à l'adresse 9 rue de St Pol, 62270 Conchy sur Canche, France » : numéro absent, espace manquant, adresse e-mail personnelle et adresse postale publiées.
- Attendu : Coordonnées complètes et voulues par le propriétaire (e-mail professionnel de préférence).
- Preuve : GraphQL shop.shopPolicies PRIVACY_POLICY body (section Contact) ; /policies/privacy-policy -> 200
- Recommandation : Le propriétaire décide des coordonnées publiées ; corriger : « veuillez nous écrire à contact@juicecraft.fr ou à l'adresse ... » et retirer la mention du téléphone si aucun numéro n'est donné. Texte légal à valider.
- Preuve du contradicteur : curl https://juicecraft-store.myshopify.com/policies/privacy-policy -> 200, texte extrait : « ...veuillez nous appeler au , nous envoyer un e-mail à l'adresseevannlassalle@gmail.com ou nous contacter à l'adresse 9 rue de St Pol, 62270 Conchy sur Canche, France » ; « Dernière mise à jour : 9 octobre 2026 ».

### INFRA-M2 — Politique de confidentialité Shopify publique incomplète : téléphone vide, renvoi à des conditions de service inexistantes, coordonnées personnelles visibles
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 3 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : La politique de confidentialité publique de la boutique contient la phrase « veuillez nous appeler au , nous envoyer un e-mail à l'adresse… » : le numéro de téléphone est vide. Elle indique comme contact l'adresse Gmail du propriétaire et une adresse postale à Conchy-sur-Canche, et renvoie à des « Conditions de service » qui n'existent pas dans la boutique. Ce n'est pas un secret (le texte est public) mais le propriétaire doit confirmer que ces coordonnées sont bien celles qu'il veut rendre publiques, et le texte doit être complété. Texte juridique : décision du propriétaire.
- Attendu : Une politique de confidentialité complète, sans champ vide, avec des coordonnées de contact choisies par le propriétaire et cohérente avec les autres textes légaux.
- Preuve : Shopify graphql_query shop.shopPolicies (PRIVACY_POLICY, mise à jour du 9 octobre 2026), section « Contact » : « …veuillez nous appeler au , nous envoyer un e-mail à l'adresse<adresse Gmail du propriétaire> ou nous contacter à l'adresse 9 rue de St Pol, 62270 Conchy sur Canche, France » ; texte : « En cas de contradiction entre nos Conditions de service et la présente Politique de confidentialité… » alors que shopPolicies ne contient aucune politique de type TERMS_OF_SERVICE ; https://juicecraft-store.myshopify.com/policies/privacy-policy -> HTTP 200.
- Recommandation : Demander au propriétaire quelle adresse et quel moyen de contact afficher (e-mail dédié de préférence à l'adresse personnelle), et compléter ou retirer la mention du téléphone. À traiter avec la création des CGV (INFRA-M1) pour que les textes se renvoient correctement. Aucune modification faite ici.

### PRIX-12 — FAQ : « nombre de tours inclus précisé dans l'offre » alors qu'il ne l'est nulle part
- Zone : Prix, offres et cohérence des contenus
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : La FAQ dit « le nombre de tours inclus est précisé dans l'offre et dans les CGV ». Ni les cartes du site, ni les descriptions Shopify (« Corrections et petites modifications », « Modifications régulières », « 2 h par mois ») ne donnent un nombre de tours, et les CGV sont introuvables (PRIX-11).
- Attendu : Nombre de tours de validation indiqué par offre, ou renvoi supprimé.
- Preuve : Texte rendu de la FAQ « Puis-je demander des modifications ? » ; descriptions /products/*.js sans nombre de tours.
- Recommandation : Soit ajouter « 2 tours de modifications avant mise en ligne » (valeur à fixer par le propriétaire) aux cartes et descriptions, soit remplacer la phrase par « Nous prévoyons des allers-retours de validation avant la mise en ligne ; le détail est communiqué avant tout engagement. »
- Preuve du contradicteur : curl https://juicecraft.fr, FAQ q4 : « le nombre de tours inclus est précisé dans l'offre et dans les CGV » ; grep « tour » sur les 3 descriptions /products/*.js : aucune occurrence ; voir PRIX-11 pour les CGV.

### ACHAT-07 — Le sélecteur de quantité permet d'acheter plusieurs abonnements (la quantité devrait toujours être 1)
- Zone : Parcours d'achat et page de paiement
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Un sélecteur de quantité (- / +) est affiché à côté du bouton d'achat des produits d'abonnement. Deux clics sur « + » donnent la quantité 3 ; le panier accepte 12 abonnements. Le panier permet aussi de modifier la quantité des lignes.
- Attendu : Quantité toujours 1 pour les abonnements et la mise en place.
- Preuve : Playwright sur /products/essentielle : 2 clics sur button[name=plus] -> input[name=quantity]=3 ; POST /cart/add.js quantity 12 -> 200, total 58800 ; capture shots/essentielle-Mensuel-desk-product.png (sélecteur - 1 +)
- Recommandation : Masquer le sélecteur de quantité dans le modèle de page produit pour ces 6 produits (édition du thème, accord du propriétaire) et fixer max=1 dans le panier.
- Preuve du contradicteur : Playwright /products/essentielle?selling_plan=692928774478&variant=61108150141262 : 2 clics sur button[name=plus] -> input[name=quantity]=3 ; clic sur button[name=add] -> /cart.js : [["ESSENTIELLE",3,14700]], total 14700. Même résultat (quantité 3) sur /products/mise-en-place-essentielle. Page /cart : boutons « Diminuer/Augmenter la quantité » sur chaque ligne.

### ACHAT-13 — Page d'accueil de la boutique : grande zone vide en haut et logo sur fond blanc
- Zone : Parcours d'achat et page de paiement
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Sur la page d'accueil de la boutique, environ 620 px entre l'en-tête et le bandeau défilant sont vides (aucun contenu héro, aucun texte). Le logo de l'en-tête est affiché avec un rectangle blanc visible sur le fond beige. Les cartes de panier ont leur image tronquée à gauche.
- Attendu : Section d'accueil renseignée ou supprimée ; logo à fond transparent.
- Preuve : shots/pg-home-desk.png (1440x900 : vide entre y=110 et y=720) ; HTML /: main ne contient que le bandeau « 🔥 Premium 🔥 Responsive... » puis « Produits » ; logo en en-tête de toutes les captures
- Recommandation : Dans l'éditeur du thème, supprimer ou compléter la première section vide et utiliser un logo PNG/SVG à fond transparent. Constat d'une capture à 3 s d'attente ; confirmer en navigateur réel.
- Preuve du contradicteur : Playwright 1440x900 sur https://juicecraft-store.myshopify.com/ : section.hero-wrapper top=109, hauteur 611, innerText vide ; section suivante (bandeau) à top=720 ; capture home-desk.png : zone vide de y=110 à y=720, logo avec fond blanc.

### ACHAT-16 — Adresse du produit Premium contenant des émojis (%F0%9F%94%B5-premium-%E2%AD%90)
- Zone : Parcours d'achat et page de paiement
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le handle du produit Premium est « 🔵-premium-⭐ », donnant une URL illisible et fragile une fois copiée. Le lien du site juicecraft.fr l'utilise.
- Attendu : Handle simple : /products/premium.
- Preuve : Lien data-plan="premium" : https://juicecraft-store.myshopify.com/products/%F0%9F%94%B5-premium-%E2%AD%90 ; /collections/all/products.json handle « 🔵-premium-⭐ »
- Recommandation : Changer le handle en « premium » avec redirection automatique 301 de l'ancien lien (option Shopify), et mettre à jour le bouton de juicecraft.fr. Accord du propriétaire requis.
- Preuve du contradicteur : /collections/all/products.json : handle « 🔵-premium-⭐ » ; https://juicecraft.fr/ : href du bouton data-plan="premium" = https://juicecraft-store.myshopify.com/products/%F0%9F%94%B5-premium-%E2%AD%90 ; clic réel -> la fiche Premium s'ouvre (200, titre « PREMIUM — ... dès 89 €/mois TTC »).

### ACHAT-17 — Options des plans d'abonnement : intitulé anglais « Delivery every » et valeur technique exposée
- Zone : Parcours d'achat et page de paiement
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : faible
- Constat : Les plans d'abonnement exposent publiquement une option « Delivery every » (anglais) dont la valeur est « 1MONTH1MONTHMIN_CYCLES=12MAX_CYCLES=NULLtrue-49.0-PRICEfalseAbonnement Mensuel ». Je n'ai pas observé d'affichage de cette valeur à l'écran (fiche, panier, paiement), seulement dans les données publiques ; elle pourrait apparaître dans des e-mails ou le compte client. Le nom du plan mensuel a aussi une espace finale.
- Attendu : Libellé en français sans chaîne technique.
- Preuve : /products/essentielle.js : selling_plan_groups[0].options[0].name « Delivery every » ; values « 1MONTH1MONTHMIN_CYCLES=12MAX_CYCLES=NULLtrue-49.0-PRICEfalseAbonnement Mensuel » ; plan name « Abonnement Mensuel » avec espace finale
- Recommandation : Dans Appstle, renommer le nom d'option du groupe de plans (« Fréquence ») et vérifier ce qui s'affiche dans l'e-mail de confirmation et le portail client. Accord requis (réglage d'application).
- Preuve du contradicteur : /products/essentielle.js : selling_plan_groups[0].options[0].name = « Delivery every » ; plan 692928774478 : name « Abonnement Mensuel » (espace finale), option value « 1MONTH1MONTHMIN_CYCLES=12MAX_CYCLES=NULLtrue-49.0-PRICEfalseAbonnement Mensuel ». Radio/select de la fiche : options « Abonnement Mensuel », « Abonnement Annuel » seulement.

### SEO-02 — Aucune balise canonical : variantes d'URL indexables en doublon
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : La page n'a pas de <link rel="canonical">. Plusieurs adresses servent la même page en 200 sans redirection : /index.html, //, ?utm=1 (paramètres de suivi). Le doublon netlify.app est limité par l'en-tête HTTP Link canonical ajouté par Netlify, mais c'est un réglage externe au code, non visible dans le HTML.
- Attendu : Une balise canonical absolue dans le head, identique pour toutes les variantes.
- Preuve : curl -I https://juicecraft.fr/index.html -> 200 ; https://juicecraft.fr/?utm=1 -> 200 ; https://juicecraft.fr// -> 200 ; grep canonical dans le HTML de juicecraft.fr -> 0. En-tête sur netlify.app : « link: <https://juicecraft.fr/>; rel="canonical" ».
- Recommandation : Ajouter dans le <head> de index.html : <link rel="canonical" href="https://juicecraft.fr/">  (publication = niveau 2). Facultatif : règle Netlify dans un fichier _redirects : « /index.html / 301 ».
- Preuve du contradicteur : curl : https://juicecraft.fr/index.html -> 200 redir=0 ; /?utm=1 -> 200 ; // -> 200 ; Playwright (390 px) document.querySelectorAll('link[rel=canonical]').length = 0 ; netlify.app : en-tête « link: <https://juicecraft.fr/>; rel="canonical" ».

### SEO-04 — Aucune donnée structurée JSON-LD sur le site
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Aucun bloc application/ld+json : pas de nom d'organisation, de logo ni de description lisibles par les moteurs (panneau de connaissance, résultats enrichis). La page ne montre aucune coordonnée (e-mail, téléphone, adresse), donc rien de factice ne doit être inventé.
- Attendu : Au minimum Organization + WebSite ; offres en option.
- Preuve : grep -c 'ld+json' sur le HTML brut et script[type="application/ld+json"] dans le DOM rendu Playwright -> 0.
- Recommandation : Ajouter avant </head> (compléter url du logo et, si le propriétaire le souhaite, e-mail et SIRET ; ne rien inventer) :
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Organization","@id":"https://juicecraft.fr/#org","name":"juicecraft","url":"https://juicecraft.fr/","logo":"https://juicecraft.fr/logo.png","description":"Studio français de création de sites internet sur mesure pour les artisans, commerces, cabinets et entreprises."},{"@type":"WebSite","@id":"https://juicecraft.fr/#site","url":"https://juicecraft.fr/","name":"juicecraft","inLanguage":"fr-FR","publisher":{"@id":"https://juicecraft.fr/#org"}}]}</script>
- Preuve du contradicteur : re.findall('ld\+json') = 0 sur le HTML brut ; Playwright script[type="application/ld+json"] = 0 ; la boutique, elle, publie bien du JSON-LD (Organization + Product lus sur la fiche Premium).

### SEO-05 — Icônes et manifest incomplets (favicon.ico, apple-touch-icon, manifest absents)
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Seul un favicon SVG en data URI est déclaré. Les navigateurs et robots qui demandent /favicon.ico (certains moteurs, flux, onglets Safari) reçoivent la page 404 ; pas d'icône d'écran d'accueil iOS ni de manifest.
- Attendu : favicon.ico ou PNG, apple-touch-icon 180x180, manifest optionnel.
- Preuve : https://juicecraft.fr/favicon.ico -> 404 ; /apple-touch-icon.png -> 404 ; /manifest.webmanifest -> 404 ; head sans <link rel="apple-touch-icon"> ni <link rel="manifest">.
- Recommandation : Exporter le logo goutte en favicon-32.png et apple-touch-icon.png (180x180) et ajouter :
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
Le manifest est facultatif pour un site vitrine.
- Preuve du contradicteur : curl -w '%{http_code}' : https://juicecraft.fr/favicon.ico 404 ; /apple-touch-icon.png 404 ; /manifest.webmanifest 404 ; grep 'apple-touch' et 'manifest' dans le HTML = 0.

### SEO-07 — Liens vers la boutique et détail des services générés uniquement par JavaScript
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Dans le HTML brut, les trois boutons « Choisir cette offre » pointent vers #contact ; l'adresse Shopify n'est posée que par le script (constante SHOP). Un robot sans JavaScript ne voit aucun lien vers les pages d'offres, et un visiteur dont le script échoue est renvoyé vers le formulaire au lieu de la boutique. De même le panneau des services (#svc-info) et le configurateur sont vides dans le HTML initial.
- Attendu : href réels vers les pages produit dans le HTML, le script ne faisant qu'améliorer.
- Preuve : HTML brut : <a class="btn btn-light" href="#contact" data-offer="Site vitrine — Essentielle" data-plan="essentielle"> ; DOM rendu : href="https://juicecraft-store.myshopify.com/products/essentielle" (idem premium, mesure). <div class="svc-info" id="svc-info" aria-live="polite"></div> vide dans le HTML brut.
- Recommandation : Écrire directement dans index.html href="https://juicecraft-store.myshopify.com/products/essentielle" (et les deux autres) avec rel="noopener", en conservant le script pour le préremplissage. Recopier le texte du premier service (Vitrine) dans #svc-info. Publication = niveau 2. À traiter ensemble avec le changement de handle Premium (SEO-17).
- Preuve du contradicteur : Regex sur le HTML brut : <a class="btn btn-light" href="#contact" data-offer="Site vitrine — Essentielle" data-plan="essentielle"> (idem premium, mesure) ; Playwright : hrefs rendus = https://juicecraft-store.myshopify.com/products/essentielle, .../%F0%9F%94%B5-premium-%E2%AD%90, .../sur-mesure ; <div class="svc-info" id="svc-info"> vide dans le HTML brut.

### SEO-08 — Titre h1 : nom accessible différent du texte visible, mot rotatif non exposé
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Le h1 porte aria-label="Votre activité mérite un site qui a du jus." alors que le texte visible, animé, est « Votre commerce / atelier / cabinet / restaurant / entreprise / boutique / projet mérite un site qui a du jus. ». Les lecteurs d'écran et certains robots lisent « activité » ; pendant la transition le DOM contient deux mots à la fois (« Votre commerce atelier mérite… »). Le premier mot dans le HTML brut est « commerce ».
- Attendu : Nom accessible cohérent avec le texte et h1 contenant le mot-clé principal.
- Preuve : HTML brut : <h1 class="h1" aria-label="Votre activité mérite un site qui a du jus."> ; innerText du h1 rendu : « Votre commerce atelier mérite un site qui a du jus . ».
- Recommandation : Conserver l'aria-label (utile) mais envisager d'ajouter un h1 plus descriptif pour le référencement, par exemple une ligne visuellement discrète « Création de sites internet sur mesure » dans le h1, ou reprendre le mot « site internet » dans la phrase. Alternative : « Votre activité mérite un site internet qui a du jus. » dans l'aria-label.
- Preuve du contradicteur : HTML brut : <h1 class="h1" aria-label="Votre activité mérite un site qui a du jus."> avec spans aria-hidden ; Playwright h1.innerText = « Votre commerce atelier mérite un site qui a du jus . ».

### SEO-09 — Hiérarchie des titres polluée par les maquettes décoratives et sauts de niveau
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le plan de titres contient un h4 vide juste après le h1, des h3/h4 appartenant aux maquettes de démonstration (« Un site professionnel qui présente votre activité. », « Des chambres au calme, face à la rivière. ») et, en pied de page, trois h4 (Navigation, Services, Informations) sans h3 parent. Cela brouille le plan du document pour les moteurs et les lecteurs d'écran.
- Attendu : h1 > h2 > h3 sans saut, titres de maquette masqués aux technologies d'assistance.
- Preuve : Playwright, liste des titres rendus : H1, H2 « Des sites adaptés à chaque besoin. », H4 « » (vide), H3 « Un site professionnel qui présente votre activité. », …, H2 « Parlons de votre projet. », H4 NAVIGATION, H4 SERVICES, H4 INFORMATIONS.
- Recommandation : Remplacer les <h4> du pied de page par <p class="foot-title"> (ou h3) et transformer les titres internes aux maquettes en <div>/<span> avec aria-hidden="true". Supprimer le h4 vide.
- Preuve du contradicteur : Playwright 390 px, liste des titres : H1, H2 « Des sites adaptés à chaque besoin. », H4 « », H3 « Un site professionnel… », … H2 « Parlons de votre projet. », H4 NAVIGATION, H4 SERVICES, H4 INFORMATIONS.

### SEO-11 — Typographie française : aucune espace insécable avant ? ! : ; ni dans les montants
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Tout le HTML n'emploie que 2 espaces insécables (&nbsp; dans « hors du commun&nbsp;? » et « écrivez-nous&nbsp;: »). Partout ailleurs ce sont des espaces simples : « Combien coûte un site internet ? », « Quel site pour votre projet ? », « Le référencement est-il inclus ? », « 49 €/mois », « 1 490 € TTC », « 1 690 € », « 0 %», « Question 1 / 3 ». Selon la largeur d'écran, le signe peut passer seul en début de ligne et « 1 490 / € » peut être coupé. Aucun cas de coupure n'a été observé à 390 px sur les montants testés : risque, pas défaut constaté.
- Attendu : Espace insécable (fine insécable pour ; : ? ! selon l'usage) avant ? ! : ; » %, après «, et dans les nombres à milliers (1 490 €).
- Preuve : Comptage sur le HTML brut : U+00A0 = 0, « &nbsp; » = 2. Exemples : « Une autre question ? Posez-la directement. », « Le délai est communiqué lors de l'échange initial » (liste complète des ? : ; ! précédés d'une espace simple : 25 occurrences relevées par expression régulière).
- Recommandation : Remplacer l'espace par &nbsp; (ou  ) : « 49&nbsp;€ », « 1&nbsp;490&nbsp;€ TTC », « 1&nbsp;690&nbsp;€ », « Combien coûte un site internet&nbsp;? », « Quel site pour votre projet&nbsp;? », « 0&nbsp;% », « Question 1&nbsp;/&nbsp;3 », « « &nbsp;Chaque pièce est dessinée pour la maison qui l'accueille.&nbsp;» », « Score visé&nbsp;: 90+ », et dans les chaînes du script (recommandations du configurateur, messages d'erreur « adresse&nbsp;: »). Ajouter white-space:nowrap sur .price b.
- Preuve du contradicteur : Python sur le HTML brut : ' ' = 0, '&nbsp;' = 2 (« hors du commun&nbsp;? », « écrivez-nous&nbsp;: ») ; regex ' [?!;:»%]' sur le texte visible = 25 ; regex '\d \d{3} ?€?' -> ['1 490 €','1 690 €','1 690 €','1 490 €'].

### SEO-15 — Vocabulaire et formulations à harmoniser
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : (1) « Chaque engagement ci-dessous est démontré en direct » : « engagement » désigne ici une promesse alors que « 12 mois d'engagement » désigne la durée du contrat. (2) FAQ : « 49 €/mois (12 mois d'engagement) » n'est précisé que pour Essentielle ; Premium et Sur mesure (« 89 €/mois », « 149 €/mois ») semblent sans engagement alors que MIN_CYCLES=12 s'applique aussi. (3) Ton : « On lui redonne du jus » alors que tout le reste emploie « nous ». (4) « Tout ce qui est inclus dans Essentielle » : préférer « dans l'offre Essentielle ». (5) Libellés variables pour une même chose : « Refonte » / « Refonte de site », « Site vitrine — Essentielle » / « Essentielle » / « Vitrine Essentielle ». (6) Chip « Optimisé SEO » et « SEO renforcé » vs « Bases SEO » pour Essentielle ; le configurateur ajoute pourtant « SEO local renforcé : structure, balises et fiche d'établissement » et « Interface d'administration simple et prise en main » à la recommandation Essentielle, qui ne les liste pas. (7) Anglicisme « Responsive » (puces, titres) à côté de « adapté aux smartphones ». (8) Faible lisibilité : « Les réponses aux questions que vous vous posez peut-être. »
- Attendu : Termes uniques et engagement indiqué pour toutes les offres.
- Preuve : Textes cités mot pour mot dans le HTML rendu de https://juicecraft.fr/ (sections #approche, #faq, #offres, tableau ADD du script ligne ~1767, recommandation « Vitrine Essentielle » : r.f = [..., ADD[p]]).
- Recommandation : (1) « Chaque promesse ci-dessous est démontrée en direct. » (2) « …puis 49 €/mois, 89 €/mois ou 149 €/mois selon l'offre (engagement de 12 mois en paiement mensuel) ou… ». (3) « Votre site a vieilli ? Nous lui redonnons du jus. » (4) « Tout ce qui est inclus dans l'offre Essentielle ». (5) Retenir « Refonte de site » et « Offre Essentielle ». (6) Remplacer « Optimisé SEO » par « Bases SEO incluses » ou nuancer ; ne pas ajouter ADD[p] aux recommandations Essentielle ou le reformuler. (7) « Adapté mobile » au lieu de « Responsive ». (8) « Les réponses aux questions que vous vous posez peut-être. » -> « Les réponses aux questions les plus courantes. »
- Preuve du contradicteur : Texte visible : « …avec 12 mois d'engagement en paiement mensuel, ou 2 mois offerts en paiement annuel » ; « L'abonnement mensuel engage sur 12 mois, l'abonnement annuel offre 2 mois » ; FAQ « Essentielle : 290 € de mise en place, puis 49 €/mois (12 mois d'engagement) … Premium … 89 €/mois ou 890 € par an » ; script ligne 1560 : « Votre site a vieilli ? On lui redonne du jus. ».

### SEO-16 — Détour de redirection www : deux sauts au lieu d'un
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : http://www.juicecraft.fr/ passe par https://www.juicecraft.fr/ avant d'arriver sur https://juicecraft.fr/ (2 redirections 301). Acceptable pour le référencement mais ralentit le premier accès et dilue légèrement le signal. Le HSTS n'a ni includeSubDomains ni preload.
- Attendu : Au plus 1 redirection vers la version canonique.
- Preuve : curl -L -w '%{num_redirects}' http://www.juicecraft.fr/ -> redirects=2 ; location: https://www.juicecraft.fr/ puis location: https://juicecraft.fr/ ; header strict-transport-security: max-age=31536000.
- Recommandation : Pas d'urgence. Si souhaité, régler le domaine principal dans Netlify (hébergement = niveau 2). Aucune action DNS n'est nécessaire.
- Preuve du contradicteur : curl -L -w '%{num_redirects}' http://www.juicecraft.fr/ -> redirects=2 final=https://juicecraft.fr/ code=200 ; curl -I http://www.juicecraft.fr/ -> location: https://www.juicecraft.fr/ ; curl -I https://www.juicecraft.fr/ -> location: https://juicecraft.fr/ ; strict-transport-security: max-age=31536000.

### SEO-17 — URL du produit Premium contenant des émojis (%F0%9F%94%B5-premium-%E2%AD%90)
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le handle « 🔵-premium-⭐ » devient une URL de 38 caractères encodés, illisible une fois copiée, fragile dans les e-mails, SMS et réseaux sociaux, et non conforme aux bonnes pratiques d'URL (caractères non ASCII). Shopify sert l'adresse canonical et og:url en minuscules (%f0%9f%94%b5-premium-%e2%ad%90) alors que le site et le sitemap utilisent des majuscules (%F0%9F%94%B5-premium-%E2%AD%90) : deux écritures de la même URL. Les autres offres ont des handles propres (essentielle, sur-mesure).
- Attendu : Handle ASCII court, sans émoji.
- Preuve : /products/essentielle.js : handle « 🔵-premium-⭐ » ; canonical de la fiche : https://juicecraft-store.myshopify.com/products/%f0%9f%94%b5-premium-%e2%ad%90 ; lien du site (constante SHOP) : .../products/%F0%9F%94%B5-premium-%E2%AD%90 ; sitemap_products_1.xml : majuscules.
- Recommandation : Changer le handle en « premium » (aucun handle existant en conflit, vérifié dans /products.json) dans Shopify admin > Produits > PREMIUM > Référencement > URL, en cochant « Créer une redirection URL » pour conserver l'ancienne adresse. Puis mettre à jour dans index.html la constante SHOP.premium = "https://juicecraft-store.myshopify.com/products/premium" (et le lien dans les e-mails/liens externes, ainsi que le lien « ajoutez-la au panier » inchangé car il pointe vers mise-en-place-premium). Séquence : 1) changer le handle avec redirection, 2) publier le site, 3) tester les deux adresses. Niveau 2 : modifie un produit et le site en ligne ; ne pas toucher aux plans Appstle (non liés au handle, à vérifier).
- Preuve du contradicteur : /products/%F0%9F%94%B5-premium-%E2%AD%90.js -> handle '🔵-premium-⭐' ; <link rel="canonical" href=".../products/%f0%9f%94%b5-premium-%e2%ad%90"> ; curl majuscules 200, minuscules 200 (redirects=0) ; sitemap_products_1.xml : <loc>.../products/%F0%9F%94%B5-premium-%E2%AD%90</loc>.

### SEO-21 — Format des montants de la boutique : « €49,00 », « €1.690,00 » et jeton « {{amount_with_comma_separator}} » visible
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Les prix sont écrits avec le symbole devant et un point comme séparateur de milliers : « €49,00 », « €1.690,00 ». Le français attend « 49,00 € » et « 1 690,00 € ». De plus le filtre de prix du catalogue affiche littéralement « €{{amount_with_comma_separator}} » : le format monétaire a été saisi avec un jeton Liquid mal interprété par le thème. Les montants de la boutique s'écartent aussi de l'écriture du site (« 49 € », « 1 490 € »).
- Attendu : « 1 690,00 € » (ou « 1 690 € »).
- Preuve : /collections/all, texte rendu : « Prix €{{amount_with_comma_separator}} € à € Le prix le plus élevé est de €1.690,00 » ; accueil : « €490,00 », « €1.690,00 » ; fiche : « €49,00 ».
- Recommandation : Admin Shopify > Paramètres > Général > Devise de la boutique > Modifier le formatage : « Formatage HTML » = {{amount_with_space_separator}} € ; « Formatage HTML avec devise » = {{amount_with_space_separator}} € EUR (ou {{amount_no_decimals_with_space_separator}} € pour afficher « 1 690 € »). Vérifier ensuite le filtre du catalogue.
- Preuve du contradicteur : Playwright /collections/all : innerText sans '{{' ; filtre Prix ouvert -> « Prix | € | à | € | Le prix le plus élevé est de €1.690,00 » ; ?filter.v.price.gte=100&lte=600 -> « €100,00–€600,00 » et token in innerText = false ; curl : <template ref="moneyFormat">€{{amount_with_comma_separator}}</template> et data-money-format="€{{amount_with_comma_separator}}" ; prix affichés « €490,00 », « €1.690,00 ».

### LEGAL-12 — Polices chargées depuis Google : l'adresse IP du visiteur est transmise à un tiers sans information
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Au chargement de juicecraft.fr, la feuille de style fonts.googleapis.com et 4 fichiers fonts.gstatic.com sont appelés. Aucun cookie n'est déposé, mais les serveurs de Google reçoivent l'adresse IP du visiteur ; cela n'est mentionné nulle part (pas de page de confidentialité sur le site).
- Attendu : Information du visiteur sur les destinataires ou hébergement local des polices pour éviter le transfert. Aucun texte de la CNIL propre à Google Fonts n'a été retrouvé (recherche cnil.fr) : position juridique à faire valider.
- Preuve : Requêtes Playwright : GET https://fonts.googleapis.com/css2?family=Mona+Sans:wdth,wght@75..125,200..900&family=Instrument+Sans… ; GET https://fonts.gstatic.com/s/monasans/v4/…woff2 ; …/instrumentsans/…, …/geistmono/…, …/instrumentserif/… (2 fichiers).
- Recommandation : Option technique : auto-héberger les 4 familles de polices (changement du site, donc accord et déploiement niveau 2) ; ou mentionner Google dans la future page de confidentialité.
- Preuve du contradicteur : Playwright https://juicecraft.fr/ (networkidle + 3 s) : hôtes [juicecraft.fr:3, fonts.googleapis.com:1, fonts.gstatic.com:5] ; ctx.cookies() = [].

### LEGAL-18 — Allégations « Score visé : 90+ » avec « 98 » affiché, et « Paiement sécurisé » à confirmer
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : La section « Rapidité » affiche un chiffre « 98 » avec « SCORE VISÉ : 90+ » ; la puce du hero « Paiement sécurisé » et la carte « Sécurité » (« Connexion chiffrée et paiements traités par des prestataires certifiés ») sont aussi des promesses. Le « 98 » est une illustration, non présentée comme telle et non mesurée ici ; aucun test de vitesse n'a été fait sur les sites clients. Le site lui-même ne traite pas de paiement (c'est Shopify).
- Attendu : Le propriétaire confirme que l'objectif est atteignable et réellement mesuré (PageSpeed), et que la promesse de paiement sécurisé repose bien sur des prestataires certifiés, ou ajoute « exemple illustratif ».
- Preuve : innerText : « 98 / SCORE VISÉ : 90+ », « Paiement sécurisé » (puce du hero et démos), « Sécurité : Connexion chiffrée et paiements traités par des prestataires certifiés. »
- Recommandation : Niveau 2 : reformuler (« objectif : 90+ sur PageSpeed, selon le contenu ») ou marquer le « 98 » comme exemple illustratif, après accord du propriétaire.
- Preuve du contradicteur : site_text.txt lignes 25 et 43 'Paiement sécurisé', lignes 144-145 '98 / SCORE VISÉ : 90+', ligne 148 'Connexion chiffrée et paiements traités par des prestataires certifiés.' ; capture badge.png : carte « Paiement sécurisé – Transaction validée ».

### LEGAL-M3 — Badge « Powered by Netlify » visible et iframe injectée sur le site de production, contraire à la mention « aucun iframe tiers »
- Zone : Juridique, vie privée et allégations commerciales
- Gravité : faible | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Le script /.netlify/scripts/hud?variant=public (balise <script> présente dans le HTML de production) injecte un iframe #nl-badge-frame (srcdoc) qui affiche un badge « Powered by Netlify » en bas à droite de chaque page. Il ne déclenche aucune requête réseau ni cookie, mais il s'agit d'une marque tierce visible sur le site d'un studio, et la déclaration de l'auditeur « aucun iframe tiers » est inexacte. L'hébergeur y apparaît sans les mentions légales requises.
- Attendu : Le propriétaire sait que ce badge apparaît, et décide de le garder ou non ; l'identité de l'hébergeur doit figurer dans les mentions légales, pas seulement dans un badge.
- Preuve : home.html ligne 1887 : <script async src="/.netlify/scripts/hud?variant=public" data-nf-variant="public"…>. Playwright : iframe#nl-badge-frame, srcdoc 10 833 caractères, rect [1079, 736, 201, 64], display block, visibility visible, opacity 1, texte « Powered by Netlify » ; capture badge.png.
- Recommandation : Décision du propriétaire (réglage Netlify du site, niveau 2) ; ne rien modifier sans accord. Ajouter l'hébergeur aux mentions légales (voir LEGAL-01).

### ACCES-02 — Badge « Powered by Netlify » fixe qui recouvre des boutons et champs
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Une iframe #nl-badge-frame (title « Powered by Netlify ») est affichée en position fixe en bas à droite de chaque écran, au-dessus de tout (z-index 2147483645). Elle masque du contenu et capte les clics sur les contrôles situés dessous : sur mobile, jusqu'à 156x55 px du bouton « Choisir cette offre » de Sur mesure, 163x45 px du champ Nom, 164x42 px d'une option du configurateur, des interrupteurs, des questions de la FAQ ; sur ordinateur, jusqu'à 53x51 px d'une question FAQ et 17x41 px du bouton « Envoyer ma demande ». Elle ajoute aussi un arrêt de Tab en fin de page sans nom accessible (iframe sans nom) et un petit décalage de mise en page à t=1,0 s.
- Attendu : Aucun élément tiers ne doit recouvrir les boutons d'achat et les champs de formulaire du site ; l'aspect de marque doit rester celui de juicecraft.
- Preuve : Script chargé par la page : <script async src="/.netlify/scripts/hud?variant=public" data-netlify-site-id="953a3a52-b9bb-46b6-91b3-4c35e0eb92d4">. Mesure Playwright : #nl-badge-frame position:fixed, rect mobile [189,780,201,64], ordinateur [1239,836,201,64] ; chevauchements d'éléments interactifs calculés tous les 300 px de défilement (listés ci-dessus) ; dernier arrêt de Tab = iframe#nl-badge-frame. Les captures montrent le badge sur tout l'écran, y compris sur le menu mobile ouvert et sur le formulaire. L'origine exacte (réglage Netlify, offre ou fonction activée) n'a pas pu être déterminée en lecture seule.
- Recommandation : Dans le tableau de bord Netlify du projet sparkling-bubblegum-b2d478, vérifier quelle fonction injecte ce script (recherche : « badge », « Powered by Netlify », fonctionnalités de rendu/équipe) et la désactiver, ou ajuster l'offre/les réglages si c'est le comportement d'une offre ; contrôler ensuite que la ligne <script src="/.netlify/scripts/hud..."> et l'iframe ont disparu du HTML servi. Aucune modification du code du site n'est nécessaire en première intention.
- Preuve du contradicteur : Diff dépôt (/home/user/juicecraft-site/index.html, 199 948 octets) contre page servie (200 132 octets) : seule différence = la balise <script async src="/.netlify/scripts/hud?variant=public" ...>, injectée par Netlify à la volée. Playwright : #nl-badge-frame position fixed, z-index 2147483645, rect [1239,836,201,64] (ordinateur), style.clipPath = path("M 3 3 H 188 V 51 H 3 Z") ; document.elementFromPoint(rect.x+2, rect.y+2) renvoie l'élément de la page (hors iframe), le centre renvoie nl-badge-frame ; title="Powered by Netlify". Documentation officielle https://docs.netlify.com/manage/projects/powered-by-netlify-badge/ : réglage « Project configuration > General > Powered by Netlify badge », effet sans redéploiement, activé par défaut pour les projets Free créés à partir du 19 août 2026.

### ACCES-05 — Étiquettes « Livrable » orange à 3,0:1 en 10,9 px
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Les étiquettes « Livrable » des 5 étapes sont en orange #ff5a1f sur #fbfbf9, à 3,0:1, taille 10,88 px, alors que 4,5:1 est requis pour du petit texte. Contrastes également limites dans les maquettes de démonstration décoratives (« Atelier / Projets / Contact » 3,74:1, étiquette .b-tag 3,18:1), qui sont des illustrations.
- Attendu : Au moins 4,5:1 pour du texte de moins de 18,66 px normal.
- Preuve : axe-core : « .on.step > .deliv > span ... contrast of 3 (foreground color: #ff5a1f, background color: #fbfbf9, font size: 8.2pt (10.88px) ». Mesure manuelle sur le DOM : 5 occurrences à 3,01:1.
- Recommandation : Utiliser un orange plus foncé pour ce texte, par exemple #c2410c (≈ 5,2:1 sur #fbfbf9), et conserver #ff5a1f pour les pastilles et filets.
- Preuve du contradicteur : axe-core 4.14.0 : « .on.step > .deliv > span : contrast of 3 (foreground #ff5a1f, background #fbfbf9, 8.2pt = 10.88px) » et la même valeur pour .step:nth-child(3..6) > .deliv > span ; « .s-links > span : 3.74 (#8c7c69 sur #faf6ef) » ; « .b-tag : 3.18 (#8a8790 sur #f4f3f1) » en mobile.

### ACCES-06 — Menu mobile : focus non piégé, la tabulation sort vers la page cachée derrière
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Menu mobile ouvert (body.lock), Tab passe par les 7 liens puis continue sur « Créer mon site », « Voir nos réalisations », « Élégant », « Audacieux », « Minimal » (éléments masqués sous le menu plein écran). L'écran n'est pas déclaré modal (pas de role=dialog/aria-modal, pas d'inert sur le reste de la page).
- Attendu : Quand un menu plein écran est ouvert, le focus reste dans le menu (ou le reste de la page est inerte) jusqu'à fermeture ; WCAG 2.4.3 et 2.4.11.
- Preuve : Séquence de Tab mesurée après Entrée sur #burger : Services | Approche | Méthode | Réalisations | Offres | FAQ | Contact | Créer mon site | Voir nos réalisations | Élégant | Audacieux | Minimal. Échap ferme bien le menu (aria-expanded=false).
- Recommandation : Dans setMenu(open), ajouter main.inert = open (et le pied de page) en gardant le bouton et le menu actifs ; à la fermeture, rendre le focus à #burger.
- Preuve du contradicteur : Playwright 390x844 : focus sur #burger, Entrée (aria-expanded=true, body.lock), 14 Tab : Services | Approche | Méthode | Réalisations | Offres | FAQ | Contact | Créer mon site | Voir nos réalisations | Élégant | Audacieux | Minimal | Site vitrine→ | En parler. querySelector('[role=dialog],[aria-modal]') = null ; main.inert = false.

### ACCES-07 — Pied de page : titres h4 qui sautent le niveau h3
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Les titres « Navigation », « Services » et « Informations » du pied de page sont des h4 qui suivent directement le h2 « Parlons de votre projet. », sans h3.
- Attendu : Les niveaux de titre augmentent d'un seul cran (WCAG 1.3.1, bonne pratique).
- Preuve : axe-core heading-order (impact modéré) : « div:nth-child(2) > h4 : Heading order invalid ». Liste des titres : ... H2:Parlons de votre projet. -> H4:NAVIGATION, H4:SERVICES, H4:INFORMATIONS.
- Recommandation : Remplacer ces trois balises <h4> par <h3> dans le pied de page (la classe CSS reste inchangée).
- Preuve du contradicteur : axe-core 4.14.0 : règle heading-order, nœud « div:nth-child(2) > h4 : Heading order invalid » (ordinateur et mobile). HTML du <footer> : <h4>Navigation</h4>, <h4>Services</h4>, <h4>Informations</h4> après le h2 de la section contact.

### ACCES-08 — Configurateur : le focus est perdu à chaque réponse
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Quand on active une option du configurateur au clavier (Entrée), le bouton est remplacé par innerHTML pour afficher la question suivante : document.activeElement devient BODY. L'utilisateur de lecteur d'écran n'est pas informé du changement de question (seul le résultat final porte aria-live).
- Attendu : Le focus doit être placé sur la nouvelle question (par exemple son titre h3 avec tabindex=-1) ou annoncé via une zone aria-live.
- Preuve : Playwright : focus sur .opt (1re option), Entrée, 600 ms plus tard document.activeElement = BODY ; Tab suivant arrive sur l'option « Une seule page » de l'étape 2.
- Recommandation : Dans renderQ(), après avoir injecté le HTML, donner tabindex="-1" au h3 de la question et appeler .focus() dessus (sauf au premier rendu) ; envelopper le bloc dans un conteneur aria-live="polite" déjà présent au chargement.
- Preuve du contradicteur : Playwright 1440x900 : focus sur le premier .opt, touche Entrée, 700 ms plus tard document.activeElement = BODY (classe has-cursor).

### ACCES-09 — Erreurs du formulaire non associées aux champs (pas d'aria-invalid ni aria-describedby)
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Après un envoi à vide, les messages sont bien annoncés (span aria-live=polite) et le focus va sur le premier champ en erreur, mais les champs en erreur n'ont ni aria-invalid="true" ni aria-describedby vers leur message ; un lecteur d'écran ne relie donc pas l'erreur au champ lorsqu'on y revient.
- Attendu : WCAG 3.3.1 : erreur identifiée dans le texte et associée au champ (aria-invalid + aria-describedby).
- Preuve : Après clic sur « Envoyer ma demande » champs vides : liste des inputs avec aria-invalid/aria-describedby non nuls = []. Spans .msg sans id.
- Recommandation : Dans setErr(), ajouter id="err-name"/"err-email" aux spans .msg, puis input.setAttribute('aria-describedby', id) et input.setAttribute('aria-invalid', !!m) ; retirer aria-invalid quand l'erreur disparaît.
- Preuve du contradicteur : Playwright : clic sur le bouton d'envoi, champs vides, requêtes api.web3forms.com interceptées (0 appel). Champs avec aria-invalid ou aria-describedby : liste vide ; spans .msg : id vide, aria-live=polite ; document.activeElement.id = f-name.

### ACCES-10 — Texte indicatif (placeholder) des champs à 4,11:1
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Les placeholders (« Camille Martin », « camille@entreprise.fr », « Atelier Martin », « Mon activité, mes objectifs... ») sont gris rgb(117,117,117) sur rgb(242,242,239), soit 4,11:1 (couleur par défaut du navigateur, non redéfinie).
- Attendu : 4,5:1 au minimum pour le texte du placeholder.
- Preuve : getComputedStyle(champ,'::placeholder').color = rgb(117,117,117) ; fond de champ rgb(242,242,239) ; ratio calculé 4,11 pour #f-name, #f-company, #f-msg.
- Recommandation : Ajouter dans la feuille de style : .form input::placeholder, .form textarea::placeholder { color: #6a6670; opacity: 1; } (≈ 4,9:1).
- Preuve du contradicteur : getComputedStyle(champ,'::placeholder').color = rgb(117, 117, 117) pour #f-name, #f-company, #f-msg, #f-email ; fond des champs rgb(242,242,239) (rgb(255,255,255) pour #f-name au moment de la mesure) ; ratio calculé #757575/#F2F2EF = 4,12:1.

### ACCES-11 — La section Services change de hauteur quand on change d'onglet (mobile, tablette, 1024 px)
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Au repos la section est stable (corrigé), mais le choix d'un onglet fait varier la hauteur du panneau et de la page : à 345 px 664 -> 716 px (Refonte) -> 639 px (Optimisation) ; à 414 px de 620 à 711 px ; à 1024 px 675 -> 700 px (Refonte). À 1440 px tout est constant (748 px). Sur ordinateur à pointeur fin, l'onglet change au simple survol, ce qui peut déplacer le contenu situé dessous.
- Attendu : Hauteur de panneau constante quelle que soit la sélection (résidu de l'ancien défaut de cartes qui changeaient de hauteur).
- Preuve : Hauteur de #svc-panel après clic sur chacun des 5 onglets : 345x740 [664,664,664,716,639] ; 414x896 [671,711,645,671,620] ; 1024x768 [675,675,675,700,675] ; 1440x900 [748 x5]. scrollHeight de la page varie de la même valeur (ex. 16 553 à 16 645 px à 414 px).
- Recommandation : Fixer une hauteur minimale commune au panneau selon la largeur (min-height égale à la plus grande valeur, par exemple 720 px à 414 px et 700 px à 1024 px), ou réserver la place du contenu le plus long dans une grille aux 5 panneaux superposés (grid-area: 1/1) pour que la hauteur soit la plus grande des 5.
- Preuve du contradicteur : Playwright, clic sur #tab-0 à #tab-4, hauteur de #svc-panel : 345x740 [664,664,664,716,639] ; 414x896 [671,711,645,671,620] ; 1024x768 [675,675,675,700,675] ; 1440x900 [748,748,748,748,748] ; scrollHeight de la page 345 px : 17566/17566/17566/17617/17540.

### ACCES-13 — LCP et charge du fil principal dégradés par l'animation du héros (mesure en environnement sans GPU)
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : faible
- Constat : Sans reduced-motion, le LCP (le titre h1) est mesuré à 2 564 ms sur ordinateur et 2 056 ms sur mobile, contre 936 ms et 1 332 ms avec reduced-motion. Le rendu WebGL des bulles génère en continu des tâches longues d'environ 110 à 250 ms (294 tâches sur 30 s en mobile), absentes en reduced-motion. Ces tâches sont probablement amplifiées par le rendu WebGL logiciel (SwiftShader) de cet environnement, donc la gravité réelle sur un appareil avec GPU n'est pas établie.
- Attendu : LCP < 2,5 s et pas de tâches longues répétées sur le fil principal (limite de réactivité INP).
- Preuve : PerformanceObserver : ordinateur lcp=2564 (SPAN.in), mobile lcp=2056 (P.lede) ; avec reduce 936 et 1 332. longtask : 294 entrées, max 200 ms (mobile) ; 3 et 2 avec reduce. Sans simulation de réseau ni de processeur.
- Recommandation : Mesurer sur un vrai mobile milieu de gamme (Lighthouse / PageSpeed Insights sur https://juicecraft.fr/). Si confirmé : limiter le canvas WebGL à une résolution plus faible (dpr plafonné à 1 sur mobile), retarder son démarrage de 1 s après le LCP (requestIdleCallback) et le suspendre quand l'onglet n'est pas visible (déjà fait pour le défilement).
- Preuve du contradicteur : PerformanceObserver largest-contentful-paint : défaut ordinateur [1048 SPAN.rot-w, 2472 SPAN.in] ; reduced-motion ordinateur [944, 992] ; mobile [888 P.eyebrow, 1200 SPAN.in, 2300 P.lede]. Chromium lancé avec --disable-3d-apis --disable-gpu : LCP ordinateur 2388 (SPAN.in), mobile 2076 (P.lede), longtasks 3 et 1. CDP Network.emulateNetworkConditions (1,6 Mbit/s, 150 ms) + CPU x4, sans WebGL : FCP 1188, LCP 2392 (P.lede). CSS : .rv.play{animation:rvIn .95s ...;animation-delay:var(--d,0s)}.

### ACCES-M3 — Polices chargées depuis Google : feuille de style bloquante et connexions tierces sans information aux visiteurs
- Zone : Accessibilité, performance et robustesse
- Gravité : faible | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Les quatre familles de polices sont chargées depuis fonts.googleapis.com (feuille de style bloquante pour le rendu) et fonts.gstatic.com (5 fichiers), soit 6 des 14 requêtes de la page et deux origines tierces supplémentaires à ouvrir. Chaque visiteur transmet donc son adresse IP à Google, alors que le site n'a aucune politique de confidentialité accessible. Le comportement sans ces polices est correct (page stable, CLS 0,0003, aucune erreur), donc c'est un gain de performance et de conformité, pas une panne.
- Attendu : Polices servies depuis le domaine du site (auto-hébergées, avec font-display: swap) pour supprimer les connexions tierces et le blocage du rendu.
- Preuve : HTML : <link rel="preconnect" href="https://fonts.googleapis.com">, <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>, <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mona+Sans:wdth,wght@75..125,200..900&family=Instrument+Sans...&display=swap">. CDP Network : requêtes par hôte juicecraft.fr 3, fonts.googleapis.com 1, fonts.gstatic.com 5, data: 4. Test avec fonts.googleapis.com et fonts.gstatic.com bloqués (route abort) : load 1 060 ms, h1 249 px, CLS 0,0003, 0 erreur.
- Recommandation : Avec l'accord du propriétaire, télécharger les fichiers woff2 des quatre familles, les déposer dans le dépôt, déclarer les @font-face avec font-display: swap et retirer les trois balises <link> Google. L'aspect juridique du transfert d'adresses IP relève du propriétaire (niveau 3) ; la partie technique reste au niveau 2.

### INFRA-04 — Clé Web3Forms publique sans restriction de domaine ; anti-spam uniquement côté navigateur
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : La clé d'accès est lisible dans le HTML. Le honeypot (case botcheck masquée) n'est testé que par le JavaScript du site (le script s'arrête silencieusement si la case est cochée) et la requête envoie toujours botcheck: false. Toute personne ou robot qui envoie directement une requête à api.web3forms.com avec cette clé contourne ce garde-fou : spam dans la boîte du propriétaire et consommation du quota mensuel du compte, ce qui peut empêcher de vrais prospects d'écrire. Le risque est théorique : aucun envoi n'a été testé (règle 2).
- Attendu : Clé restreinte aux domaines juicecraft.fr et www.juicecraft.fr et/ou captcha serveur actif ; limite de quota connue et surveillée.
- Preuve : index.html ligne 1817 : const WEB3FORMS_KEY = "405f2edc-13c8-41a6-9d39-20234ec9be36" ; ligne 1237 : <input class="hp" type="checkbox" name="botcheck" id="f-hp" ...> ; ligne 1825 : if ($("#f-hp").checked) return; ; ligne 1849 : botcheck: false. Documentation officielle Web3Forms : « You do not need to hide the access key. Access key is public. » et si quelqu'un l'obtient il « can only send you emails » (https://docs.web3forms.com/getting-started/faq) ; « Restrict to Domain : This is a PRO feature. You must have an active subscription to use this feature... even if someone else got the access key, they cannot send emails to you » (https://docs.web3forms.com/getting-started/pro-features/restrict-to-domain) ; Web3Forms dit exécuter « a server-side spam check on all form submissions » et ne marque que reCaptcha comme Pro (https://docs.web3forms.com/getting-started/customizations/spam-protection).
- Recommandation : 1) Dans le tableau de bord Web3Forms (compte du propriétaire), consulter le plan du compte et le quota mensuel ; si possible activer « Restrict to Domain » avec la valeur exacte `juicecraft.fr, www.juicecraft.fr` (sans https://, option Pro) ; tester le formulaire en production juste après (l'option bloque aussi localhost). 2) À défaut, activer hCaptcha (non marqué Pro dans la documentation) ; cela exige une modification du formulaire et une publication. 3) Régler une alerte de quota. Le chiffre de 250 envois/mois en offre gratuite provient de sites tiers, pas de la documentation officielle : à vérifier dans le compte.
- Preuve du contradicteur : /home/user/juicecraft-site/index.html : l.1817 const WEB3FORMS_KEY = "405f2edc-..." ; l.1237 <input class="hp" type="checkbox" name="botcheck" id="f-hp"> ; l.1826 if ($("#f-hp").checked) return; ; l.1849 botcheck: false. WebFetch https://docs.web3forms.com/getting-started/pro-features/restrict-to-domain : « Restrict to Domain » est une fonction PRO (« You must have an active subscription to use this feature »).

### INFRA-06 — Page 404 par défaut de Netlify, en anglais et sans lien de retour
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Une adresse inexistante affiche la page d'erreur générique de Netlify (lang="en", titre « Page not found »), sans identité juicecraft ni lien vers l'accueil, ce qui dégrade l'expérience pour un site en français.
- Attendu : Une page 404 en français, aux couleurs du site, avec lien vers l'accueil.
- Preuve : https://juicecraft.fr/page-inexistante-xyz -> HTTP/2 404, content-type text/html, 3 633 octets, corps commençant par <html lang="en"> ... <title>Page not found</title>. /404.html -> 404 : aucun fichier 404.html dans le dépôt (3 fichiers : README.md, _headers, index.html).
- Recommandation : Après accord, ajouter à la racine du dépôt un fichier 404.html minimal en français (<html lang="fr">, titre « Page introuvable · juicecraft », texte « Cette page n'existe pas ou a été déplacée. » et lien « Retour à l'accueil » vers /), avec <meta name="robots" content="noindex">. Netlify sert un 404.html placé à la racine (comportement connu, à confirmer dans la documentation Netlify avant publication). Vérifier ensuite que le code HTTP reste 404.
- Preuve du contradicteur : curl -s -D - https://juicecraft.fr/page-inexistante-xyz -> HTTP/2 404, content-type text/html; charset=utf-8, 3 633 octets ; corps : `<html lang="en">` et `<title>Page not found</title>` ; https://juicecraft.fr/404.html -> 404 ; git ls-files = README.md, _headers, index.html.

### INFRA-07 — README.md du dépôt servi publiquement
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Le fichier README.md est accessible à tous sur le site. Il ne contient aucun secret, mais décrit la chaîne de publication interne (Netlify ou Cloudflare Pages, branche main) et n'a pas vocation à être public.
- Attendu : Seuls les fichiers du site sont servis (README.md en 404, comme DELEGATION.md).
- Preuve : GET https://juicecraft.fr/README.md -> HTTP 200, content-type text/markdown; charset=UTF-8, 840 octets, identique au README.md du dépôt (diff vide).
- Recommandation : Après accord, soit publier depuis un sous-dossier (par exemple /public) et laisser le README à la racine, soit ajouter un fichier _redirects contenant la ligne `/README.md /404.html 404!` (syntaxe à valider dans la documentation Netlify). Vérifier ensuite que /README.md renvoie 404.
- Preuve du contradicteur : curl -s -D - https://juicecraft.fr/README.md -> HTTP/2 200, content-type text/markdown; charset=UTF-8, 840 octets ; diff <(curl -s https://juicecraft.fr/README.md) /home/user/juicecraft-site/README.md -> vide (identique).

### INFRA-08 — Aucune Content-Security-Policy
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : Aucun en-tête Content-Security-Policy n'est envoyé ; X-Frame-Options (SAMEORIGIN) est présent mais l'équivalent moderne frame-ancestors est absent. Le site est statique avec un seul formulaire, donc le risque est limité, mais une CSP réduirait l'impact d'une éventuelle injection.
- Attendu : CSP au moins en mode rapport (Report-Only), compatible avec les scripts en ligne du site et le badge Netlify s'il est conservé.
- Preuve : curl -D - https://juicecraft.fr/ : en-têtes = permissions-policy, referrer-policy, strict-transport-security, x-content-type-options, x-frame-options ; aucun content-security-policy. _headers du dépôt : 4 règles, sans CSP. Doc Netlify : une CSP sans 'unsafe-inline' dans script-src empêche l'affichage du badge ; la page contient des <script> et <style> en ligne.
- Recommandation : Après accord, ajouter dans _headers (sous /*) d'abord en rapport seulement : `Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'self' https://api.web3forms.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self'` (valeurs à ajuster : ajouter https://fonts.googleapis.com et https://fonts.gstatic.com tant que INFRA-02 n'est pas traité, et app.netlify.com dans form-action si le badge reste ; ouvrir la console du navigateur pour repérer les blocages avant de passer en mode bloquant). Ne pas activer la CSP bloquante sans test.
- Preuve du contradicteur : curl -s -D - https://juicecraft.fr/ (HTTP/2 200) : en-têtes = permissions-policy, referrer-policy, strict-transport-security, x-content-type-options, x-frame-options, etc. ; aucun content-security-policy ; /home/user/juicecraft-site/_headers = 4 règles sous /*, sans CSP.

### INFRA-09 — Enregistrements DNS résiduels de l'ancien hébergement OVH
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : moyenne
- Constat : La zone contient encore un TXT « 1|www.juicecraft.fr » à la racine et un sous-domaine ftp.juicecraft.fr en CNAME vers la racine (donc vers Netlify), vestiges probables de la configuration d'hébergement OVH. Ils ne causent pas de panne, mais encombrent la zone ; le TXT est hérité par ftp.juicecraft.fr. L'origine exacte du TXT n'est pas prouvée.
- Attendu : Zone ne contenant que les enregistrements utiles (A racine, CNAME www, MX, SPF, sous-domaines de messagerie).
- Preuve : https://dns.google/resolve?name=juicecraft.fr&type=TXT -> "v=spf1 include:mx.ovh.com -all" et "1|www.juicecraft.fr" (TTL 3600) ; ftp.juicecraft.fr CNAME -> juicecraft.fr. -> A 75.2.60.5 ; webmail.juicecraft.fr et les noms aléatoires -> NXDOMAIN.
- Recommandation : Dans l'espace client OVH (zone DNS), identifier l'origine du TXT « 1|www.juicecraft.fr » (marqueur lié à l'hébergement/multisite OVH, à confirmer) et, s'il n'est plus utile, le supprimer avec l'accord du propriétaire ; supprimer ou laisser ftp selon l'usage. Ne PAS toucher au TXT SPF ni aux MX. Faire une copie de la zone avant toute modification.
- Preuve du contradicteur : https://cloudflare-dns.com/dns-query?name=juicecraft.fr&type=TXT -> "1|www.juicecraft.fr" et "v=spf1 include:mx.ovh.com -all" (TTL 3600) ; https://dns.google/resolve?name=ftp.juicecraft.fr&type=A -> CNAME juicecraft.fr. puis A 75.2.60.5 ; ssh/cloud/webmail.juicecraft.fr -> Status 3.

### INFRA-10 — MTA-STS et TLS-RPT absents
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 2 | Statut : confirmé | Confiance : haute
- Constat : Aucune politique MTA-STS ni rapport TLS-RPT n'est publié : le chiffrement TLS des e-mails entrants n'est pas imposé aux expéditeurs. Amélioration optionnelle pour un petit studio, moins prioritaire que DMARC.
- Attendu : Au minimum TLS-RPT en rapport, MTA-STS en mode testing, une fois DMARC en place.
- Preuve : https://dns.google/resolve?name=_mta-sts.juicecraft.fr&type=TXT -> Status 3 ; https://dns.google/resolve?name=_smtp._tls.juicecraft.fr&type=TXT -> Status 3.
- Recommandation : À traiter après INFRA-01. TLS-RPT : TXT _smtp._tls.juicecraft.fr de valeur `v=TLSRPTv1; rua=mailto:<adresse de rapports>`. MTA-STS nécessite en plus un TXT _mta-sts (v=STSv1; id=<date>) et un fichier https://mta-sts.juicecraft.fr/.well-known/mta-sts.txt hébergé séparément (mode testing, mx: mx1.mail.ovh.net, mx2.mail.ovh.net, mx3.mail.ovh.net), ce qui ajoute un hébergement à maintenir : à décider avec le propriétaire, pas urgent.
- Preuve du contradicteur : https://dns.google/resolve?name=_mta-sts.juicecraft.fr&type=TXT -> Status 3 ; https://dns.google/resolve?name=_smtp._tls.juicecraft.fr&type=TXT -> Status 3.

### INFRA-M3 — robots.txt et sitemap.xml absents (404)
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 2 | Statut : trouvé par le contradicteur (non contre-vérifié) | Confiance : haute
- Constat : Le site ne publie ni robots.txt ni sitemap.xml ; ces adresses renvoient la page 404 Netlify en HTML. Pour un studio dont l'activité est de créer des sites, c'est un manque de référencement de base, sans effet bloquant (un 404 sur robots.txt équivaut à « tout autoriser »).
- Attendu : Un robots.txt minimal pointant vers un sitemap.xml listant https://juicecraft.fr/.
- Preuve : curl -s -o /dev/null -D - https://juicecraft.fr/robots.txt -> HTTP/2 404 content-type text/html; charset=utf-8, 3 633 octets ; https://juicecraft.fr/sitemap.xml -> HTTP/2 404 (même corps) ; git ls-files = README.md, _headers, index.html.
- Recommandation : Après accord, ajouter à la racine du dépôt un robots.txt (User-agent: * / Allow: / / Sitemap: https://juicecraft.fr/sitemap.xml) et un sitemap.xml à une URL, puis vérifier que les deux répondent 200 avec le bon type de contenu. À coordonner avec la zone référencement.

### PRIX-13 — Fiches boutique : vendeur « Ma boutique », titres en majuscules et étiquettes hétérogènes
- Zone : Prix, offres et cohérence des contenus
- Gravité : faible | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Le vendeur des 3 produits d'offre est « Ma boutique » (valeur par défaut) alors que les 3 produits de mise en place ont « juicecraft ». Titres « ESSENTIELLE », « PREMIUM », « SUR MESURE » en majuscules contre « Essentielle », « Premium », « Sur mesure » sur le site. Étiquettes : les offres ont « mensuel » (alors que l'annuel existe) et « site-internet », pas les produits de mise en place. Le handle de Premium est un emoji (🔵-premium-⭐), URL fragile.
- Attendu : Même vendeur « juicecraft » partout, intitulés alignés sur le site, étiquettes cohérentes.
- Preuve : GraphQL products : vendor "Ma boutique" (3 offres) / "juicecraft" (3 mises en place) ; tags offres ["mensuel","service","site-internet",…], mise-en-place ["mise-en-place","service"] ; productType "Service" partout (cohérent) ; handle "🔵-premium-⭐".
- Recommandation : Passer le vendeur des 3 offres à « juicecraft » ; titres « Essentielle », « Premium », « Sur mesure » ; remplacer l'étiquette « mensuel » par « abonnement ». Ne pas changer le handle emoji sans créer une redirection et sans mettre à jour le lien du site (const SHOP).
- Preuve du contradicteur : curl /collections/all/products.json : vendor « Ma boutique » (essentielle, 🔵-premium-⭐, sur-mesure) / « juicecraft » (3 mises en place), tags essentielle/premium/sur-mesure contenant « mensuel » ; graphql_query products.vendor identique.

### PRIX-14 — Accueil boutique : méta-description absente et og:description « juicecraft »
- Zone : Prix, offres et cohérence des contenus
- Gravité : faible | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : L'accueil et le catalogue de la boutique n'ont pas de meta description ; l'accueil a og:title et og:description réduits à « juicecraft », alors que les pages offres ont des textes soignés avec prix.
- Attendu : Titre et description d'accueil décrivant l'offre et le prix d'appel.
- Preuve : curl https://juicecraft-store.myshopify.com/ : 0 balise <meta name="description">, <title>juicecraft</title>, og:description content="juicecraft" ; /collections/all : 0 meta description.
- Recommandation : Renseigner dans Shopify (Préférences) : titre « juicecraft · Sites internet sur mesure dès 49 €/mois TTC » et description « Trois offres de création de site internet à prix affichés TTC : Essentielle, Premium, Sur mesure. Mise en place unique, abonnement mensuel (12 mois d'engagement) ou annuel (2 mois offerts). »
- Preuve du contradicteur : curl https://juicecraft-store.myshopify.com/ (301 521 octets) : grep -c 'name="description"' = 0 ; <title>juicecraft</title> ; <meta property="og:title" content="juicecraft"> et <meta property="og:description" content="juicecraft">.

### PRIX-15 — Textes d'interface en anglais dans la boutique
- Zone : Prix, offres et cohérence des contenus
- Gravité : faible | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Des libellés de la boutique française restent en anglais : « You may also like » (pages produit, visible sur la capture), « View all » (panier), « Submit » (page Contact).
- Attendu : Interface entièrement en français.
- Preuve : Capture /tmp/audit-prix/shot_ess_bottom.png ; texte rendu de /cart (« You may also like », « View all ») et de /pages/contact (« Submit »).
- Recommandation : Traduire dans l'éditeur de thème : « Vous aimerez aussi », « Tout voir », « Envoyer ».
- Preuve du contradicteur : curl /pages/contact : « Submit » présent ; curl /cart : « View all » et « You may also like » présents ; curl /, /cart, /pages/contact : « Join our email list » et « Get exclusive deals » présents ; capture ess_rec.png.

### ACHAT-14 — Vendeur « Ma boutique » sur les offres et « juicecraft » sur les mises en place
- Zone : Parcours d'achat et page de paiement
- Gravité : faible | Niveau : 1 | Statut : confirmé | Confiance : haute
- Constat : Les produits d'abonnement ont le vendeur par défaut « Ma boutique », les produits de mise en place « juicecraft ». Ce champ peut apparaître dans les e-mails, factures et flux produits.
- Attendu : Vendeur « juicecraft » partout.
- Preuve : /collections/all/products.json : vendor « Ma boutique » pour ESSENTIELLE, PREMIUM, SUR MESURE ; « juicecraft » pour les 3 mises en place ; /cart/add.js : "vendor":"Ma boutique"
- Recommandation : Remplacer le vendeur par « juicecraft » sur les 3 produits d'offre (admin Shopify > produit > Organisation).
- Preuve du contradicteur : /collections/all/products.json et /products/<handle>.js : vendor « Ma boutique » (essentielle, 🔵-premium-⭐, sur-mesure) ; « juicecraft » (mise-en-place-essentielle, -premium, -sur-mesure-acompte).

### SEO-24 — Images produits sans texte alternatif défini et alt incohérents sur la boutique
- Zone : Référencement, contenu et rédaction
- Gravité : faible | Niveau : 1 | Statut : confirmé | Confiance : moyenne
- Constat : Les images des produits n'ont pas de texte alternatif dans Shopify (alt null dans les données). Le thème retombe sur le titre du produit, mais les cartes « Mise en place » reprennent un alt « Logo de l'offre Essentielle / Premium / Sur mesure » (alt du site, non du produit) et plusieurs images de l'accueil ont un alt vide.
- Attendu : Alt descriptif et propre à chaque image.
- Preuve : /products.json : images[].alt = null pour les 6 produits ; Playwright /products/essentielle : images alt « Logo de l'offre Essentielle » sur les cartes « Mise en place — ESSENTIELLE » et alt "" sur 3 images de l'accueil.
- Recommandation : Renseigner un alt dans Admin > Produits > image > Modifier le texte alternatif, par exemple « Emblème juicecraft de l'offre Essentielle », « Emblème juicecraft de l'offre Premium », « Emblème juicecraft de l'offre Sur mesure » ; pour les mises en place « Emblème juicecraft, mise en place de l'offre Premium ».
- Preuve du contradicteur : /products.json images[].alt = None x6 ; Playwright /products/essentielle : alts « ESSENTIELLE » (x4), « Logo de l'offre Essentielle/Premium/Sur mesure » (cartes mise en place), « PREMIUM » ; accueil boutique : alts « (vide), ESSENTIELLE, Logo de l'offre …, PREMIUM, SUR MESURE ».

### INFRA-11 — L'archive livrables/juicecraft-site.zip ne contient pas _headers
- Zone : DNS, e-mail, sécurité, dépôt et formulaire
- Gravité : faible | Niveau : 1 | Statut : confirmé | Confiance : moyenne
- Constat : Le zip de livraison ne contient que index.html. Si ce zip est un jour déposé tel quel sur Netlify (glisser-déposer) au lieu de passer par le dépôt, les en-têtes de sécurité seraient perdus. DELEGATION.md cite encore ce zip comme support de mise à jour du site alors que la publication passe désormais par le dépôt (branche main).
- Attendu : Archive de secours identique au contenu du dépôt (index.html + _headers + éventuels 404.html).
- Preuve : unzip -l /home/user/juicecraft/livrables/juicecraft-site.zip -> 1 fichier : index.html (199 948 octets) ; _headers absent ; /home/user/juicecraft-site contient index.html, _headers, README.md.
- Recommandation : Lors du prochain rapport, régénérer le zip avec index.html et _headers (et 404.html si ajouté), ou le déclarer obsolète dans DELEGATION.md. Modification de fichiers locaux soumise à la délégation ; aucune modification faite ici.
- Preuve du contradicteur : unzip -l /home/user/juicecraft/livrables/juicecraft-site.zip -> 1 fichier, index.html (199 948 octets), pas de _headers ; /home/user/juicecraft/DELEGATION.md l.5 : « mise à jour du site dans le zip (livrables/juicecraft-site.zip) » ; l.21 : déploiement par le dépôt GitHub, branche main.

## Annexe B. Contrôles réussis (119)

### Prix, offres et cohérence des contenus
- Prix des 3 cartes d'offres du site (HTML brut curl + texte rendu Playwright) conformes à la grille TTC — https://juicecraft.fr : 49 €/mois TTC, 490 € TTC/an, + 290 € ; 89 €/mois, 890 €/an, + 590 € ; 149 €/mois, 1 490 €/an, mise en place dès 1 690 € TTC sur devis (H
- Note sous les cartes, FAQ « Combien coûte un site internet ? » et section Contact cohérentes avec la grille, mention TTC présente — Note : « Tous les prix sont TTC… L'abonnement mensuel engage sur 12 mois, l'abonnement annuel offre 2 mois. » ; FAQ : 290/49/490, 590/89/890, dès 1 690/149/1 49
- Configurateur : seul prix cité (« à partir de 149 € par mois TTC, mise en place sur devis ») conforme — Code JS de juicecraft.fr, fonction recommend(), cas g === "specific" ; aucun autre montant dans le configurateur
- Métadonnées du site sans prix ni ancien prix — <title>juicecraft · Création de sites internet sur mesure</title>, meta description et og:description sans montant
- Page en ligne identique au dépôt hors injection Netlify — diff live.html /home/user/juicecraft-site/index.html : une seule ligne différente, le script <script async src="/.netlify/scripts/hud?variant=public"> ; aucun c
- Dépôt, deploy/index.html, livrables/index.html et zip identiques — md5 dd5cd3d521ac93e9d7bf9631c11c63d3 pour /home/user/juicecraft-site/index.html, deploy/index.html, livrables/index.html et juicecraft-site.zip!index.html (1999
- Source index.html conforme au déploiement, aux différences de build près — diff source/dépôt : 23 lignes, uniquement l'en-tête/pied (head, title, favicon), const SHOP et WEB3FORMS_KEY, produits par build_deploy.py
- Prix en centimes des 6 produits conformes — /products/<handle>.js : mise-en-place-essentielle 29000, mise-en-place-premium 59000, mise-en-place-sur-mesure-acompte 169000 ; plans : 4900/49000, 8900/89000, 
- Plans Appstle : MIN_CYCLES et arithmétique — GraphQL read-only : 3 plans mensuels minCycles=12, 3 annuels minCycles=null ; 490 = 10 x 49, 890 = 10 x 89, 1 490 = 10 x 149 ; options[0].value contient MIN_CYC
- Produits non expédiables, taxables, actifs — requires_shipping=false et taxable=true sur les 6 variantes ; status ACTIVE (graphql_query) ; panier : « Droits de douane et taxes inclus »
- Totaux de paniers réels (contexte jetable) conformes — Essentielle mensuel+mise en place = 33 900 c (339 €) ; Essentielle annuel+MEP 78 000 ; Premium mensuel 67 900 ; Premium annuel 148 000 ; Sur mesure mensuel 183 
- Totaux de première année (non annoncés nulle part, calculés) — Mensuel 12 x mensualité + MEP : 878 / 1 658 / 3 478 € ; annuel + MEP : 780 / 1 480 / 3 180 € ; aucun total annoncé sur le site, la boutique ou les vidéos donc a
- Liens des descriptions Shopify et boutons du site en HTTP 200 — /products/mise-en-place-essentielle, -premium, -sur-mesure-acompte : 200 ; boutons du site vers /products/essentielle, /products/%F0%9F%94%B5-premium-%E2%AD%90,
- Textes des 3 descriptions annonçant le montant de mise en place conformes — « Mise en place obligatoire (290 € TTC… », « (590 € TTC… », « Acompte… (1 690 € TTC… montant définitif confirmé par devis) »
- og:title et meta description des 3 pages offres cohérents avec la grille — « dès 49 €/mois TTC ou 490 €/an, mise en place 290 € », « dès 89 €/mois… 890 €/an, mise en place 590 € », « dès 149 €/mois… 1 490 €/an, mise en place sur devis 
- Aucun ancien prix en ligne (39, 69, 79, 119, 129, 399, 499, 799, 899, 1 199, 1 499 €) — grep sur live.html, rendered.txt, 6 pages produit, 6 .js, all.json, accueil et collection boutique : 0 occurrence ; seuls autres montants : 48/32/24/56 € des pr
- « Devis détaillé avant tout paiement » absent du site et de la boutique en ligne — grep sur live_text.txt et page1..6.html : 0 ; « sur devis » n'apparaît que pour la mise en place Sur mesure (conforme) et « au-delà sur devis » (modifications)
- Vidéos 30 s actuelles (livrables/juicecraft_pub_30s_16x9.mp4 et 9x16.mp4) : méthode et prix conformes sauf « /mois » — Images à 18,5 s (méthode 5 étapes), 23,8 s (offres) : 49 €, 89 €, 149 €, + 290 €, + 590 €, mise en place sur devis, « Prix clairs, affichés TTC. » ; 28,5 s : lo
- Vidéos 15 s sans prix — juicecraft_pub_16x9.mp4 (15 s) planche 1 image/s : aucune carte d'offre ; video.html sans « € » ; seul « Tarifs 2011 » (maquette d'ancien site fictif)
- Grille de DELEGATION.md identique à la grille de référence — 290/590/dès 1 690 ; 49/89/149 ; 490/890/1 490 ; plans Mensuel MIN_CYCLES=12, Annuel NULL

### Parcours d'achat et page de paiement
- Accueil juicecraft.fr : 3 boutons data-plan avec bon href — curl https://juicecraft.fr/ -> 200 ; essentielle -> https://juicecraft-store.myshopify.com/products/essentielle ; premium -> /products/%F0%9F%94%B5-premium-%E2%
- Clic réel ordinateur 1440x900 sur les 3 boutons — Playwright : essentielle -> .../products/essentielle?selling_plan=692928774478&variant=61108150141262 (titre « ESSENTIELLE — Création de site internet dès 49 €/
- Clic réel mobile 390x844 sur le bouton Premium — Playwright mobile : arrivée sur .../products/%F0%9F%94%B5-premium-%E2%AD%90?selling_plan=692928807246&variant=61108252180814, 1 onglet
- Bloc d'abonnement visible et au-dessus du bouton d'achat (12 scénarios : 6 ordinateur, 6 mobile) — res-*.json : wVis=true et position du bloc inférieure à celle du bouton partout ; ordinateur 281 px contre 542 px, mobile 653 px contre 913 px ; libellés « Abon
- Prix du haut de page et du bloc suivent le choix de périodicité — Essentielle 49 € / 490 € ; Premium 89 € / 890 € ; Sur mesure 149 € / 1.490 € (premiers éléments .price après sélection dans res-*.json, desktop et mobile)
- Lien « mise en place obligatoire » dans la description, visible, vers le bon produit — Description : « Mise en place obligatoire (290 € TTC, payée une seule fois) : ajoutez-la au panier avant de payer » ; clic -> /products/mise-en-place-essentiell
- Ajout au panier : quantité 1, montant, nom du plan (12 scénarios) — /cart.js : Essentielle 4900 « Abonnement Mensuel » / 49000 « Abonnement Annuel » ; Premium 8900 / 89000 ; Sur mesure 14900 / 149000 ; quantité 1
- Totaux avec mise en place conformes à la grille — /cart.js total_price : Essentielle 33900 (mensuel) et 78000 (annuel) ; Premium 67900 et 148000 ; Sur mesure 183900 et 318000 (acompte 169000)
- Checkout atteint pour les 3 paniers demandés, en français, sans champ de livraison — Redirections vers /checkouts/cn/.../fr-fr (html lang fr-FR) ; seulement « Adresse de facturation » (pays, prénom, nom, adresse, code postal, ville, téléphone op
- Lignes, sous-total récurrent et périodicité au checkout — Essentielle mensuel : « Mise en place — ESSENTIELLE 290,00 € », « ESSENTIELLE Abonnement Mensuel 49,00 € », « Sous-total récurrent 49,00 € par période de mois »
- Format des montants au checkout — Symbole € après le montant avec espace insécable : « 339,00 € », « 1 839,00 € »
- Moyens de paiement proposés — Paiement express Shop Pay et PayPal ; Carte de crédit (Visa, Mastercard, Amex +2) ; PayPal ; aucun clic sur un bouton de paiement
- Refus d'un abonnement sans selling_plan — POST /cart/add.js (variantes 61108150141262, 61108252180814, 61108309360974 sans plan) -> 422 « La variante peut seulement être achetée avec un forfait de vente
- Aucune règle parasite de quantité minimale — POST /cart/add.js quantity 12 sur plan mensuel Essentielle -> 200, panier 58800 ; Premium mensuel 12 -> 200, 106800 (MIN_CYCLES=12 n'est que le paramètre du pla
- Page de confidentialité de la boutique accessible — GET https://juicecraft-store.myshopify.com/policies/privacy-policy -> 200, en français, mise à jour 9 octobre 2026 ; lien du pied de page checkout ouvre ce text
- Taxes incluses au niveau du réglage boutique — GraphQL shop { taxesIncluded } -> true ; devise EUR ; adresse de facturation FR
- Pages boutique : langue, produits visibles, nom et logo — html lang="fr" ; /collections/all liste 6 produits (3 offres + 3 mises en place) ; logo juicecraft et annonce « Bienvenue sur le shop de JUICECRAFT ! » présents
- Pas de débordement horizontal ni de texte tronqué au checkout — overflow-x=false (ordinateur) ; captures checkout ordinateur et mobile (390 px) lues : pas de chevauchement

### Référencement, contenu et rédaction
- Page d'accueil accessible, HTTP 200, compressée Brotli — curl -I https://juicecraft.fr/ -> HTTP/2 200, content-type text/html; charset=UTF-8, content-encoding: br, 200 132 octets
- Attribut lang — <html lang="fr"> lu dans le HTML brut
- Title présent et de longueur correcte — « juicecraft · Création de sites internet sur mesure » = 50 caractères (recommandé 30 à 60)
- Meta description présente et de longueur correcte — « juicecraft conçoit des sites internet sur mesure, rapides et soignés pour les artisans, commerces, cabinets et entreprises. » = 123 caractères (recommandé 70 
- Un seul h1 — 1 balise <h1> dans le HTML brut et dans le DOM rendu Playwright
- Aucune balise robots bloquante ni noindex sur le site — grep noindex|robots|canonical dans https://juicecraft.fr/ -> 0 occurrence (page indexable par défaut)
- Meta viewport et theme-color présents — <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"> et <meta name="theme-color" content="#F2F2EF">
- Open Graph partiel présent — og:type=website, og:locale=fr_FR, og:title « juicecraft · Des sites qui ont du jus », og:description présent (mais pas d'og:image ni d'og:url)
- Favicon SVG intégré (data URI) — <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,..."> présent dans le head
- Redirections http vers https et www vers domaine nu — http://juicecraft.fr/ -> 301 https://juicecraft.fr/ ; http://www.juicecraft.fr/ -> 301 https://www.juicecraft.fr/ -> 301 https://juicecraft.fr/ ; https://www.ju
- URL inexistante renvoie un vrai code 404 — https://juicecraft.fr/zzz-inexistante -> HTTP/2 404 (et non 200 : pas de soft 404)
- Contenu clé présent dans le HTML initial sans JavaScript — Dans le HTML brut : h1, 8 h2, titres h3 des offres, prix des 3 offres (49/89/149 € par mois, 490/890/1 490 € par an, 290/590/1 690 € de mise en place), 6 questi
- Liens externes de la page : codes HTTP — https://juicecraft-store.myshopify.com/products/essentielle -> 200 ; .../products/%F0%9F%94%B5-premium-%E2%AD%90 -> 200 ; .../products/sur-mesure -> 200 ; feuil
- Liens internes (ancres) cohérents avec les sections — Ancres #services, #approche, #methode, #realisations, #offres, #faq, #contact, #configurateur, #top, #main correspondent à des id existants ; libellés des liens
- Alt des images — 3 balises <img> (logos des offres) avec alt « Logo de l'offre Essentielle / Premium / Sur mesure » ; le reste est en SVG décoratif aria-hidden
- Doublon netlify.app : canonical par en-tête HTTP, pas de noindex — curl -D- https://sparkling-bubblegum-b2d478.netlify.app/ -> HTTP/2 200 et en-tête « link: <https://juicecraft.fr/>; rel="canonical" » ; 0 occurrence de noindex 
- En-têtes de cache et de sécurité — cache-control: public,max-age=0,must-revalidate + etag (revalidation systématique, cohérent pour un site statique sans build) ; strict-transport-security: max-a
- Messages d'erreur du formulaire (sans envoi) — Soumission à blanc en bloquant l'appel réseau Web3Forms : « Indiquez votre nom pour que l'on sache à qui répondre. » et « Vérifiez l'adresse : elle doit ressemb
- Relecture orthographe et grammaire du texte visible et des textes générés par script — Relecture complète (HTML brut, DOM rendu, tableaux SVC, Q, recommend du script) : aucune faute d'orthographe ni de grammaire repérée (confiance moyenne : relect
- Vouvoiement cohérent — Aucun « tu/ton/ta » dans le texte visible ; « vous / votre » partout (seule nuance : « On lui redonne du jus », voir constat)
- Montants et grille de prix du site conformes à la référence — Essentielle 49 €/mois, 490 €/an, 290 € ; Premium 89, 890, 590 ; Sur mesure 149, 1 490, dès 1 690 € ; engagement de 12 mois ; « 2 mois offerts » : tous lus sur h
- Boutique : robots.txt valide et non bloquant — https://juicecraft-store.myshopify.com/robots.txt -> 200, « User-agent: * Allow: / », Disallow limité à /admin, /cart/, /checkout, /orders, /account ; ligne « S
- Boutique : sitemap.xml valide — /sitemap.xml -> 200 (index) ; sitemap_products_1.xml liste /products/essentielle, /products/%F0%9F%94%B5-premium-%E2%AD%90, /products/sur-mesure ; pages (/pages
- Boutique : fiches produit avec méta, canonical, Open Graph et Twitter — /products/essentielle : title « ESSENTIELLE — Création de site internet dès 49 €/mois TTC – juicecraft », meta description « Site internet dès 49 €/mois TTC ou 
- Boutique : une seule h1 par fiche, 404 renvoie bien 404 — h1 unique sur les 6 fiches produit ; /zzz-inconnu -> HTTP/2 404 avec titre « 404 Page introuvable – juicecraft »
- Boutique : offre achetable uniquement en abonnement avec fréquence en français — Page rendue /products/essentielle : seule option « Abonnement », « Fréquence de facturation » = « Abonnement Mensuel / Abonnement Annuel », aucun bouton d'achat
- Boutique : cohérence des prix de mise en place et des plans avec la grille — /products.json : mise-en-place-essentielle 290.00, mise-en-place-premium 590.00, mise-en-place-sur-mesure-acompte 1690.00 ; plans Premium 8900 / 89000 et Sur me

### Juridique, vie privée et allégations commerciales
- Aucun cookie, localStorage ni sessionStorage déposé par juicecraft.fr au chargement (Playwright, contexte vierge, après networkidle + 3 s) — ctx.cookies() = [] ; localStorage = [] ; sessionStorage = []
- Requêtes tierces de juicecraft.fr limitées aux polices Google ; aucun outil de mesure d'audience, pixel ou iframe tiers — Hôtes observés : juicecraft.fr, fonts.googleapis.com (css2?family=Mona+Sans…), fonts.gstatic.com (4 woff2). Aucun Google Analytics, Meta, Hotjar, etc.
- Le script /.netlify/scripts/hud?variant=public ne fait aucun appel sortant au chargement ni de dépôt de stockage — GET https://juicecraft.fr/.netlify/scripts/hud?variant=public = 200 (34 481 octets, application/javascript). Lecture du code : fetch/XHR/sendBeacon absents ; se
- Mentions « concept fictif » des réalisations présentes — Texte visible : « Notre portfolio se construit. Voici des concepts de démonstration, fictifs, qui montrent notre approche. » et « CONCEPT FICTIF » sous les 4 ré
- Mention TTC présente et prix du site cohérents avec la grille — Site : « 49 €/mois TTC ou 490 € TTC par an + 290 € TTC de mise en place », 89/890/590, 149/1 490/« dès 1 690 € TTC » ; phrase « Tous les prix sont TTC » ; FAQ «
- Engagement de 12 mois et 2 mois offerts annoncés sur le site — Texte : « L'abonnement mensuel engage sur 12 mois, l'abonnement annuel offre 2 mois. » et « 12 mois d'engagement en paiement mensuel » (section Offres et FAQ).
- Prix Shopify conformes à la grille ; taxes incluses dans la boutique ; plans Appstle conformes — /collections/all/products.json : essentielle 490.00, premium 89.00 (variante de base, plans 8900/89000), sur-mesure 149.00 ; mise-en-place 290/590/1690. graphql
- Politique de confidentialité Shopify en ligne, en français, datée, avec responsable de traitement et droits RGPD — GET /policies/privacy-policy = 200, « Dernière mise à jour : 9 octobre 2026 », section Contact : evannlassalle@gmail.com, 9 rue de St Pol, 62270 Conchy sur Canc
- Lien Politique de confidentialité présent dans le pied de page de la boutique et le panier ; la réponse du formulaire de contact du site n'est pas déclenchée par l'audit — Pied de page boutique : « Politique de confidentialité => /policies/privacy-policy ». Aucun envoi du formulaire Web3Forms n'a été effectué.
- En-têtes de sécurité du site présents — curl -I https://juicecraft.fr/ : strict-transport-security, x-content-type-options: nosniff, x-frame-options: SAMEORIGIN, referrer-policy: strict-origin-when-cr
- Le paiement est traité sur le paiement Shopify chiffré (aucune saisie de carte sur le site) et le consentement à l'abonnement est affiché avant paiement — Page de paiement : « Toutes les transactions sont sécurisées et chiffrées. » ; panier : « En continuant, j'accepte la politique de résiliation et vous autorise 

### Accessibilité, performance et robustesse
- Chargement et poids de la page (ordinateur 1440x900, mobile 390x844) — https://juicecraft.fr/ HTTP 200, HTML 200 132 octets (55 Ko compressé). Événement load à 1 489 ms (ordinateur) et 1 138 ms (mobile), TTFB 151 à 454 ms, FCP 636 
- Erreurs console, JavaScript et ressources en échec — Aucun événement pageerror, aucune requête échouée (requestfailed vide), aucune réponse HTTP >= 400 sur 4 parcours (ordinateur/mobile, avec et sans reduced-motio
- Aucune dérive de mise en page au repos pendant 30 s, sans interaction (correction du 9 octobre 2026) — 10 relevés espacés de 3 s : scrollHeight constant (11 727 px ordinateur, 16 904 px mobile), hauteurs des 11 sections/en-tête/pied identiques, hauteurs des carte
- Mot rotatif du titre : jamais 4 lignes — Pour chacun des 7 mots (commerce, atelier, cabinet, restaurant, entreprise, boutique, projet), hauteur du h1 identique à 320, 360, 390 px (121 px = 3 lignes de 
- CLS (PerformanceObserver layout-shift, 30 s sans interaction) — Ordinateur 0,044 (37 petits décalages de 0,0001 à 0,006, essentiellement le mot rotatif et la démo animée du héros), mobile 0,0115, tous sous le seuil de 0,1. D
- prefers-reduced-motion: reduce arrête les animations — Avec reduce : mot rotatif figé sur « commerce » pendant 30 s, 2 décalages de mise en page seulement (CLS 0,0035 ordinateur, 0,0022 mobile), tâches longues 3 (or
- Pas de défilement horizontal (320, 390, 820, 1440 px) ni au zoom 200 % — document.documentElement.scrollWidth - clientWidth = 0 à 320, 345, 360, 390, 414, 600, 720 (équivalent zoom 200 % de 1440), 768, 820, 1024, 1280 et 1440 px. Le 
- Langue, titre, viewport, zoom — <html lang="fr">, <title>juicecraft · Création de sites internet sur mesure</title>, meta viewport « width=device-width, initial-scale=1, viewport-fit=cover » (
- axe-core (installé par npm dans /tmp/audit-acces, v la plus récente disponible) sur ordinateur, mobile, menu mobile ouvert et FAQ ouverte — 52 règles réussies (51 avec FAQ ouverte). Seules violations : color-contrast (8 à 13 nœuds) et heading-order (1 nœud). Aucune violation sur les noms accessibles
- Repères, titres, noms accessibles, textes alternatifs — header#nav, nav « Navigation principale », nav « Menu mobile », main#main, footer ; un seul h1 ; 3 images (logos d'offres) avec alt « Logo de l'offre Essentiell
- Lien d'évitement — a.skip « Aller au contenu » (href=#main) est le 1er arrêt de Tab ; hors focus il est à top:-80px (hors écran, vérifié à scrollY 0, 1500, 4000) ; au focus il app
- Navigation clavier sur toute la page, absence de piège — Parcours de 61 arrêts de Tab de la page au pied de page puis sortie de la page (body) sans blocage : liens du menu, CTA, commutateur de style de démo, onglets d
- Focus visible (mesuré 500 ms après le focus) — Liens, boutons, curseur et FAQ : contour solid 2px rgb(255,90,31). Champs de formulaire : bordure orange rgb(255,90,31) + halo rgba(255,90,31,0.15) 4 px. Une pr
- FAQ au clavier et états ARIA — Boutons #q1 à #q6 avec aria-expanded et aria-controls ; panneau role=region aria-labelledby. #q1 : Entrée -> aria-expanded=false, Espace -> true ; #q2 par Espac
- Onglets de services, commutateur de démo, interrupteurs — role=tablist / tabpanel, flèche bas passe de #tab-0 à #tab-1 (aria-selected + tabindex itinérant) ; commutateur role=radiogroup « Style du site de démonstration
- Menu mobile (390 px) — #burger 44x44 px, aria-expanded false->true, aria-label « Ouvrir/Fermer le menu », aria-controls=menu ; Entrée l'ouvre, Échap le ferme (aria-expanded=false, hid
- Taille des cibles tactiles (WCAG 2.5.8) — Sur mobile, seuls 12 liens < 24 px de haut (liens du pied de page 62x20, etc.), tous espacés d'au moins 15 px (distance centre à centre 35 px) : exception d'esp
- Formulaire de contact sans envoi (requêtes api.web3forms.com bloquées par page.route().abort()) — Champs vides -> « Indiquez votre nom pour que l'on sache à qui répondre. » et « Vérifiez l'adresse : elle doit ressembler à nom@domaine.fr. » (aria-live=polite)
- Honeypot — Case #f-honeypot f-hp : position absolute à left=-9895 px, opacity 0, tabindex=-1, aria-hidden=true ; cochée avec champs vides, le clic sur Envoyer ne produit n
- Curseur personnalisé et effets magnétiques — Actifs seulement si (hover:hover)(pointer:fine) et pas de reduced-motion ; #cur aria-hidden=true, pointer-events:none ; curseur natif conservé sur input/select/
- Contrôle visuel (captures plein écran et par section, ordinateur et mobile) — Aucune image manquante (3 images, naturalWidth 1000, complete=true), aucun texte tronqué dans les sections, carte « Maintenance possible » lisible (titre, texte

### DNS, e-mail, sécurité, dépôt et formulaire
- A de juicecraft.fr conforme (Netlify) — https://dns.google/resolve?name=juicecraft.fr&type=A -> 75.2.60.5, TTL 3600 ; Cloudflare (accept: application/dns-json) -> 75.2.60.5. Aucun AAAA (NOERROR, pas d
- www.juicecraft.fr = CNAME vers Netlify — type=CNAME -> sparkling-bubblegum-b2d478.netlify.app., TTL 3600, AD=true ; A résolu en 18.208.88.157 et 98.84.224.111 ; aucun A vers 51.91.236.255.
- Serveurs de noms et SOA OVH — NS = dns200.anycast.me. et ns200.anycast.me. (TTL 3600) ; SOA = dns200.anycast.me. tech.ovh.net. 2091582533 86400 3600 3600000 60.
- MX conformes et priorités cohérentes — MX : 1 mx1.mail.ovh.net., 5 mx2.mail.ovh.net., 100 mx3.mail.ovh.net. (TTL 3600) ; les trois noms résolvent en A (188.165.36.237, 87.98.160.167, 91.121.53.175).
- SPF valide, mécanisme final strict, include résolvable, bien sous 10 résolutions — TXT apex : "v=spf1 include:mx.ovh.com -all". L'include résout en "v=spf1 ptr:mail-out.ovh.net ptr:mail.ovh.net ip4:8.33.137.105/32 ip4:192.99.77.81/32 ?all" : 1
- DNSSEC en place et validé — DS 62926 algo 8, digest type 2 (36010691CE...DE40) présent ; DNSKEY 257 (KSK) et 256 (ZSK) algo 8 présents ; drapeau AD=true sur dns.google et cloudflare-dns.co
- Pas de caractère générique (wildcard) ni de CAA bloquant — zzrandom12345.juicecraft.fr A -> Status 3 (NXDOMAIN) ; CAA de juicecraft.fr -> NOERROR sans réponse (aucune restriction d'autorité de certification).
- Sous-domaines de messagerie OVH cohérents — mail/imap/smtp/pop3.juicecraft.fr = CNAME ssl0.ovh.net. (193.70.18.144) ; autoconfig/autodiscover = CNAME mailconfig.ovh.net. (213.186.33.5) ; webmail.juicecraf
- Le domaine ne mène plus à l'ancien serveur OVH — curl http://juicecraft.fr/ -> remote 75.2.60.5, en-tête server: Netlify, x-nf-request-id présent ; https://juicecraft.fr/ -> HTTP/2 200 server: Netlify ; www ->
- Redirections http vers https et www vers domaine nu — http://juicecraft.fr/ -> 301 https://juicecraft.fr/ ; http://juicecraft.fr/foo/bar?x=1 -> 301 https://juicecraft.fr/foo/bar?x=1 (chemin et requête conservés) ; 
- Connexion HTTPS aboutie sur les trois noms, HTTP/2 — curl https://juicecraft.fr/ et https://www.juicecraft.fr/ -> HTTP/2, certificat accepté par curl avec le CA du proxy (aucune conclusion sur l'émetteur ni l'expi
- En-têtes de sécurité du fichier _headers effectifs sur toutes les réponses — _headers du dépôt : X-Content-Type-Options: nosniff, Referrer-Policy: strict-origin-when-cross-origin, X-Frame-Options: SAMEORIGIN, Permissions-Policy: camera=(
- HSTS présent — strict-transport-security: max-age=31536000 sur https://juicecraft.fr/ et https://www.juicecraft.fr/ (valeur par défaut Netlify, absente de _headers) ; sans inc
- Compression, cache et en-têtes de page — Avec accept-encoding: br -> content-encoding: br, 55 584 octets contre 200 132 en identité ; vary: Accept-Encoding ; cache-control: public,max-age=0,must-revali
- Aucun cookie, aucun stockage local, aucun journal d'erreurs JavaScript — Playwright/Chromium sur https://juicecraft.fr/ : ctx.cookies() = [], localStorage vide, aucune erreur de page (seuls des avertissements WebGL de l'environnement
- Temps de réponse (TTFB) sur 5 mesures — curl https://juicecraft.fr/ : 0,110 / 0,165 / 0,137 / 0,135 / 0,146 s (moyenne 0,139 s ; total 0,12 à 0,18 s). Mesures indicatives : elles passent par le proxy 
- Fichiers inutiles non servis (sauf README.md, voir INFRA-08) — GET sur /.git/HEAD, /.git/config, /DELEGATION.md, /_headers, /build_deploy.py, /shop.json, /deploy/index.html, /livrables/, /netlify.toml, /404.html -> HTTP 404
- Le HTML publié est identique au dépôt hors injection Netlify — curl -H 'accept-encoding: identity' https://juicecraft.fr/ (200 132 octets) comparé à /home/user/juicecraft-site/index.html (199 948 octets) : diff = une seule 
- Pas de secret ni donnée personnelle dans le dépôt, le HTML publié et les fichiers locaux de travail — grep sur /home/user/juicecraft-site/index.html, README.md, _headers, /home/user/juicecraft/{index.html,deploy,build_deploy.py,shop.json,DELEGATION.md,logo/LISEZ
- Le script Netlify (/.netlify/scripts/hud?variant=public) n'émet aucune requête ni cookie — Script téléchargé (34 481 octets, application/javascript, cache-control public,max-age=60). Relecture : aucun fetch, XMLHttpRequest, sendBeacon, document.cookie
- Gestion d'erreur du formulaire présente (sans soumission) — index.html lignes 1822-1865 : validation nom + e-mail (regex), bouton désactivé pendant l'envoi, try/catch/finally, vérification res.ok et out.success, message 
- Erreurs 404 correctes côté protocole — https://juicecraft.fr/page-inexistante-xyz -> HTTP/2 404 (vrai code 404, pas de repli vers l'accueil), mêmes en-têtes de sécurité.

## Annexe C. Ce qui n'a pas pu être vérifié (59) et faux « OK » corrigés (4)

### Faux « OK » corrigés par les contradicteurs
- [Prix, offres et cohérence des contenus] Vidéos 30 s : prix conformes à la grille hors « /mois » ; ancien discours absent des versions à jour — résultat : ecart — ffmpeg à 24,5 s sur les deux vidéos 30 s : 49/89/149 € et 290/590 € corrects, « Prix clairs, affichés TTC. », mais « /mois » absent (voir PRIX-04) ; livrables/video/video30.html : étape 1 « Compte rendu et proposition claire » (ancien « devis détaillé » absent de la version à jour).
- [Prix, offres et cohérence des contenus] Prix TTC / TVA inclus à la caisse — résultat : non_concluant — Panier : « Droits de douane et taxes inclus » ; page de paiement (atteinte, rien saisi) : total 339,00 € mais aucune ligne de TVA ni mention TTC ; le taux de TVA du réglage de taxes de la boutique n'est pas lisible avec les outils autorisés.
- [Référencement, contenu et rédaction] Pages légales du site juicecraft.fr (contrôle présenté comme écart par l'auditeur) — résultat : ecart — https://juicecraft.fr/mentions-legales, /cgv, /confidentialite -> 404 ; libellés du pied de page non cliquables ; boutique : /policies/refund-policy 404, /policies/terms-of-service 404, /policies/privacy-policy 200.
- [Juridique, vie privée et allégations commerciales] Prix Shopify conformes à la grille, taxes incluses, plans Appstle conformes — résultat : ecart — Prix effectivement facturés conformes : cart/add.js (curl, panier jetable) annuel = 49 000 / 89 000 / 149 000 centimes ; allocations mensuelles 4 900 / 8 900 / 14 900 ; MIN_CYCLES=12 sur les 3 plans mensuels, NULL sur les annuels ; mises en place 29 000 / 59 000 / 169 000 ; shop.taxesIncluded = true ; ajout sans forfait refusé (422 « La variante peut seulement être achetée avec un forfait de vente »). Écart par rapport à la référence (prix de base = prix annuel) : prix de base 49 000 pour Essentielle mais 8 900 pour Premium et 14 900 pour Sur mesure ; le catalogue affiche €490,00 / €89,00 / €149,00 (voir LEGAL-M1). Le contrôle de l'auditeur l'avait noté entre parenthèses sans le signaler comme écart.

### Non vérifié
- Prix, offres et cohérence des contenus : Page de paiement Shopify (checkout) non ouverte : affichage des conditions d'abonnement, des taxes et de l'engagement à ce stade non contrôlé.
- Prix, offres et cohérence des contenus : Réglages et textes de l'application Appstle (portail client, conditions de résiliation, courriels d'abonnement), modèles d'e-mails de commande et de confirmation : non accessibles en lecture avec les outils autorisés.
- Prix, offres et cohérence des contenus : Capture d'écran de la page PREMIUM : chargement Playwright (networkidle) dépassé à deux reprises (probable lenteur de l'environnement) ; le défaut de prix de PRIX-01 y est déduit du texte rendu, confirmé par capture seulement sur la page Essentielle. La page Sur mesure ne reproduit pas le défaut dans le texte lu.
- Prix, offres et cohérence des contenus : Configurateur non parcouru en cliquant : les textes et la logique ont été lus dans le code source de la page en ligne, pas exécutés pas à pas.
- Prix, offres et cohérence des contenus : Vidéos : seules les images demandées (18,5 s, 23,8 s, 28,5 s ; plus 22,8 s et 24,5 s en 16:9), les anciens masters à 23,8 s et une planche à 1 image/s de la vidéo 15 s 16:9 ont été regardées ; la vidéo 15 s 9:16, les masters 15 s, le kit de logos (juicecraft_kit-logos.zip) et les fichiers du dossier video/review n'ont pas été inspectés image par image.
- Prix, offres et cohérence des contenus : Cause exacte de l'absence de « /mois » dans les vidéos (hypothèse CSS) non vérifiée par un nouveau rendu, car cela exigerait de modifier ou régénérer des fichiers.
- Prix, offres et cohérence des contenus : Réglage fiscal réel de la boutique (prix TTC, TVA 20 %) : seulement déduit de « Droits de douane et taxes inclus » dans le panier et de taxable=true ; pas de lecture du réglage de taxes.
- Prix, offres et cohérence des contenus : Contenu du dépôt GitHub distant : seul le clone local en lecture seule a été comparé à la page en ligne (identique) ; historique git non examiné pour d'anciens prix.
- Prix, offres et cohérence des contenus : Statut de publication par canal (Boutique en ligne, Google, Shop) et champs SEO des produits de mise en place (vides) : lecture GraphQL limitée aux produits ; canaux non interrogés.
- Parcours d'achat et page de paiement : Paiement réel, e-mail de confirmation, portail client Appstle et résiliation effective de l'abonnement : interdits (aucune commande), donc non testés ; le comportement du MIN_CYCLES=12 à la résiliation n'est pas vérifié.
- Parcours d'achat et page de paiement : Les 12 scénarios offre x périodicité x appareil ont été relus depuis les fichiers res-*.json de /tmp/audit-achat produits par un passage antérieur de scen.js (horodatés 23:14 à 23:31) ; je ne les ai pas réexécutés intégralement. Seules les valeurs ont été relues et recoupées avec la grille ; j'ai réexécuté moi-même l'ajout au panier et le checkout des 3 paniers demandés (ess-M, ess-A, mes-M) et les cas limites.
- Parcours d'achat et page de paiement : Checkout mobile : seule la capture mobile Essentielle mensuel a été lue ; le checkout Essentielle annuel et Sur mesure mensuel sur mobile n'a pas été relu visuellement. Les captures mobiles des fiches produit n'ont été lues que pour Essentielle annuel et Sur mesure mensuel.
- Parcours d'achat et page de paiement : Position exacte du symbole € et des taxes vérifiée sur ordinateur uniquement pour le checkout ; l'aperçu du récapitulatif mobile (Résumé de la commande) n'a pas été déplié.
- Parcours d'achat et page de paiement : Apple Pay / Google Pay et moyens de paiement conditionnels : un Chromium sans portefeuille ne les affiche pas ; la liste réelle des moyens activés (+2 cartes derrière « +2 ») n'a pas été dépliée.
- Parcours d'achat et page de paiement : Régime de TVA réel du propriétaire (franchise ou TVA 20 %) : inconnu ; la commande test #1001 à 0 de taxe pourrait précéder la configuration des taxes.
- Parcours d'achat et page de paiement : Fenêtre « Détails de l'abonnement » d'Appstle : texte lu ; le contenu éventuel d'un portail client ou d'e-mails Appstle n'a pas été consulté.
- Parcours d'achat et page de paiement : La zone vide de la page d'accueil de la boutique est observée après 3 s d'attente ; un contenu chargé plus tard (animation, image lente) n'est pas exclu.
- Parcours d'achat et page de paiement : Les liens « Remboursement » : le paiement ne propose aucun lien intitulé remboursement ; seul /policies/refund-policy a été testé (404). Le lien « Conditions » et la « Politique de confidentialité » de Shop au paiement mènent à des sites Shopify externes, non audités.
- Parcours d'achat et page de paiement : Test de connexion lente effectué une seule fois sur Essentielle en mobile émulé (400 kbit/s, 400 ms) ; non répété sur les autres offres.
- Référencement, contenu et rédaction : Indexation et positionnement réels dans Google : aucune requête vers un moteur de recherche (hors périmètre réseau), donc aucune donnée Search Console, pages indexées, requêtes ou erreurs d'exploration.
- Référencement, contenu et rédaction : Mesures de performance (Core Web Vitals, poids réel des polices Google Fonts) : hors mission de la zone ; seule la compression Brotli et les en-têtes de cache ont été lus.
- Référencement, contenu et rédaction : Panier, page de paiement et e-mails : non explorés. Le clic sur « Ajouter au panier » a été tenté dans un navigateur jetable mais n'a pas abouti (bouton hors zone visible) ; l'affichage de « Delivery every » dans le panier, le paiement, les e-mails de commande et l'espace client n'a donc pas été contrôlé, seul le nom de l'option dans /products/essentielle.js l'atteste.
- Référencement, contenu et rédaction : Effet réel au paiement du prix de base 89 € / 149 € des produits Premium et Sur mesure (SEO-18) : seule la donnée publique a été lue, aucune commande simulée.
- Référencement, contenu et rédaction : Réglage Netlify « domaine principal », déclenchant l'en-tête Link canonical du domaine netlify.app : lu uniquement dans la réponse HTTP, pas dans la console Netlify.
- Référencement, contenu et rédaction : Contenu des e-mails envoyés par la boutique et par Web3Forms, texte des CGV, politique de confidentialité de la boutique (non relue en détail) et formulaire de contact de la boutique (non soumis).
- Référencement, contenu et rédaction : Le point d'accès api.web3forms.com/submit a répondu 403 à une requête HEAD ; il n'a volontairement pas été testé en POST (envoi d'e-mail).
- Référencement, contenu et rédaction : Pages /blogs/actualites et /collections/frontpage de la boutique : présentes dans le sitemap, non relues.
- Référencement, contenu et rédaction : Rendu visuel sur mobile pour les coupures de ligne dans les montants : 390 px testé sur quelques montants seulement (aucune coupure observée), 320 px non testé.
- Référencement, contenu et rédaction : Recherche de fautes : relecture humaine des textes, sans correcteur orthographique automatisé externe ; les textes des maquettes volontairement fautives (« Bienvenue sur notre site !!! », « Tarifs 2011 », « Visiteurs : 001337 ») ont été considérés comme des caricatures intentionnelles.
- Juridique, vie privée et allégations commerciales : Formulaire de contact : aucun envoi réalisé (interdit, il enverrait un e-mail au propriétaire) ; durée de conservation, lieu de traitement (UE ou hors UE) et rôle de Web3Forms non sourcés : https://web3forms.com/privacy et la fonction WebFetch renvoient 403, et ce domaine est hors du périmètre réseau autorisé.
- Juridique, vie privée et allégations commerciales : Comportement du bandeau de cookies Shopify pour un visiteur situé en France : le test a été fait depuis un réseau non français (consentHeader « AMPS_US… ») ; le réglage « Confidentialité des clients » de Shopify n'est pas lisible avec les outils de lecture.
- Juridique, vie privée et allégations commerciales : Portail client Appstle (résiliation en ligne, accès « résilier votre contrat ») : accessible seulement après une vraie commande ; non testé. Contenu des e-mails de confirmation de commande et des e-mails d'abonnement non vu.
- Juridique, vie privée et allégations commerciales : Contenu exact des textes de loi : Légifrance et plusieurs pages economie.gouv.fr renvoient 403 à WebFetch ; les références (LCEN art. 1-1, Code de la consommation L215-1-1, D215-1/D215-2, L221-3, L221-5, L221-18, L221-28, L612-1, L616-1/R616-1, CNIL cookies et prospection) proviennent des résultats de recherche sur les sites officiels, pas d'une relecture intégrale : toutes les obligations sont « à faire valider ». Art. L112-1 (prix TTC) et L111-1 cités de mémoire et non retrouvés dans une source consultée.
- Juridique, vie privée et allégations commerciales : Réalité des prestations promises (sauvegardes quotidiennes, surveillance, mises à jour, assistance prioritaire, 2 h/mois, nombre de pages, délais) : seule la cohérence des textes a été comparée, la réalité opérationnelle relève du propriétaire.
- Juridique, vie privée et allégations commerciales : Statut juridique du propriétaire (micro-entrepreneur, société, franchise de TVA), existence d'un SIRET, d'un médiateur, d'un DPO, et clientèle exclusivement professionnelle : inconnus.
- Juridique, vie privée et allégations commerciales : Coordonnées exactes de l'hébergeur Netlify à citer dans les mentions légales : non relevées.
- Juridique, vie privée et allégations commerciales : Cookies et traceurs lors d'une vraie transaction (PayPal, Shop Pay, 3-D Secure) : arrêt avant toute saisie sur la page de paiement, comme exigé.
- Juridique, vie privée et allégations commerciales : Vérification des e-mails de domaine OVH, du DNS et de la sécurité technique : hors périmètre de cette zone.
- Accessibilité, performance et robustesse : État de chargement du bouton (« Envoi en cours… », bouton désactivé) et message d'échec « La demande n'est pas partie… » : ils ne se déclenchent qu'après une validation réussie, donc un envoi valide, interdit par les règles ; vérifiés uniquement par lecture du code (sendBtn.disabled = true, libellé « Envoi en cours… », rétabli dans finally).
- Accessibilité, performance et robustesse : Envoi réel du formulaire et réception de l'e-mail via Web3Forms : volontairement non testés (bloqué par route().abort()).
- Accessibilité, performance et robustesse : Lecteurs d'écran réels (NVDA, VoiceOver, TalkBack) : aucun test avec technologie d'assistance ; les constats ARIA reposent sur le DOM et axe-core.
- Accessibilité, performance et robustesse : Performance réelle sur appareil mobile avec GPU et réseau 4G : l'environnement utilise un WebGL logiciel et aucun étranglement réseau ; LCP et tâches longues sont donc indicatifs.
- Accessibilité, performance et robustesse : Contrastes de texte superposés à des dégradés ou à la bulle WebGL animée (axe-core : 137 à 161 éléments « incomplets ») : seules la légende de démo et le paragraphe d'introduction ont été échantillonnés par pixel ; le texte en dégradé des titres (background-clip:text) n'a pas été mesuré.
- Accessibilité, performance et robustesse : Zoom à 400 % avec polices agrandies et espacement de texte modifié (WCAG 1.4.12) : non testé ; le débordement horizontal à 195 px (zoom mobile extrême) est de 83 px, au-delà de la limite de 320 px exigée par WCAG 1.4.10, et n'a pas été traité comme écart.
- Accessibilité, performance et robustesse : Chargement des polices : Google Fonts (fonts.googleapis.com, fonts.gstatic.com) est utilisé et chargé correctement (4 fichiers woff2, 220 Ko) ; l'effet d'un blocage éventuel de ces domaines (texte de repli, décalage de mise en page) n'a pas été simulé.
- Accessibilité, performance et robustesse : Comportement avec JavaScript désactivé et sur Safari/Firefox : seul Chromium a été utilisé.
- Accessibilité, performance et robustesse : Origine exacte de l'iframe « Powered by Netlify » : visible seulement côté tableau de bord Netlify, hors du périmètre de lecture seule.
- DNS, e-mail, sécurité, dépôt et formulaire : Certificat TLS réel (émetteur, dates d'expiration, SAN) : le proxy de l'environnement réémet les certificats, aucune conclusion possible (règle 6). Seul le succès de la connexion et du HTTP/2 est constaté.
- DNS, e-mail, sécurité, dépôt et formulaire : Sélecteurs DKIM : aucun TXT trouvé pour selector1, selector2, default, google, s1, s2, k1, ovh, mail, dkim, x sous _domainkey.juicecraft.fr (tous NXDOMAIN), mais les sélecteurs réellement utilisés par OVH ne sont pas devinables ; l'activation et l'état du DKIM chez OVH sont à vérifier dans l'espace client. Il est donc impossible de dire si DMARC aurait un alignement DKIM.
- DNS, e-mail, sécurité, dépôt et formulaire : Contenu complet de la zone DNS : une zone ne se liste pas à distance. Seuls l'apex, www et une trentaine de noms usuels ont été testés ; d'autres enregistrements (par exemple des validations ou des CNAME oubliés) peuvent exister.
- DNS, e-mail, sécurité, dépôt et formulaire : Ancien serveur OVH 51.91.236.255 (noté « conservé comme secours » dans DELEGATION.md) : le domaine n'y mène plus par le DNS, mais je n'ai pas testé si ce serveur répond encore à l'hôte juicecraft.fr (connexion directe à une autre IP hors périmètre autorisé).
- DNS, e-mail, sécurité, dépôt et formulaire : Autres expéditeurs légitimes de @juicecraft.fr (notifications Shopify, Appstle, Web3Forms) : leur compatibilité SPF/DKIM n'a pas été vérifiée ; à contrôler avant de durcir DMARC.
- DNS, e-mail, sécurité, dépôt et formulaire : Réception réelle des e-mails et fonctionnement du formulaire Web3Forms en conditions réelles (livraison à la boîte du propriétaire, quota, restrictions du compte) : non testés pour ne pas envoyer de message ; plan du compte Web3Forms et quota mensuel (250 envois par mois annoncé seulement par des sources tierces) non vérifiés.
- DNS, e-mail, sécurité, dépôt et formulaire : Plan Netlify du projet (Free ou payant) et état du réglage du badge : non accessibles ; la déduction « plan Free » vient seulement de la date de création et de la documentation Netlify.
- DNS, e-mail, sécurité, dépôt et formulaire : Commentaire HTML « en tête de page » ajouté par Netlify : non observé (le HTML servi commence par <!doctype html> et ne diffère du dépôt que par la ligne de script finale). Il peut dépendre de la requête, du cache ou d'un état antérieur ; non reproduit.
- DNS, e-mail, sécurité, dépôt et formulaire : Visibilité réelle du dépôt GitHub (privé annoncé) et paramètres de protection de branche : non vérifiables (GitHub hors périmètre réseau) ; seul le clone local a été lu (2 commits, branche main, arbre propre).
- DNS, e-mail, sécurité, dépôt et formulaire : Absence de limitation de débit ou de protection contre l'abus côté Netlify/Web3Forms : non testée (audit passif).
- DNS, e-mail, sécurité, dépôt et formulaire : Validité juridique du chargement de Google Fonts, des mentions légales, de la politique de confidentialité et du bandeau de consentement : hors périmètre de cette zone, relève du niveau 3.
- DNS, e-mail, sécurité, dépôt et formulaire : Valeurs de TTFB mesurées via le proxy de l'environnement (remote_ip 127.0.0.1) : indicatives, pas représentatives d'un visiteur réel ; pas de mesure de performance côté navigateur au-delà du chargement Playwright.
