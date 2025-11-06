if [ -z "$1" ]; then
    echo "Usage: ./restore_database.sh <backup_file.sql.gz>"
    exit 1
fi

BACKUP_FILE=$1
DB_NAME="civic_issues"

# Decompress
gunzip -c $BACKUP_FILE > /tmp/restore.sql

# Restore
psql -U civicapp $DB_NAME < /tmp/restore.sql

# Cleanup
rm /tmp/restore.sql

echo "Database restored from: $BACKUP_FILE"