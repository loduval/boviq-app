# BOVIQ — MEMORY SESSION

Dernière mise à jour : **22/03/2026 — 20h30** — BOVIQ MilKlic : Santé Mamelles, fix import Windows, audit JS 32/32, backup complet

---

## État du projet — 22/03/2026 soir

| Fichier | Lignes | Taille | Dernier commit |
|---------|--------|--------|----------------|
| `boviq-v6-latest.html` | 6 321 | ~480 KB | `78d8946` |
| `boviq-milklic.html` | ~500 | ~158 KB | `db45218` |
| `boviq-cours-marche.html` | 1 139 | 47 KB | — |
| `index.html` | 370 | ~19 KB | `4cae003` |
| `scripts/backup-nas.sh` | 82 | — | `db45218` |

**Repo GitHub** : `loduval/boviq-app` (public)  
**GitHub Pages** : `loduval.github.io/boviq-app/`  
**_dataVersion** : `20260321` · **162 animaux** · 82 VL contrôlées au 04/03/26

---

## ⚠️ RÈGLE ABSOLUE — NE PLUS JAMAIS FAIRE

```bash
# ❌ INTERDIT — écrase le hub index.html par le code V6
cp boviq-v6-latest.html index.html
# ✅ CORRECT — pousser les fichiers séparément
git add boviq-v6-latest.html boviq-milklic.html
git commit -m "..." && git push
```

`index.html` = **hub portal 370 lignes**. Ne jamais écraser.

---

## ⚠️ RÈGLE TECHNIQUE — TOUJOURS VÉRIFIER SYNTAXE JS

Après tout edit_block sur un fichier HTML contenant du JS :
```bash
node -e "const h=require('fs').readFileSync('boviq-milklic.html','utf8'); \
require('fs').writeFileSync('/tmp/t.js',h.substring(h.indexOf('<script>')+8,h.lastIndexOf('</script>')));" \
&& node --check /tmp/t.js && echo "OK"
```
Une fonction manquante (ex: `function openSanteModal` effacée par erreur) casse **tout le JS silencieusement**.

---

## Architecture fichiers actifs

```
BOVIQ/
├── index.html                  ← HUB ~370L (JAMAIS écraser!)
├── boviq-v6-latest.html        ← 6321L, ~480KB, gestion troupeau V6
├── boviq-milklic.html          ← ~500L, 158KB, contrôle laitier
├── boviq-cours-marche.html     ← 1139L, 47KB, cours marché DG AGRI
├── manifest.json               ← PWA
├── sw.js                       ← cache
├── scripts/
│   ├── backup-nas.sh           ← sauvegarde NAS auto-détection
│   ├── audit-boviq.py          ← audit V6
│   ├── milklic-sync.py         ← sync Windows
│   └── update-cours-data.py
├── docs/
│   ├── MEMORY.md  INDEX.md  ROADMAP.md  BOVIQ-COURS-NOTES.md
├── _backups-v6/                ← snapshots HTML horodatés
│   └── boviq-milklic-20260322-2002.html  ← dernier bon état
└── DERNIERE-VERSION/           ← 8 CSV MilKlic 21/03/2026
```

---

## BOVIQ MilKlic — État complet 22/03/2026

### Pages disponibles (6)
| Nav btn | Page | Fonction render |
|---------|------|-----------------|
| Import CSV | `page-import` | `handleFiles()` |
| Tableau de bord | `page-dashboard` | `renderDashboard()` |
| Cellules | `page-cellules` | `renderCellules()` |
| Repro / IA | `page-repro` | `renderRepro()` |
| **Santé mamelles** ← NOUVEAU | `page-sante` | `renderSante()` |
| Courbes | `page-courbes` | `renderCourbesInit()` |
| Intégration BOVIQ | `page-bridge` | `renderBridge()` |

### Page Santé Mamelles (nouveau — session 22/03/2026)
- Tableau toutes VL avec données (en traite + taries)
- **Sparkline SVG** 12 mois par vache, ligne seuil 200k pointillée
- **Code couleur** : 🟢 Saine / 🔵 Épisodique / 🟠 Fréquente / 🔴 Chronique (≥3 consécutifs >200k)
- **Filtres** : Toutes / par profil, boutons colorés avec état actif
- **Recherche** par nom ou n° travail, temps réel
- **Compteur** : "12 / 82 vaches"
- **Modal** au clic sur le nom : historique 12 mois avec barres colorées

### Fix import Windows Chrome (session 22/03/2026)
- Bug : `fi.value=''` immédiatement après `handleFiles()` invalidait les File objects sur Windows Chrome
- Fix : `fi.value=''` déplacé dans `Promise.all().then()` après lecture complète
- Aussi : `accept=".csv,.CSV,text/csv"`, input `opacity:0` au lieu de `display:none`
- Bouton "📂 Choisir les fichiers" ajouté comme fallback

### Audit JS 22/03/2026 — 32/32 OK
- Syntaxe valide (node --check)
- 35 getElementById() → tous présents
- 31 fonctions définies
- 6 pages / 6 nav buttons cohérents
- 24 CSS variables toutes définies
- 1 faux positif : `data-p="milklic"` dans un `<pre>` de documentation

### localStorage
- Clé unique : `boviq` (contient BOVIQ_MILKLIC_DATA complet)
- INIT_ML_DATA embarqué : 162 animaux, contrôle 04/03/2026

---

## Backups 22/03/2026

| Type | Chemin | Contenu |
|------|--------|---------|
| Local | `~/Desktop/BOVIQ_BACKUP_20260322-201743/` | 86 fichiers, 17MB |
| GitHub | commit `db45218` | historique complet |
| NAS | à faire : `./scripts/backup-nas.sh` | quand NAS monté |
| Snapshot HTML | `_backups-v6/boviq-milklic-20260322-2002.html` | bon état 20h02 |

---

## Mots-clés de reprise

- `BOVIQ V6` → dev troupeau (`boviq-v6-latest.html`)
- `BOVIQ BILAN` → module financier
- `BOVIQ ROADMAP` → `docs/ROADMAP.md`
- `BOVIQ COURS` → cours marché DG AGRI
- `BOVIQ AMI` → retours testeur EARL La Rousselière
- `BOVIQ MILKLIC` → contrôle laitier (`boviq-milklic.html`)
- `BOVIQ MILKLIC MAJ` → mise à jour CSV + INIT_ML_DATA
- `BOVIQ AUDIT` → audit complet 100/100
- `BOVIQ NAS` → sync NAS (`./scripts/backup-nas.sh`)

---

## Historique commits récents (milklic)

```
db45218  backup: script NAS auto-détection
cdfac33  clean: suppression panel diagnostic, syntaxe validée
ff236d8  fix: SyntaxError - function openSanteModal manquante
b4d518d  feat: sante mamelles - filtres + recherche + compteur
a007a06  feat: page Santé Mamelles - sparklines, code couleur, modal
1e15c4c  fix: grid 2x2 direct dashboard
71ceea1  fix: fi.value='' dans Promise.all (import Windows)
```
