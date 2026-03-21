# Rapport d'investigation — EC Agridata API & Sources de données agricoles
## BOVIQ — Cours du marché (Lait + Viande bovine)
**Date :** 28 février 2026
**Statut :** Investigation terminée — Sources alternatives identifiées ✅

---

## 1. Verdict sur l'API REST Agridata

### Résultat du smoke test (prod + acceptance)

| Base URL | Endpoint | Status | Qlik Cookie | Verdict |
|----------|----------|--------|-------------|---------|
| agridata.ec.europa.eu | /api/ | 404 | Oui | Qlik |
| agridata.ec.europa.eu | /api/rawMilk/prices?FR | 404 | Oui | Qlik |
| agridata.ec.europa.eu | /api/beef/prices?FR | 404 | Oui | Qlik |
| acceptance.agridata.ec.europa.eu | /api/ | 404 | Oui | Qlik |
| acceptance.agridata.ec.europa.eu | /api/rawMilk/prices?FR | 404 | Oui | Qlik |
| acceptance.agridata.ec.europa.eu | /api/beef/prices?FR | 404 | Oui | Qlik |

**Conclusion : API REST documentée NON déployée en production.**

## 2. Sources de données FONCTIONNELLES

### 2.1 LAIT CRU — Série historique complète (Excel)
URL: https://agriculture.ec.europa.eu/document/download/62d01488-33a0-4601-a841-ca48fa11d999_en?filename=eu-milk-historical-price-series_en.xlsx
- Taille: ~994 Ko | Onglets: Raw Milk Prices, Organic milk prices, Dairy Products Prices
- France = colonne index 10 (code fr) | Couverture: 1977 à aujourd'hui
- Dernière donnée FR: 2026m02 = 47.35 EUR/100kg

### 2.2 VIANDE BOVINE — Prix carcasses hebdomadaires (Excel)
URL: https://agriculture.ec.europa.eu/document/download/db5b282e-a2b4-4d18-91bd-bd4854dc2030_en?filename=bovine-carcase-prices-latest_en.xlsx
- Onglets: Weekly ACZ Carcase Prices, Weekly All Carcase Prices
- Catégories FR: Jeunes bovins, Bœufs, Vaches, Génisses (toutes conformations)
- Prix moyen FR toutes catégories: 517.35 EUR/100kg carcasse

### 2.3 VIANDE BOVINE — Prix animaux vivants (Excel)
URL: https://agriculture.ec.europa.eu/document/download/286a0ec3-3b08-4e08-a9f5-98f988f0b19b_en?filename=bovine-live-prices-latest_en.xlsx

### 2.4 PDFs complémentaires
- Dashboard Dairy: .../c9474932-d061-4169-80f1-38951aa8615e_en?filename=dashboard-dairy_en.pdf
- Beef Weekly: .../25d11726-93c5-4184-85c9-ab7e73b82975_en?filename=beef-weekly-prices_en.pdf

## 3. Architecture recommandée pour BOVIQ
1. GitHub Action hebdo: télécharge les 3 Excel
2. Script Python: extrait FR, normalise en JSON
3. Commit auto: data/market-prices.json
4. BOVIQ: fetch JSON statique depuis GitHub Pages

Alternative: bouton "MAJ cours" côté client avec SheetJS (xlsx.js) + localStorage

## 4. Résumé
- API REST /api/*: NON déployée (404+Qlik sur prod ET acceptance)
- Données Qlik: WebSocket propriétaire, pas HTTP
- Excel DG AGRI (lait + beef): FONCTIONNELS et à jour
- Eurostat API: dataset non disponible
