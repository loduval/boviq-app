#!/usr/bin/env python3
"""
BOVIQ - Mise à jour automatique des cours du marché
Télécharge les Excel DG AGRI, extrait les prix France, génère boviq-cours-data.js

Usage:
  python3 boviq-update-cours.py

Peut être ajouté en crontab pour mise à jour automatique:
  crontab -e
  0 8 * * 1 cd ~/Desktop/01-Projects/BOVIQ && python3 boviq-update-cours.py
  (= chaque lundi à 8h)
"""

import urllib.request
import json
import os
import sys
from datetime import datetime

# Essayer openpyxl, sinon utiliser le module csv comme fallback
try:
    import openpyxl
except ImportError:
    print("⚠️  openpyxl non installé. Installation...")
    os.system(f"{sys.executable} -m pip install openpyxl --quiet")
    import openpyxl

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# === CONFIGURATION ===
SOURCES = {
    'milk': {
        'url': 'https://agriculture.ec.europa.eu/document/download/62d01488-33a0-4601-a841-ca48fa11d999_en?filename=eu-milk-historical-price-series_en.xlsx',
        'filename': 'milk-prices.xlsx',
        'sheet': 'Raw Milk Prices',
        'fr_col': 11,   # col K (1-indexed)
        'eu_col': 31,   # col AE
        'date_col': 1,  # col A
    },
    'beef': {
        'url': 'https://agriculture.ec.europa.eu/document/download/db5b282e-a2b4-4d18-91bd-bd4854dc2030_en?filename=bovine-carcase-prices-latest_en.xlsx',
        'filename': 'beef-prices.xlsx',
        'sheet': 'Weekly All Carcase Prices',
        'fr_col': 11,   # col K (1-indexed)
    },
}

BEEF_CATEGORIES = {
    'jb_r3':      {'label': 'Young Bulls 12>24m A-R3', 'fr': 'Jeune Bovin R3'},
    'vache_o3':   {'label': 'Cows D-O3',               'fr': 'Vache O3'},
    'vache_r3':   {'label': 'Cows D-R3',               'fr': 'Vache R3'},
    'genisse_r3': {'label': 'Heifers  E-R3',           'fr': 'Génisse R3'},
    'boeuf_r3':   {'label': 'Bullocks  C-R3',          'fr': 'Bœuf R3'},
    'vache_o2':   {'label': 'Cows D-O2',               'fr': 'Vache O2'},
    'vache_p2':   {'label': 'Cows D-P2',               'fr': 'Vache P2'},
    'moyenne':    {'label': 'All CAT Avg Price',        'fr': 'Moyenne toutes catég.'},
}
