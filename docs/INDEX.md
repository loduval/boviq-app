# BOVIQ — INDEX FONCTIONS

Mis à jour : 21/03/2026 — boviq-v6-latest.html (~5760 lignes), dark mode actif

---

## Infrastructure
| Ligne approx. | Fonction | Rôle |
|---|---|---|
| ~17 | `:root` CSS | Palette dark : `--bg:#0A1810`, `--brand:#4ED87A`, `--ink:#F2EDE4` |
| ~33 | `body::before` | Grain overlay fractalNoise |
| ~1145 | `debounce(fn,ms)` | Anti-rebond recherche — **doit être déclaré AVANT** `debouncedSearchAnimaux` |
| ~1360 | `load()` | localStorage + fallback INIT_DATA (`_dataVersion:20260321`) |
| ~1380 | `save()` | Persistance + catch plein |
| ~1381 | `esc(s)` | Sanitisation XSS |

## Import/Export
| ~1386 | `exportJSON()` | Export backup JSON |
| ~1396 | `validateImportData(data)` | Validation schéma import |
| ~1471 | `importJSON(input)` | Import replace/merge |
| ~2714 | `exportReproCSV()` | Export repro CSV |
| ~4154 | `exportSantePdf()` async | Export carnet sanitaire PDF (jsPDF lazy) |
| ~4251 | `exportBilanPdf()` async | Export bilan PDF |
| ~3739 | `loadPdfJs()` | CDN pdf.js lazy |
| ~3751 | `parseBilanPdf(input)` async | Import PDF bilan |
| ~3789 | `parseGecagriText(text)` | Parser texte Gecagri |

## Navigation
| ~1563 | `goTo(p)` | Navigation entre pages |
| | | Hooks : `p==='dashboard'→initMeteo`, `p==='milklic'→renderMilklic`, `p==='planning'→renderPlanning` |
| ~1570 | `toggleSidebar()` | Mobile sidebar |
| ~1584 | `openM(id)` / `closeM(id)` | Modals |
| ~2429 | `goToFiltered(f)` | KPI → animaux filtrés |

## Météo
| ~2773 | `METEO_CFG` | `{lat:47.95, lng:-0.65, lieu:'La Rousselière'}` |
| ~2805 | `initMeteo()` async | Fetch open-meteo + cache 30min + `setTimeout(initMeteo,100)` dans renderDashboard |
| ~2823 | `renderMeteoWidget(data)` | Rendu widget météo — **bulletproof** : try/catch + accès sécurisé (hWcode[j]||0, idx≥0) |

## Animaux
| ~1590 | `popSelects()` | Alimente tous les selects |
| ~1630 | `openAnimalModal(id)` | Modal animal |
| ~1660 | `saveAnimal()` | CRUD animal |
| ~1686 | `delAnimal(id)` | Suppression animal |
| ~1688 | `getAnimalStatut(a)` | Calcul statut dynamique |
| ~1824 | `populateFilters()` | Filtres race/statut/âge |
| ~1849 | `renderAnimaux()` | Tableau animaux + badge score |
| ~2053 | `openSortieModal(id)` | Modal sortie |
| ~2060 | `confirmerSortie()` | Marquer sorti |

## Reproduction
| ~1614 | `recalcRepro()` | Auto-calc gestation/vêlage |
| ~1929 | `openReproModal(id)` | Modal saillie |
| ~1953 | `saveRepro()` | CRUD repro |
| ~1976 | `openVelageModal()` | Modal vêlage rapide |
| ~1984 | `saveVelage()` | Déclarer vêlage + créer veau |
| ~2039 | `toggleReproView(mode)` | Basculer tableau/gantt |
| ~2049 | `renderReproGantt()` | Gantt gestations — cible `#repro-gantt-content` |
| ~2177 | `renderRepro()` | Tableau repro |

## Sanitaire
| ~2225 | `getSanteMaxDelais(s)` | Délais max via lignes[] |
| ~2254 | `addLigneSante(l)` | Ajouter produit ordonnance |
| ~2303 | `openSanteModal(id)` | Modal ordonnance |
| ~2325 | `saveSante()` | CRUD traitement |
| ~2348 | `renderSante()` | Tableau sanitaire |

## Vaccination
| ~2458 | `getVaccinStatus(animal,proto)` | Statut rappel vaccin |
| ~2483 | `quickVaccin(animalId,pid)` | Vacciner 1 animal |
| ~2495 | `batchVaccin(pid)` | Vacciner le troupeau |
| ~2516 | `renderPlanVaccinal()` | Afficher plan vaccinal |

## Dashboard
| ~2996 | `renderDashboard()` | Dashboard complet |
| ~3093 | | → `renderCalendar(); renderStats(); setTimeout(initMeteo,100)` |
| ~3101 | `renderStats()` | Répartition troupeau (4 cartes répartition) |
| ~3204 | `renderCalendar()` | Calendrier + dots événements |
| ~2917 | `updateCounts()` | Badges sidebar + `updateMilklicCount()` |
| ~5622 | `document.addEventListener('visibilitychange')` | Refresh météo si >30min |

