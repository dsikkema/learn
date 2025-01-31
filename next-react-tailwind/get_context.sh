#!/usr/bin/env sh
tree app
find app -name "*.js" -exec sh -c  "echo \\\\nFilename: {}\\\\n && cat {} " \;
