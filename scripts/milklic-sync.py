#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOVIQ — Mil'Klic Sync
=====================
Télécharge automatiquement les CSV depuis Mil'Klic (Seenovia / EARL La Rousselière).

CE QU'IL RÉCUPÈRE :
  - Uniquement des fichiers CSV exportés par Mil'Klic (bouton "Exporter la grille en CSV")
  - Chaque CSV = contenu exact de la grille/tableau visible sur la page
  - Encodage Windows-1252, séparateur point-virgule
  - Fichiers renommés avec préfixe date : YYYYMMDD_XX-NomPage_NomOriginal.csv

FLUX D'AUTHENTIFICATION :
  1. POST /site_admin/  →  cookies WP session
  2. POST /wp-admin/admin-ajax.php  action=module_auth&externalId=53059073  →  token auth
  3. POST sk-milklic.seenergi.fr/Routage.aspx  →  cookies Mil'Klic session
  4. GET chaque page Mil'Klic + clic bouton Export

USAGE :
  python milklic-sync.py              # téléchargement normal
  python milklic-sync.py --visible    # afficher le navigateur (debug)

CONFIG :
  scripts/.env  →  SEENOVIA_LOGIN + SEENOVIA_PASS

SORTIE :
  _backups-ami/milklic-YYYYMMDD/*.csv

Compatible : macOS et Windows
"""

import os, sys, time, argparse
from pathlib import Path
from datetime import datetime

# ── Auto-install dépendances ─────────────────────────────────────────────────
def _pip(pkg):
    os.system(f'"{sys.executable}" -m pip install {pkg} --break-system-packages -q')

try:
    from dotenv import load_dotenv
except ImportError:
    _pip("python-dotenv"); from dotenv import load_dotenv

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    _pip("playwright")
    os.system(f'"{sys.executable}" -m playwright install chromium')
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# ── Config ────────────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).resolve().parent
BASE_DIR    = SCRIPTS_DIR.parent
load_dotenv(SCRIPTS_DIR / ".env")

LOGIN      = os.getenv("SEENOVIA_LOGIN", "").strip()
PASS       = os.getenv("SEENOVIA_PASS",  "").strip()
EXTERNAL_ID = "53059073"   # fixe = numéro UAT EARL La Rousselière

if not LOGIN or not PASS or "METTRE_LE" in PASS:
    print("❌  Renseignez SEENOVIA_LOGIN et SEENOVIA_PASS dans scripts/.env")
    sys.exit(1)

DATE_TAG = datetime.now().strftime("%Y%m%d")
DL_DIR   = BASE_DIR / "_backups-ami" / f"milklic-{DATE_TAG}"
DL_DIR.mkdir(parents=True, exist_ok=True)

BASE_MK   = "https://sk-milklic.seenergi.fr"
LOGIN_URL = "https://www.seenovia.fr/se-connecter/"
AJAX_URL  = "https://www.seenovia.fr/wp-admin/admin-ajax.php"
ROUTAGE   = "https://sk-milklic.seenergi.fr/Routage.aspx"

# Pages à exporter : (chemin_aspx, label_fichier)
PAGES = [
    ("/Controle/ResultatsBrutsControle.aspx",   "01-ResultatsBruts"),
    ("/Controle/ValoriseIndividuel.aspx",        "02-ValoriseIndividuel"),
    ("/Controle/HistoriqueLait.aspx",            "03-HistoLait"),
    ("/Controle/HistoriqueTB.aspx",              "04-HistoTB"),
    ("/Controle/HistoriqueTP.aspx",              "05-HistoTP"),
    ("/Sante/HistoriqueCellules.aspx",           "06-HistoCellules"),
    ("/Elevage/Inventaire.aspx",                 "07-Inventaire"),
    ("/Controle/ResultatControle.aspx",          "08-ResultatControle"),
    ("/Reproduction/IndicateurGestation.aspx",   "09-Gestation"),
    ("/Sante/Neosporose.aspx",                   "10-Neosporose"),
    ("/Sante/Paratub.aspx",                      "11-Paratuberculose"),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def log(msg, end="\n"):
    print(msg, end=end, flush=True)

def dismiss_cookies(page):
    """Ferme le bandeau Tarteaucitron si présent."""
    for sel in ["#tarteaucitronAllDenied2", "#tarteaucitronPersonalize2",
                "button:has-text('Tout refuser')", "button:has-text('Tout accepter')"]:
        try:
            b = page.locator(sel).first
            if b.is_visible(timeout=1500):
                b.click()
                time.sleep(0.4)
                return
        except Exception:
            pass

def click_export(page, timeout_s=15):
    """Attend que #Export soit actif (classe sans 'Disabled'), clique. Retourne True/False."""
    try:
        btn = page.locator("#Export")
        btn.wait_for(state="attached", timeout=6000)
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            cls = btn.get_attribute("class") or ""
            if "Disabled" not in cls and "disabled" not in cls:
                btn.click()
                return True
            time.sleep(0.4)
    except Exception:
        pass
    return False

def export_page(mk_page, path, label):
    """
    Navigue sur une page Mil'Klic, attend le chargement des grilles DevExpress,
    clique Export CSV, sauvegarde le fichier téléchargé.
    Retourne le Path du fichier ou None si échec.
    """
    url = BASE_MK + path
    log(f"  {label}", end=" … ")
    try:
        with mk_page.expect_download(timeout=30_000) as dl_ctx:
            mk_page.goto(url, wait_until="networkidle", timeout=35_000)
            time.sleep(2.5)   # laisser les grilles DevExpress se charger

            # Page Résultat contrôle : 2 boutons à cliquer avant Export
            if "ResultatControle.aspx" in path:
                for sel in [
                    "#MainContent_ASPxCallbackPanelResultats_ASPxButtonResultats_I",
                    "#MainContent_ASPxButtonLstVL_I",
                ]:
                    try:
                        mk_page.locator(sel).click(timeout=4000)
                        time.sleep(2.5)
                    except Exception:
                        pass

            if not click_export(mk_page):
                log("⚠️  Export non disponible (données vides ou page non prise en charge)")
                return None

        dl   = dl_ctx.value
        name = f"{DATE_TAG}_{label}_{dl.suggested_filename}"
        dest = DL_DIR / name
        dl.save_as(dest)
        kb   = dest.stat().st_size // 1024
        log(f"✅  {dl.suggested_filename}  ({kb} Ko)")
        return dest

    except PWTimeout:
        log("⏱️  Timeout — page trop longue à charger")
        return None
    except Exception as exc:
        log(f"❌  {exc}")
        return None

# ── Main ──────────────────────────────────────────────────────────────────────
def main(headless=True):
    log(f"\n🐄  BOVIQ — Mil'Klic Sync — {DATE_TAG}")
    log(f"    Compte  : {LOGIN}")
    log(f"    Sortie  : {DL_DIR}")
    log(f"    Mode    : {'silencieux' if headless else 'navigateur visible'}\n")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=headless,
            downloads_path=str(DL_DIR),
        )
        ctx = browser.new_context(
            accept_downloads=True,
            viewport={"width": 1280, "height": 900},
            locale="fr-FR",
        )
        page = ctx.new_page()

        # ── ÉTAPE 1 : Login Seenovia ──────────────────────────────────────────
        log("🔑  Connexion Seenovia …")
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30_000)
        time.sleep(1.5)
        dismiss_cookies(page)
        time.sleep(0.5)

        try:
            # Formulaire WP custom : name="log" / name="pwd" / id="wp-submit"
            page.locator("input#user_login, input[name='log']").fill(LOGIN, timeout=8000)
            page.locator("input#user_pass, input[name='pwd']").fill(PASS)
            # Forcer la visibilité du bouton (parfois masqué par le CSS)
            page.evaluate("var b=document.getElementById('wp-submit'); if(b) b.style.display='block';")
            page.locator("input#wp-submit").click(timeout=8000)
            page.wait_for_load_state("networkidle", timeout=20_000)
        except Exception as e:
            log(f"❌  Formulaire login : {e}")
            browser.close(); sys.exit(1)

        if "logged-in" not in (page.locator("body").get_attribute("class") or ""):
            log("❌  Échec authentification — vérifiez scripts/.env")
            browser.close(); sys.exit(1)
        log("    ✅  Connecté\n")

        # ── ÉTAPE 2 : Obtenir le token Mil'Klic (module_auth) ─────────────────
        log("🔗  Obtention token Mil'Klic …")
        auth_result = page.evaluate(f"""
            async () => {{
                const resp = await fetch('{AJAX_URL}', {{
                    method: 'POST',
                    credentials: 'include',
                    headers: {{'Content-Type': 'application/x-www-form-urlencoded'}},
                    body: 'action=module_auth&externalId={EXTERNAL_ID}'
                }});
                return await resp.json();
            }}
        """)
        auth_token = auth_result.get("auth") if auth_result else None
        if not auth_token:
            log(f"❌  Token Mil'Klic non obtenu : {auth_result}")
            browser.close(); sys.exit(1)
        log(f"    ✅  Token obtenu ({auth_token[:16]}…)\n")

        # ── ÉTAPE 3 : Ouvrir la session Mil'Klic via Routage.aspx ────────────
        log("🚪  Ouverture session Mil'Klic …")
        mk_page = ctx.new_page()
        # POST vers Routage avec le token
        mk_page.goto("about:blank")
        mk_page.evaluate(f"""
            () => {{
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '{ROUTAGE}';
                form.target = '_self';
                const inp = document.createElement('input');
                inp.type = 'hidden'; inp.name = 'auth'; inp.value = '{auth_token}';
                form.appendChild(inp);
                document.body.appendChild(form);
                form.submit();
            }}
        """)
        mk_page.wait_for_load_state("networkidle", timeout=20_000)
        time.sleep(1.5)
        log(f"    ✅  {mk_page.url}\n")

        # ── ÉTAPE 4 : Télécharger chaque page ────────────────────────────────
        log("📥  Téléchargements CSV :")
        results = {}
        for path, label in PAGES:
            results[label] = export_page(mk_page, path, label)

        browser.close()

    # ── Bilan ─────────────────────────────────────────────────────────────────
    ok     = [p for p in results.values() if p]
    failed = [k for k, p in results.items() if not p]
    total  = sum(f.stat().st_size for f in ok)

    log(f"\n{'='*55}")
    log(f"✅  {len(ok)}/{len(PAGES)} fichiers  —  {total // 1024} Ko total")
    for f in sorted(ok):
        log(f"    {f.name}  ({f.stat().st_size // 1024} Ko)")
    if failed:
        log(f"\n⚠️  Sans export ({len(failed)}) : {', '.join(failed)}")
    log(f"{'='*55}\n")
    log(f"📁  Dossier : {DL_DIR}")

    return len(ok)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BOVIQ — Mil'Klic Sync")
    parser.add_argument("--visible", action="store_true",
                        help="Afficher le navigateur (mode debug)")
    args = parser.parse_args()
    main(headless=not args.visible)
