# Outils

Scripts Node (Playwright) en lecture seule sur la boutique et le site :
- `storefront.js <dossier> <libellé>` : prix, données structurées, barre d'ajout rapide, « You may also like » et catalogue des 3 offres.
- `annual.js <dossier> <libellé> [id_thème]` : choisit l'abonnement annuel et relève les prix barrés visibles ; avec un id de thème, contrôle un thème brouillon en aperçu.
- `reco.js [id_thème]` : prix des cartes « You may also like ».
- `stickydom.js` : HTML du prix de la barre d'ajout rapide.
- `previewpages.js <id_thème>` : compare accueil et catalogue entre le thème en ligne et un brouillon.
- `sitecheck.js <fichier html> <dossier>` : contrôle local du site construit (TTC, mention TVA, maintenance, configurateur), sans requête externe.

Ils chargent Playwright depuis `/opt/node22/lib/node_modules/playwright` (environnement Claude Code cloud) : adapter le chemin sur un PC (`npm i playwright`).

Scripts Python de correction appliqués le 2026-10-10 (gardés pour traçabilité) : `patch_site_franchise.py`, `patch_video_*.py`.
