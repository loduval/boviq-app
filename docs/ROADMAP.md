# 🐄 BOVIQ — Roadmap

> **Dernière MAJ** : 28 février 2026
> **Version courante** : V6 Sprint C (boviq-v6-latest.html — 3635 lignes, ~218 KB, 8 modules)
> **Audit code** : complet — 27/02/2026
> **Phase 1** : ✅ Terminée (17/17 items — 27/02/2026)
> **Phase 2** : ✅ Sprints A, B, C terminés (28/02/2026)

---

## 📐 État du code V6

| Métrique | Valeur |
|----------|--------|
| Lignes totales | 3635 (CSS ~600 / HTML ~300 / JS ~2700) |
| Fonctions JS | ~80 |
| Modules | 8 (Dashboard, Animaux, Repro, Sanitaire, Taureaux, Vaccinal, Bilan, Races) |
| INIT_DATA | 18 animaux, 14 repros, 3 santé, 3 taureaux, 2 bilans |
| Dépendances | Google Fonts, Tabler CSS, Chart.js, pdf.js, jsPDF (CDN) |
| Stockage | localStorage clé "boviq" — try/catch + alerte quota |
| Build step | Aucun (fichier HTML autonome) |

---

## ✅ Phase 1 — Consolidation (terminée 27/02/2026)

17/17 items : XSS esc(), validation import JSON, recherche multi-critères, fiche animal,
IVV, badge onglet, CONST object, sortTable() refactoré, debounce, parseGecagri fix, etc.

---

## ✅ Phase 2 — Fonctionnalités avancées (terminée 28/02/2026)

### Sprint A — Plan vaccinal ✅
- [x] Protocoles français : IBR, BVD, RSV/PI3, FCO, Clostridies, Vermifuge
- [x] Plan vaccinal configurable par exploitation (toggles ON/OFF)
- [x] Matrice vaccination par animal (statut : à jour / en retard / jamais)
- [x] Vaccination par lot (sélection multiple → enregistrement batch)
- [x] Détection automatique vaccins existants dans historique santé

### Sprint B — Charts financiers + PDF santé ✅
- [x] Historique multi-années avec graphiques évolution (Chart.js)
- [x] Export PDF registre sanitaire complet (jsPDF)
- [x] Calendrier vaccinal fonctionnel (lié au Sprint A)

### Sprint C — Bilan amélioré ✅
- [x] Formulaire dual : mode simple (12 champs) + mode avancé (3 sections dépliantes)
- [x] Auto-calculs live : totaux, charges, marge brute en temps réel
- [x] Score /100 basé benchmarks IDELE/INOSYS 2023 (jauge visuelle pondérée)
- [x] Aides personnalisées : éligibilité automatique, badges probabilité, montants estimés
- [x] Export PDF bilan annuel complet
- [x] Duplication N-1 pour accélérer saisie nouvelles années

---

## 🌐 BOVIQ COURS — Cours du marché (✅ module standalone DONE)

**Fichier** : boviq-cours-marche.html (727 lignes) — SheetJS + Excel DG AGRI côté client
**Repo** : github.com/loduval/boviq-app — GitHub Pages actif (index.html V4 obsolète)

| Étape | Statut |
|-------|--------|
| boviq-cours-marche.html (SheetJS + Excel DG AGRI) | ✅ DONE (727 lignes) |
| CORS proxy (corsproxy.io) + fallback import manuel | ✅ DONE |
| Cache localStorage + Chart.js graphiques | ✅ DONE |
| API EC Agridata REST | ❌ MORTE (Qlik Sense, pas d'endpoint public) |
| data.gouv.fr CSV direct | ❌ IMPASSE (VISIONet ASP.NET, redirections) |
| GitHub Actions workflow | ❌ OBSOLÈTE (remplacé par SheetJS client-side) |
| Copier boviq-cours-marche.html sur Mac | ⬜ TODO |
| Intégration dans BOVIQ V6 principal | ⬜ Phase 3 |
| Pousser sur loduval/boviq-app GitHub Pages | ⬜ Optionnel |

---

## 🚀 Phase 2 restante — Items non couverts par les sprints

### Reproduction
- [ ] Historique vêlages archivés (carrière complète par vache)
- [ ] Graphique IVV par vache (évolution temporelle Chart.js)
- [ ] Conseils génétiques : matching taureau/vache basé sur races
- [ ] Gestion IA vs monte naturelle (champ type dans repro)

### UX
- [ ] Notifications navigateur (Notification API) pour alertes critiques
- [ ] Mode sombre (dark mode) via prefers-color-scheme
- [ ] Actions swipe mobile sur lignes de tableau

---

## 🌐 Phase 3 — Intégrations externes (mars-avril 2026)

### Cours et marchés
- [ ] Finaliser workflow GitHub Actions (BOVIQ COURS)
- [ ] Intégrer widget cours dans BOVIQ V6 dashboard
- [ ] Cache localStorage avec TTL pour données API
- [ ] Alertes prix (seuils configurables)

### Webservices institutionnels (complexité 5-7/10)
- [ ] EDNOTIF : notification mouvements bovins (EDE/BDNI)
- [ ] EDEL : échanges données élevage
- [ ] APIBOV : données zootechniques

---

## 📱 Phase 4 — Distribution (mai-juin 2026)

- [ ] Service Worker + cache hors-ligne
- [ ] PWA installable (manifest.json, icônes)
- [ ] Packaging EXE/DMG (PyWebView ou Tauri)
- [ ] Synchronisation multi-appareils (backend léger — optionnel)

---

## 🔮 Phase 5 — Vision long terme

### IoT & capteurs
- [ ] Intégration Mozaë, Allflex, Gallagher
- [ ] Détection chaleurs automatique, monitoring rumination
- [ ] Scan NFC boucles smartphone

### Intelligence artificielle
- [ ] Assistant IA conversationnel
- [ ] Prédiction sanitaire, benchmarking régional
- [ ] Optimisation alimentaire

### Cartographie
- [ ] Carte parcellaire GPS, rotation pâturage + météo

---

## 📊 Métriques

| KPI | Actuel | Cible | Horizon |
|-----|--------|-------|---------|
| Modules fonctionnels | 8 | 12 | Phase 3 |
| Lignes de code | 3635 | < 5000 | Maintenu |
| Taille fichier | 218 KB | < 300 KB | Maintenu |
| Bugs connus | 0 | 0 | ✅ |
| Éleveurs testeurs | 1 | 5 | Phase 3 |

---

## 📋 Mots-clés de reprise

- **BOVIQ V6** → dev troupeau (app principale)
- **BOVIQ BILAN** → analyse financière
- **BOVIQ ROADMAP** → cette feuille de route
- **BOVIQ COURS** → cours du marché (GitHub Pages)

---
*Roadmap BOVIQ — Claude — MAJ 28/02/2026*
