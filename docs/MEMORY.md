# BOVIQ — MEMORY SESSION

Dernière mise à jour : **26/03/2026 — 17h30** — Session Stats + fix PAT token + module Lait

---

## État du projet — 26/03/2026 17h30

| Fichier | Lignes | Dernier commit |
|---------|--------|----------------|
| `boviq-v6-latest.html` | ~7 750 | `4858d7e` |
| `boviq-milklic.html` | 973 | `b48dbee` |
| `boviq-cours-marche.html` | ~1 139 | — |
| `index.html` | 370 | `4cae003` (NE JAMAIS ÉCRASER) |
| `data/boviq-data.json` | — | source de vérité GitHub |
| `lbc-maec-rousseliere.html` | — | dossier HTML imprimable |

**Repo GitHub** : `loduval/boviq-app` (public)  
**GitHub Pages** : `loduval.github.io/boviq-app/`  
**_dataVersion** : `20260321` · **160 animaux** · **134 soins** · **28 repros**

---

## ⚠️ RÈGLES ABSOLUES

- **JAMAIS** `cp boviq-v6-latest.html index.html` — index.html = HUB 370L
- Toujours `node --check` après édition JS
- Toujours `git pull --rebase` avant push si rejet

---

## 🔑 ARCHITECTURE STORAGE — GitHub centralisé

| Élément | Rôle |
|---------|------|
| `data/boviq-data.json` | Source de vérité unique sur GitHub |
| `load()` | async fetch `raw.githubusercontent.com` au démarrage |
| `save()` | debounce 1.5s → API PUT GitHub |
| `boviq_gh_pat` | PAT stocké dans localStorage |
| Badge sync | sidebar — état OK/saving/error |
| Fallback | `INIT_DATA` embarqué si fetch échoue |

**MilkLic bridge** : `saveML()` et `loadML()` écrivent aussi dans `localStorage['BOVIQ_MILKLIC']` pour que V6 puisse lire les données de contrôle laitier.

---

## ✅ FEATURES LIVRÉES session 26/03/2026

### Page Statistiques (`id="p-stats"`) — 9 graphiques Chart.js
| Graphique | Source | Contenu |
|---|---|---|
| Camembert revenus | Bilan 2024 | Lait 59% / Aides 20% / Viande 19% / Divers 2% |
| Camembert troupeau | STATE.animaux | VL / Génisses / Mâles / Veaux |
| Histogramme charges | Bilan 2024 | Alim / Véto / Élevage / SF / Structure |
| Histogramme ventes | Bilan 2024 | Vaches / Veaux / Génisses / Taureaux en € |
| Pyramide naissances | STATE.animaux | 2010→2026 par année |
| Distribution production | mlControles | Tranches L/j — 82 vaches |
| Cellules somatiques | mlControles | Camembert <200k / 200-400k / >400k |
| TB individuel | mlControles | Barres triées, seuil 38 g/kg |
| TP individuel | mlControles | Barres triées, seuil 32 g/kg |

**Architecture** : `renderStats()` → Chart.js chargé async si absent → bouton ↺ Actualiser
**MilkLic fallback** : lit `localStorage['boviq'].mlControles` si `D.mlControles` vide (GitHub Pages)

### Fix PAT token GitHub
- Bouton "Effacer token" → confirm obligatoire avant suppression
- Badge `nopat` → message explicite `🔑 token GitHub requis`
- Token ne saute plus sur erreur 401 (pas de `clearPAT()` automatique)

### Module BOVIQ Lait (fichier standalone `boviq-module-lait.html`)
- Suivi quotas printemps Montsûrs (mars-juillet)
- Alertes contractuelles (seuil bas 4%, dépassement quota)
- CA estimé mensuel + indemnité tank
- Simulateur décalage juillet→août

### Diagnostics EARL La Rousselière (documents analysés)
- 160 animaux Simmental | production 2025 : ~235 000 L
- Prix lait 2025 : moy 496€/kL | 2026 : moy 508€/kL (grille Montsûrs)
- TB moy 36.3g (sous seuil 38) | TP moy 28.4g (sous 32 → pénalité probable)
- 11 vaches >400k cellules (mammites) | CA lait ~117k€/an
- Bilan 2024 : EBE 56 912€ | Résultat net -13 429€ | Charges structure 74 140€

---

## ✅ FEATURES LIVRÉES session 23/03/2026

