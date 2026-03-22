# BOVIQ — INDEX DES FONCTIONS

Mis à jour : **22/03/2026 soir** · boviq-v6-latest.html 6321L · boviq-milklic.html 658L

---

## boviq-v6-latest.html

### Navigation & Lifecycle
| Fonction | Rôle |
|----------|------|
| `goTo(page)` | Naviguer vers une page |
| `renderAll()` | Re-render toutes les vues |
| `save()` | Sauvegarder D dans localStorage `boviq` |
| `load()` | Charger depuis localStorage ou INIT_DATA |
| `updateCounts()` | Mettre à jour les badges nav |
| `updateTitle()` | Titre onglet avec badge alertes |
| `toggleSidebar()` | Mobile : ouvrir/fermer sidebar |

### Render pages
| Fonction | Page |
|----------|------|
| `renderDashboard()` | Tableau de bord + KPIs |
| `renderAnimaux()` | Inventaire animaux + badges cellules |
| `renderRepro()` / `renderReproGantt()` | Suivi reproduction |
| `renderSante()` | Carnet sanitaire |
| `renderPlanVaccinal()` | Plan vaccinal |
| `renderTaureaux()` | Registre taureaux |
| `renderBilan()` | Analyse financière |
| `renderJournal()` | Journal d'élevage |
| `renderBDNI()` | Alertes BDNI |
| `renderRaces()` | Référentiel races |
| `renderAides()` | Aides éleveur |
| `renderMilklic()` | Dashboard MilKlic inline V6 |
| `renderPlanning()` | Planning semaines |
| `renderTankRisk()` | Carte "Impact sur la qualité du tank" |
| `renderUGBPrev()` | Prévision UGB par trimestre |

### Fiche animal
| Fonction | Rôle |
|----------|------|
| `openFicheAnimal(id)` | Ouvre la fiche modale |
| `renderFicheCharts(trav)` | Courbes MilKlic dans fiche (async, setTimeout 50ms après openM) |
| `exportFicheImage(id)` | **Export PNG canvas HTML5** — fiche complète avec courbes, emojis, accents |

### Historique leucos (NOUVEAU)
| Fonction | Rôle |
|----------|------|
| `getLeucosHisto(trav)` | Lit `D.mlControles[]` → `[{date, lc, l, tb, tp}]` triés |
| `getLeucosRecurrenceColor(trav)` | Couleur récurrence 12 mois : rouge≥3, amber=2, vert=1 |

### Modals
| Fonction | Modal |
|----------|-------|
| `openAnimalModal(id?)` | Créer/modifier animal |
| `openReproModal(id?)` | Créer/modifier saillie |
| `openVelageModal()` | Déclarer vêlage |
| `openSanteModal(id?)` | Enregistrer traitement |
| `openTaureauModal(id?)` | Créer/modifier taureau |
| `openSortieModal(id)` | Sortie d'animal |
| `openBilanModal(id?)` | Saisir exercice comptable |
| `openJournalModal(id?)` | Événement journal |
| `openFicheAnimal(id)` | Fiche détaillée animal |
| `closeM(name)` | Fermer modal |
| `openM(name)` | Ouvrir modal |

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
| `delAnimal(id)` | Supprimer animal |
| `delRepro(id)` | Supprimer saillie |
| `delSante(id)` | Supprimer traitement |
| `delTaureau(id)` | Supprimer taureau |
| `dupBilan(year)` | Dupliquer bilan N-1 |

### Exports
| Fonction | Format | Contenu |
|----------|--------|---------|
| `exportJSON()` | JSON | Toutes données BOVIQ |
| `importJSON()` | JSON | Import + validation |
| `exportReproCSV()` | CSV | Suivi reproductions |
| `exportSantePdf()` | PDF | Carnet sanitaire (jsPDF) |
| `exportBilanPdf()` | PDF | Bilan financier (jsPDF) |
| `exportFicheImage(id)` | **PNG** | **Fiche animal canvas HTML5** |

