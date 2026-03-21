# 🐄 BOVIQ — Roadmap

> **Dernière MAJ** : 20/03/2026
> **Version courante** : V6 post-audit (boviq-v6-latest.html — 4791 lignes)
> **Dernier commit** : `a7fcbe0`
> **Phase 1** : ✅ Terminée
> **Phase 2** : ✅ Sprints A, B, C terminés
> **Audit 20/03** : ✅ 0 bug, 0 fonction morte, 0 ID orphelin

---

## ✅ Réalisé en session 20/03/2026

- [x] Audit complet code (fonctions, IDs, modals, cohérence)
- [x] Suppression fonctions mortes (`noTravailFn`, `calcIVVTroupeau`)
- [x] Fix select `a-type` option "Veau" manquante
- [x] Bilan 2024 EARL La Rousselière injecté en dur (migration `load()`)
- [x] Benchmarks Simmental : seuils lait/VL 5000→4500, référence 7200→4500
- [x] 3 conseils ciblés analyse financière (structure saine, potentiel CA, chute prod)
- [x] BDNI : fix lien EDE (`id-bovin.fr`) + disclaimer Boviclic/Oribase
- [x] Investigation Seenovia/Mil'Klic : pas d'API, consultation seule, attente export

---

## 🔴 Tâches prioritaires (prochaine session)

### Ergonomie — raccourcis clavier (demande AMI)
- [ ] `Ctrl+S` dans page Repro → ouvre modal Saillie
- [ ] `Ctrl+D` dans page Repro → ouvre modal Vêlage
- [ ] `Ctrl+T` dans page Sanitaire → ouvre modal Traitement
- [ ] `Ctrl+P` dans modal Sanitaire → ajoute un produit (`addLigneSante()`)
- [ ] **Tab modal-only** : focus Tab doit rester dans le modal ouvert (pas de fuite vers sidebar)

### Import Seenovia / Mil'Klic
- [ ] Attendre export fichier (CSV ou Excel) de l'ami depuis Mil'Klic desktop
- [ ] Construire parseur SheetJS selon format réel du fichier
- [ ] Nouveau module "Performances laitières" : Lait/TB/TP/Cellules par boucle + date pesée
- [ ] Historique pesées par animal (graphique courbe de lactation)

### Bilan financier
- [ ] Import PDF natif Gecagri (demander au comptable PDF non scanné)
- [ ] OCR fallback via API Claude (si PDF scanné — clé API à gérer)
- [ ] Bilan 2025 : injecter en dur même méthode (comparatif N vs N-1 automatique dans "Évolution")

---

## 🟠 Tâches secondaires

### Reproduction
- [ ] Historique vêlages archivés (carrière complète par vache)
- [ ] Graphique IVV par vache (Chart.js)
- [ ] Gestion IA vs monte naturelle (champ type dans repro)

### BDNI
- [ ] Vérifier lien `id-bovin.fr` dans `renderBDNI()` (ligne 4661 — même correction à valider)

### UX
- [ ] Mode sombre (dark mode via `prefers-color-scheme`)
- [ ] Notifications navigateur (Notification API) alertes critiques
- [ ] Actions swipe mobile sur lignes tableau

---

## 🟡 Phase 3 — Intégrations externes

### Cours et marchés
- [ ] Widget cours marché dans BOVIQ V6 dashboard (BOVIQ COURS standalone existant)
- [ ] Cache localStorage avec TTL
- [ ] Alertes prix (seuils configurables)

### Webservices institutionnels (complexité haute)
- [ ] EDNOTIF : notification mouvements bovins
- [ ] EDEL : échanges données élevage
- [ ] APIBOV : données zootechniques

---

## 🔵 Phase 4 — Distribution

- [x] PWA manifest + sw.js + icônes ✅ (19/03/2026)
- [ ] Packaging EXE/DMG (PyWebView ou Tauri)
- [ ] Synchronisation multi-appareils (backend léger)

---

## 🔮 Phase 5 — Vision long terme

- [ ] Intégration Mozaë, Allflex, Gallagher (IoT)
- [ ] Scan NFC boucles smartphone
- [ ] Assistant IA conversationnel (déjà testé via API Claude)
- [ ] Prédiction sanitaire, benchmarking régional
- [ ] Cartographie parcellaire GPS + rotation pâturage

---

## 📊 Métriques

| KPI | Actuel | Cible |
|-----|--------|-------|
| Modules | 9 | 12 |
| Lignes de code | 4791 | < 5500 |
| Fonctions JS | 125 | < 130 |
| Bugs connus | 0 | 0 |
| Éleveurs testeurs | 1 | 5 |

---

## 📋 Mots-clés de reprise

- **`BOVIQ V6`** → dev troupeau app principale
- **`BOVIQ BILAN`** → analyse financière
- **`BOVIQ ROADMAP`** → cette feuille de route
- **`BOVIQ COURS`** → cours du marché (module standalone)
- **`BOVIQ AMI`** → retours testeur EARL La Rousselière

---
*Roadmap BOVIQ — Claude — MAJ 20/03/2026*