### 8 features implémentées
| # | Feature | Détail |
|---|---|---|
| F1 | Raccourcis clavier | Alt+S/D/T/A/V/C/B + Ctrl+Shift + Tab trap modals |
| F2 | Alerte génisses prêtes | Conseil #22 — 24-34 mois sans saillie |
| F3 | Perf. par taureau | Conseil #23 — taux vêlages Sirocco/Ucello/U40 |
| F4 | Courbe de lactation | Chart.js async — prod moy + TB/TP par rang L1→L13 |
| F5 | Score économique fiche | Classement vache dans troupeau, 6 critères |
| F6 | Saisonnalité vêlages | Histogramme 12 mois Chart.js async |
| F7 | Widget cours dashboard | Prix lait (courbe Chart.js) + cotations viande |
| F8 | Dark mode + Notifs | Toggle 🌙/☀️ + 🔔 alertes navigateur |

### 3 fixes dashboard
- **Graphiques vides** : `loadChartJs` est une Promise → corrigé `async/await`
- **Sparkline cours** : remplacée par courbe Chart.js, axe Y borné `min/max±2€`
- **MilkLic "données non disponibles"** : bridge localStorage ajouté dans `loadML()` + `saveML()`

---

## Module Conseils & leviers — 23 analyses

| # | Analyse | Niveau |
|---|---|---|
| 1 | CCS > 400k | urgent |
| 2 | TB < 36g | attn |
| 3 | IVV > 390j | attn |
| 4 | Vaches sans reprise repro 60-180j | attn |
| 5 | Génisses > 28 mois non vêlées | attn |
| 6 | Candidates réforme | attn |
| 7 | TP < 30g | urgent |
| 8 | Ratio TB/TP < 1.2 (acidose SARA) | attn |
| 9 | Urée hors normes | attn |
| 10 | Production forte baisse | attn |
| 11 | CCS prévues > 400k | attn |
| 12 | Fortes productrices sans repro | urgent |
| 13 | Rang IA ≥ 3 | attn |
| 14 | Persistance faible | attn |
| 15 | Primipares < 7L | urgent |
| 16 | Génisses excédentaires | attn |
| 17 | Primes qualité manquées | attn |
| 18 | Coût sanitaire par vache | ok |
| 19 | Vaches improductives | attn |
| 20 | Projection vêlages → trésorerie | ok |
| 21 | Simulation changement filière | ok |
| 22 | Génisses 24-34 mois non saillies | urgent |
| 23 | Performance par taureau | attn |

---

## Données troupeau (INIT_DATA / boviq-data.json)

- **93 VL Simmental** | 50 GL | 13 mâles | 3 taureaux (U40, Ucello, Sirocco)
- **Production** : moy 9.4 L/j, prod annuelle ~234k L, CA ~98k€
- **TB moy** : 36.3g | **TP moy** : 28.4g (72% sous 30g!) | **CCS moy** : 236k
- **Taux gestation** : 22% (20/93 VL)
- **Mammite chronique** : Fellah (1465k) + Lazure (1651k)
- **Couverture FCO** : 81% (130/160)

---

## Roadmap — Reste à faire

### PENDING priorité haute
- [ ] Import CSV MilkLic dans V6 (SheetJS) — 32 VL sans données _ml_
- [ ] Widget cours marché dans dashboard (fait mais peut être enrichi)
- [ ] Histogramme saisonnalité vêlages ✅ FAIT
- [ ] Dark mode ✅ FAIT

### PENDING priorité basse (intégrations externes)
- [ ] Import PDF bilan Gecagri (OCR Claude API)
- [ ] EDNOTIF/EDEL/APIBOV
- [ ] Bilan 2025

---

## Mots-clés de reprise

| Mot-clé | Contexte |
|---------|---------|
| `BOVIQ V6` | dev troupeau principal (`boviq-v6-latest.html`) |
| `BOVIQ BILAN` | module financier (Sprint C) |
| `BOVIQ ROADMAP` | `docs/ROADMAP.md` |
| `BOVIQ COURS` | cours marché DG AGRI (`boviq-cours-marche.html`) |
| `BOVIQ AMI` | retours testeur (EARL La Rousselière) |
| `BOVIQ MILKLIC` | contrôle laitier (`boviq-milklic.html`) |
| `BOVIQ MILKLIC MAJ` | mise à jour CSV contrôle laitier |
| `BOVIQ AUDIT` | audit complet 100/100 |
| `BOVIQ GITHUB` | storage centralisé GitHub |
| `BOVIQ CONSEILS` | module 23 analyses zootechniques/économiques |
| `BOVIQ AIDES` | page aides éleveur + dossier LBC/MAEC |
| `BOVIQ STATS` | page Statistiques — 9 graphiques Chart.js |
| `BOVIQ LAIT` | module quotas Montsûrs + optimisation lactation |
