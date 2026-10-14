export const meta = {
  name: 'audit-juicecraft-complet',
  description: "Audit complet en lecture seule de juicecraft.fr, de la boutique Shopify, du DNS et de l'e-mail, avec contre-vérification indépendante de chaque constat",
  whenToUse: "Audit complet périodique du site, de la boutique et de l'infrastructure juicecraft",
  phases: [
    { title: 'Audit', detail: '6 agents en lecture seule, un par domaine' },
    { title: 'Contre-vérification', detail: '6 agents tentent de réfuter chaque constat' },
  ],
}

const CTX = `CONTEXTE (à lire d'abord)
- Entreprise : juicecraft, studio français de création de sites internet (un seul propriétaire, francophone). Site : https://juicecraft.fr (www redirige vers le domaine nu), hébergé sur Netlify (projet sparkling-bubblegum-b2d478, adresse sparkling-bubblegum-b2d478.netlify.app) et publié automatiquement depuis le dépôt GitHub privé evannlassalle-prog/juicecraft-site (clone local en lecture seule : /home/user/juicecraft-site). Dossier de travail : /home/user/juicecraft (index.html source, deploy/index.html, build_deploy.py, shop.json, DELEGATION.md, livrables/, video/, logo/).
- DNS chez OVH (serveurs de noms ns200.anycast.me et dns200.anycast.me). Attendu : A de juicecraft.fr = 75.2.60.5 (Netlify) ; www = CNAME vers sparkling-bubblegum-b2d478.netlify.app. E-mail chez OVH : MX mx1, mx2 et mx3.mail.ovh.net, SPF "v=spf1 include:mx.ovh.com -all". L'ancien hébergement OVH (51.91.236.255 et 2001:41d0:301::29) ne doit plus servir le domaine.
- Boutique Shopify : https://juicecraft-store.myshopify.com (plan Basic, EUR, France). Produits d'offre (handles) : essentielle ; %F0%9F%94%B5-premium-%E2%AD%90 ; sur-mesure. Produits de mise en place : mise-en-place-essentielle ; mise-en-place-premium ; mise-en-place-sur-mesure-acompte. Abonnements gérés par l'application Appstle (plans « Abonnement Mensuel » et « Abonnement Annuel »). Données publiques : /products/<handle>.js et /collections/all/products.json.
- GRILLE DE RÉFÉRENCE (prix TTC) : Essentielle : mise en place 290 €, mensuel 49 € (engagement 12 mois, MIN_CYCLES=12), annuel 490 €. Premium : 590 €, 89 €, 890 €. Sur mesure : mise en place dès 1 690 € sur devis (acompte de 1 690 € sur Shopify), mensuel 149 € (MIN_CYCLES=12), annuel 1 490 €. Annuel = 10 mensualités (2 mois offerts). Le prix de base Shopify des produits d'offre est le prix annuel ; la quantité est toujours 1.
- Formulaire de contact du site : Web3Forms (clé publique 405f2edc-13c8-41a6-9d39-20234ec9be36), message envoyé à la boîte du propriétaire.`;

