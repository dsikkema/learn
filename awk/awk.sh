#!/usr/bin/env bash
PS4=' $ '
set -x
cat employees.txt
: get the "second" column
awk '{print $2}' employees.txt

: override default separator with ","
awk -F, '{print $2}' employees.txt

: now skip the first line
awk -F, 'NR > 1 {print $2}' employees.txt

: TOODO skip lines starting with "&"
