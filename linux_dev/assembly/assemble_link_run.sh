#!/bin/bash
if [ "$#" -ne 1 ]; then
    printf "Compile & run assembly:\n\nUsage: $0 filename.s\n"
    exit 1
fi

BASENAME=$(basename "$1" .s)
SOURCEFILE="$1"

mkdir -p target

as "$SOURCEFILE" -o "target/${BASENAME}.o"

if [ $? -ne 0 ]; then
    echo 'Assembly failed'
    exit 1
fi

ld "target/${BASENAME}.o" -o "target/${BASENAME}"
if [ $? -ne 0 ]; then
    echo 'Linking failed'
    exit 1
fi

"target/${BASENAME}"
echo "Exited with code: $?"