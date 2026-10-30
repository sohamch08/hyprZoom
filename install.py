#!/usr/bin/env python3

import os
import shutil

repo = os.path.dirname(os.path.realpath(__file__))
config = os.path.expanduser("~/.config")

files = {
    "zoomrules.lua": "hypr/modules/zoomrules.lua",
    "scripts/zoom-chat-popup.py": "hypr/scripts/zoom-chat-popup.py",
    "scripts/zoom-sharing-input.py": "hypr/scripts/zoom-sharing-input.py",
    "scripts/zoom-chat-notifications.py": "hypr/scripts/zoom-chat-notifications.py",
    "scripts/zoom_chat_accessibility.py": "hypr/scripts/zoom_chat_accessibility.py",
    "zoom-hyprland-chat.service": "systemd/user/zoom-hyprland-chat.service",
}

for source, destination in files.items():
    target = os.path.join(config, destination)
    if os.path.lexists(target):
        print(f"Keeping existing file: {target}")
        continue

    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(os.path.join(repo, source), target)
    print(f"Installed: {target}")

print("""
Add this once to ~/.config/hypr/hyprland.lua
(skip it if your configuration already loads the module):
Then run:
hyprctl reload
systemctl --user daemon-reload
systemctl --user enable --now zoom-hyprland-chat.service
""")
