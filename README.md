# juicecraft-agence

Dossier de référence de l'agence juicecraft, à cloner sur chaque PC. Dépôt privé : ne jamais le rendre public (il contient l'audit, les brouillons et les coordonnées).

## Contenu
| Dossier ou fichier | Rôle |
|---|---|
| `CLAUDE.md` | Contexte lu automatiquement par Claude Code : règles, décisions, prix, état, tâches en attente |
| `DELEGATION.md` | Ce que Claude peut faire seul, après accord, ou jamais |
| `index.html`, `build_deploy.py`, `shop.json` | Source du site vitrine et sa construction |
| `deploy/index.html` | Site construit, prêt à publier |
| `logo/` | Logos, favicon, animations, planche de marque |
| `video/` | Sources et scripts des vidéos publicitaires, bande-son |
| `livrables/` | Fichiers livrés : vidéos web, zip du site, kit logos, bandes-son |
| `docs/` | Audit, brouillon des mentions légales, liste avant ouverture |
| `outils/` | Scripts de contrôle en lecture seule (Playwright) et scripts de correction utilisés |

Absents volontairement : les images de rendu vidéo (12 Go, régénérables avec les scripts) et les masters vidéo de 130 Mo (au-delà de la limite de GitHub). Les masters sont joints à la version « masters-2026-10-10 » du dépôt (onglet Releases) quand l'envoi a réussi, sinon ils se régénèrent avec `video/redo30_franchise.sh` puis `video/encode30.sh`.

## Travailler sur deux PC
1. Installer GitHub Desktop, se connecter, cloner `evannlassalle-prog/juicecraft-agence`.
2. Avant de travailler : « Fetch origin » puis « Pull ».
3. Après : « Commit to main » avec une phrase qui dit ce qui a changé, puis « Push origin ».
4. Ne pas modifier le même fichier sur les deux PC sans avoir poussé entre les deux.
5. Avec Claude Code, ouvrir ce dossier : `CLAUDE.md` donne le contexte, inutile de tout réexpliquer. Mettre à jour la section « En attente » quand une tâche est faite.
