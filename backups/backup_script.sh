#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

. "$DIR""/../.envs/.production/.django"
. "$DIR""/../.envs/.production/.postgres"

CELERY_BROKER_URL="${REDIS_URL}"
DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
LOCAL_BACKUP_DIR="$DIR""/archives/"
REMOTE_BACKUP_DIR="/groups/irset/archives/web/genoViewer/"
DATE=`eval date +%Y%m%d`

echo "Writing Postgres dump"
/usr/local/bin/docker-compose -f "$DIR""/../production.yml" exec -T postgres sh -c "pg_dump --clean -U $POSTGRES_USER $POSTGRES_DB > /backups/DB_backup"
mv "$DIR""/DB_backup" "$REMOTE_BACKUP_DIR"
