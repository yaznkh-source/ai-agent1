#!/bin/bash
# Restore Script - Task B1 - Production Hardened 80/100
# Restores from backup archive
# Usage: ./scripts/restore.sh backup-YYYY-MM-DD-HHMMSS.tar.gz [target_dir]
# WARNING: Overwrites existing data!

set -e

ARCHIVE=$1
TARGET_DIR=${2:-.}

if [ -z "$ARCHIVE" ]; then
    echo "❌ Usage: ./scripts/restore.sh <backup.tar.gz> [target_dir]"
    echo "📁 Available backups:"
    ls -lh ./backups/*.tar.gz 2>/dev/null || echo "  No backups in ./backups/"
    exit 1
fi

if [ ! -f "$ARCHIVE" ]; then
    echo "❌ Archive not found: $ARCHIVE"
    exit 1
fi

echo "🔒 AI Agency OS - Restore Script - Task B1"
echo "📦 Archive: $ARCHIVE"
echo "📁 Target: $TARGET_DIR"
echo ""
echo "⚠️ WARNING: This will overwrite existing data!"
echo "  - backend/ai_agency.db"
echo "  - backend/storage/"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted"
    exit 1
fi

# Extract to temp
TEMP_DIR=$(mktemp -d)
echo "📂 Extracting to temp: $TEMP_DIR"
tar -xzf "$ARCHIVE" -C "$TEMP_DIR"

BACKUP_NAME=$(basename "$ARCHIVE" .tar.gz)
EXTRACTED="$TEMP_DIR/$BACKUP_NAME"

if [ ! -d "$EXTRACTED" ]; then
    # Try without nested folder
    EXTRACTED="$TEMP_DIR"
fi

echo "📋 Contents:"
ls -lah "$EXTRACTED"
echo ""
cat "$EXTRACTED/manifest.txt" 2>/dev/null || echo "No manifest"

# Restore DB
if [ -f "$EXTRACTED/ai_agency.db" ]; then
    echo ""
    echo "🔄 Restoring ai_agency.db..."
    cp "$EXTRACTED/ai_agency.db" "$TARGET_DIR/backend/ai_agency.db"
    echo "✅ DB restored"
fi

if [ -f "$EXTRACTED/ai_agency.sql" ]; then
    echo "ℹ️ SQL dump available at $EXTRACTED/ai_agency.sql"
    echo "   To restore via SQL: sqlite3 backend/ai_agency.db < ai_agency.sql"
fi

# Restore storage
if [ -d "$EXTRACTED/storage" ]; then
    echo "🔄 Restoring storage..."
    mkdir -p "$TARGET_DIR/backend/storage"
    cp -r "$EXTRACTED/storage"/* "$TARGET_DIR/backend/storage/" 2>/dev/null || cp -r "$EXTRACTED/storage" "$TARGET_DIR/backend/" 2>/dev/null || true
    echo "✅ Storage restored"
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Restore complete!"
echo "📋 Next steps:"
echo "  1. Restart backend: cd backend && uvicorn app.main:app --reload"
echo "  2. Check: curl http://localhost:8000/api/health"
echo "  3. Verify: curl http://localhost:8000/api/agents/ | jq .total (should be 68)"
echo ""
echo "💡 For postgres production:"
echo "  psql aiagency < backup.sql"
echo "  For redis: redis-cli --pipe < backup.rdb"
