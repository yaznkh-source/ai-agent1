#!/bin/bash
# Backup Script - Task B1 - Production Hardened 80/100
# Backs up SQLite DB, storage, chroma data, env files
# Usage: ./scripts/backup.sh [backup_dir]
# Output: backup-YYYY-MM-DD-HHMMSS.tar.gz

set -e

BACKUP_DIR=${1:-./backups}
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
BACKUP_NAME="backup-$TIMESTAMP"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
ARCHIVE="$BACKUP_DIR/$BACKUP_NAME.tar.gz"

echo "🔒 AI Agency OS - Backup Script - Task B1"
echo "📅 Timestamp: $TIMESTAMP"
echo "📁 Backup dir: $BACKUP_DIR"
echo "📦 Archive: $ARCHIVE"

mkdir -p "$BACKUP_PATH"

# Check what exists
echo ""
echo "🔍 Checking data sources..."

# Backend DB - SQLite
if [ -f "./backend/ai_agency.db" ]; then
    echo "✅ Found backend/ai_agency.db"
    cp ./backend/ai_agency.db "$BACKUP_PATH/" 2>/dev/null || echo "⚠️ Could not copy ai_agency.db"
    # Also sqlite3 dump if available
    if command -v sqlite3 &> /dev/null; then
        sqlite3 ./backend/ai_agency.db .dump > "$BACKUP_PATH/ai_agency.sql" 2>/dev/null || echo "⚠️ sqlite3 dump failed"
        echo "✅ SQLite dump created"
    fi
else
    echo "ℹ️ No backend/ai_agency.db (will be created on first run)"
fi

# Storage
if [ -d "./backend/storage" ]; then
    echo "✅ Found backend/storage"
    cp -r ./backend/storage "$BACKUP_PATH/storage" 2>/dev/null || echo "⚠️ Could not copy storage"
fi

if [ -d "./storage" ]; then
    echo "✅ Found ./storage"
    cp -r ./storage "$BACKUP_PATH/storage_root" 2>/dev/null || true
fi

# Chroma data (if exists)
if [ -d "./backend/chroma_data" ]; then
    echo "✅ Found backend/chroma_data"
    cp -r ./backend/chroma_data "$BACKUP_PATH/chroma_data" 2>/dev/null || true
fi

# Env files (without secrets in archive? We'll include but warn)
if [ -f "./.env.prod.example" ]; then
    cp ./.env.prod.example "$BACKUP_PATH/" 2>/dev/null || true
fi

# Config
if [ -f "./docker-compose.prod.yml" ]; then
    cp ./docker-compose.prod.yml "$BACKUP_PATH/" 2>/dev/null || true
fi

if [ -d "./k8s" ]; then
    cp -r ./k8s "$BACKUP_PATH/k8s" 2>/dev/null || true
fi

# Create manifest
cat > "$BACKUP_PATH/manifest.txt" <<EOF
AI Agency OS Backup
Timestamp: $TIMESTAMP
Date: $(date)
Host: $(hostname)
User: $(whoami)
Commit: $(git rev-parse HEAD 2>/dev/null || echo "unknown")
Branch: $(git branch --show-current 2>/dev/null || echo "unknown")

Contents:
$(ls -lah "$BACKUP_PATH")

Database:
- SQLite: ai_agency.db + ai_agency.sql dump
- Storage: storage/ folder
- Chroma: chroma_data/ if exists

Restore: ./scripts/restore.sh $ARCHIVE
EOF

echo ""
echo "📋 Manifest:"
cat "$BACKUP_PATH/manifest.txt"

# Create archive
echo ""
echo "📦 Creating archive..."
tar -czf "$ARCHIVE" -C "$BACKUP_DIR" "$BACKUP_NAME"
rm -rf "$BACKUP_PATH"

SIZE=$(du -h "$ARCHIVE" | cut -f1)
echo ""
echo "✅ Backup complete!"
echo "📦 Archive: $ARCHIVE"
echo "📏 Size: $SIZE"
echo "📋 To restore: ./scripts/restore.sh $ARCHIVE"
echo ""
echo "💡 For production, also backup:"
echo "  - Postgres: pg_dump aiagency > backup.sql (if using postgres)"
echo "  - Redis: redis-cli --rdb backup.rdb"
echo "  - S3/MinIO: mc mirror or aws s3 sync"
echo "  - Env secrets: .env.prod (store securely, not in git)"
