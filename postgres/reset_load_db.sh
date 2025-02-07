#!/usr/bin/env bash

set -e # fail whole script on any error

# validate inputs

REQUIRED_VARS=('PGHOST' 'PGPASSWORD' 'PGUSER' 'PGPORT' 'PGDATABASE')
MISSING_VARS=()

CONTAINER_NAME='dvd_rentals_pg'

# $arr[@] - the @ means all elements of array
# "$arr[@]" - the @ means all elements, but preserving spaces _inside_ elements,
#             rather than exploding space-separated words in an element into 
#             different elements
# the curly braces around a parameter are required when doing special expansion features
# (such as those involving arrays) and then, everything needs to be inside of ${}. Things
# like $arr[@] will go badly.
for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z ${!var+x} ]] then # !var means var holds the name of the variable to insert.
        MISSING_VARS+=("$var") # oh cool, += appends stuff to an array
    fi
done

if [[ ${#MISSING_VARS[@]} -ne 0 ]]; then # the pound operator in ${#arr[@]} gets the array length
    echo "Required variable(s) are not set: ${MISSING_VARS[*]}"
    exit 1
fi


ARCHIVE_NAME=dvdrental.tar
echo "Reset from previous runs"

test -f $ARCHIVE_NAME && rm $ARCHIVE_NAME # -f flag is required for test to check file existence

echo "Unzip archive"
unzip dvdrental.zip

# docker inspect produces json with lots of metadata about container and its state
# jq command reads "State.Running" from the first array element (there is an array
# element returned for each container requested in the inspect command)
container_running=$(docker inspect $CONTAINER_NAME | jq -r ".[0].State.Running")
if [[ $container_running == "false" ]]; then
    echo "Starting docker container $CONTAINER_NAME"
    docker start dvd_rentals_pg
else
    echo "Container $CONTAINER_NAME already running"
fi

test $ARCHIVE_NAME
if test -f $ARCHIVE_NAME; then
    echo "Archive $ARCHIVE_NAME is present"
else
    echo "Archive $ARCHIVE_NAME not found"
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
pg_restore -d $PGDATABASE $ARCHIVE_NAME

echo "Success. Tables loaded into $PGDATABASE:"

# psql will run commands in stdin. Using here-doc to simplify managing quotes in the command.
psql << 'EOF'
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;
EOF

echo "Clean up archive"
rm $ARCHIVE_NAME

