# 🐄 BOVIQ — Index Complet du Projet

> **Dernière MAJ** : 28 février 2026 (réorganisation dossier)
> **Dossier** : `~/Desktop/01-Projects/BOVIQ/`

---

## 📁 Arborescence

```
BOVIQ/
├── 🟢 boviq-v6-latest.html          ← APP PRINCIPALE (3635 lignes, Sprint C ✅)
├── 🟢 boviq-cours-marche.html        ← MODULE COURS MARCHÉ (727 lignes, SheetJS)
├── .github/workflows/
│
├── docs/                             ← Documentation projet
│   ├── INDEX.md                      ← Ce fichier
│   ├── MEMORY.md                     ← Mémoire centralisée
│   ├── ROADMAP.md                    ← Feuille de route 5 phases
│   ├── BOVIQ-COURS-NOTES.md          ← Notes module cours
│   └── agridata-investigation-report.md
│
├── data/                             ← Données
│   ├── bilan/                        ← Documents comptables
│   │   ├── 2024 BILAN.pdf            ← Bilan Gecagri original (37 pages)
│   │   └── 2024 BILAN_compressed.pdf
│   ├── market/                       ← Cours marché Excel DG AGRI
│   │   ├── beef-carcass-latest.xlsx
│   │   ├── beef-prices.xlsx
│   │   ├── milk-historical-prices.xlsx
│   │   └── milk-prices.xlsx
│   ├── suivi_reproduction_bovine.xlsx
│   └── boviq_export_2026-02-27.csv
│
├── scripts/                          ← Scripts utilitaires
│   └── boviq-update-cours.py
│
├── _backups-v6/                      ← Snapshots V6 (précieux)
│   ├── boviq-v6-backup-phase1.html   ← Backup pré-Phase 2 (2616 lignes)
│   └── boviq-v6-backup-sprintB.html  ← Backup pré-Sprint C (3216 lignes)
│
├── _backups-ami/                     ← Données réelles éleveur (ISOLÉES)
│   ├── boviq_backup_2026-02-25 (3).json
│   ├── boviq_backup_2026-02-25_3.json
│   └── boviq_export_2026-02-27.csv
│
└── _archives/                        ← Historique complet versions
    ├── app/                          ← Anciennes versions app (v0→v5)
    │   ├── boviq.html → boviq-5.html
    │   ├── boviq-v0-draft.html
    │   ├── boviq-v1-original.html
    │   ├── boviq-v1-mobile.html
    │   ├── boviq-v4.html
    │   ├── boviq-v5.html
    │   └── boviq-v5_1 → v5_4.html
    └── bilan/                        ← Anciennes versions bilan
        ├── bilan-simplifie-v1.html
        └── boviq-bilan-v2.html
```

---

## 🗂️ Historique des versions
| Version | Date | Lignes | Changements majeurs |
|---------|------|--------|---------------------|
| V0 | 22/02 | ~800 | Premier brouillon HTML |
| V1 | 22/02 | ~1200 | MVP : animaux, repro, sanitaire, taureaux, 15 races IDELE |
| V4 | 25/02 | ~1400 | Migration Tabler + Chart.js, design pro |
| V5 | 26/02 | ~1363 | Retours éleveur : catégories, alertes, auto-promotion |
| V6 base | 27/02 | 2288 | 8 modules complets, bilan financier, import PDF Gecagri |
| V6 Phase 1 | 27/02 | 2616 | 17 correctifs (XSS, validation, recherche, IVV) |
| V6 Sprint A | 27/02 | ~2846 | Plan vaccinal protocoles français |
| V6 Sprint B | 27/02 | ~3216 | Charts financiers + PDF sanitaire |
| V6 Sprint C | 28/02 | 3635 | Bilan amélioré : auto-calculs, score IDELE, aides, PDF |

---

## 🌐 BOVIQ COURS (module cours du marché)

| Élément | Détail |
|---------|--------|
| Fichier | `boviq-cours-marche.html` (727 lignes) ✅ DONE |
| Approche | SheetJS côté client, parse Excel DG AGRI |
| Sources | Lait=doc 62d01488, Beef=doc db5b282e |
| Repo GitHub | `loduval/boviq-app` |
| GitHub Pages | `https://loduval.github.io/boviq-app/` |

---

## 📌 Mots-clés de reprise Claude

- **BOVIQ V6** → dev troupeau (app principale)
- **BOVIQ BILAN** → module analyse financière
- **BOVIQ ROADMAP** → feuille de route
- **BOVIQ COURS** → cours du marché (GitHub Pages)
- **BOVIQ AMI** → retours testeur

---
*Index — MAJ 28/02/2026 — post-réorganisation*