const RULES = `RÈGLES ABSOLUES (elles priment sur tout)
1. LECTURE SEULE. Ne modifie aucun fichier du projet ni du dépôt (aucun commit, aucun push), ne change aucun réglage, n'appelle aucun outil qui écrit ou modifie quoi que ce soit : côté Shopify uniquement des outils de lecture (search_products, get-product, get-shop-info, graphql_query), jamais update-product, create-*, graphql_mutation, publication, inventaire, thème ou réductions ; n'utilise ni Gmail ni Google Calendar ; ne publie rien (ni artefact ni document). Tu peux écrire des fichiers temporaires uniquement dans /tmp/audit-<ta zone>/.
2. Aucune action irréversible ni visible par des tiers : ne soumets jamais le formulaire de contact (il enverrait un e-mail au propriétaire) ; ne saisis aucune donnée personnelle ; ne passe aucune commande et ne va jamais au-delà de la page de paiement Shopify, où tu ne saisis rien ; n'envoie de message à personne. Seule écriture tolérée : ajouter des articles au panier d'un contexte de navigateur jetable.
3. Ne cherche ni ne demande aucun mot de passe, jeton, code ou identifiant ; ne contourne aucune protection ; ne scanne pas de ports et ne tente aucune attaque (audit passif uniquement).
4. Périmètre réseau : juicecraft.fr, www.juicecraft.fr, sparkling-bubblegum-b2d478.netlify.app, juicecraft-store.myshopify.com, les résolveurs DNS publics en lecture (https://dns.google/resolve et https://cloudflare-dns.com/dns-query), et les sources officielles ou documentations pour citer un texte (outils WebSearch et WebFetch : charge-les avec ToolSearch si besoin). Pas plus d'environ 2 requêtes par seconde vers la boutique Shopify ; en cas de 429, attends 30 s puis réessaie une fois.
5. Honnêteté : ne déclare « vérifié » que ce que tu as réellement contrôlé. Chaque constat cite une preuve exacte (adresse testée, commande et résultat, valeur lue). Ne devine rien ; ce que tu ne peux pas contrôler va dans non_verifie. Donne ton niveau de confiance. Un contrôle réussi est une information utile : note-le dans controles_ok.
6. Environnement : Chromium et Playwright sont déjà installés (module Node /opt/node22/lib/node_modules/playwright, binaire /opt/pw-browsers/chromium) ; n'exécute pas playwright install. Les sorties HTTPS passent par un proxy d'environnement qui RÉÉMET les certificats TLS (l'émetteur observé est « Anthropic » : c'est un artefact de l'environnement) ; n'en déduis rien sur le certificat réel. L'outil dig n'existe pas : utilise curl vers https://dns.google/resolve?name=...&type=... . Donne un timeout à chaque commande (100 s au plus) et découpe les longs tests en plusieurs commandes. Ne lance jamais pkill, killall ni aucune commande qui arrête des processus qui ne sont pas les tiens (d'autres agents travaillent en parallèle).
7. Durée : vise 25 minutes de travail au maximum. Réponds en français. Ta réponse finale est exclusivement la donnée structurée demandée (le schéma), sans texte autour.`;

const DEFS = `DÉFINITIONS
- gravite : critique = fait perdre de l'argent, bloque l'achat ou expose à un risque légal ou de sécurité sérieux ; élevé = dégrade nettement la conversion, la confiance ou la conformité ; moyen = défaut visible ou risque modéré ; faible = amélioration ou détail.
- niveau = niveau de l'action qui applique la correction EN LIGNE : 1 = texte ou référencement côté boutique, ou brouillon préparé sans effet public (autonome avec compte rendu) ; 2 = exige l'accord explicite du propriétaire (publication d'un changement sur le site en ligne, prix, produits, e-mails aux clients, codes de réduction, DNS ou hébergement, réglages d'applications) ; 3 = ne se décide jamais seul : juridique (CGV, mentions légales, politique de remboursement), TVA, remboursements, litiges, client mécontent.`;

const SORTIE = `SORTIE (schéma imposé, en français)
- zone : le nom de ta zone ; resume : 3 à 6 phrases factuelles.
- controles_ok : TOUS les contrôles réussis, chacun avec sa preuve (valeur lue, adresse, code HTTP).
- constats : uniquement des écarts réels et prouvés, un problème précis par constat, id de la forme @@ZONE@@-01, @@ZONE@@-02... Pour chaque constat : constat (ce que tu observes), attendu, preuve exacte, recommandation concrète et applicable (texte exact quand c'est possible), confiance.
- non_verifie : ce que tu n'as pas pu contrôler, et pourquoi.
${'' }`;

const SEV = ['critique', 'élevé', 'moyen', 'faible'];

const FINDING = {
  type: 'object',
  properties: {
    id: { type: 'string', description: 'Identifiant unique de la forme ZONE-01' },
    titre: { type: 'string' },
    gravite: { type: 'string', enum: SEV },
    niveau: { type: 'integer', enum: [1, 2, 3], description: "Niveau de l'action qui applique la correction en ligne (voir les définitions)" },
    constat: { type: 'string', description: 'Ce qui est observé' },
    attendu: { type: 'string' },
    preuve: { type: 'string', description: 'Preuve exacte : URL, commande et résultat, valeur lue' },
    recommandation: { type: 'string' },
    confiance: { type: 'string', enum: ['haute', 'moyenne', 'faible'] },
  },
  required: ['id', 'titre', 'gravite', 'niveau', 'constat', 'attendu', 'preuve', 'recommandation', 'confiance'],
};

