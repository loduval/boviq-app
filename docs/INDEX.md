# BOVIQ — INDEX FONCTIONS

Mis à jour : 21/03/2026 — boviq-v6-latest.html (5749 lignes)

## Infrastructure
| Ligne | Fonction | Rôle |
|---|---|---|
| ~1145 | `debounce(fn,ms)` | Anti-rebond recherche |
| ~1360 | `load()` | localStorage + fallback INIT_DATA (_dataVersion 20260321) |
| ~1380 | `save()` | Persistance + catch plein |
| ~1381 | `esc(s)` | Sanitisation XSS |

## Import/Export
| ~1386 | `exportJSON()` | Export backup JSON |
| ~1396 | `validateImportData(data)` | Validation schéma import |
| ~1471 | `importJSON(input)` | Import replace/merge |
| ~2714 | `exportReproCSV()` | Export repro CSV |
| ~3368 | `exportSantePdf()` async | Export carnet sanitaire PDF |
| ~3465 | `exportBilanPdf()` async | Export bilan PDF |
| ~3739 | `loadPdfJs()` | CDN pdf.js lazy |
| ~3751 | `parseBilanPdf(input)` async | Import PDF bilan |
| ~3789 | `parseGecagriText(text)` | Parser texte Gecagri |

## Navigation
| ~1563 | `goTo(p)` | Navigation entre pages (pages = querySelectorAll('.page')) |
| ~1570 | `toggleSidebar()` | Mobile sidebar |
| ~1584 | `openM(id)` / `closeM(id)` | Modals |
| ~2429 | `goToFiltered(f)` | KPI → animaux filtrés |

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
| ~2071 | `annulerSortie(id)` | Annuler sortie |

## Reproduction
| ~1614 | `recalcRepro()` | Auto-calc gestation/vêlage |
| ~1929 | `openReproModal(id)` | Modal saillie |
| ~1953 | `saveRepro()` | CRUD repro |
| ~1971 | `delRepro(id)` | Suppression repro |
| ~1976 | `openVelageModal()` | Modal vêlage rapide |
| ~1984 | `saveVelage()` | Déclarer vêlage + créer veau |
| ~2039 | `toggleReproView(mode)` | Basculer tableau/gantt |
| ~2049 | `renderReproGantt()` | Gantt gestations |
| ~2163 | `reproStatut(r)` | Statut saillie |
| ~2177 | `renderRepro()` | Tableau repro + refresh gantt |

## Sanitaire
| ~2210 | `filterAnimalSelect()` | Filtre select animaux |
| ~2220 | `getLignesSante(s)` | Lignes traitements (rétrocompat) |
| ~2225 | `getSanteMaxDelais(s)` | Délais max via lignes[] |
| ~2231 | `ligneHTML(idx,l)` | HTML ligne ordonnance |
| ~2254 | `addLigneSante(l)` | Ajouter produit |
| ~2261 | `removeLigneSante(idx)` | Retirer produit |
| ~2265 | `getLignesFromModal()` | Lire lignes depuis modal |
| ~2303 | `openSanteModal(id)` | Modal ordonnance |
| ~2325 | `saveSante()` | CRUD traitement |
| ~2342 | `delSante(id)` | Suppression traitement |
| ~2348 | `renderSante()` | Tableau sanitaire |

## Vaccination
| ~2434 | `toggleVaccinConfig()` | Toggle config vaccin |
| ~2438 | `toggleProtocole(pid)` | Activer/désactiver protocole |
| ~2443 | `getVaccinHistory(animalId,proto)` | Historique vaccinations |
| ~2458 | `getVaccinStatus(animal,proto)` | Statut rappel vaccin |
| ~2483 | `quickVaccin(animalId,pid)` | Vacciner 1 animal |
| ~2495 | `batchVaccin(pid)` | Vacciner le troupeau |
| ~2516 | `renderPlanVaccinal()` | Afficher plan vaccinal |

## Taureaux
| ~2598 | `openTaureauModal(id)` | Modal taureau |
| ~2613 | `saveTaureau()` | CRUD taureau |
| ~2626 | `delTaureau(id)` | Suppression |
| ~2628 | `renderTaureaux()` | Tableau taureaux |

