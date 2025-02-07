#!/usr/bin/env bash
set -v
echo $0
realpath "$0"

# directory containing this file, no matter where it's run from (symlinks resolved)
dirname "$(realpath $0)"
