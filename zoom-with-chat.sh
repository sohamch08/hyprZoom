#!/usr/bin/env bash

/usr/bin/flatpak run --branch=stable --arch=x86_64 \
  --command=zoom --file-forwarding us.zoom.Zoom "$@" &
launcher_pid=$!

# Only one launcher monitors Zoom, even when opening multiple meeting links.
exec 9>"${XDG_RUNTIME_DIR:?}/zoom-chat-watch.lock"

if flock -n 9; then
    systemctl --user start hyprlife-zoom-chat.service

    idle=0
    while (( idle < 3 )); do
        if kill -0 "$launcher_pid" 2>/dev/null ||
           flatpak ps --columns=application |
               grep -Fxq 'us.zoom.Zoom'; then
            idle=0
        else
            idle=$((idle + 1))
        fi
        sleep 2
    done

    systemctl --user stop hyprlife-zoom-chat.service
fi

wait "$launcher_pid"
