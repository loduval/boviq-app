# BOVIQ — INDEX DES FONCTIONS

Mis à jour : 22/03/2026 · boviq-v6-latest.html 5827L · boviq-milklic.html 621L

---

## boviq-v6-latest.html

### Navigation & Lifecycle
| Fonction | Rôle |
|----------|------|
| `goTo(page)` | Naviguer vers une page (active la page, désactive les autres) |
| `renderAll()` | Re-render toutes les vues |
| `save()` | Sauvegarder D dans localStorage |
| `loadData()` | Charger depuis localStorage ou INIT_DATA |
| `updateCounts()` | Mettre à jour les badges nav |
| `updateTitle()` | Mettre à jour le titre de l'onglet (badge alertes) |
| `toggleSidebar()` | Mobile : ouvrir/fermer la sidebar |

### Render pages
| Fonction | Page | Dépendances |
|----------|------|-------------|
| `renderDashboard()` | Tableau de bord | Chart.js, D.animaux, D.repros, D.sante |
| `renderAnimaux()` | Inventaire animaux | D.animaux, filtres, tri |
| `renderRepro()` / `renderReproGantt()` | Suivi reproduction | D.repros, D.taureaux |
| `renderSante()` | Carnet sanitaire | D.sante, filtres SF |
| `renderPlanVaccinal()` | Plan vaccinal | D.animaux, D.planVaccinal, D.sante |
| `renderTaureaux()` | Registre taureaux | D.taureaux, D.repros |
| `renderBilan()` | Analyse financière | D.bilans, Chart.js |
| `renderJournal()` | Journal d'élevage | D.journal |
| `renderViande()` | Ventes viande | D.viande (si présent) |
| `renderBDNI()` | Alertes BDNI | D.animaux, D.repros |
| `renderRaces()` | Référentiel races | RACES const |
| `renderAides()` | Aides éleveur | D.bilans (lb.annee\|\|lb.year) |
| `renderMilklic()` | Dashboard MilKlic inline | localStorage BOVIQ_MILKLIC |
| `renderPlanning()` | Planning semaines | D.animaux, D.repros, D.sante |

### Modals — Ouvrir/Fermer
| Fonction | Modal |
|----------|-------|
| `openAnimalModal(id?)` | Créer/modifier animal |
| `openReproModal(id?)` | Créer/modifier saillie |
| `openVelageModal()` | Déclarer un vêlage |
| `openSanteModal(id?)` | Enregistrer traitement |
| `openTaureauModal(id?)` | Créer/modifier taureau |
| `openSortieModal(id)` | Sortie d'animal |
| `openBilanModal(id?)` | Saisir exercice comptable |
| `openJournalModal(id?)` | Événement journal |
| `openViandeModal()` | Enregistrer vente viande |
| `openFicheAnimal(id)` | Fiche détaillée animal (modal) |
| `closeM(name)` | Fermer une modal |

### Save / Delete
| Fonction | Action |
|----------|--------|
| `saveAnimal()` | Sauvegarder animal |
| `saveRepro()` | Sauvegarder saillie |
| `saveVelage()` | Déclarer vêlage |
| `saveSante()` | Enregistrer traitement |
| `saveTaureau()` | Sauvegarder taureau |
| `saveSortie()` | Sortir animal |
| `saveBilan()` | Enregistrer bilan |
| `saveJournal()` | Sauvegarder événement |
| `saveViande()` | Enregistrer vente |
| `delAnimal(id)` | Supprimer animal |
| `delRepro(id)` | Supprimer saillie |
| `delSante(id)` | Supprimer traitement |
| `delTaureau(id)` | Supprimer taureau |
| `dupBilan(year)` | Dupliquer bilan N-1 |

### Exports
| Fonction | Format | Contenu |
|----------|--------|---------|
| `exportJSON()` | JSON | Toutes les données BOVIQ |
| `importJSON()` | JSON | Import + validation stricte |
| `exportReproCSV()` | CSV | Tableau suivi reproductions |
| `exportSantePdf()` | PDF | Carnet sanitaire (jsPDF) |
| `exportBilanPdf()` | PDF | Bilan financier complet |

### Calculs
| Fonction | Calcul |
|----------|--------|
| `calcIVV(a)` | IVV moyen d'un animal |
| `calcSanteScore(a)` | Score santé /100 |
| `calcBilanScore(b)` | Score IDELE /100 (benchmarks IDELE/INOSYS 2023) |
| `getLignesSante(s)` | Lignes d'un acte sanitaire |
| `getVaccStatut(a, proto)` | Statut vaccinal animal/protocole |
| `esc(s)` | XSS protection (escape HTML) |
| `pf(s)` | Parse float (virgule → point) |
| `fmtD(s)` / `fmt(d)` | Format dates DD/MM/YYYY ↔ ISO |
| `diffD(d)` | Différence en jours vs aujourd'hui |
| `addD(d, n)` | Ajouter n jours à une date ISO |

### Utilitaires UI
| Fonction | Action |
|----------|--------|
| `goToFiltered(filter)` | Aller aux animaux avec filtre pré-appliqué |
| `resetSanteFiltres()` | Effacer filtres sanitaire |
| `toggleVaccinConfig()` | Afficher/masquer config vaccinal |
| `sortTable(table, col)` | Tri colonne tableau |
| `debounce(fn, delay)` | Debounce (300ms sur recherche) |
| `scanBoucle(targetId)` | Scanner boucle (caméra Android) |
| `toggleVaccinProtocole(id)` | Activer/désactiver protocole |

