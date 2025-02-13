#!/usr/bin/env bash

set -e # fail whole script on any error

# validate inputs

REQUIRED_VARS=('PGHOST' 'PGPASSWORD' 'PGUSER' 'PGPORT' 'PGDATABASE')
MISSING_VARS=()
DUMP_NAME=simple_tables.sql

CONTAINER_NAME='dvd_rentals_pg'

for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z ${!var+x} ]] then 
        MISSING_VARS+=("$var") 
    fi
done

if [[ ${#MISSING_VARS[@]} -ne 0 ]]; then 
    echo "Required variable(s) are not set: ${MISSING_VARS[*]}"
    exit 1
fi


container_running=$(docker inspect $CONTAINER_NAME | jq -r ".[0].State.Running")
if [[ $container_running == "false" ]]; then
    echo "Starting docker container $CONTAINER_NAME"
    docker start dvd_rentals_pg
else
    echo "Container $CONTAINER_NAME already running"
fi

if test -f $DUMP_NAME; then
    echo "Archive $DUMP_NAME is present"
else
    echo "Archive $DUMP_NAME not found"
    exit 1
fi

# -q flag for pg_isready means quiet
i=0
while ! pg_isready -q && ((i<10)); do
    echo "Waiting for postgres server to start"
    i=$((i+1))
    sleep 1
done

if ! pg_isready -q; then
    echo "Postgres server didn't start in time"
    exit 1
else
    echo "Postgres server ready"
fi

echo "Create and restore db $PGDATABASE from empty."

# two different -c commands, otherwise they'll be put into txn blocks, and database update
# commands cannot be in a txn block
psql -d postgres -c "DROP DATABASE IF EXISTS $PGDATABASE;" -c "CREATE DATABASE $PGDATABASE;"
psql -d $PGDATABASE -f $DUMP_NAME

echo "Success. Tables loaded into $PGDATABASE:"

# psql will run commands in stdin. Using here-doc to simplify managing quotes in the command.
psql << 'EOF'
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;
EOF