const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    zone: { type: 'string' },
    resume: { type: 'string' },
    controles_ok: { type: 'array', items: { type: 'object', properties: { controle: { type: 'string' }, preuve: { type: 'string' } }, required: ['controle', 'preuve'] } },
    constats: { type: 'array', items: FINDING },
    non_verifie: { type: 'array', items: { type: 'string' } },
  },
  required: ['zone', 'resume', 'controles_ok', 'constats', 'non_verifie'],
};

const VERIF_SCHEMA = {
  type: 'object',
  properties: {
    zone: { type: 'string' },
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          verdict: { type: 'string', enum: ['confirmé', 'réfuté', 'non_concluant'] },
          raison: { type: 'string' },
          preuve_independante: { type: 'string' },
          gravite_ajustee: { type: 'string', enum: SEV },
          niveau_ajuste: { type: 'integer', enum: [1, 2, 3] },
        },
        required: ['id', 'verdict', 'raison', 'preuve_independante', 'gravite_ajustee', 'niveau_ajuste'],
      },
    },
    controles_reverifies: {
      type: 'array',
      items: {
        type: 'object',
        properties: { controle: { type: 'string' }, resultat: { type: 'string', enum: ['ok', 'ecart', 'non_concluant'] }, preuve: { type: 'string' } },
        required: ['controle', 'resultat', 'preuve'],
      },
    },
    constats_manques: { type: 'array', items: FINDING },
  },
  required: ['zone', 'verdicts', 'controles_reverifies', 'constats_manques'],
};

