# 🐄 BOVIQ — Mémoire Centralisée

> **Dernière MAJ** : 28 février 2026
> **Dossier** : `~/Desktop/01-Projects/BOVIQ/`
> **Projet Claude** : Fichiers boviq.html (V6), boviq-v5.html, 2024_BILAN_compressed.pdf

---

## 🔑 Mots-clés de reprise

| Mot-clé | Scope | Description |
|---------|-------|-------------|
| `BOVIQ V6` | Gestion troupeau | App complète : animaux, repro, sanitaire, taureaux, vaccins, bilan, KPI |
| `BOVIQ BILAN` | Analyse financière | Module bilan intégré : formulaire simple/avancé, score IDELE, aides, export PDF |
| `BOVIQ ROADMAP` | Feuille de route | ROADMAP.md — planification phases |
| `BOVIQ COURS` | Cours du marché | GitHub loduval/boviq-app — cotations viande/lait temps réel |

---

## 📋 Contexte projet

**BOVIQ** est une application de gestion de troupeau bovin pour éleveurs laitiers français. Remplace les tableurs Excel par un outil fonctionnel, visuel et pratique. Testée avec le troupeau d'un ami éleveur (EARL La Rousselière, Bauvin).

### Principes directeurs
- **Simplicité** : focus usage quotidien, pas de fonctions institutionnelles complexes
- **Single-file HTML** : zéro infra serveur, ouvre dans un navigateur
- **Données réelles** : testée avec troupeau réel (18 animaux, 14 repros, 3 traitements, 3 taureaux)
- **Design soigné** : Tabler CSS + Chart.js, polices Playfair Display + DM Sans
- **localStorage** : persistance locale, clé "boviq"
- **Approche non anxiogène** : bilan financier constructif, pas alarmiste

---

## 🏗️ Architecture technique

```
Stack  : Single HTML (3635 lignes — V6 Sprint C)
CSS    : Tabler 1.0.0-beta17 CDN + CSS vars (--brand green)
JS     : Chart.js 4.4.7 CDN, pdf.js (module bilan), jsPDF (exports PDF)
Fonts  : Playfair Display (titres), DM Sans (corps)
Data   : localStorage clé "boviq" + bilans[]
Export : JSON (backup/restore), CSV, PDF
```

---

## 📦 État des modules (V6 — 28 fév 2026)

### 1. Dashboard
- Grille 2×2 centrée (940px) : calendrier, échéances, alertes, répartition troupeau
- KPIs cliquables : Vaches, Génisses, Gestantes, Taries, Terme dépassé, Délais attente
- 3 sections alertes : vêlage, délai lait, délai viande
- Badge titre onglet "(3) BOVIQ" avec alertes actives

### 2. Animaux
- CRUD complet + fiche modale individuelle (généalogie, timeline repro+santé)
- Tabs : Tous / Vaches / Génisses / Mâles
- Tri multi-colonnes, recherche avancée multi-critères (race, statut, âge)
- Promotion auto Génisse → Vache après vêlage, icônes ♀/♂/🐂

### 3. Reproduction
- Modals séparés : Saillie + Naissance (auto-création veau + parenté)
- Affichage gestantes + taries uniquement, nom ROUGE si <15j du terme
- IVV par vache + moyenne troupeau
- Référentiel 15 races IDELE (277-295j gestation)

### 4. Sanitaire
- Multi-lignes traitement par ordonnance (plusieurs produits/intervenants)
- Délais d'attente lait et viande, sélecteur animaux avec icônes
- Export PDF registre sanitaire

### 5. Taureaux — Registre complet ✅

### 6. Plan vaccinal (Sprint A)
- Protocoles français : IBR, BVD, RSV/PI3, FCO, Clostridies, Vermifuge
- Plan vaccinal configurable par exploitation
- Matrice vaccination par animal, vaccination par lot
- Détection automatique vaccins existants dans historique santé

### 7. Analyse financière / Bilan (Sprint B+C)
- **Formulaire dual** : mode simple (12 champs) + mode avancé (3 sections dépliantes)
- Import PDF Gecagri (pdf.js) + saisie manuelle
- **Auto-calculs live** : totaux, charges, marge brute en temps réel
- **Score /100** basé sur benchmarks IDELE/INOSYS 2023 (jauge visuelle pondérée)
- **Aides personnalisées** : éligibilité auto, badges probabilité, montants estimés
- Comparatif N/N-1 avec ratios EBE/UGB/VL
- **Export PDF bilan annuel** complet (jsPDF)
- Duplication N-1 pour accélérer la saisie
- Charts financiers (Chart.js) : évolution CA, charges, résultats
- 10 aides détaillées (PAC, ACL, MAEC, PCAE, bien-être, protéines, assurance, DJA, ICHN, ACSEA)

