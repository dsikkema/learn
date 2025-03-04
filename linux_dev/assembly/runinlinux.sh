#!/usr/bin/env bash
../lazy_start_linux.sh
docker exec -t linux_dev /assembly/assemble_link_run.sh "/assembly/${1}"
