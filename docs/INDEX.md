# BOVIQ — INDEX DES FICHIERS

Dernière mise à jour : **26/03/2026 17h30**

---

## Fichiers actifs (racine)

| Fichier | Rôle | Lignes |
|---------|------|--------|
| `index.html` | **HUB** — page d'accueil GitHub Pages (**NE JAMAIS ÉCRASER**) | 370 |
| `boviq-v6-latest.html` | App principale troupeau V6 — 9 charts Stats | ~7 750 |
| `boviq-milklic.html` | Module contrôle laitier MilKlic | 973 |
| `boviq-cours-marche.html` | Module cours marché DG AGRI | ~1 139 |
| `boviq-module-lait.html` | Module quotas Montsûrs + lactation (standalone) | ~500 |
| `lbc-maec-rousseliere.html` | Dossier HTML imprimable LBC/MAEC | — |

---

## Répertoire docs/

| Fichier | Contenu |
|---------|---------|
| `MEMORY.md` | État complet du projet, features, données |
| `INDEX.md` | Ce fichier |
| `ROADMAP.md` | Fonctionnalités futures planifiées |
| `BOVIQ-COURS-NOTES.md` | Notes techniques module cours marché |

---

## Répertoire data/

| Fichier/Dossier | Contenu |
|----------------|---------|
| `data/boviq-data.json` | Source de vérité troupeau (GitHub storage) |
| `data/milklic-live.json` | Données contrôle laitier (GitHub storage) |
| `data/market/cours-data.json` | Cours lait + viande DG AGRI (mis à jour lundi par GH Actions) |
| `data/bilan/` | Documents comptables EARL La Rousselière |

---

## Répertoire scripts/

| Script | Rôle |
|--------|------|
| `scripts/audit-boviq.py` | Audit complet V6 (26 vérifications) |
| `scripts/backup-nas.sh` | Sauvegarde locale vers NAS |
| `scripts/milklic-sync.py` | Sync MilKlic CSV (Windows C:\BOVIQ\) |

---

## Archives et sauvegardes

| Dossier | Contenu |
|---------|---------|
| `_backups-v6/` | Snapshots HTML boviq-v6 |
| `_backups-ami/` | Exports JSON/CSV de l'ami éleveur |
| `_archives/app/` | Versions legacy V1-V5 |
| `_archives/bilan/` | Anciens fichiers bilan |

---

## GitHub

- **Repo** : `loduval/boviq-app` (public)
- **Pages** : `https://loduval.github.io/boviq-app/`
- **Push** : `git add -A && git commit -m "x" && git push`
- **Dernier commit** : `6ae0783` — fix sparkline axe Y borné ±2, hauteur 80px

---

## Stack technique

| Élément | Détail |
|---------|--------|
| Architecture | Single HTML file, no build tooling |
| Storage | GitHub API (PAT) + fallback INIT_DATA |
| CDN | Chart.js 4.x, jsPDF, SheetJS, pdf.js, Google Fonts |
| Benchmarks | IDELE/INOSYS 2023 |
| Données marché | DG AGRI Excel downloads (agriculture.ec.europa.eu) |
| Automatisation | GitHub Actions (lundi 8h → cours-data.json) |
