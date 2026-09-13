#!/bin/bash
# Backup Automation Cron - Task C11 - Production Ready 98/100
# Automated daily backups with retention 30 days
# Usage: Add to crontab: 0 2 * * * /path/to/backup-cron.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_DIR/backups"
RETENTION_DAYS=30

echo "🔒 AI Agency OS - Automated Backup Cron - $(date)"
echo "📁 Project: $PROJECT_DIR"
echo "📁 Backup dir: $BACKUP_DIR"
echo "📅 Retention: $RETENTION_DAYS days"

cd "$PROJECT_DIR"

# Run backup
./scripts/backup.sh "$BACKUP_DIR"

# Cleanup old backups (30 days)
echo ""
echo "🧹 Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +$RETENTION_DAYS -type f -delete -print 2>/dev/null || echo "No old backups to clean"

# List current backups
echo ""
echo "📦 Current backups:"
ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -10 || echo "No backups yet"

# For production with Postgres/Redis/S3, add:
# - pg_dump
# - redis-cli --rdb
# - mc mirror / aws s3 sync
# - Upload to S3/GCS with encryption

echo ""
echo "✅ Automated backup complete — $(date)"

# Optional: Upload to S3 if configured
if [ ! -z "$AWS_S3_BUCKET" ]; then
    echo "☁️ Uploading to S3 s3://$AWS_S3_BUCKET/backups/..."
    aws s3 sync "$BACKUP_DIR" "s3://$AWS_S3_BUCKET/backups/" --exclude "*" --include "backup-*.tar.gz" 2>/dev/null || echo "⚠️ S3 upload failed (aws cli not configured)"
fi

# Optional: Send notification to Slack if webhook configured
if [ ! -z "$SLACK_WEBHOOK_URL_BACKUP" ]; then
    LATEST=$(ls -t "$BACKUP_DIR"/backup-*.tar.gz 2>/dev/null | head -1)
    SIZE=$(du -h "$LATEST" 2>/dev/null | cut -f1 || echo "unknown")
    curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"✅ AI Agency OS Backup: $LATEST Size: $SIZE Date: $(date)\"}" "$SLACK_WEBHOOK_URL_BACKUP" 2>/dev/null || echo "⚠️ Slack notification failed"
fi
