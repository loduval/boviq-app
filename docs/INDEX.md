# BOVIQ — INDEX FONCTIONS

Mis à jour : 19/03/2026 — boviq-v6-latest.html (4773 lignes)

## Infrastructure
| Ligne | Fonction | Rôle |
|---|---|---|
| 1145 | `debounce(fn,ms)` | Anti-rebond recherche |
| 1155 | `load()` | localStorage + fallback INIT_DATA + migration |
| 1176 | `save()` | Persistance + catch plein |
| 1177 | `esc(s)` | Sanitisation XSS |

## Import/Export
| 1182 | `exportJSON()` | Export backup JSON |
| 1192 | `validateImportData(data)` | Validation schéma import |
| 1267 | `importJSON(input)` | Import replace/merge |
| 2714 | `exportReproCSV()` | Export repro CSV |
| 3368 | `exportSantePdf()` async | Export carnet sanitaire PDF |
| 3465 | `exportBilanPdf()` async | Export bilan PDF |
| 3739 | `loadPdfJs()` | CDN pdf.js lazy |
| 3751 | `parseBilanPdf(input)` async | Import PDF bilan |
| 3789 | `parseGecagriText(text)` | Parser texte Gecagri |

## Navigation
| 1331 | `goTo(p)` | Navigation entre pages |
| 1338 | `toggleSidebar()` | Mobile sidebar |
| 1352 | `openM(id)` / `closeM(id)` | Modals |
| 2429 | `goToFiltered(f)` | KPI → animaux filtrés |

## Animaux
| 1359 | `popSelects()` | Alimente tous les selects |
| 1403 | `openAnimalModal(id)` | Modal animal |
| 1434 | `saveAnimal()` | CRUD animal |
| 1460 | `delAnimal(id)` | Suppression animal |
| 1462 | `getAnimalStatut(a)` | Calcul statut dynamique |
| 1598 | `populateFilters()` | Filtres race/statut/âge |
| 1623 | `renderAnimaux()` | Tableau animaux + badge score |
| 2053 | `openSortieModal(id)` | Modal sortie |
| 2060 | `confirmerSortie()` | Marquer sorti |
| 2071 | `annulerSortie(id)` | Annuler sortie |

## Reproduction
| 1388 | `recalcRepro()` | Auto-calc gestation/vêlage |
| 1703 | `openReproModal(id)` | Modal saillie |
| 1727 | `saveRepro()` | CRUD repro |
| 1745 | `delRepro(id)` | Suppression repro |
| 1750 | `openVelageModal()` | Modal vêlage rapide |
| 1758 | `saveVelage()` | Déclarer vêlage + créer veau |
| 1813 | `toggleReproView(mode)` | Basculer tableau/gantt |
| 1823 | `renderReproGantt()` | Gantt gestations |
| 1937 | `reproStatut(r)` | Statut saillie |
| 1951 | `renderRepro()` | Tableau repro + refresh gantt |
| 4052 | `calcIVV(animalId)` | IVV individuel |
| 4064 | `calcIVVTroupeau()` | IVV moyen troupeau |

## Sanitaire
| 1984 | `filterAnimalSelect()` | Filtre select animaux |
| 1994 | `getLignesSante(s)` | Lignes traitements (rétrocompat) |
| 1999 | `getSanteMaxDelais(s)` | Délais max via lignes[] |
| 2005 | `ligneHTML(idx,l)` | HTML ligne ordonnance |
| 2028 | `addLigneSante(l)` | Ajouter produit |
| 2035 | `removeLigneSante(idx)` | Retirer produit |
| 2039 | `getLignesFromModal()` | Lire lignes depuis modal |
| 2077 | `openSanteModal(id)` | Modal ordonnance |
| 2099 | `saveSante()` | CRUD traitement |
| 2116 | `delSante(id)` | Suppression traitement |
| 2122 | `renderSante()` | Tableau sanitaire (esc() OK) |

## Vaccination
| 2208 | `toggleVaccinConfig()` | Toggle config vaccin |
| 2212 | `toggleProtocole(pid)` | Activer/désactiver protocole |
| 2217 | `getVaccinHistory(animalId,proto)` | Historique vaccinations |
| 2232 | `getVaccinStatus(animal,proto)` | Statut rappel vaccin |
| 2257 | `quickVaccin(animalId,pid)` | Vacciner 1 animal |
| 2269 | `batchVaccin(pid)` | Vacciner le troupeau |
| 2290 | `renderPlanVaccinal()` | Afficher plan vaccinal |

## Taureaux
| 2373 | `openTaureauModal(id)` | Modal taureau |
| 2388 | `saveTaureau()` | CRUD taureau |
| 2401 | `delTaureau(id)` | Suppression |
| 2403 | `renderTaureaux()` | Tableau taureaux |

## Dashboard
| 2438 | `renderDashboard()` | Dashboard complet |
| 2542 | `renderStats()` | Répartition troupeau |
| 2597 | `getAllEcheances()` | Échéances repro+délais |
| 2623 | `getAllEcheancesVaccin()` | Rappels vaccin 60j |
| 2644 | `renderCalendar()` | Calendrier + vaccins |
| 2692-2694 | `calPrev/Next/selectDay` | Navigation calendrier |
| 2699 | `updateCounts()` | Badges sidebar |
| 4029 | `countAlerts()` | Compteur alertes (getSanteMaxDelais+vaccin) |
| 4046 | `updateTitle()` | Badge titre onglet |

## Score santé
| 4072 | `calcSanteScore(animalId)` | Score A/B/C (4 critères, getSanteMaxDelais) |

## Fiche animal
| 4111 | `openFicheAnimal(id)` | Modal fiche détaillée |

## Bilan financier
| 2741 | `toggleAdvBilan(el)` | Section avancée |
| 2747 | `bilanAutoCalc()` | Auto-calc recettes/charges |
| 2761 | `openBilanModal(editId)` | Modal bilan |
| 2802 | `saveBilan()` | CRUD bilan |
| 2848 | `delBilan()` | Suppression bilan |
| 2855 | `duplicateBilan()` | Dupliquer N-1 |
| 2876 | `renderBilan()` | Vue bilan annuel |
| 3167 | `renderBilanMulti()` async | Vue multi-années |
| 3313 | `toggleBilanView(mode)` | Annuel/évolution |

## Aides éleveur
| 3889 | `renderAides()` | Page aides PAC |

## Journal / Viande / BDNI
| 4323 | `filterJournalSelect()` | Filtre select journal |
| 4328 | `openJournalModal(id)` | Modal journal |
| 4349 | `saveJournal()` | CRUD journal |
| 4365 | `renderJournal()` | Afficher journal |
| 4403 | `calcViandeTotal()` | Calcul total vente |
| 4409 | `openViandeModal(id)` | Modal vente viande |
| 4433 | `saveViande()` | CRUD vente |
| 4460 | `renderViande()` | Tableau ventes |
| 4486 | `getBDNIMouvements()` | Mouvements à déclarer |
| 4525 | `marquerDeclare(key)` | Marquer déclaré |
| 4529 | `annulerDeclare(key)` | Annuler déclaration |
| 4533 | `renderBDNI()` | Page BDNI |

## Popup alertes
| ~4640 | `buildPopupAlertes()` | Construire et afficher popup |
| ~4720 | `closePopupAlertes()` | Fermer + snooze |

## Global
| 4751 | `renderAll()` | Tout re-rendre |
| 4755 | init | `popSelects();renderAll();setTimeout(buildPopupAlertes,800)` |
| 4758 | sort | `th.addEventListener` → `sortTable` |
| 4762 | SW | `serviceWorker.register('./sw.js')` |
