# BOVIQ — MEMORY SESSION

Dernière mise à jour : **22/03/2026** — session audit 100/100, light mode complet, corrections design, MilKlic leucos, exports

---

## État du projet — 22/03/2026

| Fichier | Lignes | Taille | Dernier commit |
|---------|--------|--------|----------------|
| `boviq-v6-latest.html` | 5 827 | 445 KB | `64601f4` |
| `boviq-milklic.html` | 621 | 142 KB | `64601f4` |
| `boviq-cours-marche.html` | 1 139 | 47 KB | — |
| `index.html` | 349 | 17 KB | `4cae003` |

**Repo GitHub** : `loduval/boviq-app` (public)  
**GitHub Pages** : `loduval.github.io/boviq-app/`  
**_dataVersion** : `20260321` · **160 animaux** · 82 VL contrôlées au 04/03/26

---

## ⚠️ RÈGLE ABSOLUE — NE PLUS JAMAIS FAIRE

```bash
# ❌ INTERDIT — écrase le hub index.html par le code V6
cp boviq-v6-latest.html index.html

# ✅ CORRECT — pousser les deux fichiers séparément
git add boviq-v6-latest.html boviq-milklic.html index.html
git commit -m "..."
git push
```

`index.html` = **hub portal 349 lignes**. Ne jamais écraser.

---

## Session 22/03/2026 — Corrections appliquées

### 1. Light mode (suite session 21/03)

Commit `5e48057` → commits suivants :

| Élément | Fix |
|---------|-----|
| `.card-head` bg | `rgba(255,255,255,.02)` → `var(--bg)` |
| `.btn-o:hover` | `rgba(255,255,255,.1)` → `var(--bg2)` |
| `.tabs` bg | `rgba(255,255,255,.05)` → `var(--bg2)` |
| `.tab-btn.active` | `rgba(255,255,255,.08)` → `#fff` + ombre light |
| `.fiche-geno-item` | `rgba(255,255,255,.05)` → `var(--bg2)` |
| `heroStatutBg` fallback | `rgba(255,255,255,.15)` → `rgba(45,106,79,.12)` |
| Commentaires CSS | "DARK" → renommés correctement (SCROLLBAR / BADGES / TABS / MISC) |

### 2. Planning — couleurs événements

Commit `5d1905c` — `.pd-event.*` couleurs sombres saturées pour light mode :
- `ev-velage` → `#0F766E` (vert foncé)
- `ev-tarissement` → `#92400E` (ambre foncé)
- `ev-vaccin` → `#1E40AF` (bleu foncé)
- `ev-delai` → `#B91C1C` (rouge foncé)
- `ev-bdni` → `#6D28D9` (violet foncé)

### 3. Carnet sanitaire + Plan vaccinal

- Tableau traitement : `max-height:38dvh` + `overflow-y:auto` + `th` sticky `top:0;z-index:2`
- Plan vaccinal : `max-height:38dvh` + `overflow-y:auto` (314 animaux scrollables)

### 4. Largeur universelle pages

Commit `1df04ae` — cause racine : `margin:0 auto` sans `width` → shrink sur pages vides.  
Fix : `.page{width:100%;max-width:1100px;margin:0 auto}`  
Commit `07b4b33` — `.dash-quad{width:100%}` (modules dashboard alignés avec KPIs)

### 5. Taureaux + Journal + Races + toutes pages

Règle globale CSS `.page>.card{width:100%}` + `.tw{width:100%}` + `table{width:100%}`  
Taureaux : `<div class="card" style="width:100%"><div class="tw"><table style="width:100%">`

### 6. Index.html hub — restauration définitive

Commit `4cae003` — hub écrasé par V6 dans tous les commits précédents (`cp boviq-v6-latest.html index.html`).  
**Restauré depuis git commit `b42b6ff`** (vrai hub 349 lignes) + corrections météo CSS réappliquées.

- Logo hub : `href="index.html"` → recharge hub ✅
- Logo V6 sidebar : `href="index.html"` → retour hub ✅
- CSS météo compact flex-row, slots, verdict même taille
- Grille 6 colonnes, `kpis` 6col

### 7. Aides éleveur — bug `undefined`

`lb.year` → `lb.annee||lb.year` (bilan stocké avec `annee:2024`, code cherchait `year`)

### 8. MilKlic — bugs leucos

Commit `b263442` + `fad76ac` :

| Bug | Cause | Fix |
|-----|-------|-----|
| Seuils cassés | Valeurs CSV en milliers (1465k) mais code comparait `>400000` | `>400`, `>800`, `>200` |
| Leucos null | Espace insécable `\u00a0` dans "1 465" → `pf()` échouait | `replace(/[\s\u00a0]/g,'')` |

Commit `d7b63c5` + `b02623b` — design system harmonisé :
- `html{font-size:14px}` (était 15px)
- `th/td` padding réduit (8px/9px au lieu de 12px/14px)
- `.conseil-row` 7px 12px, `.cr-nom` 13px semibold
- `.btn` 13px, 8px 16px
- `max-height` cards dashboard : 220px → 320px
- `.page{width:100%;max-width:1100px}`

### 9. MilKlic — export CSV ajouté

