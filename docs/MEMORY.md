# BOVIQ — MEMORY SESSION

Dernière mise à jour : 20/03/2026 (session PM — fix scanner desktop + audit complet + fix B1 journal)

---

## État du projet

**boviq-v6-latest.html** — 4791 lignes  
Dernier commit : `a7fcbe0` — 🏛️ BDNI fix EDE + disclaimer  
**Repo GitHub** : `loduval/boviq-app` (public)  
**GitHub Pages** : `loduval.github.io/boviq-app/`  
**Page d'accueil** : `index.html` (landing page 2 cartes)  
**App principale** : `boviq-v6-latest.html`  
**Working tree** : ✅ propre (clean)

---

## Session 20/03/2026 PM — fix scanner + audit + corrections

### Fix scanner index.html (`14504f9`)
- `lancerScan()` redirigait silencieusement vers boviq-v6-latest.html sur desktop
- Correction : détection userAgent → popup "Fonction mobile uniquement" sur desktop
- Popup "Navigateur non compatible" sur mobile sans BarcodeDetector
- cache-bust 20260320-6

### Audit complet (`af91dad`)
- Syntaxe JS : 0 erreur (`node --check`)
- IDs HTML : 2 anomalies → 1 faux positif (querySelector class), 1 bug réel
- **B1 corrigé** : `jv-type` → `jn-type` dans `renderJournal()` (clic "+ Ajouter" dans module journal vide)
- Intégrité données : 0 référence orpheline (animaux/repros/sante)
- Doublons sanitaire : 0
- **B2 data** (à valider avec ami) : Oxygène a 2 repros avec velageReel=2026-02-28 (doublon saillie)
- **B3 data** (à valider avec ami) : Larousse a 2 saillies actives sans vêlage (2025-09-12 + 2025-05-21)
- B4 mineur : 133 entrées sante[] conservent champs legacy top-level (nettoyés à load(), non bloquant)

### État fichiers actifs
- `boviq-v6-latest.html` : 5579 lignes
- `index.html` : 267 lignes (landing 3 cartes + météo)
- Dernier commit : `af91dad`



### Audit code (matin)
- **Double check** : 0 bug fonctionnel, 0 ID orphelin, 0 modal sans fermeture
- **Fonctions mortes supprimées** : `noTravailFn` (doublon closure), `calcIVVTroupeau` (jamais appelée)
- **Fix** : select `a-type` manquait option "Veau" (4 animaux dans données) → `6bc634d`
- **commit** nettoyage fonctions mortes → `0c8987d`

### Bilan financier 2024 EARL La Rousselière
- PDF Gecagri = **scan** (image) → parseur pdf.js ne peut pas lire — détection BOVIQ correcte
- Données extraites manuellement + injectées en dur dans `load()` (migration propre) → `3441422`
- **Benchmarks Simmental** : `SEUIL_LAIT_VL` 5000→4500, `BENCH.laitVL` 7200→4500 → `b9d625f`
- **3 conseils ciblés** dans "Pistes et conseils" → `36c9d61` :
  1. "La structure économique est saine" (résultat courant +38 730 € positif)
  2. "+29 911 € de CA accessibles" (objectif 3 500 L/VL sans investissement)
  3. "Production -15% vs 2023 — à investiguer" (chute individuelle malgré +6 VL)

### BDNI
- Lien EDE Mayenne cassé (`mayenne.chambagri.fr`) → remplacé par `id-bovin.fr` (national)
- Disclaimer ajouté : BOVIQ = outil suivi privé, non certifié BDNI, Boviclic/Oribase obligatoires → `a7fcbe0`

### Investigation Seenovia / Mil'Klic
- Mil'Klic = extranet SIEL, accès via `seenovia.fr` (Seenovia = membre réseau SIEL dép. 53)
- **Pas d'API publique** ni export CSV documenté côté éleveur — consultation seulement + imprimer
- Données proviennent de : agent de pesée Seenovia (1×/mois, smartphone, + labo TB/TP/cellules)
- **Plan** : attendre que l'ami exporte un fichier depuis Mil'Klic desktop pour construire parseur

---

## Commits session 20/03/2026

| Commit | Description |
|--------|-------------|
| `6bc634d` | Fix select a-type option "Veau" |
| `9ace1de` | MEMORY.md màj audit |
| `0c8987d` | Suppression fonctions mortes (noTravailFn, calcIVVTroupeau) |
| `3441422` | Bilan 2024 EARL La Rousselière injecté en dur |
| `b9d625f` | Benchmarks Simmental: seuils lait/VL |
| `36c9d61` | 3 conseils ciblés analyse financière |
| `a7fcbe0` | BDNI: fix EDE + disclaimer Boviclic/Oribase |

---

## Chiffres clés bilan 2024 EARL La Rousselière (injectés)

| Indicateur | 2024 | 2023 |
|---|---|---|
| VL | 96 | 90 |
| Lait produit | 259 659 L | 285 146 L |
| Lait/VL | **2 705 L** | 3 168 L (-15%) |
| Quota contractuel | 320 000 L | — |
| Sous-quota | **60 549 L** = -29 911 € CA | — |
| Prix lait | 0,494 €/L | — |
| EBE | 56 912 € | 77 352 € |
| Résultat courant | +38 730 € | +61 898 € |
| Résultat net | **-13 429 €** | +11 498 € |
| Rémunération associés | 50 400 € | 50 400 € |
| Annuités 2025 (prévu) | 25 351 € | 20 197 € |

---

## Architecture fichiers actifs

```
BOVIQ/
├── index.html
├── boviq-v6-latest.html        ← 4791 lignes
├── boviq-cours-marche.html
├── manifest.json + sw.js       ← PWA
├── icons/ (180/192/512)
├── docs/ (MEMORY/INDEX/ROADMAP/BOVIQ-COURS-NOTES)
├── data/bilan/                 ← 2024_BILAN.pdf (scan)
├── data/market/
├── scripts/
├── _backups-v6/
├── _backups-ami/
└── _archives/
```

---

## Données réelles intégrées

`_dataVersion: 20260318` — ~155 animaux EARL La Rousselière  
Troupeau Simmental + quelques Holstein, Mayenne (53), La Chapelle Rainsouin  
3 taureaux : U40 (Holstein Red), Ucello (Simmental), Sirocco (Normande)  
Bilan 2024 : injecté via migration `load()` (id: `bilan2024-rousseliere`)

---

## Mot-clé reprise

**`BOVIQ V6 REPRISE`**  
Actions : 1) `git log --oneline -5 && git status && wc -l boviq-v6-latest.html`  
2) Comparer avec fichier uploadé si présent  
3) Push corrections si nécessaire  
4) Màj MEMORY.md + docs
