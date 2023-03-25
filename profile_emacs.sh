#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

if [[ $1 == "profiler" ]]; then
    emacs -Q \
          --eval "(profiler-start 'cpu)" \
          -l ~/.emacs.d/init.el \
          -f profiler-stop \
          -f profiler-report
elif [[ $1 == "packages" ]]; then
    emacs -Q \
          --eval '(setq use-package-compute-statistics t)' \
          -l ~/.emacs.d/init.el \
          -f use-package-report
fi
