#!/usr/bin/env python3
"""
BOVIQ — Mise à jour automatique des données de marché
Télécharge les Excel DG AGRI (Commission Européenne) et génère cours-data.json
Utilisé par GitHub Actions (hebdomadaire) ou manuellement.
"""

import json, os, sys, time, urllib.request, urllib.error, tempfile
from datetime import datetime, timezone

try:
    import openpyxl
except ImportError:
    print("Installing openpyxl...")
    os.system(f"{sys.executable} -m pip install openpyxl -q")
    import openpyxl

# === CONFIG ===
MILK_URL = "https://agriculture.ec.europa.eu/document/download/62d01488-33a0-4601-a841-ca48fa11d999_en?filename=eu-milk-historical-price-series_en.xlsx"
BEEF_URL = "https://agriculture.ec.europa.eu/document/download/db5b282e-a2b4-4d18-91bd-bd4854dc2030_en?filename=bovine-carcase-prices-latest_en.xlsx"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_PATH = os.path.join(PROJECT_DIR, "data", "market", "cours-data.json")

# Local fallbacks (if download fails)
LOCAL_MILK = os.path.join(PROJECT_DIR, "data", "market", "milk-prices.xlsx")
LOCAL_BEEF = os.path.join(PROJECT_DIR, "data", "market", "beef-prices.xlsx")


# DG AGRI limite le debit par moments : un 429 ne veut pas dire que le
# fichier est indisponible, seulement qu'il faut attendre un peu.
TENTATIVES = 4
ATTENTE_BASE = 20       # secondes, doublees a chaque echec
ATTENTE_MAX = 180