### Calculs
| Fonction | Calcul |
|----------|--------|
| `calcIVV(id)` | IVV moyen animal |
| `calcSanteScore(id)` | Score santé /100 |
| `calcBilanScore(b)` | Score IDELE /100 (benchmarks IDELE/INOSYS 2023) |
| `getAnimalStatut(a)` | Statut animal (libellé + couleur) |
| `reproStatut(r)` | Statut repro (libellé + couleur) |
| `gestFor(race)` | Durée gestation par race |
| `getLignesSante(s)` | Lignes d'un acte sanitaire |
| `esc(s)` | XSS — escape HTML |
| `pf(s)` | Parse float (virgule→point) |
| `fmt(d)` | ISO → DD/MM/YYYY |
| `addD(d, n)` | Ajouter n jours à date ISO |
| `normBoucle(s)` | Normaliser N° boucle |

### Chargement librairies (lazy)
| Fonction | Lib |
|----------|-----|
| `loadChartJs()` | Chart.js 4.4.1 (CDN) |
| `loadJsPdf()` | jsPDF 2.5.1 (CDN) |
| `loadAutoTable()` | jsPDF-autoTable (CDN) |

---

## boviq-milklic.html

### Navigation
| Fonction | Rôle |
|----------|------|
| `showPage(page)` | Afficher page ('import','dashboard','cellules','repro','courbes','bridge') |
| `updateSidebar()` | Compteurs sidebar + badge alertes |

### Import CSV
| Fonction | Rôle |
|----------|------|
| `handleFiles(files)` | Traiter fichiers droppés/sélectionnés |
| `detectType(filename)` | Type CSV depuis nom fichier |
| `parseCSV(txt)` | Parser CSV latin-1 → tableau 2D |
| `pf(s)` | Parse float + gère `\u00a0` (espace insécable "1 465") |
| `processBruts(rows)` | `01-ResultatsBruts` |
| `processValorise(rows)` | `02-ValoriseIndividuel` |
| `processHisto(rows, field)` | `03-HistoLait`, `04-HistoTB`, `05-HistoTP` |
| `processHistoCell(rows)` | `06-HistoCellules` |
| `processInventaire(rows)` | `07-Inventaire` |

### Render
| Fonction | Page |
|----------|------|
| `renderDashboard()` | KPIs + alertes cellulaires + repro |
| `renderCellules()` | Tableau leucocytes seuil filtrable |
| `renderRepro()` | IA déconseillée / à inséminér / tarissements |
| `renderCourbes()` / `renderCourbesInit()` | Chart.js lait/TB/TP/cellules par animal |
| `renderBridge()` | Infos intégration V6 |
| `renderTankRisk()` | Impact sur qualité du tank |

### Persistance
| Fonction | Rôle |
|----------|------|
| `saveML()` | Sauvegarde `BOVIQ_MILKLIC` + **archive dans `D.mlControles[]`** (boviq localStorage) |
| `loadML()` | Charge depuis localStorage ou INIT_ML_DATA |
| `clearData()` | Effacer localStorage + recharger |
| `exportMLCSV()` | Export CSV UTF-8 BOM (18 colonnes) |

### ⚠️ Unités leucocytes
Leucocytes **en milliers** (k cell/mL). Seuils : `>400` élevé, `>800` critique, `>200` surveillance.

---

## index.html (Hub)

| Fonction | Rôle |
|----------|------|
| `initMeteo()` | Appel Open-Meteo API, render météo |
| `renderM(data)` | HTML bandeau météo |
| `wi(code)` | Emoji météo WMO |
| `wd(code)` | Description texte WMO |
| `verdict(c, hs)` | Calcul "Sortie au pré" (ok/warn/bad) |

KPIs hub : lecture directe `localStorage boviq` + `BOVIQ_MILKLIC` + `cours-data.json`

---

## scripts/audit-boviq.py — 26 vérifications

