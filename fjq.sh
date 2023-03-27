#!/usr/bin/env bash

# from https://gist.github.com/reegnz/b9e40993d410b75c2d866441add2cb55
# TODO: would be nice if it outputs the final query or result

if [[ -z $1 ]] || [[ $1 == "-" ]]; then
    input=$(mktemp)
    trap 'rm -f "$input"' EXIT
    cat /dev/stdin > "$input"
else
    input=$1
fi

echo '' \
    | fzf --disabled \
        --preview-window='up:90%' \
        --print-query \
        --preview "jq --color-output -r {q} $input"
