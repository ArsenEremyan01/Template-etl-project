#!/bin/bash

backup_date=$(date +%Y%m%d)
docker exec -i database pg_dump -U postgres -d mrr_db > ./backups/mrr_db_${backup_date}.sql
docker exec -i database pg_dump -U postgres -d staging_db > ./backups/staging_db_${backup_date}.sql
docker exec -i database pg_dump -U postgres -d dwh_db > ./backups/dwh_db_${backup_date}.sql