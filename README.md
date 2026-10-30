# Zoom Meeting Setup for Hyprland

I use zoom from flatpak. So most of the fixes assume you have flatpak zoom installed but I think you guys can change it accordingly for your installation. Files in my repository: [sohamch08/hyprZoom](https://github.com/sohamch08/hyprZoom)

The fixes handle the clipped audio/video prejoin window, incorrectly tiled auxiliary windows, native chat popups appearing on unrelated workspaces, and unresponsive screen-sharing controls. They also provide desktop meeting-chat notifications showing **the sender’s name and message**, including when you’re on another workspace.

## Fixes

- **Window layout:** Keeps the main Zoom windows tiled and auxiliary windows floating, avoiding oversized empty areas in the layout.
- **Window appearance:** Removes blur, shadows, borders, rounding, and animations that interfere with transparent surfaces or clip floating controls.
- **Preview and dialog sizing:** Fixes the clipped pre-meeting audio/video window and correctly sizes and centers feedback dialogs.
- **Native chat bubbles:** Keeps them on the meeting’s workspace without stealing focus, sizes and positions them correctly, and makes them follow the meeting when it moves or resizes.
- **Desktop chat notifications:** Shows the sender’s name and message even while you’re on another workspace.
- **Screen-sharing controls:** Restores mouse input to the toolbar and preview, positions them together, and keeps them visible across workspaces.
- **Notification service:** Starts with the graphical session and restarts after failures, without logging message contents.

## Behaviour

- [`zoomrules.lua`](./zoomrules.lua) identifies chat bubbles so Lua can keep them with their meeting without stealing focus.
- [`zoom-chat-notifications.py`](./zoom-chat-notifications.py) uses accessibility events to send desktop notifications containing the sender and message.
- [`zoom-sharing-input.py`](./zoom-sharing-input.py) repairs the sharing controls’ X11 window type so clicks work.
- [`zoom-hyprland-chat.service`](./zoom-hyprland-chat.service) starts the notification listener with your session and restarts it after failures.

## Installation

- Install Zoom from flatpak: Run

```sh
flatpak install --user flathub us.zoom.Zoom
```

Then, inside `~/.var/app/us.zoom.Zoom/config/zoomus.conf` ensure `xwayland=true` option is enabled

- Clone the repo:

```sh
git clone https://github.com/sohamch08/hyprZoom.git
cd hyprZoom
python install.py
```

- Hyprland config change: Add this in your hyprland config

```lua
require("modules.zoomrules")
```

- Reload Hyprland and systemctl

```sh
hyprctl reload
systemctl --user daemon-reload
systemctl --user enable --now zoom-hyprland-chat.service
```

- Check `zoom-hyprland-chat` service status

```sh
systemctl --user status zoom-hyprland-chat.service
```