| # | Vérification |
|---|---|
| 1 | Fichiers requis présents et taille |
| 2 | Règle absolue index.html ≠ boviq-v6 |
| 3 | Syntaxe JS (`node --check`) |
| 4 | Balance backticks / accolades / parenthèses |
| 5 | IDs HTML dupliqués |
| 6 | Fonctions `onclick` vs définitions JS |
| 7 | Encodage PDF — chars non-Latin1 dans `doc.text()` |
| 8 | Corps de fonction orphelins |
| 9 | Variables CSS `--xxx` définies vs utilisées |
| 10 | Clés localStorage cohérentes |
| 11 | CDN versions + HTTP vs HTTPS |
| 12 | INIT_DATA JSON valide, IDs uniques, refs mère |
| 13 | Seuils leucos en milliers (pas unités brutes) |
| 14 | Service Worker — 4 assets couverts |
| 15 | manifest.json start_url = `./index.html` |
| 16 | 25 fonctions BOVIQ requises présentes |
| 17 | Fonctions définies en double |
| 18 | Balance `<div>` HTML |
| 19 | `_dataVersion` cohérent |
| 20 | Git — fichiers non commités |
| 21 | Taille fichiers (< seuils) |
| 22 | Motifs dangereux (cp V6→index, eval, clear) |
| 23 | Bridge mlControles boviq-milklic → boviq-v6 |
| 24 | `renderFicheCharts` avec setTimeout |
| 25 | Courbes PDF — `addImage` présent |
| 26 | CSS scroll — height:100dvh / overflow:hidden |

---

## Structure données D (localStorage `boviq`)

```javascript
D = {
  _dataVersion: 20260321,
  animaux: [{
    id, nom, type, race, boucle, naissance, sexe, mere, pere, notes,
    _trav,            // N° travail (4 derniers chiffres boucle)
    _categ_ml,        // VL / GL / GV / MA
    _ml_statut,       // T / TT / TFV / FV / NC / null
    _ml_lait24,       // L/j
    _ml_tb, _ml_tp,   // g/kg
    _ml_leucos,       // k cell/mL ← EN MILLIERS
    _ml_leuco_prev,   // k cell/mL ← EN MILLIERS
    _ml_uree,         // mg/L
    _ml_lact,         // numéro lactation
    _ml_var_lait,     // variation % vs N-1
    _ml_sdir,         // S/D/I/R
    _ml_date_ia, _ml_jours_ia, _ml_rang_ia,
    _ml_tar_prev,     // ISO date
    _ml_conseil_ia, _ml_taureau_ia
  }],
  repros: [{id, vache, taureau, dateSaillie, primo, velageReel, sexeVeau, poids, facilite, notes}],
  sante: [{id, date, animaux[], type, produit, posologie, intervenant,
           delaiLait, delaiViande, ordonnance, notes, lignes:[...]}],
  taureaux: [{id, nom, race, boucle, naissance, poids, notes}],
  bilans: [{id, annee, sau, vaches, ugb, ...}],
  planVaccinal: [{id, actif}],
  journal: [{id, date, type, animal, notes}],
  mlControles: [{         // ← NOUVEAU 22/03/2026
    date: "YYYY-MM-DD",
    vaches: [{t, lc, l, tb, tp}]  // lc en k cell/mL
  }],
  _mlControleDate: "04/03/26"
}
```

## Structure données ML (localStorage `BOVIQ_MILKLIC`)

```javascript
ML = {
  importDate: "2026-03-22",
  controleDate: "04/03/26",
  animaux: {
    "8668": {
      trav, nom, numNat, categ, sexe, race, naissance, statut,
      lait24, tb, tp,
      leucos: 1465,      // k cell/mL ← EN MILLIERS
      leucoPrev: 562,    // k cell/mL ← EN MILLIERS
      sdir, sdirN1, varLait, evolLeucoTxt, numLact,
      dateIA, joursIA, rangIA, taureau, tarPrev, conseilIA,
      histoLait: {"2024-04-22": 13.1, ...},   // L/j
      histoTB: {"2024-04-22": 35.0, ...},     // g/kg
      histoTP: {"2024-04-22": 29.8, ...},     // g/kg
      histoCell: {"2024-04-22": 562, ...},    // k cell/mL
    }
  }
}
```
