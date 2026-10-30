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
    "zoom-with-chat.sh": "~/.local/bin",
}

for source, destination in files.items():
    target = os.path.join(destination)
    if os.path.lexists(target):
        print(f"Keeping existing file: {target}")
        continue

    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(os.path.join(repo, source), target)
    print(f"Installed: {target}")

print("""
Add this once to ~/.config/hypr/hyprland.lua
(skip it if your configuration already loads the module):

require("modules.zoomrules")

Then run:
hyprctl reload
systemctl --user daemon-reload
systemctl --user enable --now zoom-hyprland-chat.service
""")
