#!/bin/zsh
# ═══════════════════════════════════════════════════════
# BOVIQ — Script de sauvegarde NAS
# Usage: ./scripts/backup-nas.sh
# ═══════════════════════════════════════════════════════

set -e

PROJET="/Users/laurentduval/Desktop/01-Projects/BOVIQ"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# ── Chercher le NAS automatiquement ──────────────────────
NAS_MOUNT=""
for vol in /Volumes/*/; do
  if [ -d "${vol}BOVIQ" ] || [ -d "${vol}Projets" ] || [ -d "${vol}Projects" ]; then
    NAS_MOUNT="$vol"
    break
  fi
done

# Si non trouvé, chercher tout volume non-système
if [ -z "$NAS_MOUNT" ]; then
  for vol in /Volumes/*/; do
    name=$(basename "$vol")
    if [ "$name" != "Macintosh HD" ] && [ -d "$vol" ]; then
      NAS_MOUNT="$vol"
      break
    fi
  done
fi

if [ -z "$NAS_MOUNT" ]; then
  echo "❌ Aucun NAS monté dans /Volumes/"
  echo "   → Monte ton NAS d'abord (Finder → Go → Connect to Server)"
  echo "   → Puis relance ce script"
  exit 1
fi

echo "✅ NAS trouvé: $NAS_MOUNT"

# ── Destination sur le NAS ────────────────────────────────
NAS_DEST="${NAS_MOUNT}BOVIQ_BACKUPS"
mkdir -p "$NAS_DEST"

# ── 1. Snapshot horodaté ──────────────────────────────────
SNAP_DIR="$NAS_DEST/snapshots/BOVIQ_$TIMESTAMP"
mkdir -p "$SNAP_DIR"
rsync -av --exclude='.git' --exclude='__pycache__' --exclude='.DS_Store' \
  "$PROJET/" "$SNAP_DIR/"
echo "✅ Snapshot → $SNAP_DIR"

# ── 2. Version courante (latest) ─────────────────────────
LATEST_DIR="$NAS_DEST/latest"
mkdir -p "$LATEST_DIR"
rsync -av --delete --exclude='.git' --exclude='__pycache__' --exclude='.DS_Store' \
  "$PROJET/" "$LATEST_DIR/"
echo "✅ Latest → $LATEST_DIR"

# ── 3. Fichiers actifs séparés ────────────────────────────
FILES_DIR="$NAS_DEST/fichiers-actifs"
mkdir -p "$FILES_DIR"
cp "$PROJET/boviq-v6-latest.html"     "$FILES_DIR/boviq-v6-latest_$TIMESTAMP.html"
cp "$PROJET/boviq-milklic.html"       "$FILES_DIR/boviq-milklic_$TIMESTAMP.html"
cp "$PROJET/boviq-cours-marche.html"  "$FILES_DIR/boviq-cours_$TIMESTAMP.html"
cp "$PROJET/index.html"               "$FILES_DIR/index_$TIMESTAMP.html"
echo "✅ Fichiers actifs copiés séparément"

# ── 4. Manifest ───────────────────────────────────────────
echo "=== BOVIQ BACKUP NAS ===" > "$NAS_DEST/DERNIERE_SAUVEGARDE.txt"
echo "Date: $(date '+%d/%m/%Y %H:%M:%S')" >> "$NAS_DEST/DERNIERE_SAUVEGARDE.txt"
echo "Snapshot: $SNAP_DIR" >> "$NAS_DEST/DERNIERE_SAUVEGARDE.txt"
echo "Git commit:" >> "$NAS_DEST/DERNIERE_SAUVEGARDE.txt"
cd "$PROJET" && git log --oneline -5 >> "$NAS_DEST/DERNIERE_SAUVEGARDE.txt"

echo ""
echo "═══════════════════════════════════════"
echo "✅ BACKUP NAS COMPLET — $TIMESTAMP"
echo "   Snapshot  : $SNAP_DIR"
echo "   Latest    : $LATEST_DIR"
echo "   Actifs    : $FILES_DIR"
echo "═══════════════════════════════════════"
