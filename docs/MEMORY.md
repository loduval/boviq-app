# BOVIQ — MEMORY SESSION

Dernière mise à jour : 21/03/2026 (session — BOVIQ MILKLIC : analyse CSV + fusion données + onglet contrôle laitier + fix layout + debug TDZ)

---

## État du projet

**boviq-v6-latest.html** — 5749 lignes, 439 KB  
Dernier commit : `181e9db` — fix: page p-milklic repositionnée dans .content  
**boviq-milklic.html** — 511 lignes, 36 KB (module MilKlic standalone)  
**Repo GitHub** : `loduval/boviq-app` (public)  
**GitHub Pages** : `loduval.github.io/boviq-app/`  
**Page d'accueil** : `index.html` (landing page 3 cartes : BOVIQ V6 + Cours + MilKlic)  
**Working tree** : ✅ propre (clean)

---

## Session 21/03/2026 — BOVIQ MILKLIC

### Analyse complète des 8 CSV MilKlic

Fichiers récupérés dans `DERNIERE-VERSION/` (sync tâche planifiée Windows lundi 7h) :

| Fichier | Contenu | Animaux |
|---|---|---|
| 01-ResultatsBruts | Dernier contrôle : lait 24h, TB, TP, leucos, urée | 93 VL + statuts |
| 02-ValoriseIndividuel | Vue complète : repro, conseils IA, évolution | 95 animaux |
| 03-HistoLait | Courbe lait 12 contrôles (avr.24→mar.26) | 75 VL |
| 04-HistoTB | Idem TB | 75 VL |
| 05-HistoTP | Idem TP | 75 VL |
| 06-HistoCellules | SDIR + leucos 5 contrôles | 83 VL |
| 07-Inventaire | Registre complet VL/GL/GV/MA | ~155 animaux |
| 09-Gestation | Vide (crash serveur 08) | — |

**Clé de jointure** : `Trav` (4 derniers chiffres N° travail) ↔ `boucle` BOVIQ normalisée (`s.replace(/\s/g,'')`)

### Fusion données réalisée

Script Python `processBruts + processValorise + processInventaire` :
- 160 animaux fusionnés (152 BOVIQ + 8 nouveaux inventaire)
- 82 VL avec données contrôle (`_ml_lait24`, `_ml_tb`, `_ml_tp`, `_ml_leucos`, `_ml_uree`)
- 49 dates d'IA avec tarissements prévus
- 19 conseils IA (déconseillée / à inséminér / possible)
- Champs `_ml_*` ajoutés dans chaque animal BOVIQ

**`_dataVersion: 20260321`** — à incrémenter à chaque regénération

### Onglet "🥛 Contrôle Laitier" dans BOVIQ V6

- Nav button ajouté après "Analyse financière"
- Page `id="p-milklic"` avec KPIs, alertes cellules, conseils IA, table filtrable
- `goTo('milklic')` → `renderMilklic()` — filtre : all / alert / conseil / tar / vide
- Lien vers `boviq-milklic.html` pour module standalone avec courbes

### Module boviq-milklic.html (standalone)

Fichier indépendant — import CSV côté client (windows-1252) :
- Drop-zone multi-fichiers
- Parse 8 types de CSV auto-détectés par nom
- localStorage `BOVIQ_MILKLIC` (clé partagée avec BOVIQ V6)
- Dashboard : KPIs, alertes, repro, signaux faibles
- Page Cellules : tableau classé leucos + SDIR + seuil filtrable
- Page Repro : IA déconseillée / à inséminér / tarissements / vaches vides FV/TFV
- Page Courbes : Chart.js lait/TB/TP/cellules par animal
- Page Intégration : instructions bridge localStorage + statut correspondances

### Infrastructure Git — problèmes résolus

**Situation initiale** : deux repos (Mac `~/Desktop/01-Projects/BOVIQ` + Windows `C:\BOVIQ`) en conflit.
- Mac = source de vérité ✅
- Windows = clone pour tâche planifiée MilKlic uniquement (pas de commits directs)
- `index.html` perdu lors rebase → restauré depuis `git show f9040e0:index.html`
- `DERNIERE-VERSION/` (CSV MilKlic) committé dans le repo (à déplacer dans .gitignore si lourd)