const AREAS = [
  {
    key: 'prix',
    nom: 'Prix, offres et cohérence des contenus',
    mission: `MISSION : vérifier que tous les prix, conditions et promesses sont identiques et corrects partout.
1. Sur https://juicecraft.fr (HTML brut avec curl ET texte rendu avec Playwright), relève tous les montants et conditions : cartes d'offres, note sous les cartes, FAQ, configurateur, section contact, métadonnées, mentions TTC/HT, « 12 mois d'engagement », « 2 mois offerts », mises en place.
2. Côté Shopify, pour les 3 produits d'offre et les 3 produits de mise en place, lis /products/<handle>.js (titre, description HTML et ses liens, prix en centimes, variantes, requires_shipping, selling_plan_groups : prix mensuel et annuel, code MIN_CYCLES dans options[0].value), /collections/all/products.json, et les balises og:title et meta description des pages produits. Si des outils Shopify en lecture sont disponibles (ToolSearch « shopify »), complète avec statut, tags, vendor, productType, champs SEO et groupes de plans ; jamais d'outil d'écriture.
3. Compare site, Shopify, grille de référence, /home/user/juicecraft/DELEGATION.md et fichiers locaux : arithmétique (annuel = 10 x mensuel ; total de la première année = 12 x mensuel + mise en place ; totaux annoncés), cohérence du vendeur, des tags et du type de produit, liens des descriptions (HTTP 200). Le dépôt (/home/user/juicecraft-site/index.html), /home/user/juicecraft/deploy/index.html et la page en ligne doivent être identiques, hors injections Netlify (commentaire HTML en tête de page et script /.netlify/scripts/hud).
4. Compare les PROMESSES de contenu de chaque offre entre site et boutique (nombre de pages, hébergement, maintenance, modifications incluses, assistance, SEO, animations) : signale toute promesse présente d'un seul côté ou différente.
5. Vidéos : lis les textes de /home/user/juicecraft/video/video30.html (scènes offres et méthode) ; avec ffmpeg, extrais une image à 18,5 s, 23,8 s et 28,5 s de /home/user/juicecraft/livrables/juicecraft_pub_30s_16x9.mp4 et de juicecraft_pub_30s_9x16.mp4, regarde-les (outil de lecture d'image) et relève prix et textes visibles. Liste les autres vidéos livrées et indique si elles peuvent contenir d'anciens prix.
6. Cherche toute trace d'ancien prix ou d'ancienne formulation sur le site, la boutique, les métadonnées et les livrables : 39, 69, 79, 119, 129, 399, 499, 799, 899, 1 199, 1 499 € (hors usage légitime, à justifier), « Sur devis » dans les offres, « devis détaillé avant tout paiement ».`,
  },
  {
    key: 'achat',
    nom: "Parcours d'achat et page de paiement",
    mission: `MISSION : vérifier qu'un visiteur peut choisir une offre, voir le bon prix et arriver jusqu'à la page de paiement sans défaut. Rien n'est payé.
Astuces déjà éprouvées : require('/opt/node22/lib/node_modules/playwright') ; bouton d'achat : button.add-to-cart-button:not(.sticky-add-to-cart__button) ; bloc d'abonnement : .appstle_sub_widget avec un select (libellés « Abonnement Mensuel » et « Abonnement Annuel ») ; panier : fetch('/cart.js') dans la page ; un contexte de navigateur NEUF par scénario (sinon le panier s'accumule) ; un scénario par commande pour rester sous le timeout ; la page de paiement s'ouvre par navigation vers https://juicecraft-store.myshopify.com/checkout (redirection vers /checkouts/...).
1. Sur https://juicecraft.fr : les trois boutons « Choisir cette offre » (attribut data-plan : essentielle, premium, mesure) ont le bon href ; un clic réel ouvre la bonne page produit (ordinateur 1440x900 pour les trois boutons ; mobile 390x844 pour un seul bouton ; onglet, rel).
2. Pour chaque offre x {mensuel, annuel} sur ordinateur (6 scénarios), puis sur mobile pour la seule offre Essentielle (mensuel et annuel ; le modèle de page est commun aux trois produits) : bloc d'abonnement visible et placé AU-DESSUS du bouton d'achat ; prix du haut de page et du bloc qui suivent le choix ; libellés en français ; lien « mise en place obligatoire » dans la description ; ajout au panier puis lecture de /cart.js (quantité 1, montant, nom du plan). Attendus : mensuel 49 / 89 / 149 € ; annuel 490 / 890 / 1 490 €.
3. Ajoute ensuite le produit de mise en place correspondant et vérifie les totaux : Essentielle 339 € (mensuel) / 780 € (annuel) ; Premium 679 € / 1 480 € ; Sur mesure 1 839 € / 3 180 €.
4. Ouvre /checkout en lecture seule (ne saisis rien) pour trois paniers seulement (Essentielle mensuel + mise en place, Essentielle annuel + mise en place, Sur mesure mensuel + acompte) : lignes, total, « sous-total récurrent » et périodicité, absence de champs de livraison, affichage TTC et taxes, format des montants (position du symbole €), cases pré-cochées (consentement marketing), moyens de paiement proposés, liens (politique de résiliation, remboursement, confidentialité : suis-les, relève code HTTP et contenu), textes restés en anglais, mentions de renouvellement. Ne clique sur aucun bouton de paiement.
5. Cas limites dans un contexte jetable : POST /cart/add.js d'un produit d'abonnement SANS selling_plan (doit être refusé) ; ajout avec quantity 12 sur le plan mensuel (une règle parasite de quantité minimale ne doit plus exister) ; page produit avec connexion lente.
6. Pages de la boutique (accueil, /collections/all, /cart, contact) : langue, textes anglais restants, produits visibles, cohérence de marque (nom, logo, vendeur « Ma boutique » ou « juicecraft »), défauts visuels. Prends des captures d'écran (page produit et checkout, ordinateur et mobile), regarde-les et relève chevauchements, textes tronqués, images manquantes. Durée : vise 20 minutes ; si un scénario est trop lent (page lente), note-le dans non_verifie au lieu de le répéter.`,
  },
  {
    key: 'seo',
    nom: 'Référencement, contenu et rédaction',
    mission: `MISSION : évaluer le référencement, la qualité du contenu et la rédaction du site et de la boutique.
1. Sur https://juicecraft.fr (HTML brut avec curl ET rendu Playwright) : title et meta description (longueurs), canonical, balises robots, Open Graph et Twitter (og:image, og:url, twitter:card), lang, hreflang, favicon, apple-touch-icon, manifest, données structurées JSON-LD, hiérarchie des titres (un seul h1), attributs alt, liens internes et externes (code HTTP de CHAQUE lien externe), contenu clé présent dans le HTML initial sans JavaScript ?, robots.txt, sitemap.xml, comportement d'une URL inexistante (404), chaîne de redirections (http vers https, www vers domaine nu), en-têtes de cache.
2. Doublon d'indexation : https://sparkling-bubblegum-b2d478.netlify.app sert la même page ; relève canonical, noindex ou redirection éventuels et le risque de contenu dupliqué.
3. Rédaction française : relis tout le texte visible du site (sections, FAQ, configurateur, pied de page, messages d'erreur du formulaire) : orthographe, grammaire, typographie (espaces insécables avant ? ! : ; et autour des guillemets, symbole €), cohérence vous/tu et du vocabulaire (offres, mise en place, TTC, engagement), phrases ambiguës, titres et ancres qui ne correspondent pas. Cite chaque faute avec le texte exact et la correction.
4. Boutique : titres et méta des produits (og:title, meta description), pages d'accueil et de catalogue, textes restés en anglais (par exemple « Join our email list », « You may also like », « Disclosures », « Delivery every »), alt des images, format des montants (« €399,00 » ou « 399,00 € »), URL du produit Premium contenant des émojis (%F0%9F%94%B5-premium-%E2%AD%90) : risques et correction propre (changer un handle impose de mettre à jour le site et la boutique : niveau 2), robots.txt et sitemap de la boutique, cohérence avec le site.
5. Classe les constats par impact attendu sur la visibilité et la conversion. Pour chaque correction, donne le texte exact à appliquer (balises, contenu de robots.txt, sitemap.xml, JSON-LD) quand c'est possible.`,
  },
  {
    key: 'legal',
    nom: 'Juridique, vie privée et allégations commerciales',
    mission: `MISSION : relever les écarts juridiques, de vie privée et d'allégations commerciales visibles, SANS donner de conseil juridique : tu constates, tu cites la référence officielle et tu indiques ce que le propriétaire doit faire valider. Toute correction de nature juridique (CGV, mentions légales, politique de remboursement ou de rétractation, TVA) est de niveau 3.
1. Pages et mentions : sur https://juicecraft.fr, examine le pied de page (éléments cliquables ou non), les routes évoquées (/mentions-legales, /cgv, /confidentialite...), les mentions d'identification de l'éditeur (nom ou dénomination, statut, SIRET/RCS, adresse, e-mail ou téléphone, directeur de publication, hébergeur Netlify, TVA), les renvois aux CGV dans la FAQ. Sur Shopify : /policies/privacy-policy (lis-la en entier : entreprise, coordonnées, base légale, sous-traitants, durées, droits, langue, texte générique non adapté), /policies/terms-of-service, /policies/refund-policy, /policies/legal-notice, /policies/contact-information, /policies/shipping-policy, /policies/subscription-policy (statut HTTP) ; liens du pied de page et du checkout (« politique de résiliation » : URL cible, code HTTP, contenu).
2. Données personnelles : formulaire de contact du site (champs collectés, information au point de collecte, case de consentement, finalité, destinataire et sous-traitant Web3Forms, lieu de traitement : à vérifier, ne rien affirmer sans source, durée de conservation) ; case marketing pré-cochée au checkout ; cookies et traceurs réellement déposés : avec Playwright, liste cookies, localStorage, sessionStorage et requêtes tierces au chargement du site et de la boutique (y compris le script /.netlify/scripts/hud et ses appels sortants), puis indique si un bandeau de consentement paraît nécessaire.
3. Vente en ligne et abonnement : informations précontractuelles visibles (prix TTC, durée d'engagement de 12 mois, reconduction, modalités de résiliation, droit de rétractation et ses exceptions pour les prestations de service, médiateur de la consommation, TVA), distinction particuliers / professionnels (le site vise surtout des professionnels : à confirmer par le propriétaire), obligation éventuelle de pouvoir résilier en ligne un contrat conclu en ligne. Utilise WebSearch ou WebFetch sur des sources officielles (legifrance.gouv.fr, service-public.fr, cnil.fr, economie.gouv.fr) pour citer précisément l'article ou la fiche, et indique si l'obligation vise les consommateurs, les professionnels ou les deux. Ne présente jamais une obligation comme certaine si tu ne l'as pas retrouvée dans une source officielle : écris « à faire valider ».
4. Allégations commerciales à justifier : relève toutes les promesses du site et de la boutique qui engagent le propriétaire et dont il doit confirmer la réalité (par exemple « Sauvegardes quotidiennes », « Surveillance », « Mises à jour régulières », « Maintenance », « Hébergement » inclus, « Assistance prioritaire », « Paiement sécurisé », « Score visé : 90+ », nombre de pages, 2 h de modifications par mois, délais). Vérifie aussi les mentions « concept fictif » ou « exemple illustratif » des réalisations et la présence de la mention TTC près des prix.`,
  },
  {
    key: 'acces',
    nom: 'Accessibilité, performance et robustesse',
    mission: `MISSION : mesurer l'accessibilité, la performance et la robustesse de https://juicecraft.fr sur ordinateur (1440x900) et mobile (390x844, émulation tactile).
1. Performance (Playwright Chromium) : temps de chargement, LCP, CLS observé pendant 30 s SANS interaction (PerformanceObserver layout-shift) et variations de hauteur des sections et cartes au repos, poids transféré et nombre de requêtes, erreurs console et JavaScript, ressources en échec, tâches longues, effet de prefers-reduced-motion: reduce (les animations s'arrêtent-elles ?), absence de défilement horizontal à 320, 390, 820 et 1440 px, zoom 200 %. Historique : la page bougeait au repos (mot rotatif du titre passant sur 4 lignes, cartes de la section Services changeant de hauteur) ; corrigé le 9 octobre 2026 : cherche toute régression.
2. Accessibilité : essaie d'installer axe-core avec npm dans /tmp/audit-acces (s'il est indisponible, fais des contrôles manuels équivalents) et exécute-le sur la page (ordinateur et mobile, menu mobile et FAQ ouverts) ; contrastes de texte (valeurs mesurées), noms accessibles des boutons, liens et champs, textes alternatifs, ordre des titres, repères (landmarks), lien d'évitement, langue ; navigation au clavier sur toute la page (Tab, Maj+Tab, Entrée, Espace, Échap) : focus visible, menu mobile, FAQ, configurateur, formulaire et boutons « Choisir cette offre » atteignables et activables, absence de piège au clavier ; états ARIA (aria-expanded, aria-pressed, aria-live pour les erreurs du formulaire) ; curseur personnalisé et effets « magnétiques » ; taille des cibles tactiles (au moins 24x24 px) ; animations automatiques de plus de 5 s sans pause possible.
3. Formulaire de contact SANS l'envoyer : bloque toute requête vers api.web3forms.com avec page.route(...).abort() avant tout test ; teste les validations (champs vides, e-mail invalide), les messages d'erreur, le honeypot, l'état de chargement. N'essaie JAMAIS un envoi valide.
4. Contrôle visuel : captures pleine page (ordinateur et mobile), regarde-les (outil de lecture d'image) et relève chevauchements, textes tronqués, images manquantes, carte « Maintenance possible » lisible, démos animées cohérentes.`,
  },
  {
    key: 'infra',
    nom: 'DNS, e-mail, sécurité, dépôt et formulaire',
    mission: `MISSION : vérifier le DNS, l'e-mail, HTTPS, les en-têtes de sécurité, le script injecté par Netlify, le dépôt et le formulaire.
1. DNS (https://dns.google/resolve?name=<nom>&type=<type>, et au besoin https://cloudflare-dns.com/dns-query avec l'en-tête accept: application/dns-json) pour juicecraft.fr et www.juicecraft.fr : NS, SOA, A, AAAA, CNAME, MX, TXT, CAA, DS et DNSKEY (DNSSEC, drapeau AD), TTL ; enregistrements résiduels vers l'ancien hébergement OVH ; conformité avec l'attendu ; sous-domaines courants (mail, ftp, autoconfig, autodiscover, imap, smtp, pop3, webmail, _dmarc, _mta-sts, sélecteurs DKIM plausibles). Tu ne peux pas lister toute la zone : ne conclus que sur ce que tu observes et mets le reste dans non_verifie.
2. E-mail : SPF (syntaxe, nombre de résolutions DNS inférieur ou égal à 10, mécanisme final, include valide), DKIM (sélecteurs plausibles), DMARC (absence constatée le 9 octobre 2026 : propose une politique de départ p=none avec rua, à faire valider), MTA-STS et TLS-RPT, cohérence des priorités MX.
3. HTTPS et en-têtes : redirections (http vers https, www vers domaine nu, chaînes), HSTS (valeur, includeSubDomains, preload), X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, absence éventuelle de Content-Security-Policy, cookies, cache, compression, HTTP/2. Compare avec le fichier _headers du dépôt. Ne conclus RIEN sur l'émetteur ni l'expiration réels du certificat (voir règle 6) : vérifie seulement que la connexion aboutit et que les noms correspondent.
4. Script injecté par Netlify (/.netlify/scripts/hud?variant=public, plus un commentaire HTML en tête de page, absents du dépôt) : télécharge-le (lecture seule), décris précisément ce qu'il fait (requêtes sortantes, cookies, stockage, données envoyées, domaine contacté), évalue le risque vie privée et performance, et cherche dans la documentation officielle de Netlify (WebSearch ou WebFetch) s'il peut être retiré ; n'affirme rien sans source.
5. Dépôt et fichiers locaux (lecture seule) : /home/user/juicecraft-site (git log, fichiers, .gitignore) et /home/user/juicecraft (index.html source, deploy/, build_deploy.py, shop.json, DELEGATION.md) : recherche de secrets ou données sensibles (mots de passe, jetons, clés, e-mail personnel, téléphone) dans le dépôt ET dans le HTML publié. La clé Web3Forms est publique par conception : évalue le risque d'abus (envoi de spam à la boîte du propriétaire via la clé publique), lis la gestion d'erreur et le honeypot dans le JavaScript, et note les restrictions possibles côté Web3Forms (documentation officielle, à vérifier). Vérifie aussi que _headers est effectif, qu'aucun fichier inutile n'est servi publiquement (/.git, /DELEGATION.md, /README.md) et que le dépôt et le site publié restent identiques hors injections Netlify.
6. Disponibilité : le domaine ne mène plus à l'ancien serveur OVH ; temps de réponse (TTFB) mesuré 5 fois ; comportement des erreurs 404.`,
  },
];

