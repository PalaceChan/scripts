#!/bin/bash -x
# This can be triggered on startup from a windows host with the following .bat script
# start "" "%SYSTEMDRIVE%\Program Files\Git\git-bash.exe" -- /C/scripts/windows_from_linux.sh linux_host_name
# usually goes in windows start menu / programs / startup accessible via winkey+r (run) shell:startup

ssh -t ${1?specify hostname} '
    umask 077
    F=~/.win.fifo
    trap "rm -f \"$F\"" SIGINT SIGTERM EXIT
    unlink "$F"
    mkfifo "$F"
    cat <> "$F"
' | while read -r line; do
    cmd=()
    IFS=',' read -ra BASE64_CMD <<< ${line}
    for x in "${BASE64_CMD[@]}"; do
	cmd+=( "$(printf '%s' "$x" | base64 -d)" )
    done
    "${cmd[@]}"
done