**Partage réseau Mac→Windows** :
- `\\192.168.1.50\laurentduval` = home Mac (symlinks Desktop non traversables)
- `\\192.168.1.50\Macintosh HD` = disque Mac complet (X:)
- `\\192.168.1.50\01-Projects` = partage dédié (accessible)
- Écriture fichiers Mac depuis filesystem MCP via `/Users/laurentduval/...` ✅

### Bug critique identifié (non résolu)

**Erreur TDZ** : `Cannot access 'pages' before initialization` à la ligne 1564 (goTo)  
Cause probable : variable `const pages` déclarée dans le scope global ET dans `renderMilklic` (code injecté)  
Symptôme : tous les onglets cassés, données ne s'affichent pas  
**Workaround** : vider le localStorage `boviq` dans le navigateur → INIT_DATA 20260321 se charge  
**Fix définitif à faire** : audit `const pages` dans renderMilklic → renommer en `mlAnimals` ou `filteredAnimals`

---

## Commits session 21/03/2026

| Commit | Description |
|--------|-------------|
| `91f33b1` | docs: MEMORY.md + INDEX.md mis à jour session 21/03 (MilKlic sync + fixes) |
| `b98cb4e` | feat: module contrôle laitier MilKlic standalone |
| `d7cb48c` | chore: sync .gitignore + merge Windows commits |
| `d51e207` | restore: boviq-v6-latest.html (5627L) + backup |
| `ad95083` | restore: index.html (landing page) + lien MilKlic |
| `290ba0a` | feat: onglet Contrôle Laitier + fusion données MilKlic 21/03/26 |
| `181e9db` | fix: page p-milklic repositionnée dans .content + padding + goTo hook |

---

## Données réelles intégrées

`_dataVersion: 20260321` — 163 animaux EARL La Rousselière  
- ~96 VL en lactation, génisses U/V/A, veaux récents
- 82 VL avec données contrôle MilKlic du 04/03/26
- 3 taureaux : U40 (Holstein Red), Ucello (Simmental), Sirocco (Normande)
- 134 actes sanitaires (dont campagne FCO 17/03/26)
- 28 repros actives
- Bilan 2024 injecté (id: `bilan2024-rousseliere`)

---

## Architecture fichiers actifs

```
BOVIQ/
├── index.html                  ← landing 3 cartes
├── boviq-v6-latest.html        ← 5749 lignes, 439 KB
├── boviq-milklic.html          ← 511 lignes, module MilKlic
├── boviq-cours-marche.html
├── manifest.json + sw.js
├── icons/
├── DERNIERE-VERSION/           ← CSV MilKlic 21/03/26
├── docs/ (MEMORY/INDEX/ROADMAP/BOVIQ-COURS-NOTES)
├── data/bilan/
├── data/market/
├── scripts/                    ← milklic-sync.py (Windows)
├── _backups-v6/                ← boviq-v6-20260321-avant-milklic.html
├── _backups-ami/               ← boviq_backup_20260321.json
└── _archives/
```

---

## À faire session suivante (BUG PRIORITAIRE)

1. **Fix TDZ `const pages`** dans `renderMilklic()` — renommer variable locale
2. Tester l'onglet Contrôle Laitier avec données réelles dans le navigateur ami
3. Enrichir fiches animaux individuelles avec données `_ml_*` (section dans modal animal)
4. Mettre à jour ROADMAP.md

---

## Mots-clé reprise

**`BOVIQ V6 REPRISE`** — reprise sur Mac  
Actions : `cd ~/Desktop/01-Projects/BOVIQ && git log --oneline -5 && git status && wc -l boviq-v6-latest.html`

**`BOVIQ MILKLIC`** — module contrôle laitier  
Script sync : `C:\BOVIQ\scripts\milklic-sync.py` (Windows, lundi 7h)  
Bug TDZ à corriger : `const pages` dans `renderMilklic()`

**`BOVIQ AMI`** — tests éleveur ami  
localStorage à vider manuellement (version 20260318 → forcer 20260321)

**`BOVIQ MILKLIC FIX`** — corriger bug TDZ + tester onglet complet