const auditPrompt = (a) => [
  CTX,
  RULES,
  'TA ZONE : ' + a.nom,
  a.mission,
  DEFS,
  SORTIE.split('@@ZONE@@').join(a.key.toUpperCase()),
].join('\n\n');

const verifPrompt = (a, audit) => {
  const k = a.key.toUpperCase();
  return [
    CTX,
    RULES,
    'TA MISSION : tu es le contradicteur indépendant de la zone « ' + a.nom + ' ». Un premier agent a audité cette zone ; son rapport JSON figure en bas. Tu cherches à RÉFUTER ses constats et à détecter ses faux « OK ». Tu as accès aux mêmes outils que lui, avec les mêmes règles absolues.',
    'MÉTHODE\n' +
      "1. Pour CHAQUE constat : refais le contrôle toi-même par une méthode indépendante (autre commande, autre outil, autre moment), sans te fier à la preuve de l'auditeur. Verdict : confirmé (tu l'as reproduit), réfuté (tu as une preuve contraire) ou non_concluant (impossible à reproduire ou à trancher). Si tu ne peux pas reproduire, réponds non_concluant ; ne réponds jamais confirmé sur la seule foi de l'auditeur. Donne une preuve_independante (valeur lue, commande, adresse).\n" +
      '2. Reconsidère la gravité et le niveau de chaque constat d\'après les définitions ; renvoie les valeurs finales dans gravite_ajustee et niveau_ajuste (identiques si inchangées).\n' +
      "3. Recontrôle les 6 contrôles « OK » les plus importants de l'auditeur (ceux dont l'échec coûterait le plus : prix, achat, DNS, HTTPS, légal) pour détecter un faux « OK » ; mets-les dans controles_reverifies.\n" +
      "4. Cherche rapidement jusqu'à 3 constats importants que l'auditeur a manqués dans la même zone (constats_manques), uniquement s'ils sont prouvés par toi ; ids de la forme " + k + '-M1, ' + k + '-M2.',
    DEFS,
    "RAPPORT DE L'AUDITEUR (JSON) :\n" + JSON.stringify(audit),
  ].join('\n\n');
};