### Météo (dashboard inline V6)
Pas de `renderMeteo` dans V6 — météo gérée dans `index.html` uniquement.

---

## boviq-milklic.html

### Navigation
| Fonction | Rôle |
|----------|------|
| `showPage(page)` | Afficher une page ('import','dashboard','cellules','repro','courbes','bridge') |
| `updateSidebar()` | Mettre à jour compteurs sidebar + badge alertes |

### Import CSV
| Fonction | Rôle |
|----------|------|
| `handleFiles(files)` | Traiter les fichiers droppés/sélectionnés |
| `detectType(filename)` | Détecter type CSV depuis le nom du fichier |
| `parseCSV(txt)` | Parser CSV latin-1 → tableau 2D |
| `pf(s)` | Parse float + **gère `\u00a0`** (espace insécable dans "1 465") |
| `fmtD(s)` | DD/MM/YY ou DD/MM/YYYY → ISO |
| `normN(s)` | Normaliser numéro national (supprimer espaces) |

### Processeurs CSV
| Fonction | Fichier source |
|----------|---------------|
| `processBruts(rows)` | `01-ResultatsBruts` |
| `processValorise(rows)` | `02-ValoriseIndividuel` |
| `processHisto(rows, field)` | `03-HistoLait`, `04-HistoTB`, `05-HistoTP` |
| `processHistoCell(rows)` | `06-HistoCellules` |
| `processInventaire(rows)` | `07-Inventaire` |

### Render
| Fonction | Page |
|----------|------|
| `renderDashboard()` | KPIs + alertes cellulaires + statuts + repro + signaux production |
| `renderCellules()` | Tableau leucocytes avec seuil filtrable |
| `renderRepro()` | IA déconseillée / à inséminér / tarissements / vides |
| `renderCourbes()` / `renderCourbesInit()` | Chart.js lait/TB/TP/cellules par animal |
| `renderBridge()` | Instructions intégration BOVIQ V6 |

### Persistance
| Fonction | Rôle |
|----------|------|
| `saveML()` | Sauvegarder ML dans localStorage `BOVIQ_MILKLIC` |
| `loadML()` | Charger depuis localStorage ou `INIT_ML_DATA` (si vide) |
| `clearData()` | Effacer localStorage + recharger |

### Export
| Fonction | Format | Contenu |
|----------|--------|---------|
| `exportMLCSV()` | CSV UTF-8 BOM | Tous animaux consolidés (18 colonnes) |

### ⚠️ Unités leucocytes
**Leucocytes stockés en milliers** (comme les CSV Seenergi).
- Seuils : `>400` (élevé), `>800` (critique), `>200` (surveillance)
- Affichage : `a.leucos.toFixed(0)+'k'` (pas de `/1000`)
- HistoCell CSV : valeurs déjà en milliers/mL

---

## index.html (Hub)

### Fonctions météo
| Fonction | Rôle |
|----------|------|
| `initMeteo()` | Appel Open-Meteo API, render météo |
| `renderM(data)` | Construire HTML du bandeau météo |
| `wi(code)` | Emoji météo depuis WMO code |
| `wd(code)` | Description texte WMO code |
| `verdict(c, hs)` | Calcul "Sortie au pré" (ok/warn/bad) |

### Render hub
Pas de fonctions nommées — rendu direct depuis `localStorage BOVIQ` + `BOVIQ_MILKLIC` + `cours-data.json`.

---

## Structure données D (localStorage BOVIQ)

```javascript
D = {
  _dataVersion: 20260321,
  animaux: [{id, nom, type, race, boucle, naissance, sexe, mere, pere, notes,
              _trav, _categ_ml, _ml_statut, _ml_lait24, _ml_tb, _ml_tp,
              _ml_leucos, _ml_uree, _ml_lact, _ml_var_lait, _ml_leuco_prev,
              _ml_sdir, _ml_date_ia, _ml_jours_ia, _ml_rang_ia,
              _ml_tar_prev, _ml_conseil_ia, _ml_taureau_ia}],
  repros: [{id, vache, taureau, dateSaillie, primo, velageReel, sexeVeau, poids, facilite, notes}],
  sante: [{id, date, animaux[], type, produit, posologie, intervenant,
           delaiLait, delaiViande, ordonnance, notes, lignes:[{type,produit,...}]}],
  taureaux: [{id, nom, race, boucle, naissance, poids, notes}],
  bilans: [{id, annee, sau, vaches, ugb, ...}],
  planVaccinal: [{id, actif}],
  journal: [{id, date, type, animal, notes}],
}
```

## Structure données ML (localStorage BOVIQ_MILKLIC)

```javascript
ML = {
  importDate: "2026-03-22",
  controleDate: "04/03/26",
  animaux: {
    "8668": {
      trav: "8668", nom: "FELLAH", numNat: "FR5381248668",
      lait24: 5.7, tb: 38.0, tp: 33.9,
      leucos: 1465,        // ← EN MILLIERS
      leucoPrev: 562,      // ← EN MILLIERS
      sdir: "R", sdirN1: "R",
      varLait: -16, evolLeucoTxt: "R",
      numLact: 13, dateIA: "2025-12-30",
      conseilIA: null, taureau: "U40",
      tarPrev: "2026-08-14",
      histoLait: {"2024-04-22": 13.1, ...},
      histoCell: {"2024-04-22": 562, ...}, // ← EN MILLIERS
      statut: null, categ: "VL", race: "39"
    },
    ...
  }
}
```