## Bilan financier
| ~2980 | `openBilanModal(editId)` | Modal bilan |
| ~3021 | `saveBilan()` | CRUD bilan |
| ~3075 | `duplicateBilan()` | Dupliquer N-1 |
| ~3095 | `renderBilan()` | Vue bilan annuel |
| ~3386 | `renderBilanMulti()` async | Vue multi-années Chart.js |

## Contrôle Laitier MilKlic
| ~5657 | `renderMilklic()` | Page contrôle laitier — filtre all/alert/conseil/tar/vide |
| ~5739 | `updateMilklicCount()` | Badge rouge cnt-milklic (VL >400k leucos) |

## Popup alertes
| ~4860 | `buildPopupAlertes()` | Construire et afficher popup au démarrage |
| ~4940 | `closePopupAlertes()` | Fermer + snooze |

## Global
| ~5312 | `renderAll()` | Tout re-rendre (appelle tous les render*) |
| ~5412 | init | `popSelects();renderAll();setTimeout(buildPopupAlertes,800)` |
| SW | | `sw.js` cache `boviq-v20260321` — invalide à chaque bump |

---

## Module boviq-milklic.html (541 lignes, 140KB)

### INIT_ML_DATA
Objet JS inline `{importDate, controleDate, animaux:{trav:{...}}}` — 160 animaux :
- **VL:93** (vaches laitières) — données contrôle + historiques 12 dates
- **GL:50** (génisses laitières)
- **MA:13** (mâles/taureaux)
- **GV:4** (génisses viande)

Champs par animal :
`trav, nom, numNat, categ, sexe, race, naissance, statut, lait24, tb, tp, leucos, uree, numLact, leucoPrev, conseilIA, taureau, dateIA, joursIA, rangIA, tarPrev, sdir, histoLait{}, histoTB{}, histoTP{}, histoCell{}`

Historiques = **objets** `{"2024-04-22": 13.1}` (pas des arrays).

### loadML()
Auto-charge INIT_ML_DATA si localStorage vide → effet wahoo à la 1ère ouverture.

### Fonctions parse (import CSV manuel)
| Fonction | CSV source | Rôle |
|---|---|---|
| `processBruts(rows)` | 01 | lait24, tb, tp, leucos, urée, statuts |
| `processValorise(rows)` | 02 | repro, conseilIA, taureau, dateIA, joursIA, rangIA, tarPrev, leucoPrev |
| `processHisto(rows,field)` | 03/04/05 | histoLait, histoTB, histoTP |
| `processHistoCell(rows)` | 06 | histoCell + sdir |
| `processInventaire(rows)` | 07 | categ VL/GL/GV/MA, naissance, numNat |

### Fonctions render
| Fonction | Rôle |
|---|---|
| `renderDashboard()` | KPIs + alertes leucos + conseils IA + signaux faibles |
| `renderCellules()` | Tableau leucos classé + seuil filtrable |
| `renderRepro()` | IA déconseillée / à inséminér / tarissements / vaches vides |
| `renderCourbesInit()` | Select animaux groupé par catégorie (VL/GL/MA) |
| `renderCourbes()` | Charts lait/TB+TP/cellules pour 1 animal (Chart.js) |
| `renderBridge()` | Statut localStorage BOVIQ V6 + correspondances Trav↔boucle |
| `updateSidebar()` | `160 animaux · 93 VL · 82 contrôlées` |

---

## Script Python — mise à jour INIT_ML_DATA

**Fichier** : `/tmp/gen_milklic_final.py`  
**Source** : `~/Desktop/01-Projects/BOVIQ/DERNIERE-VERSION/*.csv`  
**Résultat** : `/tmp/milklic-final.json`  
**Injection** : remplacer `const INIT_ML_DATA=...;` dans boviq-milklic.html  
**Commande** : `python3 /tmp/gen_milklic_final.py`

---

## GitHub Actions — cours du marché

**Workflow** : `.github/workflows/update-market-data.yml`  
**Script** : `scripts/update-cours-data.py`  
**Source** : EC DG AGRI Excel (agriculture.ec.europa.eu)  
**Output** : `data/market/cours-data.json`  
**Schedule** : lundi 8h UTC — ou déclencher manuellement depuis GitHub Actions

---

## CDN dépendances

| Lib | Version | URL |
|-----|---------|-----|
| Chart.js | 4.4.1 | cdnjs.cloudflare.com |
| jsPDF | 2.5.1 | cdnjs.cloudflare.com |
| jsPDF AutoTable | 3.8.2 | cdnjs.cloudflare.com |
| pdf.js | 3.11.174 | cdnjs.cloudflare.com |
| Chart.js (MilKlic) | 4.4.2 | cdn.jsdelivr.net |
| Chart.js (Cours) | 4.4.0 | cdn.jsdelivr.net |
