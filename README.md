# 🐄 BOVIQ — Gestion de troupeau laitier

Outils de gestion pour éleveurs laitiers français. 100% local, zéro serveur, données privées.

## 🚀 Accès direct

**👉 [Ouvrir BOVIQ](https://loduval.github.io/boviq-app/)**

## Applications

| App | Description |
|-----|------------|
| [Gestion de troupeau](https://loduval.github.io/boviq-app/boviq-v6-latest.html) | Animaux, reproduction, sanitaire, vaccinations, bilan financier |
| [Cours du marché](https://loduval.github.io/boviq-app/boviq-cours-marche.html) | Prix lait, viande, céréales — données DG AGRI |

## Architecture

- **Single-file HTML** — chaque app est un fichier autonome
- **localStorage** — données stockées dans le navigateur, rien ne sort
- **Tabler CSS + Chart.js** — UI professionnelle, graphiques intégrés
- **Aucun serveur** — ouvrir le fichier HTML suffit

## Stack technique

- HTML/CSS/JS vanilla
- [Tabler](https://tabler.io/) (framework CSS)
- [Chart.js](https://www.chartjs.org/) (visualisations)
- [jsPDF](https://github.com/parallax/jsPDF) (export PDF)
- [SheetJS](https://sheetjs.com/) (lecture Excel DG AGRI)

## Licence

MIT
