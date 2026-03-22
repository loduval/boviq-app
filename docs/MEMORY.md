# BOVIQ — MEMORY SESSION

Dernière mise à jour : 21/03/2026 — session dark mode + données CSV inline + 160 animaux MilKlic

---

## État du projet

**boviq-v6-latest.html** — ~5760 lignes, 439 KB  
**boviq-milklic.html** — 541 lignes, 140 KB (INIT_ML_DATA inline 160 animaux)  
**boviq-cours-marche.html** — 1140 lignes, 48 KB  
**index.html** — landing dark mode (Cormorant Garamond + DM Sans)  
**Repo GitHub** : `loduval/boviq-app` (public)  
**GitHub Pages** : `loduval.github.io/boviq-app/`  
**Dernier commit** : `b82de0e` — sw.js cache bust → boviq-v20260321

---

## Sessions 21/03/2026 — Résumé complet

### Bugs corrigés

| Bug | Commit | Fix |
|-----|--------|-----|
| `debounce is not defined` crash silencieux | `4f9766b` | Déplacer `function debounce` avant `debouncedSearchAnimaux` |
| TDZ `const pages` → `navPages` | `68c6c7b` | Conflit jsPDF — renommé `navPages` |
| boviq-cours-marche.html 404 | `4f9766b` | Restauré depuis commit `1f4847a` |
| sw.js + manifest.json manquants | `fc03624` | Créés |
| Logo MilKlic + lien retour | `31b97b0` | `🐄` + `href="index.html"` |
| Météo dashboard absente | `3f3b1cd` + `39ed491` | Hook `goTo dashboard` + `setTimeout(initMeteo,100)` + fix bulletproof `try/catch` |
| `renderMeteoWidget` crash silencieux | `ef4bd1f` | Accès sécurisé tous les champs API (idx=-1, hWcode[j]||0) |
| index.html 3 cartes non alignées | `39ed491` | `grid-template-columns:repeat(3,1fr)` |
| Logos → index.html | `39ed491` | Tous les modules pointent vers index.html |
| Cache SW bloque les màj | `b82de0e` | Cache renommé `boviq-v20260321` |

### Dark mode + redesign

Commit `ef4bd1f` — palette identique au site landing `boviq-landing.html` :
- `:root` → `--bg:#0A1810`, `--brand:#4ED87A`, `--ink:#F2EDE4`
- Police : Cormorant Garamond (titres) + DM Sans (corps)
- Grain overlay `body::before` (SVG fractalNoise)
- Sidebar → `#070F09` + border rgba
- Cards : border `rgba(255,255,255,.07)`, dark inputs/selects/modals
- Scrollbar CSS dark, `height:100dvh` par page active
- KPI values : Cormorant Garamond 32px
- Badges, tabs, vaccin-rows, score-wrap, aide-card → dark

### Données CSV MilKlic inline

Commit `ef4bd1f` → `cde9a02` :

**`boviq-v6-latest.html`** : INIT_DATA enrichi avec les valeurs CSV fraîches 04/03/26  
(93 animaux avec `_ml_leucos`, `_ml_lait24`, `_ml_tb`, `_ml_tp`, `_ml_sdir` mis à jour)

**`boviq-milklic.html`** : `INIT_ML_DATA` inline (102KB→140KB) :
- **160 animaux** depuis CSV 07 Inventaire comme base (VL:93, GL:50, MA:13, GV:4)
- Structure objet `{trav: {...}}` indexé comme ML.animaux JS le requiert
- Vrais noms de champs JS : `histoLait`, `histoTB`, `histoTP`, `histoCell`, `conseilIA`, `numLact`, `tarPrev`, `taureau`, `dateIA`, `joursIA`, `rangIA`, `leucoPrev`
- Historiques en objets `{"2024-04-22": 13.1}` (pas des arrays)
- 82 VL avec lait24, 89 avec histoLait, 89 avec histoCell
- Tarissements, conseils IA, SDIR issus du CSV 02 Valorisé

**`loadML()`** : auto-charge `INIT_ML_DATA` si localStorage vide → 1ère ouverture = données présentes sans action

**`renderCourbesInit()`** : select groupé par catégorie (VL / Génisses / Mâles)

**`updateSidebar()`** : affiche `160 animaux · 93 VL · 82 contrôlées`

### Cours du marché

Commit `39ed491` :
- boviq-cours-marche.html restauré depuis commit `1f4847a` (lit `data/market/cours-data.json`)
- Workflow GitHub Actions `.github/workflows/update-market-data.yml` recréé (lundi 8h UTC)
- `data/market/cours-data.json` présent (données 16/03/2026)
- Conversion lait ×10 : 44,93 €/100kg → 449 €/1000L
- Vache R3 : 766 €/100kg → 7,66 €/kg

