#!/usr/bin/env bash

set -e # fail whole script on any error

# validate inputs

REQUIRED_VARS=('PGHOST' 'PGPASSWORD' 'PGUSER' 'PGPORT' 'PGDATABASE')
MISSING_VARS=()

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

echo "Start docker container just in case"
docker start dvd_rentals_pg

echo "Make sure archive is there"
test $ARCHIVE_NAME

echo "Create and restore db $PGDATABASE from empty."

# two different -c commands because each command is in its own transaction; drop database can't 
# happen inside a txn block.
psql -d postgres -c "DROP DATABASE IF EXISTS $PGDATABASE;" -c "CREATE DATABASE $PGDATABASE;"
pg_restore -d $PGDATABASE $ARCHIVE_NAME

echo "Success. Tables loaded into $PGDATABASE:"

# psql will run commands in stdin. Using here-doc to simplify managing quotes in the command.
psql << 'EOF'
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;
EOF

echo "Clean up archive"
rm $ARCHIVE_NAME