const RANK = { 'critique': 0, 'élevé': 1, 'moyen': 2, 'faible': 3 };

const results = await pipeline(
  AREAS,
  (prev, item) => {
    const a = (item && item.key) ? item : prev;
    return agent(auditPrompt(a), { label: 'audit:' + a.key, phase: 'Audit', schema: AUDIT_SCHEMA, effort: 'high' });
  },
  async (audit, item) => {
    const a = item;
    if (!audit) {
      log('Audit « ' + a.nom + ' » indisponible : zone non couverte');
      return { zone: a.nom, audit: null, verif: null };
    }
    log('Audit « ' + a.nom + ' » terminé : ' + audit.constats.length + ' constat(s), ' + audit.controles_ok.length + ' contrôle(s) réussi(s). Contre-vérification lancée.');
    const verif = await agent(verifPrompt(a, audit), { label: 'verif:' + a.key, phase: 'Contre-vérification', schema: VERIF_SCHEMA, effort: 'xhigh' });
    if (!verif) log('Contre-vérification « ' + a.nom + ' » indisponible : constats non contre-vérifiés');
    return { zone: a.nom, audit, verif };
  }
);

const constats = [];
const refutes = [];
const fauxOk = [];
const ok = [];
const nonVerifie = [];
const zones = [];
const echecs = [];

