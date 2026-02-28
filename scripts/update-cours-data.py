#!/usr/bin/env python3
"""
BOVIQ — Télécharge les Excel DG AGRI et génère cours-data.json
Utilisé par GitHub Actions (chaque lundi) ou en local.
"""

import json, os, sys, urllib.request, tempfile, datetime, re

try:
    import openpyxl
except ImportError:
    os.system(f"{sys.executable} -m pip install openpyxl -q")
    import openpyxl

# --- CONFIG ---
MILK_URL = "https://agriculture.ec.europa.eu/document/download/62d01488-33a0-4601-a841-ca48fa11d999_en"
BEEF_URL = "https://agriculture.ec.europa.eu/document/download/db5b282e-a2b4-4d18-91bd-bd4854dc2030_en"
OUTPUT = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "data", "market", "cours-data.json")


def download(url, name):
    print(f"  ⬇ {name}...")
    tmp = os.path.join(tempfile.gettempdir(), name)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 BOVIQ'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(tmp, 'wb') as f:
            f.write(resp.read())
    print(f"    OK ({os.path.getsize(tmp)//1024} KB)")
    return tmp


def sfloat(v):
    try:
        return round(float(v), 2) if v else None
    except (ValueError, TypeError):
        return None


def parse_milk(path):
    """Prix lait France — historique mensuel."""
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb['Raw Milk Prices']
    france_col = 11  # Col K
    data = []

    for r in range(8, ws.max_row + 1):
        period = ws.cell(r, 1).value
        price = sfloat(ws.cell(r, france_col).value)
        if not period or price is None:
            continue
        p = str(period).strip()
        if 'm' in p:
            parts = p.split('m')
            date_str = f"{parts[0]}-{parts[1].zfill(2)}"
        else:
            date_str = p
        data.append({"date": date_str, "price": price})

    wb.close()
    cutoff = datetime.datetime.now().year - 5
    data = [d for d in data if int(d["date"][:4]) >= cutoff]
    print(f"    Lait: {len(data)} mois, dernier={data[-1]['date']} → {data[-1]['price']}€")
    return data


def parse_beef(path):
    """Prix viande bovine France — 'Weekly All Carcase Prices', col FR=11."""
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb['Weekly All Carcase Prices']
    fr_col = 11

    # Map Excel labels → JSON keys attendues par l'app
    label_map = {
        'Young Bulls 12>24m A-U2': 'jb_u2',
        'Young Bulls 12>24m A-U3': 'jb_u3',
        'Young Bulls 12>24m A-R2': 'jb_r2',
        'Young Bulls 12>24m A-R3': 'jb_r3',
        'Young Bulls 12>24m A-O2': 'jb_o2',
        'Young Bulls 12>24m A-O3': 'jb_o3',
        'Cows D-R3': 'vache_r3',
        'Cows D-R4': 'vache_r4',
        'Cows D-O2': 'vache_o2',
        'Cows D-O3': 'vache_o3',
        'Cows D-O4': 'vache_o4',
        'Cows D-P2': 'vache_p2',
        'Cows D-P3': 'vache_p3',
        'Heifers  E-U3': 'genisse_u3',
        'Heifers  E-R2': 'genisse_r2',
        'Heifers  E-R3': 'genisse_r3',
        'Heifers  E-R4': 'genisse_r4',
        'Heifers  E-O3': 'genisse_o3',
        'Bullocks  C-R3': 'boeuf_r3',
        'Bullocks  C-O3': 'boeuf_o3',
    }

    prices = {}
    for r in range(1, ws.max_row + 1):
        label = ws.cell(r, 1).value
        if not label:
            continue
        label = str(label).strip()
        if label in label_map:
            p = sfloat(ws.cell(r, fr_col).value)
            if p:
                prices[label_map[label]] = p

    # Récupérer la date de semaine depuis l'onglet ACZ
    ws2 = wb['Weekly ACZ Carcase Prices']
    week_date = ''
    for r in range(1, 5):
        v = ws2.cell(r, 31).value  # Col AE souvent "Last update"
        if v and 'update' in str(v).lower():
            # Extract date from "Last update:25.02.2026"
            m = re.search(r'(\d{2}\.\d{2}\.\d{4})', str(v))
            if m:
                week_date = m.group(1)
                break
    # Fallback: check row 2
    if not week_date:
        for c in range(25, 36):
            v = ws2.cell(2, c).value
            if v and re.search(r'\d{2}\.\d{2}\.\d{4}', str(v)):
                week_date = re.search(r'(\d{2}\.\d{2}\.\d{4})', str(v)).group(1)
                break

    wb.close()
    print(f"    Viande: {len(prices)} catégories, semaine={week_date}")
    for k, v in list(prices.items())[:5]:
        print(f"      {k}: {v}€/100kg")
    return prices, week_date


def main():
    print("🐄 BOVIQ — Mise à jour des cours du marché")
    print(f"   {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    milk_path = download(MILK_URL, "milk-prices.xlsx")
    beef_path = download(BEEF_URL, "beef-carcass-latest.xlsx")

    print("\n📊 Extraction...")
    milk_history = parse_milk(milk_path)
    beef_prices, week_date = parse_beef(beef_path)

    # Format attendu par boviq-cours-marche.html → jsonToMarketData()
    output = {
        "meta": {
            "generated": datetime.datetime.now().isoformat(),
            "source": "DG AGRI / Commission Européenne"
        },
        "milk": {
            "latest": {
                "date": milk_history[-1]["date"],
                "price": milk_history[-1]["price"]
            },
            "prices": milk_history
        },
        "beef": {
            "week_date": week_date,
            "prices": beef_prices
        }
    }

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    sz = os.path.getsize(OUTPUT) // 1024
    print(f"\n✅ {OUTPUT}")
    print(f"   {sz} KB — {len(milk_history)} mois lait + {len(beef_prices)} prix viande")


if __name__ == "__main__":
    main()