def download(url, label):
    """Telecharge vers un fichier temporaire. Renvoie son chemin, ou None."""
    print(f"  📥 Downloading {label}...")
    attente = ATTENTE_BASE
    for essai in range(1, TENTATIVES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BOVIQ-MarketData/1.0"})
            tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
            with urllib.request.urlopen(req, timeout=60) as resp:
                tmp.write(resp.read())
            tmp.close()
            size_kb = os.path.getsize(tmp.name) // 1024
            suffixe = "" if essai == 1 else f" (essai {essai})"
            print(f"  ✅ {label}: {size_kb} KB{suffixe}")
            return tmp.name
        except Exception as e:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass
            # Le serveur dit parfois lui-meme combien de temps attendre.
            pause = attente
            if isinstance(e, urllib.error.HTTPError):
                entete = e.headers.get("Retry-After") if e.headers else None
                if entete and str(entete).strip().isdigit():
                    pause = min(int(str(entete).strip()), ATTENTE_MAX)
                reessayable = e.code == 429 or 500 <= e.code < 600
            else:
                reessayable = True      # reseau, delai depasse
            if essai == TENTATIVES or not reessayable:
                print(f"  ⚠️  Download failed ({label}): {e}")
                return None
            print(f"  ⏳ {label}: {e} — nouvel essai dans {pause} s "
                  f"({essai}/{TENTATIVES - 1})")
            time.sleep(pause)
            attente = min(attente * 2, ATTENTE_MAX)
    return None


def section_vide(cle, valeur):
    """Une section sans aucune cotation exploitable."""
    if not valeur:
        return True
    if cle == "beef":
        return not (valeur.get("prices") or {})
    return not (valeur.get("prices") or [])


def section_precedente(cle):
    """Reprend une section du cours-data.json deja publie.

    C'est la vraie sauvegarde : elle est versionnee dans le depot, au
    contraire des .xlsx de repli qui n'y ont jamais ete.
    """
    try:
        with open(OUTPUT_PATH, encoding="utf-8") as f:
            ancien = json.load(f)
        valeur = ancien.get(cle)
        if valeur:
            meta = ancien.get("meta") or {}
            # La fraicheur propre au flux, et non la date de generation du
            # fichier : sinon une section reprise telle quelle se retrouverait
            # datee du jour, ce qui est precisement le mensonge a eviter.
            quand = meta.get(f"{cle}_updated") or meta.get("generated")
            return valeur, quand
    except Exception:
        pass
    return None, None


def extract_milk(path):
    """Extract France milk prices from DG AGRI Excel."""
    print("  🥛 Extracting milk prices...")
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Raw Milk Prices"]
    
    # France = col 11, periods in col 1, data from row 8
    # Find France column dynamically
    fr_col = None
    for c in range(1, ws.max_column + 1):
        v = ws.cell(7, c).value
        if v and "france" in str(v).lower():
            fr_col = c
            break
    if not fr_col:
        print("  ⚠️  France column not found in milk sheet")
        wb.close()
        return {"latest": None, "prices": []}
    
    prices = []
    for r in range(8, ws.max_row + 1):
        period = ws.cell(r, 1).value
        price = ws.cell(r, fr_col).value
        if period and price and isinstance(price, (int, float)):
            prices.append({"period": str(period), "price": round(float(price), 2)})
    
    wb.close()
    
    # Keep last 36 months for the app
    prices = prices[-36:] if len(prices) > 36 else prices
    latest = prices[-1] if prices else None
    
    print(f"  ✅ Milk: {len(prices)} months, latest = {latest}")
    return {"latest": latest, "prices": prices}


def extract_beef(path):
    """Extract France beef carcass prices from DG AGRI Excel."""
    print("  🥩 Extracting beef prices...")
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Weekly All Carcase Prices"]
    
    # Find France column (row 9 has country codes)
    fr_col = None
    for c in range(1, ws.max_column + 1):
        v = ws.cell(9, c).value
        if v and str(v).strip().upper() == "FR":
            fr_col = c
            break
    if not fr_col:
        print("  ⚠️  France column not found in beef sheet")
        wb.close()
        return {"week_date": "", "prices": {}}
    
    # Extract all categories for France
    category_map = {
        "Young Bulls 12>24m A-U2": "jb_u2",
        "Young Bulls 12>24m A-U3": "jb_u3",
        "Young Bulls 12>24m A-R2": "jb_r2",
        "Young Bulls 12>24m A-R3": "jb_r3",
        "Young Bulls 12>24m A-O2": "jb_o2",
        "Young Bulls 12>24m A-O3": "jb_o3",
        "Bullocks  C-R3": "boeuf_r3",
        "Bullocks  C-O3": "boeuf_o3",
        "Cows D-R3": "vache_r3",
        "Cows D-R4": "vache_r4",
        "Cows D-O2": "vache_o2",
        "Cows D-O3": "vache_o3",
        "Cows D-O4": "vache_o4",
        "Cows D-P2": "vache_p2",
        "Cows D-P3": "vache_p3",
        "Heifers  E-U3": "genisse_u3",
        "Heifers  E-R2": "genisse_r2",
        "Heifers  E-R3": "genisse_r3",
        "Heifers  E-R4": "genisse_r4",
        "Heifers  E-O3": "genisse_o3",
    }
    
    prices = {}
    for r in range(10, ws.max_row + 1):
        cat = ws.cell(r, 1).value
        price = ws.cell(r, fr_col).value
        if cat and price and isinstance(price, (int, float)):
            cat_str = str(cat).strip()
            key = category_map.get(cat_str)
            if key:
                prices[key] = round(float(price), 2)
    
    # Get week date from sheet 1 (scans first rows for dd.mm.yyyy pattern)
    import re
    ws1 = wb["Weekly ACZ Carcase Prices"]
    week_date = ""
    for r in range(1, 7):
        for c in range(1, 40):
            v = ws1.cell(r, c).value
            if v:
                m = re.search(r"(\d{2}\.\d{2}\.\d{4})", str(v))
                if m:
                    week_date = m.group(1)
                    break
        if week_date:
            break
    
    wb.close()
    print(f"  ✅ Beef: {len(prices)} categories, week = {week_date}")
    return {"week_date": week_date, "prices": prices}


def main():
    print("🐄 BOVIQ — Mise à jour des cours du marché")
    print(f"   {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print()
    
    maintenant = datetime.now(timezone.utc).isoformat()
    milk_path = download(MILK_URL, "Lait")
    # Une pause entre les deux : enchaines sans repit, le second
    # telechargement se faisait refuser par la limitation de debit.
    if milk_path:
        time.sleep(5)
    beef_path = download(BEEF_URL, "Viande")

    # Les .xlsx de repli ne sont pas dans le depot, mais on les lit s'ils
    # existent (execution a la main, a cote d'un telechargement manuel).
    if not milk_path and os.path.exists(LOCAL_MILK):
        print("  📄 Lait : fichier local")
        milk_path = LOCAL_MILK
    if not beef_path and os.path.exists(LOCAL_BEEF):
        print("  📄 Viande : fichier local")
        beef_path = LOCAL_BEEF

    repris = []

    if milk_path:
        milk = extract_milk(milk_path)
        milk_maj = maintenant
        # Une extraction qui ne rend rien ne doit pas effacer ce qui est
        # publie : la source est parfois incomplete au moment du passage.
        if section_vide("milk", milk):
            ancien, ancien_maj = section_precedente("milk")
            if not section_vide("milk", ancien):
                print("  ♻️  Lait : aucune cotation dans le fichier du jour, "
                      "cotations précédentes conservées")
                milk, milk_maj = ancien, ancien_maj
                repris.append(f"lait (source vide, inchangé depuis "
                              f"{(ancien_maj or '?')[:10]})")
    else:
        # Un flux indisponible ne doit pas emporter l'autre : on garde les
        # cotations deja publiees et on dit qu'elles n'ont pas bouge.
        milk, milk_maj = section_precedente("milk")
        if milk:
            repris.append(f"lait (inchangé depuis {(milk_maj or '?')[:10]})")
            print("  ♻️  Lait : cotations précédentes conservées")

    if beef_path:
        beef = extract_beef(beef_path)
        beef_maj = maintenant
        if section_vide("beef", beef):
            ancien, ancien_maj = section_precedente("beef")
            if not section_vide("beef", ancien):
                print("  ♻️  Viande : aucune cotation par classe dans le "
                      "fichier du jour, cotations précédentes conservées")
                beef, beef_maj = ancien, ancien_maj
                repris.append(f"viande (source vide, inchangée depuis "
                              f"{(ancien_maj or '?')[:10]})")
    else:
        beef, beef_maj = section_precedente("beef")
        if beef:
            repris.append(f"viande (inchangée depuis {(beef_maj or '?')[:10]})")
            print("  ♻️  Viande : cotations précédentes conservées")

    # On n'echoue que s'il ne reste vraiment rien a publier.
    if not milk and not beef:
        print("❌ Aucune donnée disponible : ni téléchargement, ni historique.")
        sys.exit(1)

    # Build output JSON
    result = {
        "meta": {
            "generated": maintenant,
            "source": "DG AGRI — Commission Européenne",
            "country": "France",
            "milk_unit": "EUR/100kg",
            "beef_unit": "EUR/100kg carcasse",
            # Fraicheur par flux : sans cela, « generated » laissait croire
            # que tout datait du jour meme.
            "milk_updated": milk_maj,
            "beef_updated": beef_maj
        },
        "milk": milk,
        "beef": beef
    }
    
    # Write JSON
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"\n✅ cours-data.json généré ({size_kb:.1f} KB)")
    print(f"   → {OUTPUT_PATH}")
    
    if repris:
        print("\n⚠️  Téléchargement partiel — repris de la version publiée : "
              + ", ".join(repris))

    # Cleanup temp files
    for p in [milk_path, beef_path]:
        if p and p.startswith(tempfile.gettempdir()):
            os.unlink(p)


if __name__ == "__main__":
    main()
