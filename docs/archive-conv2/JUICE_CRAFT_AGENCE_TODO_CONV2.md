# État du projet et tâches restantes (conversation 2, au 2026-10-14)

Légende : **Fait** = réalisé et vérifié dans cette conversation · **Fait (non vérifié)** · **Abandonné ou remplacé** · **À faire**.

## 1. Réalisé
| Élément | Statut | Preuve ou remarque |
|---|---|---|
| Premier site vitrine mono-page (WebGL, démos, configurateur, FAQ, formulaire) | Fait, puis **remplacé** le 12/10 par le site Stripe (autre conversation) | archivé dans `archives/site-vitrine-2026-10-10/` |
| Formulaire Web3Forms | Fait (non vérifié) | envoi réel jamais testé ; le site actuel a peut-être un autre mécanisme |
| Vidéo 15 s (16:9 et 9:16) | Fait | 15,000 s, 60 i/s, −14 LUFS |
| Vidéo 30 s, corrigée le 10/10 | Fait | identique au pixel près hors de la scène des offres ; affiche l'ancienne grille |
| Kit de logos + 3 emblèmes d'offres + logo animé | Fait | `logo/` |
| Hébergement Netlify + DNS OVH + HTTPS | Fait | vérifié le 09/10, e-mails OVH intacts |
| Délégation à 3 niveaux | Fait | `DELEGATION.md` |
| Audit complet (12 agents) | Fait | rapport dans `docs/` |
| Boutique Shopify + Appstle (plans, 12 cycles, mise en place, thème) | Fait, puis **abandonné** le 14/10 | 6 produits archivés, pages en 404 |
| Dossier de référence `juicecraft-agence` sur GitHub | Fait | dernier commit `531ae01` avant cette archive |
| Masters 30 s sauvegardés en morceaux | Fait | empreintes vérifiées |
| Brouillon de mentions légales | Fait (brouillon, niveau 3) | `docs/brouillon-mentions-legales.md`, en partie dépassé par les pages légales du site actuel |

## 2. Non réalisé ou abandonné (ne pas confondre avec du réalisé)
- Site corrigé du 10/10 (franchise, maintenance) : **jamais publié**. Le site actuel l'a rendu inutile.
- Thème Shopify « sans prix barré Appstle » : **jamais publié**, sans objet.
- Réglage Appstle « prix de première commande » pour imposer la mise en place : jamais exploré (recherche refusée), sans objet avec Stripe.
- Test d'ajout au panier après le changement de prix du 10/10 : refusé par le contrôle de permissions.
- Retrait du badge Netlify, DMARC, polices auto-hébergées, page 404 en français : proposés, non faits (à vérifier sur le site actuel).
- Vidéos 30 s refaites avec la grille Stripe : non fait.

## 3. À faire, dans l'ordre
1. **Fermer la boutique Shopify** (propriétaire) : désinstaller Appstle, désactiver les moyens de paiement, puis Paramètres → Forfait → Désactiver la boutique. Ça marche si la page myshopify affiche « boutique indisponible » et si la facture finale apparaît.
2. **Routine du lundi** (prochain passage le 19/10) : la mettre à jour sur le site Stripe (`juicecraft.fr`, `/commande`, `offres.js`, pages légales), ou la supprimer. Sinon, elle remontera de faux écarts sur Shopify. Le rapport du 12/10 reste à lire (session `cse_01RtJUA12ErndaRJtGXrYx6s`).
3. **SIRET** : attendre le numéro avant d'ouvrir les ventes, puis l'ajouter aux mentions légales, aux factures Stripe et aux CGV.
4. **Médiateur de la consommation** : obligatoire, puisque des particuliers sont acceptés. L'indiquer sur le site et dans les CGV.
5. **Pages légales** du site actuel (brouillon selon son README) : relecture par un professionnel (niveau 3), avec rétractation de 14 jours pour les particuliers.
6. **Contact et adresse** : trancher entre `contact@juicecraft.fr` (site actuel) et le Gmail (réponse du 11/10). Vérifier que `contact@juicecraft.fr` existe chez OVH (boîte ou redirection) et reçoit bien.
7. **Vidéos** : refaire la scène des offres avec les prix de `offres.js` (création 890 / 2 490 €, Sur mesure sur devis) avant toute publicité. Retirer ou mettre à jour l'emblème Sur mesure si l'offre n'est plus vendue en ligne.
8. **NIS2** : valider l'e-mail du titulaire du domaine chez OVH avant le 22/11/2026.
9. **Hébergement OVH gratuit** : décider s'il est encore utile en secours.
10. **`docs/checklist-ouverture.md`** : la réécrire pour le parcours Stripe (rédigée avant la bascule).
11. **Validation finale** : commande réelle de test sur Stripe en mode test, lecture des e-mails automatiques, puis nouvel audit complet visant zéro constat critique ou élevé.

## 4. Points nécessitant une décision du propriétaire
- Sort de la routine hebdomadaire (mise à jour ou suppression).
- Contact public définitif (Gmail ou `contact@juicecraft.fr`) et adresse affichée (avec ou sans rue, ou domiciliation).
- Avenir de l'offre Sur mesure (sur devis seulement ?) et de son emblème.
- Refaire les vidéos ou non.