## Dashboard
| ~2663 | `renderDashboard()` | Dashboard complet + météo |
| ~2767 | `renderStats()` | Répartition troupeau |
| ~2822 | `getAllEcheances()` | Échéances repro+délais |
| ~2848 | `getAllEcheancesVaccin()` | Rappels vaccin 60j |
| ~2869 | `renderCalendar()` | Calendrier + vaccins |
| ~2917 | `updateCounts()` | Badges sidebar + updateMilklicCount() |
| ~4250 | `countAlerts()` | Compteur alertes |
| ~4266 | `updateTitle()` | Badge titre onglet |

## Score santé
| ~4290 | `calcSanteScore(animalId)` | Score A/B/C |

## Fiche animal
| ~4330 | `openFicheAnimal(id)` | Modal fiche détaillée |

## Bilan financier
| ~2960 | `toggleAdvBilan(el)` | Section avancée |
| ~2966 | `bilanAutoCalc()` | Auto-calc recettes/charges |
| ~2980 | `openBilanModal(editId)` | Modal bilan |
| ~3021 | `saveBilan()` | CRUD bilan |
| ~3068 | `delBilan()` | Suppression bilan |
| ~3075 | `duplicateBilan()` | Dupliquer N-1 |
| ~3095 | `renderBilan()` | Vue bilan annuel |
| ~3386 | `renderBilanMulti()` async | Vue multi-années |
| ~3532 | `toggleBilanView(mode)` | Annuel/évolution |

## Aides éleveur
| ~4100 | `renderAides()` | Page aides PAC |

## Journal / Viande / BDNI
| ~4540 | `filterJournalSelect()` | Filtre select journal |
| ~4545 | `openJournalModal(id)` | Modal journal |
| ~4566 | `saveJournal()` | CRUD journal |
| ~4582 | `renderJournal()` | Afficher journal |
| ~4620 | `calcViandeTotal()` | Calcul total vente |
| ~4626 | `openViandeModal(id)` | Modal vente viande |
| ~4650 | `saveViande()` | CRUD vente |
| ~4677 | `renderViande()` | Tableau ventes |
| ~4703 | `getBDNIMouvements()` | Mouvements à déclarer |
| ~4742 | `marquerDeclare(key)` | Marquer déclaré |
| ~4746 | `annulerDeclare(key)` | Annuler déclaration |
| ~4750 | `renderBDNI()` | Page BDNI |

## Contrôle Laitier MilKlic (NOUVEAU 21/03/26)
| ~5657 | `renderMilklic()` | Page contrôle laitier — filtre all/alert/conseil/tar/vide |
| ~5739 | `updateMilklicCount()` | Badge rouge cnt-milklic (vaches >400k leucos) |

⚠️ BUG TDZ : variable locale `const pages` dans renderMilklic() entre en conflit  
avec `const pages=document.querySelectorAll('.page')` du scope global → renommer

## Popup alertes
| ~4860 | `buildPopupAlertes()` | Construire et afficher popup |
| ~4940 | `closePopupAlertes()` | Fermer + snooze |

## Global
| ~5283 | `renderAll()` | Tout re-rendre |
| ~5290 | init | `popSelects();renderAll();setTimeout(buildPopupAlertes,800)` |
| ~5295 | sort | `th.addEventListener` → `sortTable` |
| ~5310 | SW | `serviceWorker.register('./sw.js')` |

---

## Module boviq-milklic.html (511 lignes)

| Fonction | Rôle |
|---|---|
| `detectType(name)` | Identifie le CSV par nom (01→bruts, 02→valorise, etc.) |
| `processBruts(rows)` | Parse CSV 01 : lait24, tb, tp, leucos, urée, statuts |
| `processValorise(rows)` | Parse CSV 02 : repro, conseils IA, SDIR, tarissement |
| `processHisto(rows,field)` | Parse CSV 03/04/05 : historique par date |
| `processHistoCell(rows)` | Parse CSV 06 : cellules + SDIR |
| `processInventaire(rows)` | Parse CSV 07 : catég VL/GL/GV/MA, naissance |
| `handleFiles(files)` | Import multi-fichiers → fusion → localStorage BOVIQ_MILKLIC |
| `renderDashboard()` | KPIs + alertes + conseils + signaux faibles |
| `renderCellules()` | Tableau leucos classé + seuil filtrable |
| `renderRepro()` | IA déconseillée / à inséminér / tarissements / vaches vides |
| `renderCourbesInit()` | Peuple le select animal |
| `renderCourbes()` | Charts lait/TB+TP/cellules pour 1 animal |
| `renderBridge()` | Statut localStorage BOVIQ V6 + correspondances |