---

## Commits session chronologiques

| Commit | Description |
|--------|-------------|
| `68c6c7b` | fix: renommer const pages → navPages |
| `4f9766b` | fix: debounce + restore boviq-cours-marche.html |
| `fc03624` | fix: sw.js + manifest.json |
| `31b97b0` | fix: logo 🐄 + lien retour + drop-zone |
| `3f3b1cd` | fix: météo goTo hook + milklic cards |
| `39ed491` | fix: cours-marche restauré + workflow Actions + data/market + index 3col + météo setTimeout + logos |
| `ef4bd1f` | feat: dark mode + données MilKlic CSV inline (95→160 animaux v1) + météo bulletproof |
| `cde9a02` | fix: INIT_ML_DATA 160 animaux structure JS correcte (histoLait obj, vrais noms champs) |
| `b82de0e` | fix: sw.js cache bust → boviq-v20260321 |

---

## Données réelles intégrées (EARL La Rousselière)

`_dataVersion: 20260321` dans INIT_DATA V6 :
- 160 animaux (93 VL + 50 GL + 13 MA + 4 GV)
- 82 VL contrôlées au 04/03/2026 (données MilKlic Seenergi)
- 12 dates de contrôle historiques : avr.24 → mar.26
- 3 taureaux : U40 (Holstein Red), Ucello (Simmental), Sirocco (Normande)
- 134 actes sanitaires dont campagne FCO 130 animaux 17/03/2026
- 28 repros actives
- Bilan EARL 2024 injecté

---

## Architecture fichiers actifs

```
BOVIQ/
├── index.html                  ← landing dark mode (Cormorant + DM Sans)
├── boviq-v6-latest.html        ← ~5760L, 439KB, dark mode
├── boviq-milklic.html          ← 541L, 140KB, INIT_ML_DATA 160 animaux
├── boviq-cours-marche.html     ← 1140L, 48KB
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
├── DERNIERE-VERSION/           ← 8 CSV MilKlic 21/03/2026
├── _backups-v6/
└── _archives/
```

---

## URLs GitHub Pages

| Module | URL |
|--------|-----|
| Landing | `https://loduval.github.io/boviq-app/` |
| App principale | `https://loduval.github.io/boviq-app/boviq-v6-latest.html` |
| Contrôle laitier | `https://loduval.github.io/boviq-app/boviq-milklic.html` |
| Cours du marché | `https://loduval.github.io/boviq-app/boviq-cours-marche.html` |

---

## Points en suspens (prochaine session)

1. **Météo** — vérifier affichage réel sur GitHub Pages (API open-meteo OK en local)
2. **Dark mode** — finaliser `.gantt` CSS manquant (`.gantt-wrap` OK mais `.gantt` seul absent)
3. **Modal animal** — enrichir avec section données MilKlic `_ml_*` (courbes mini Chart.js)
4. **boviq-milklic.html** — tester renderCourbes() + renderCellules() avec INIT_ML_DATA réel
5. **Import nouveaux CSV** — quand nouvel export MilKlic arrive, relancer le script Python et pousser
6. **Sync CSV régulière** — envisager GitHub Actions hebdo (comme cours marché) pour màj automatique MilKlic

---

## Mots-clés reprise

**`BOVIQ V6`** — reprise dev troupeau (app principale)  
**`BOVIQ BILAN`** — module financier  
**`BOVIQ ROADMAP`** — roadmap (`docs/ROADMAP.md`)  
**`BOVIQ COURS`** — cours marché DG AGRI  
**`BOVIQ AMI`** — retours testeur (ami éleveur)  
**`BOVIQ MILKLIC`** — module contrôle laitier CSV  
**`BOVIQ DARK`** — redesign dark mode en cours  
**`BOVIQ MILKLIC MAJ`** — mise à jour données CSV → relancer `/tmp/gen_milklic_final.py` + injecter dans boviq-milklic.html

## Session 2026-03-22
- Light mode complet : --bg:#F6FAF7, --brand:#2D6A4F, sidebar sombre brand3
- Blocs dark neutralisés : inputs/forms, tables, modals, color-scheme:light
- Météo : bandeau compact 44px full-width dans .content (avant toutes les pages)
- Fiche animal / sanitaire : chaque ligne traitement enrichie (type+badge, produit bold, intervenant, posologie, délais actif/terminé en couleur)
- Commit: 5e48057