for (const r of results) {
  if (!r) { echecs.push('une zone a été interrompue avant tout résultat'); continue; }
  if (!r.audit) { echecs.push(r.zone + ' : audit indisponible, zone non couverte'); continue; }
  const A = r.audit;
  const V = r.verif;
  zones.push({ zone: r.zone, resume: A.resume, nb_constats: (A.constats || []).length, nb_controles_ok: (A.controles_ok || []).length, contre_verifiee: !!V });
  (A.controles_ok || []).forEach(c => ok.push({ zone: r.zone, controle: c.controle, preuve: String(c.preuve || '').slice(0, 160) }));
  (A.non_verifie || []).forEach(t => nonVerifie.push(r.zone + ' : ' + t));
  const byId = {};
  if (V) (V.verdicts || []).forEach(v => { byId[v.id] = v; });
  for (const f of (A.constats || [])) {
    const v = byId[f.id];
    if (v && v.verdict === 'réfuté') {
      refutes.push({ zone: r.zone, id: f.id, titre: f.titre, raison: v.raison, preuve: v.preuve_independante });
      continue;
    }
    constats.push({
      zone: r.zone, id: f.id, titre: f.titre,
      gravite: v ? v.gravite_ajustee : f.gravite,
      niveau: v ? v.niveau_ajuste : f.niveau,
      statut: v ? v.verdict : 'non contre-vérifié',
      constat: f.constat, attendu: f.attendu, preuve: f.preuve, recommandation: f.recommandation, confiance: f.confiance,
      preuve_independante: v ? v.preuve_independante : '',
      avis_contradicteur: v ? v.raison : '',
    });
  }
  if (V) {
    (V.constats_manques || []).forEach(f => constats.push({
      zone: r.zone, id: f.id, titre: f.titre, gravite: f.gravite, niveau: f.niveau,
      statut: 'trouvé par le contradicteur (non contre-vérifié)',
      constat: f.constat, attendu: f.attendu, preuve: f.preuve, recommandation: f.recommandation, confiance: f.confiance,
      preuve_independante: '', avis_contradicteur: '',
    }));
    (V.controles_reverifies || []).filter(c => c.resultat !== 'ok').forEach(c => fauxOk.push({ zone: r.zone, controle: c.controle, resultat: c.resultat, preuve: c.preuve }));
  }
}

constats.sort((x, y) => ((RANK[x.gravite] ?? 9) - (RANK[y.gravite] ?? 9)) || (y.niveau - x.niveau));

const totaux = {
  zones_couvertes: zones.length,
  zones_contre_verifiees: zones.filter(z => z.contre_verifiee).length,
  constats: constats.length,
  confirmes: constats.filter(c => c.statut === 'confirmé').length,
  non_concluants: constats.filter(c => c.statut === 'non_concluant').length,
  non_contre_verifies: constats.filter(c => c.statut !== 'confirmé' && c.statut !== 'non_concluant').length,
  refutes: refutes.length,
  faux_ok_detectes: fauxOk.length,
  controles_reussis: ok.length,
};
log('Audit terminé : ' + totaux.constats + ' constat(s) retenu(s) dont ' + totaux.confirmes + ' confirmé(s), ' + totaux.refutes + ' réfuté(s), ' + totaux.faux_ok_detectes + ' faux OK détecté(s), ' + echecs.length + ' zone(s) en échec.');

return { totaux, zones, constats, refutes, faux_ok: fauxOk, controles_ok: ok, non_verifie: nonVerifie, echecs };
