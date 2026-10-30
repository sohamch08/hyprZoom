#!/usr/bin/env python3

import os
import shutil

repo = os.path.dirname(os.path.realpath(__file__))

files = {
    "zoomrules.lua": "~/.config/hypr/modules/zoomrules.lua",
    "scripts/zoom-chat-popup.py": "~/.config/hypr/scripts/zoom-chat-popup.py",
    "scripts/zoom-sharing-input.py": "~/.config/hypr/scripts/zoom-sharing-input.py",
    "scripts/zoom-chat-notifications.py": "~/.config/hypr/scripts/zoom-chat-notifications.py",
    "scripts/zoom_chat_accessibility.py": "~/.config/hypr/scripts/zoom_chat_accessibility.py",
    "zoom-hyprland-chat.service": "~/.config/systemd/user/zoom-hyprland-chat.service",
    "zoom-with-chat.sh": "~/.local/bin/zoom-with-chat",
    "us.Zoom.desktop": "~/.local/share/applications/us.zoom.Zoom.desktop",
}

for source, destination in files.items():
    target = os.path.expanduser(destination)
    if os.path.lexists(target):
        backup = target + ".bak"
        number = 1
        while os.path.lexists(backup):
            backup = f"{target}.bak.{number}"
            number += 1
        os.rename(target, backup)
        print(f"Backed up: {target} -> {backup}")

    os.makedirs(os.path.dirname(target), exist_ok=True)
    if source == "us.Zoom.desktop":
        with open(os.path.join(repo, source), encoding="utf-8") as file:
            desktop = file.read().replace("$HOME", os.path.expanduser("~"))
        with open(target, "w", encoding="utf-8") as file:
            file.write(desktop)
    else:
        shutil.copy2(os.path.join(repo, source), target)
    if source == "zoom-with-chat.sh":
        os.chmod(target, 0o755)
    print(f"Installed: {target}")

print("""
Add this once to ~/.config/hypr/hyprland.lua
(skip it if your configuration already loads the module):

require("modules.zoomrules")

Then run:
hyprctl reload
systemctl --user daemon-reload
systemctl --user disable --now zoom-hyprland-chat.service

If upgrading from the old HyprLife service, also run:
systemctl --user disable --now hyprlife-zoom-chat.service

Launch Zoom from the application menu. Its wrapper starts the chat service
and stops it shortly after Zoom closes. Do not enable the service at login.
""")
