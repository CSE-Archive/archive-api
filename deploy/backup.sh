#!/bin/sh
# CSE Archive production backup — nightly database dump + weekly media tar.
# Installed on the VM as /usr/local/bin/csearchive-backup (from this file) and
# driven by /etc/cron.d/csearchive-backup (times are the VM's LOCAL time):
# dumps in /var/backups/csearchive, log lines via syslog (tag
# csearchive-backup).
#
# What is backed up and why:
#   - database: nightly, 14-day retention (admin edits, new content)
#   - media:    weekly full tar, 2 copies kept (~2.6 GB each; the set barely
#               changes — it was restored once from the archive zip)

set -eu

BACKUP_DIR=/var/backups/csearchive
COMPOSE_DIR=/opt/csearchive
LOG_TAG=csearchive-backup

DB_RETENTION_DAYS=14
MEDIA_RETENTION_COPIES=2

log() { logger -t "$LOG_TAG" -s -- "$1" 2>&1; }

mkdir -p "$BACKUP_DIR"

# --- database ---------------------------------------------------------------
stamp=$(date +%Y%m%d-%H%M)
db_dump="$BACKUP_DIR/csearchive-db-$stamp.sql.gz"

if cd "$COMPOSE_DIR" && docker compose exec -T db pg_dump -U csearchive csearchive \
        | gzip > "$db_dump" && [ -s "$db_dump" ]; then
    log "db dump ok: $db_dump ($(du -h "$db_dump" | cut -f1))"
else
    rm -f "$db_dump"
    log "ERROR: db dump failed"
    exit 1
fi

find "$BACKUP_DIR" -name 'csearchive-db-*.sql.gz' -mtime +$DB_RETENTION_DAYS -delete

# --- media (weekly: ISO week changed since the newest existing tar) ---------
newest_media=$(ls -1t "$BACKUP_DIR"/csearchive-media-*.tar.gz 2>/dev/null | head -1 || true)
current_week=$(date +%G-W%V)
if [ -z "$newest_media" ] || [ "${newest_media##*csearchive-media-}" != "$current_week.tar.gz" ]; then
    media_tar="$BACKUP_DIR/csearchive-media-$current_week.tar.gz"
    if tar -C "$COMPOSE_DIR/data" -czf "$media_tar" media \
            && [ -s "$media_tar" ]; then
        log "media tar ok: $media_tar ($(du -h "$media_tar" | cut -f1))"
        # Keep only the newest N media tars.
        ls -1t "$BACKUP_DIR"/csearchive-media-*.tar.gz | tail -n +$((MEDIA_RETENTION_COPIES + 1)) | xargs -r rm --
    else
        rm -f "$media_tar"
        log "ERROR: media tar failed"
        exit 1
    fi
else
    log "media tar for $current_week already exists, skipping"
fi

log "backup finished"
