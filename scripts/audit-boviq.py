# -*- coding: utf-8 -*-
"""
BOVIQ — Script d'audit complet
================================
Vérifie la syntaxe JS, la structure HTML, les IDs, les fonctions,
les encodages PDF, les règles projet et l'intégrité des données.

Usage : python3 scripts/audit-boviq.py
"""

import re, sys, os, subprocess, json
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
V6   = BASE / "boviq-v6-latest.html"
ML   = BASE / "boviq-milklic.html"
HUB  = BASE / "index.html"
SW   = BASE / "sw.js"

PASS = "\033[92m✅\033[0m"
FAIL = "\033[91m❌\033[0m"
WARN = "\033[93m⚠️ \033[0m"
INFO = "\033[96mℹ️ \033[0m"

errors   = []
warnings = []
passes   = []

def ok(msg):   passes.append(msg);   print(f"  {PASS} {msg}")
def fail(msg): errors.append(msg);   print(f"  {FAIL} {msg}")
def warn(msg): warnings.append(msg); print(f"  {WARN} {msg}")
def info(msg):                        print(f"  {INFO} {msg}")
def section(title): print(f"\n{'─'*60}\n  {title}\n{'─'*60}")

def read(p):
    return p.read_text(encoding="utf-8")

def extract_js(html):
    return "\n".join(re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL))

# ─── 1. FICHIERS PRÉSENTS ────────────────────────────────────────────────────
section("1. Fichiers requis")
for f, label in [(V6,"boviq-v6-latest.html"),(ML,"boviq-milklic.html"),
                  (HUB,"index.html"),(SW,"sw.js")]:
    if f.exists(): ok(f"{label} présent ({f.stat().st_size//1024} Ko, {len(read(f).splitlines())} lignes)")
    else:           fail(f"{label} MANQUANT")

# ─── 2. RÈGLE ABSOLUE : index.html ≠ boviq-v6 ───────────────────────────────
section("2. Règle absolue — index.html ≠ boviq-v6")
if HUB.exists():
    hub = read(HUB)
    v6  = read(V6)
    if hub.strip() == v6.strip():
        fail("index.html est IDENTIQUE à boviq-v6-latest.html — règle absolue violée !")
    elif len(hub.splitlines()) > 2000:
        warn(f"index.html a {len(hub.splitlines())} lignes — semble trop long pour un hub")
    else:
        ok(f"index.html est différent de boviq-v6 ({len(hub.splitlines())} lignes)")
    # Vérifier que le hub référence bien boviq-v6
    if 'boviq-v6-latest.html' in hub:
        ok("index.html référence boviq-v6-latest.html")
    else:
        warn("index.html ne semble pas référencer boviq-v6-latest.html")

# ─── 3. SYNTAXE JAVASCRIPT (node --check) ────────────────────────────────────
section("3. Syntaxe JavaScript")
for html_file, label in [(V6, "boviq-v6"),(ML, "boviq-milklic")]:
    html = read(html_file)
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    js = "\n".join(scripts)
    tmp = Path("/tmp") / f"boviq_audit_{label}.js"
    tmp.write_text(js, encoding="utf-8")
    r = subprocess.run(["node","--check",str(tmp)], capture_output=True, text=True)
    if r.returncode == 0:
        ok(f"{label} — syntaxe JS valide ({len(js.splitlines())} lignes JS extraites)")
    else:
        err_line = r.stderr.strip().split('\n')[0] if r.stderr else "erreur inconnue"
        fail(f"{label} — ERREUR JS : {err_line}")


