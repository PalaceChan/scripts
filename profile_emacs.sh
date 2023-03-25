#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail

emacs -Q \
      --eval "(profiler-start 'cpu)" \
      -l ~/.emacs.d/init.el \
      -f profiler-stop \
      -f profiler-report
