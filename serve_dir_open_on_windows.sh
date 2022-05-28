#!/bin/bash

dir_to_serve="$1"

[ "X${dir_to_serve}" = "X" ] && echo "Must provide directory to serve." 1>&2 && exit -1

# kill all children on receiving signal
trap 'kill 0' SIGINT SIGHUP SIGTERM EXIT

echo "starting http server in subshell"
exec 3< <(export PYTHONUNBUFFERED=1 && python -m http.server -d ${dir_to_serve} 0)

echo "reading portnum from server process"
read line <&3
echo "${line}"
port_num=$(echo $line | sed 's/.*port \([0-9]\+\).*/\1/')
server_url="http://$(hostname):${port_num}/"
echo "${server_url}"

~/scripts/linux_to_windows.sh "start" "${server_url}"
cat <&3
exec 3>&-
