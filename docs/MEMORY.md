# BOVIQ — MEMORY SESSION

Dernière mise à jour : **22/03/2026 — soir** — fiche animal PNG canvas, audit 26 checks, historique leucos, courbes fiche+PDF, fix encodage Latin1

---

## État du projet — 22/03/2026

| Fichier | Lignes | Taille | Dernier commit |
|---------|--------|--------|----------------|
| `boviq-v6-latest.html` | 6 321 | ~480 KB | `78d8946` |
| `boviq-milklic.html` | 658 | ~145 KB | `d299aa6` |
| `boviq-cours-marche.html` | 1 139 | 47 KB | — |
| `index.html` | 370 | ~19 KB | `949b13f` |
| `manifest.json` | 17 | — | `949b13f` |
| `scripts/audit-boviq.py` | ~380 | — | `f315e8c` |

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

`index.html` = **hub portal 370 lignes**. Ne jamais écraser.

---

## Architecture fichiers actifs

```
BOVIQ/
├── index.html                  ← HUB ~370L (JAMAIS écraser par V6!)
├── boviq-v6-latest.html        ← 6321L, ~480KB, light mode
├── boviq-milklic.html          ← 658L, 145KB, INIT_ML_DATA 160 animaux
├── boviq-cours-marche.html     ← 1139L, 47KB
├── manifest.json               ← PWA, start_url=./index.html
├── sw.js                       ← cache boviq-v20260321
├── .github/workflows/
│   └── update-market-data.yml  ← GitHub Actions lundi 8h UTC
├── data/market/
│   └── cours-data.json         ← données marché DG AGRI
├── docs/
│   ├── MEMORY.md               ← ce fichier
│   ├── INDEX.md                ← index fonctions
│   ├── ROADMAP.md
│   └── BOVIQ-COURS-NOTES.md
├── scripts/
│   ├── audit-boviq.py          ← audit complet 26 vérifications
│   ├── milklic-sync.py         ← Windows tâche planifiée lundi 7h
│   └── update-cours-data.py    ← GitHub Actions DG AGRI
└── _backups-v6/                ← snapshots V6 horodatés
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
| **`BOVIQ AUDIT`** | `python3 scripts/audit-boviq.py` — 26 vérifications |

---

## Commits session 22/03/2026 (chronologique complet)

| Commit | Description |
|--------|-------------|
| `cab7d12` | fix: scroll pages — supprime height:100dvh+overflow-y:hidden |
| `949b13f` | fix: start_url index.html PWA + 3 KPIs dashboard |
| `4b98f9d` | feat: badge cellules + tank risk + UGB prévisionnel + fix seuils leucos |
| `1f2ef92` | docs: MEMORY.md |
| `5e81883` | feat: section MilKlic dans fiche animal modale |
| `26b75a0` | feat: section MilKlic dans PDF fiche animal |
| `2947dfd` | feat: PDF fiche animal — miroir complet |
| `b83cd27` | fix: supprime corps orphelin exportFichePdf (crash inventaire) |
| `d299aa6` | feat: historique leucos D.mlControles — accumulation imports, graphe fiche, badge récurrence |
| `3525c03` | docs: MEMORY.md |
| `ae97d1c` | feat: courbes contrôle laitier dans fiche animal (setTimeout) |
| `50e7656` | fix: courbes fiche après openModal + PDF sans emojis/accents |
| `a4295ef` | feat: courbes PDF fiche — canvas off-screen → base64 PNG → addImage |
| `f315e8c` | fix: PDF encodage Latin1 complet (—, •, accents) + script audit-boviq.py |
| **`78d8946`** | **feat: exportFicheImage — fiche animal PNG canvas HTML5 (emojis, courbes, accents natifs)** |

---

## Fonctionnalités clés session 22/03 (après-midi)

### 🖼️ Fiche animal → Image PNG (exportFicheImage)
- **Remplace** `exportFichePdf()` pour la fiche individuelle
- Canvas HTML5 natif — aucune dépendance (jsPDF supprimé pour la fiche)
- **Emojis** : 🥛 💚 💊 👪 🏛️ 📝 tous rendus nativement
- **Accents** : sans contrainte Latin-1 (é è â û ô corrects)
- **Courbes** : Chart.js off-screen → `drawImage()` dans le canvas
- **Format** : PNG 794px largeur, hauteur dynamique selon contenu
- **Téléchargement** : `Fiche_NomVache_Boucle.png`
- Sections : identité · contrôle laitier · courbes · généalogie · reproductions · traitements · BDNI · notes

### 📈 Historique leucos multi-contrôles (D.mlControles)
- `saveML()` dans boviq-milklic.html archive chaque import dans `D.mlControles[]` (localStorage boviq)
- Format : `{date: "YYYY-MM-DD", vaches: [{t, lc, l, tb, tp}]}` — max 24 entrées
- `getLeucosHisto(trav)` → points triés chronologiquement
- `getLeucosRecurrenceColor(trav)` → rouge ≥3 contrôles >400k/12 mois, amber=2, vert=1
- Graphique barres verticales dans la fiche animal modale
- Badge point coloré ● récurrence dans inventaire
- **Prérequis** : boviq-milklic.html et boviq-v6 ouverts dans le même navigateur

### 🔍 Script audit (scripts/audit-boviq.py)
26 vérifications : syntaxe JS, IDs HTML, fonctions manquantes, encodage PDF, seuils leucos, règle index.html, CSS scroll, localStorage, CDN, INIT_DATA JSON, corps orphelins, git état...  
Usage : `python3 scripts/audit-boviq.py`

### 📄 PDF encodage Latin1 (tous les PDFs)
- Registre sanitaire : `—` → `-`, `•` → `-`, accents → ASCII
- Bilan financier : idem
- Fiche individuelle : remplacée par image PNG (problème supprimé)
- Autres `doc.text()` : tous nettoyés de caractères non-Latin1

### 🔧 Corrections bugs
- Corps orphelin `exportFichePdf` (96 lignes hors fonction) → inventaire vidé au chargement
- `renderFicheCharts` appelée via `setTimeout(50ms)` après `openM('fiche')` (canvas visible)
- Seuils leucos dans V6 : `>400000` → `>400` (valeurs en k cell/mL)

---

## Structure données D.mlControles (NOUVEAU)

```javascript
D.mlControles = [
  {
    date: "2026-03-04",        // YYYY-MM-DD
    vaches: [
      {t: "8668", lc: 1465, l: 5.7, tb: 38.0, tp: 33.9},  // lc en k cell/mL
      {t: "9093", lc: 1651, l: 8.1, tb: 42.5, tp: 34.6},
      // ... 82 vaches
    ]
  },
  // ... jusqu'à 24 contrôles (environ 2 ans)
]
```

---

## Points en suspens / Roadmap

1. **Suivi cellules 12 mois** — nécessite ≥2 contrôles importés dans boviq-milklic (premier import = premier point)
2. **"Pourrisseurs du tank"** sur 12/24 mois — même prérequis D.mlControles
3. **sw.js cache** — mettre à jour version après déploiements majeurs
4. **BDNI** — 4 alertes actives (veaux Oxygène, Ultra, Saturne nés)
5. **Import nouveaux CSV MilKlic** — prochain export Seenergi → relancer milklic-sync.py

---

## Règles encodage PDF (pour tout futur doc.text())

```javascript
// ❌ INTERDIT — jsPDF Helvetica = Latin-1 uniquement
doc.text('BOVIQ — Analyse', ...)   // — = U+2014, hors Latin-1
doc.text('• 5 traitements', ...)   // • = hors Latin-1
doc.text('Éditée le...', ...)      // É = OK Latin-1 mais E accent parfois corrompu

// ✅ CORRECT
doc.text('BOVIQ - Analyse', ...)   // tiret ASCII
doc.text('- 5 traitements', ...)   // tiret ASCII
doc.text('Editee le...', ...)      // pas d'accent du tout
```