# ─── 4. BALANCE BACKTICKS / ACCOLADES ───────────────────────────────────────
section("4. Balance templates JS (backticks, accolades, parenthèses)")
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic")]:
    js = extract_js(read(html_file))
    bt = js.count('`')
    if bt % 2 != 0: fail(f"{label} — backticks IMPAIRS ({bt}) → template literal non fermé")
    else:           ok(f"{label} — {bt} backticks équilibrés")
    # Vérifier accolades/parenthèses hors strings (approximatif — exclut commentaires)
    clean = re.sub(r'//[^\n]*','', js)
    clean = re.sub(r'/\*.*?\*/','',clean,flags=re.DOTALL)
    clean = re.sub(r'"(?:[^"\\]|\\.)*"','""',clean)
    clean = re.sub(r"'(?:[^'\\]|\\.)*'","''",clean)
    # Retirer les template literals pour l'analyse des accolades
    depth_b = sum(1 if c=='{' else -1 if c=='}' else 0 for c in clean)
    depth_p = sum(1 if c=='(' else -1 if c==')' else 0 for c in clean)
    if depth_b != 0: warn(f"{label} — déséquilibre accolades : {depth_b:+d}")
    else:            ok(f"{label} — accolades équilibrées")
    if depth_p != 0: warn(f"{label} — déséquilibre parenthèses : {depth_p:+d}")
    else:            ok(f"{label} — parenthèses équilibrées")

# ─── 5. IDs HTML DUPLIQUÉS ───────────────────────────────────────────────────
section("5. IDs HTML dupliqués")
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic"),(HUB,"index.html")]:
    html = read(html_file)
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
    dup = {i:ids.count(i) for i in set(ids) if ids.count(i) > 1}
    if dup:
        for id_, cnt in sorted(dup.items()):
            fail(f"{label} — ID dupliqué : #{id_} ({cnt}×)")
    else:
        ok(f"{label} — aucun ID dupliqué ({len(ids)} IDs uniques)")