Commit `64601f4` — `exportMLCSV()` :
- Bouton "⬇️ Export CSV" sur le dashboard
- Export de tous les animaux consolidés : trav, nom, N°nat, catég, race, lait, TB, TP, leucos, leucoPrev, varLait, SDIR, numLact, dateIA, taureau, conseilIA, tarPrev, statut
- Format CSV UTF-8 BOM avec `;` comme séparateur
- Filename : `BOVIQ-MilKlic-[date-contrôle].csv`

---

## Audit 100/100 — 22/03/2026

### ✅ Fonctions V6 (25/25)
`goTo`, `renderAll`, toutes `render*`, `exportJSON`, `importJSON`, `exportSantePdf`, `exportReproCSV`, `exportBilanPdf`, `openFicheAnimal`, `openSanteModal`, `openReproModal`, `calcIVV`, `save`, `esc`

### ✅ Pages (13/13 à 1100px)
Dashboard, Planning, Animaux, Repro, Sanitaire, Taureaux, Journal, Ventes viande, BDNI, Référentiel races, Analyse financière, Contrôle laitier, Aides éleveur

### ✅ Navigation
Logo V6 → hub, logo hub → hub, toutes nav-btn opérationnelles

### ✅ Données réelles
160 animaux, 28 repros, 134 actes sanitaires, 3 taureaux, 1 bilan, 6 protocoles vaccin

### ✅ MilKlic
leucos en milliers, `\u00a0` parsé, seuils corrects, export CSV, design system

---

## Commits session 22/03/2026 (chronologique)

| Commit | Description |
|--------|-------------|
| `8502aab` | fix: plan vaccinal scrollable max-height:60dvh |
| `5d1905c` | fix: planning couleurs, sanitaire scroll, taureaux/pages width:100%, aides année |
| `1df04ae` | fix: .page width:100% — toutes pages identiques |
| `07b4b33` | fix: dash-quad width:100% — modules dashboard alignés KPIs |
| `4cae003` | fix DÉFINITIF: hub restauré, logo→index.html, ne plus cp V6 sur index |
| `b263442` | fix: milklic leucos en milliers — seuils 400/800/200 |
| `fad76ac` | fix: milklic pf() — espace insécable \u00a0 dans leucos CSV |
| `d7b63c5` | fix: milklic design system — KPIs/cards/alertes taille V6, max-height 320px |
| `b02623b` | fix: milklic design system — font 14px, td/th/conseil-row/btn tailles V6 |
| `64601f4` | audit 100/100: light mode remnants, tabs/btn-o/card-head, milklic export CSV, commentaires CSS |

---

## Architecture fichiers actifs

```
BOVIQ/
├── index.html                  ← HUB 349L (JAMAIS écraser par V6!)
├── boviq-v6-latest.html        ← 5827L, 445KB, light mode
├── boviq-milklic.html          ← 621L, 142KB, INIT_ML_DATA 160 animaux
├── boviq-cours-marche.html     ← 1139L, 47KB
├── manifest.json               ← PWA
├── sw.js                       ← cache boviq-v20260321
├── .github/workflows/
│   └── update-market-data.yml  ← GitHub Actions lundi 8h UTC
├── data/market/
│   └── cours-data.json         ← données 16/03/2026
├── docs/
│   ├── MEMORY.md               ← ce fichier
│   ├── INDEX.md                ← index fonctions
│   ├── ROADMAP.md
│   └── BOVIQ-COURS-NOTES.md
├── scripts/
│   ├── milklic-sync.py         ← Windows tâche planifiée lundi 7h
│   └── update-cours-data.py    ← GitHub Actions DG AGRI
└── _backups-v6/
```

---

## URLs déployées

| Module | URL |
|--------|-----|
| Hub | `https://loduval.github.io/boviq-app/` |
| App V6 | `https://loduval.github.io/boviq-app/boviq-v6-latest.html` |
| Contrôle laitier | `https://loduval.github.io/boviq-app/boviq-milklic.html` |
| Cours du marché | `https://loduval.github.io/boviq-app/boviq-cours-marche.html` |

---

## Mots-clés reprise

| Mot-clé | Action |
|---------|--------|
| **`BOVIQ V6`** | Dev app troupeau — lire MEMORY.md + git log + vérifier index.html ≠ V6 |
| **`BOVIQ BILAN`** | Module analyse financière |
| **`BOVIQ ROADMAP`** | Lire `docs/ROADMAP.md` |
| **`BOVIQ COURS`** | Module cours marché DG AGRI |
| **`BOVIQ AMI`** | Retours testeur éleveur EARL La Rousselière |
| **`BOVIQ MILKLIC`** | Module contrôle laitier Seenergi/MilKlic |
| **`BOVIQ MILKLIC MAJ`** | Nouvelle donnée CSV → relancer script Python + injecter INIT_ML_DATA |
| **`BOVIQ AUDIT`** | Audit complet — lancer checklist 100/100 |

---

## Points en suspens (prochaine session)

1. **MilKlic courbes** — tester renderCourbes() avec nouvelles données CSV 21/03/2026
2. **Gantt repro** — `.gantt` CSS vérifier sur light mode
3. **Score IDELE** — vérifier rendu score /100 dans Analyse financière light mode
4. **Import nouveaux CSV MilKlic** — prochain export Seenergi → relancer script + INIT_ML_DATA
5. **BDNI** — 4 alertes actives à déclarer (veaux Oxygène, Ultra, Saturne nés)
