#!/bin/bash
test $# -eq 0 && { echo "ERROR: no args passed" 1>&2; exit 1; }
test -p ~/.win.fifo || { echo "ERROR: ~/.win.fifo pipe does not exist, call windows start script first" 1>&2; exit 1; }
encoded_cmd=""
for x; do
    encoded_cmd+=,$(printf "%s" "$x" | base64 | tr -d \\n)
done
echo ${encoded_cmd:1} > ~/.win.fifo