# ─── 6. FONCTIONS DÉFINIES VS APPELÉES (onclick + appels directs) ─────────────
section("6. Fonctions — définitions vs appels onclick")
v6_html = read(V6)
v6_js   = extract_js(v6_html)
defined = set(re.findall(r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\())', v6_js))
defined_names = set()
for t in defined:
    defined_names.update(n for n in t if n)
# Appels onclick dans le HTML
onclick_calls = re.findall(r'onclick=["\'][^"\']*?(\w+)\(', v6_html)
missing = []
BUILTINS = {'alert','confirm','setTimeout','setInterval','document','window','console','Math',
            'parseInt','parseFloat','JSON','Object','Array','Date','Promise','fetch','Chart',
            'new','return','if','for','let','const','var','true','false','null','undefined',
            'closest','getElementById','querySelector','toggle','classList','stopScan',
            'stopPropagation','preventDefault','location','history','navigator'}
for fn in set(onclick_calls):
    if fn not in defined_names and fn not in BUILTINS:
        missing.append(fn)
if missing:
    for fn in sorted(missing):
        warn(f"boviq-v6 — onclick appelle '{fn}()' : non trouvé dans les définitions JS")
else:
    ok(f"boviq-v6 — tous les onclick ({len(set(onclick_calls))}) pointent vers des fonctions connues")
info(f"boviq-v6 — {len(defined_names)} fonctions/variables définies")

# ─── 7. ENCODAGE PDF — caractères non-Latin1 dans doc.text() ─────────────────
section("7. PDF jsPDF — caractères non-Latin1 dans doc.text()")
NON_LATIN1 = re.compile(r'[^\x00-\xFF]')
EMOJI_RE   = re.compile(r'[\U00010000-\U0010FFFF]|[\U0001F300-\U0001FAFF]|[🀄-🿿]', re.UNICODE)

for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic")]:
    html  = read(html_file)
    lines = html.splitlines()
    pdf_issues = []
    for i, line in enumerate(lines, 1):
        if 'doc.text(' in line or 'addSection(' in line:
            emojis = EMOJI_RE.findall(line)
            non_l1 = [c for c in line if ord(c) > 255]
            if emojis:
                pdf_issues.append((i, f"emoji(s) {emojis[:3]}", line.strip()[:80]))
            elif non_l1:
                pdf_issues.append((i, f"char non-Latin1 {non_l1[:3]}", line.strip()[:80]))
    if pdf_issues:
        for ln, typ, ctx in pdf_issues:
            fail(f"{label} ligne {ln} — {typ} → '{ctx}'")
    else:
        ok(f"{label} — aucun caractère non-Latin1 dans les appels PDF")


# ─── 8. CORPS DE FONCTION ORPHELINS (code hors fonction) ─────────────────────
section("8. Corps de fonction orphelins")
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic")]:
    js = extract_js(read(html_file))
    lines = js.splitlines()
    depth = 0; fn_depths = []; orphan_lines = []
    in_fn = False
    for i, line in enumerate(lines, 1):
        for ch in line:
            if ch == '{':
                depth += 1
                if depth == 1: in_fn = True
            elif ch == '}':
                depth -= 1
                if depth == 0: in_fn = False
        if depth < 0:
            orphan_lines.append((i, line.strip()[:60]))
            depth = 0  # reset
    if orphan_lines:
        for ln, ctx in orphan_lines[:5]:
            fail(f"{label} ligne JS ~{ln} — accolade fermante orpheline : '{ctx}'")
    else:
        ok(f"{label} — aucun corps orphelin détecté")

# ─── 9. VARIABLES CSS MANQUANTES ─────────────────────────────────────────────
section("9. Variables CSS — var(--xxx) définies vs utilisées")
for html_file, label in [(V6,"boviq-v6")]:
    html    = read(html_file)
    defined = set(re.findall(r'--(\w[\w-]+)\s*:', html))
    used    = set(re.findall(r'var\(--(\w[\w-]+)\)', html))
    missing_vars = used - defined
    unused_vars  = defined - used
    if missing_vars:
        for v in sorted(missing_vars):
            fail(f"{label} — var(--{v}) utilisée mais NON définie")
    else:
        ok(f"{label} — toutes les var CSS utilisées sont définies ({len(used)} vars)")
    if unused_vars:
        for v in sorted(list(unused_vars)[:5]):
            warn(f"{label} — --{v} définie mais inutilisée (info seulement)")


# ─── 10. CLÉS LOCALSTORAGE COHÉRENTES ────────────────────────────────────────
section("10. Cohérence des clés localStorage")
EXPECTED_KEYS = {'boviq', 'BOVIQ_MILKLIC', 'boviq_popup_snooze', 'boviq_market_v2'}
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic"),(HUB,"index.html")]:
    html = read(html_file)
    found_keys = set(re.findall(r'localStorage\.\w+\(["\']([^"\']+)["\']', html))
    unknown = found_keys - EXPECTED_KEYS
    if unknown:
        for k in sorted(unknown):
            warn(f"{label} — clé localStorage inattendue : '{k}'")
    elif found_keys:
        ok(f"{label} — clés localStorage OK : {found_keys & EXPECTED_KEYS}")

# ─── 11. CDN / RESSOURCES EXTERNES ───────────────────────────────────────────
section("11. CDN — cohérence versions entre fichiers")
CDN_PATTERN = re.compile(r'https?://[^\s"\'<>]+')
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic")]:
    html = read(html_file)
    cdns = CDN_PATTERN.findall(html)
    # Détecter les mixtes HTTP (non-HTTPS)
    http_only = [c for c in cdns if c.startswith('http://')]
    if http_only:
        for u in http_only:
            warn(f"{label} — ressource HTTP (non-sécurisée) : {u[:80]}")
    chart_vers = re.findall(r'chart\.js/([\d.]+)/', html, re.I)
    if len(set(chart_vers)) > 1:
        fail(f"{label} — versions Chart.js mixtes : {set(chart_vers)}")
    elif chart_vers:
        ok(f"{label} — Chart.js version unique : {chart_vers[0]}")
    jspdf_vers = re.findall(r'jspdf/([\d.]+)/', html, re.I)
    if jspdf_vers:
        ok(f"{label} — jsPDF version : {jspdf_vers[0]}")

# Vérifier cohérence Chart.js entre V6 et milklic
v6_chart = set(re.findall(r'chart\.js/([\d.]+)/', read(V6), re.I))
ml_chart = set(re.findall(r'chart\.js/([\d.]+)/', read(ML), re.I))
if v6_chart and ml_chart and v6_chart != ml_chart:
    fail(f"Versions Chart.js différentes : V6={v6_chart} vs MilKlic={ml_chart}")
elif v6_chart and ml_chart:
    ok(f"Versions Chart.js cohérentes entre V6 et MilKlic : {v6_chart}")


# ─── 12. INTÉGRITÉ INIT_DATA (boviq-v6) ──────────────────────────────────────
section("12. Intégrité INIT_DATA")
v6 = read(V6)
m = re.search(r'const INIT_DATA\s*=\s*(\{.*?\});', v6, re.DOTALL)
if not m:
    fail("boviq-v6 — INIT_DATA introuvable")
else:
    try:
        data = json.loads(m.group(1))
        animaux = data.get('animaux', [])
        ok(f"boviq-v6 — INIT_DATA valide JSON ({len(animaux)} animaux)")
        # Vérifier les champs obligatoires
        required = {'id','nom','type','race','boucle','naissance','sexe'}
        issues = []
        for a in animaux:
            missing = required - set(a.keys())
            if missing:
                issues.append(f"{a.get('nom','?')} : champs manquants {missing}")
        if issues:
            for iss in issues[:5]: fail(f"INIT_DATA — {iss}")
        else:
            ok(f"INIT_DATA — tous les animaux ont les champs requis")
        # Vérifier IDs uniques
        ids = [a['id'] for a in animaux]
        dup_ids = {i: ids.count(i) for i in set(ids) if ids.count(i) > 1}
        if dup_ids:
            for i, c in dup_ids.items(): fail(f"INIT_DATA — ID dupliqué : {i} ({c}×)")
        else:
            ok(f"INIT_DATA — {len(ids)} IDs animaux tous uniques")
        # Vérifier dataVersion
        dv = data.get('_dataVersion')
        if dv: ok(f"INIT_DATA — _dataVersion = {dv}")
        else:  warn("INIT_DATA — _dataVersion absent")
        # Vérifier références mère
        id_set = set(ids)
        bad_mere = [a['nom'] for a in animaux if a.get('mere') and a['mere'] not in id_set]
        if bad_mere:
            for n in bad_mere[:5]: warn(f"INIT_DATA — '{n}' référence une mère inexistante")
        else:
            ok("INIT_DATA — toutes les références mère sont valides")
    except json.JSONDecodeError as e:
        fail(f"boviq-v6 — INIT_DATA JSON invalide : {e}")


# ─── 13. SEUILS LEUCOS (milliers, pas unités brutes) ─────────────────────────
section("13. Seuils leucos — vérification unités (k cell/mL)")
v6_js = extract_js(read(V6))
# Chercher des comparaisons >400000 ou >800000 qui seraient une régression
bad_thresholds = re.findall(r'_ml_leucos\s*[><=!]+\s*([1-9]\d{4,})', v6_js)
if bad_thresholds:
    for val in bad_thresholds:
        fail(f"boviq-v6 — seuil leucos en unités brutes détecté : {val} (doit être en k, ex: 400)")
else:
    ok("boviq-v6 — seuils leucos en milliers (ex: >400, >800, >200)")
# Vérifier aussi dans milklic
ml_js = extract_js(read(ML))
bad_ml = re.findall(r'leucos\s*[><=!]+\s*([1-9]\d{4,})', ml_js)
if bad_ml:
    for val in bad_ml:
        fail(f"boviq-milklic — seuil leucos en unités brutes : {val}")
else:
    ok("boviq-milklic — seuils leucos OK")

# ─── 14. SERVICE WORKER — version cache ──────────────────────────────────────
section("14. Service Worker")
if SW.exists():
    sw = read(SW)
    cache_names = re.findall(r"CACHE\s*=\s*['\"]([^'\"]+)['\"]", sw)
    if cache_names:
        ok(f"sw.js — cache name : {cache_names[0]}")
    else:
        warn("sw.js — nom de cache introuvable")
    # Vérifier que les 4 fichiers HTML sont dans ASSETS
    assets = re.findall(r"['\"](\./[^'\"]+\.html)['\"]", sw)
    expected_assets = ['./boviq-v6-latest.html','./boviq-milklic.html','./boviq-cours-marche.html','./index.html']
    for ea in expected_assets:
        if ea in assets: ok(f"sw.js — {ea} dans ASSETS")
        else:            warn(f"sw.js — {ea} absent de ASSETS")

# ─── 15. manifest.json — start_url ───────────────────────────────────────────
section("15. manifest.json — start_url")
manifest_path = BASE / "manifest.json"
if manifest_path.exists():
    try:
        mf = json.loads(read(manifest_path))
        su = mf.get('start_url','')
        if 'boviq-v6' in su:
            fail(f"manifest.json — start_url pointe vers V6 : '{su}' (doit être './index.html')")
        elif 'index.html' in su or su in ('./', '/'):
            ok(f"manifest.json — start_url correct : '{su}'")
        else:
            warn(f"manifest.json — start_url inhabituel : '{su}'")
    except Exception as e:
        fail(f"manifest.json — JSON invalide : {e}")
else:
    warn("manifest.json — absent")


# ─── 16. FONCTIONS SPÉCIFIQUES BOVIQ REQUISES ─────────────────────────────────
section("16. Fonctions BOVIQ requises présentes")
REQUIRED_FNS_V6 = [
    'renderAnimaux','renderAll','openFicheAnimal','exportFichePdf',
    'openAnimalModal','saveAnimal','delAnimal','renderMilklic',
    'renderFicheCharts','getLeucosHisto','getLeucosRecurrenceColor',
    'openM','closeM','save','load','esc','normBoucle',
    'calcIVV','calcSanteScore','getAnimalStatut',
    'renderTankRisk','renderUGBPrev',
    'loadChartJs','loadJsPdf','loadAutoTable',
]
v6_js_text = extract_js(read(V6))
for fn in REQUIRED_FNS_V6:
    # Chercher définition (function X ou const X = ou async function X)
    pat = re.compile(rf'(?:function\s+{fn}\b|(?:const|let|var)\s+{fn}\s*=|async\s+function\s+{fn}\b)')
    if pat.search(v6_js_text):
        ok(f"boviq-v6 — {fn}() définie")
    else:
        fail(f"boviq-v6 — {fn}() MANQUANTE ou renommée")

REQUIRED_FNS_ML = [
    'saveML','loadML','handleFiles','parseCSV','renderDashboard',
    'renderCellules','renderCourbes','renderFichesMilklic',
]
ml_js_text = extract_js(read(ML))
for fn in REQUIRED_FNS_ML:
    pat = re.compile(rf'(?:function\s+{fn}\b|(?:const|let|var)\s+{fn}\s*=)')
    if pat.search(ml_js_text):
        ok(f"boviq-milklic — {fn}() définie")
    else:
        warn(f"boviq-milklic — {fn}() non trouvée (peut être inline)")


# ─── 17. DOUBLE DÉFINITION DE FONCTIONS ──────────────────────────────────────
section("17. Fonctions définies plusieurs fois")
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic")]:
    js = extract_js(read(html_file))
    all_fns = re.findall(r'(?:async\s+)?function\s+(\w+)\s*\(', js)
    dup_fns = {f: all_fns.count(f) for f in set(all_fns) if all_fns.count(f) > 1}
    if dup_fns:
        for fn, cnt in sorted(dup_fns.items()):
            fail(f"{label} — fonction '{fn}' définie {cnt}× (corps orphelin potentiel !)")
    else:
        ok(f"{label} — aucune fonction définie en double")

# ─── 18. BALISES HTML NON FERMÉES (basique) ───────────────────────────────────
section("18. Structure HTML — balises div/section")
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic"),(HUB,"index.html")]:
    html  = read(html_file)
    # Retirer scripts et styles pour l'analyse
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>',   '', clean, flags=re.DOTALL)
    divs_open  = len(re.findall(r'<div[\s>]', clean))
    divs_close = len(re.findall(r'</div>', clean))
    diff = divs_open - divs_close
    if diff != 0:
        warn(f"{label} — <div> : {divs_open} ouvertures, {divs_close} fermetures (diff : {diff:+d})")
    else:
        ok(f"{label} — <div> équilibrés ({divs_open})")

# ─── 19. VÉRIFICATION data-version INIT_DATA ─────────────────────────────────
section("19. _dataVersion cohérence")
v6_html = read(V6)
dv_matches = re.findall(r'_dataVersion["\']?\s*:\s*(\d+)', v6_html)
if len(set(dv_matches)) == 1:
    ok(f"boviq-v6 — _dataVersion cohérente : {dv_matches[0]}")
elif len(set(dv_matches)) > 1:
    warn(f"boviq-v6 — plusieurs _dataVersion trouvées : {set(dv_matches)}")
else:
    warn("boviq-v6 — _dataVersion introuvable dans le HTML")


# ─── 20. GIT — état du dépôt ─────────────────────────────────────────────────
section("20. Git — état du dépôt")
r = subprocess.run(['git','-C',str(BASE),'status','--porcelain'], capture_output=True, text=True)
if r.stdout.strip():
    uncommitted = r.stdout.strip().splitlines()
    warn(f"Fichiers non commités ({len(uncommitted)}) :")
    for line in uncommitted: info(f"  {line}")
else:
    ok("Dépôt propre — aucun fichier non commité")

r2 = subprocess.run(['git','-C',str(BASE),'log','--oneline','-1'], capture_output=True, text=True)
info(f"Dernier commit : {r2.stdout.strip()}")

# ─── 21. AUDIT TAILLE FICHIERS ────────────────────────────────────────────────
section("21. Taille des fichiers")
MAX_V6  = 600  # Ko max raisonnable pour V6
MAX_ML  = 300
for f, label, max_kb in [(V6,"boviq-v6",MAX_V6),(ML,"boviq-milklic",MAX_ML)]:
    kb = f.stat().st_size // 1024
    if kb > max_kb:
        warn(f"{label} — {kb} Ko (seuil alerté : {max_kb} Ko)")
    else:
        ok(f"{label} — {kb} Ko (< {max_kb} Ko)")

# ─── 22. MOTIFS CONNUS DANGEREUX ─────────────────────────────────────────────
section("22. Motifs dangereux connus")
DANGEROUS = [
    (r'cp\s+boviq-v6-latest\.html\s+index\.html', "Commande interdite cp V6 → index.html"),
    (r'localStorage\.clear\(\)', "localStorage.clear() — effacement total"),
    (r'eval\s*\(', "eval() — risque de sécurité"),
    (r'document\.write\s*\(', "document.write() — pratique obsolète"),
    (r'innerHTML\s*\+=', "innerHTML += (concaténation) — peut être lent sur gros DOM"),
]
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic"),(HUB,"index.html")]:
    content = read(html_file)
    for pattern, msg in DANGEROUS:
        if re.search(pattern, content):
            warn(f"{label} — {msg}")

ok_dangerous = True
for html_file, label in [(V6,"boviq-v6"),(ML,"boviq-milklic")]:
    content = read(html_file)
    if re.search(r'cp\s+boviq-v6-latest\.html\s+index\.html', content):
        ok_dangerous = False
if ok_dangerous:
    ok("Aucun motif dangereux critique détecté")


# ─── 23. COHÉRENCE saveML → D.mlControles ────────────────────────────────────
section("23. Bridge mlControles — boviq-milklic → boviq-v6")
ml_html = read(ML)
v6_html = read(V6)
if 'mlControles' in ml_html and 'D.mlControles' in v6_html:
    ok("saveML() écrit D.mlControles ET getLeucosHisto() le lit dans V6")
elif 'mlControles' not in ml_html:
    fail("boviq-milklic — saveML() ne semble plus écrire mlControles")
elif 'D.mlControles' not in v6_html:
    fail("boviq-v6 — D.mlControles non référencé (lecture historique cassée)")

# Vérifier getLeucosHisto présente et utilisant D.mlControles
if 'getLeucosHisto' in v6_html and 'D.mlControles' in v6_html:
    ok("boviq-v6 — getLeucosHisto() référence D.mlControles")
else:
    fail("boviq-v6 — getLeucosHisto() ou D.mlControles manquant")

# ─── 24. renderFicheCharts — setTimeout présent ───────────────────────────────
section("24. renderFicheCharts — appel différé (setTimeout)")
v6_js = extract_js(read(V6))
if re.search(r'setTimeout\s*\(\s*\(\s*\)\s*=>\s*renderFicheCharts', v6_js):
    ok("boviq-v6 — renderFicheCharts appelée via setTimeout (canvas visible)")
elif re.search(r'renderFicheCharts', v6_js):
    warn("boviq-v6 — renderFicheCharts présente mais appel direct (sans setTimeout) — risque canvas vide")
else:
    fail("boviq-v6 — renderFicheCharts introuvable")

# ─── 25. COURBES PDF — addImage présent ──────────────────────────────────────
section("25. Courbes PDF — doc.addImage() présent dans exportFichePdf")
if 'doc.addImage' in v6_js and 'toDataURL' in v6_js:
    ok("boviq-v6 — courbes PDF : toDataURL + doc.addImage présents")
else:
    fail("boviq-v6 — courbes PDF manquantes (doc.addImage ou toDataURL absent)")

# ─── 26. SCROLL — height:100dvh / overflow-y:hidden ─────────────────────────
section("26. CSS scroll — vérification régression height:100dvh")
v6_html = read(V6)
# Ces règles avaient cassé le scroll en session précédente — vérifier qu'elles ne sont pas revenues
styles = re.findall(r'<style[^>]*>(.*?)</style>', v6_html, re.DOTALL)
css_full = "\n".join(styles)
# Vérifier .content sans overflow-y:hidden
content_block = re.findall(r'\.content\s*\{([^}]+)\}', css_full)
for blk in content_block:
    if 'overflow-y' in blk and 'hidden' in blk:
        fail("boviq-v6 — .content a overflow-y:hidden — risque de bloquer le scroll !")
    if 'height' in blk and '100dvh' in blk and 'overflow-y' in blk and 'auto' not in blk:
        fail("boviq-v6 — .content a height:100dvh sans overflow-y:auto — risque de bloquer le scroll !")
# Chercher dans les règles #p-*.active
active_rules = re.findall(r'#p-\w+\.active\s*\{([^}]+)\}', css_full)
scroll_breaks = []
for rule in active_rules:
    if 'overflow-y' in rule and 'auto' in rule and 'height' in rule and ('100dvh' in rule or '100vh' in rule):
        scroll_breaks.append(rule.strip()[:60])
if scroll_breaks:
    for sb in scroll_breaks:
        warn(f"boviq-v6 — règle #p-*.active potentiellement bloquante : {sb}")
else:
    ok("boviq-v6 — aucune règle CSS bloquant le scroll détectée")


# ─── RAPPORT FINAL ────────────────────────────────────────────────────────────
print(f"\n{'═'*60}")
print(f"  RAPPORT FINAL — BOVIQ Audit")
print(f"{'═'*60}")
print(f"  {PASS} Succès   : {len(passes)}")
print(f"  {WARN} Warnings : {len(warnings)}")
print(f"  {FAIL} Erreurs  : {len(errors)}")
print(f"{'═'*60}")

if errors:
    print(f"\n  ❌ ERREURS À CORRIGER :")
    for i, e in enumerate(errors, 1):
        print(f"     {i}. {e}")

if warnings:
    print(f"\n  ⚠️  WARNINGS (à examiner) :")
    for i, w in enumerate(warnings, 1):
        print(f"     {i}. {w}")

if not errors and not warnings:
    print(f"\n  🎉 AUDIT PARFAIT — Aucun problème détecté !")
elif not errors:
    print(f"\n  ✅ Aucune erreur bloquante — {len(warnings)} warning(s) à examiner")
else:
    print(f"\n  🚨 {len(errors)} erreur(s) bloquante(s) à corriger")

print(f"\n{'═'*60}\n")
sys.exit(1 if errors else 0)