---

## 🌐 BOVIQ COURS — Module cours du marché (✅ DONE)

### Solution finale (28 fév 2026)
- **Fichier** : `boviq-cours-marche.html` (727 lignes, standalone single-file)
- **Approche** : SheetJS côté client — parse les Excel DG AGRI directement dans le navigateur
- **CORS** : proxy corsproxy.io + fallback import manuel Excel
- **Cache** : localStorage avec TTL
- **Graphiques** : Chart.js (évolution prix)

### Sources de données validées
| Donnée | Document ID | Colonne FR |
|--------|------------|------------|
| Prix lait cru (mensuel) | 62d01488 | Col K, ligne 11 |
| Cotations bovins carcasse (hebdo) | db5b282e | Col K, ligne 11 |

URL pattern : `agriculture.ec.europa.eu/document/download/{DOC_ID}_en?filename=...xlsx`

### Ce qui a été abandonné
- **API REST EC Agridata** : MORTE (Qlik Sense, pas d'endpoint JSON public)
- **data.gouv.fr CSV** : IMPASSE (VISIONet ASP.NET, redirections 302 infinies)
- **GitHub Actions workflow** : OBSOLÈTE (remplacé par SheetJS client-side)

### Repo GitHub existant
- **Repo** : `loduval/boviq-app` (public)
- **GitHub Pages** : `https://loduval.github.io/boviq-app/` — actif
- **État actuel** : index.html V4 (ancienne version CSV-based, OBSOLÈTE)
- **Usage futur** : héberger boviq-cours-marche.html ou BOVIQ V6 complet

### Prochaines étapes
1. Copier boviq-cours-marche.html sur le Mac
2. Intégrer module cours dans BOVIQ V6 (onglet ou widget dashboard)
3. Optionnel : pousser sur GitHub Pages (loduval/boviq-app)

---

## 🧪 Données de test (INIT_DATA)

- **18 animaux** dont Tagada (génisse vêlée 08/02 → auto-promotion vache)
- **14 repros**, **3 santé**, **3 taureaux**
- Source : backup JSON éleveur ami (25 fév 2026)

---

## 📊 Benchmark concurrentiel

Analysé : Troup'O/ISAGRI, Synel, VacApp, Tambero, MilkingCloud, Cattlytics, My Cattle Manager, SMAG Bovin, Mozaë, Pilot'Elevage

### Différenciateurs BOVIQ
- Zéro abonnement, zéro cloud, zéro installation
- Module bilan financier intégré (unique sur le marché)
- Cours du marché temps réel (aucun concurrent ne l'intègre)
- Plan vaccinal protocoles français
- Design premium vs interfaces datées concurrents

---

## 🔌 Sources de données & API

| Source | Données | Accès | Statut |
|--------|---------|-------|--------|
| DG AGRI Excel (EC) | Prix lait FR + cotations bovins carcasse | Excel download (SheetJS) | 🟢 ACTIF |
| data.gouv.fr | Cotations viande bovine FranceAgriMer | CSV (bloqué VISIONet) | 🔴 IMPASSE |
| Agridata EC API | Prix lait, viande (JSON REST) | API morte (Qlik Sense) | 🔴 MORT |
| EDNOTIF | Identification bovine | Webservice auth | 🔵 Futur |
| EDEL | Échanges élevage | Webservice auth | 🔵 Futur |
| APIBOV | Données zootechniques | Webservice auth | 🔵 Futur |

---

## 💬 Sessions clés

| Date | Titre | Contenu |
|------|-------|---------|
| 22 fév | Gestion cycles reproduction | V0→V1, recherche API cours, mockup mobile, étude marché |
| 25 fév | Autosave et exe | V2→V4 Tabler, packaging PyWebView |
| 25-26 fév | Retours éleveur | V5 retours terrain (catégories, alertes, multi-traitements) |
| 27 fév | Bilan comptable | Extraction PDF Gecagri, prototype bilan |
| 27 fév | Dev V6 complet | Phase 1 (17 correctifs), organisation dossier Mac |
| 27 fév | Sprint A+B | Vaccinal + charts financiers + PDF santé |
| 28 fév | Sprint C | Bilan amélioré : auto-calculs, score IDELE, aides, PDF export |
| 28 fév | BOVIQ COURS | API EC morte, data.gouv impasse → solution SheetJS client-side (727 lignes) |
| 28 fév | BOVIQ COURS v2 | Investigation CORS proxies, Excel DG AGRI (lait 62d01488, beef db5b282e) |

---
*Fichier généré par Claude — Projet BOVIQ — MAJ 28/02/2026*
