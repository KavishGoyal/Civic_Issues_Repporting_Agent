BACKUP_DIR="/opt/civic-backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="civic_issues"
BACKUP_FILE="$BACKUP_DIR/civic_backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

# Create backup
pg_dump -U civicapp $DB_NAME > $BACKUP_FILE

# Compress
gzip $BACKUP_FILE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "civic_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE.gz"