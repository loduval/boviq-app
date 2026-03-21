# BOVIQ COURS - Notes techniques (MAJ 28/02/2026)

## ✅ Solution finale : SheetJS côté client

### Approche retenue
boviq-cours-marche.html (727 lignes) — standalone single-file HTML
- Parse les Excel DG AGRI directement dans le navigateur via SheetJS
- CORS proxy (corsproxy.io) pour télécharger les .xlsx depuis agriculture.ec.europa.eu
- Fallback : import manuel Excel si proxy indisponible
- Cache localStorage avec TTL pour éviter les requêtes répétées
- Affichage : tableaux + graphiques Chart.js (évolution prix lait, cotations viande)

### Sources de données (VALIDÉES)
| Donnée | Document ID | URL Excel | Colonne FR |
|--------|------------|-----------|------------|
| Prix lait cru | 62d01488 | agriculture.ec.europa.eu/document/download/62d01488-33a0-4601-a841-ca48fa11d999_en | Col K, ligne 11 |
| Cotations bovins carcasse | db5b282e | agriculture.ec.europa.eu/document/download/db5b282e-a2b4-4d18-91bd-bd4854dc2030_en | Col K, ligne 11 |

### Stack technique
- SheetJS (xlsx.full.min.js) via CDN — parsing Excel côté client
- Chart.js 4.x — graphiques d'évolution
- Tabler CSS — cohérent avec BOVIQ V6
- localStorage — cache des données parsées

---

## ❌ Approches abandonnées

### 1. API REST EC Agridata — MORTE
- Tous les endpoints /api/* renvoient 404 "Cannot GET"
- Le site tourne sur Qlik Sense derrière reverse proxy
- Aucun endpoint JSON public accessible
- Headers Qlik (X-Qlik-Session) ne débloquent rien

### 2. data.gouv.fr FranceAgriMer — IMPASSE
- URLs redirigent vers VISIONet (ASP.NET dynamique)
- curl/wget → boucles de redirections 302 infinies
- Tabular API → 404, ressources non indexées

### 3. GitHub Actions workflow (data.gouv.fr → CSV) — OBSOLÈTE
- Repo loduval/boviq-app existe toujours sur GitHub
- Le workflow update-cotations.yml ne fonctionnait pas (source data.gouv bloquée)
- Remplacé par approche client-side SheetJS

---

## 🔗 Repo GitHub existant

- **Repo** : github.com/loduval/boviq-app (public)
- **GitHub Pages** : https://loduval.github.io/boviq-app/
- **État** : index.html V4 (ancienne version CSV-based, OBSOLÈTE)
- **Usage futur possible** : héberger boviq-cours-marche.html ou BOVIQ V6 complet

---

## Prochaines étapes
1. ☐ Copier boviq-cours-marche.html sur le Mac (~/Desktop/01-Projects/BOVIQ/)
2. ☐ Intégrer le module cours dans BOVIQ V6 (onglet dédié ou widget dashboard)
3. ☐ Optionnel : pousser la version finale sur loduval/boviq-app GitHub Pages
4. ☐ Ajouter alertes prix (seuils configurables par l'éleveur)

---
*Notes BOVIQ COURS — MAJ 28/02/2026*
