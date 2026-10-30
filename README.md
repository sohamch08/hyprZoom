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
- **Notification service:** Starts when Zoom is launched through the wrapper and stops shortly after Zoom closes. Restarts after failures without logging message contents.

## Behaviour

- [`zoomrules.lua`](./zoomrules.lua) controls window layout, appearance, sizing, and chat bubble placement.
- [`zoom-chat-popup.py`](./scripts/zoom-chat-popup.py) identifies native chat bubbles and their meeting windows.
- [`zoom-chat-notifications.py`](./scripts/zoom-chat-notifications.py) uses accessibility events to send desktop notifications containing the sender and message.
- [`zoom-sharing-input.py`](./scripts/zoom-sharing-input.py) repairs the sharing controls' X11 window type so clicks work.
- [`zoom-with-chat.sh`](./zoom-with-chat.sh) launches Zoom, starts the listener, and stops it shortly after Zoom exits.
- [`zoom-hyprland-chat.service`](./zoom-hyprland-chat.service) runs the listener and restarts it after failures. The wrapper starts it; it does not need to be enabled at login.

## Installation

Use a working Hyprland session with Lua support and XWayland. The reference
setup uses Hyprland 0.57.0 and Zoom Flatpak. The service expects a managed
graphical session such as UWSM.

Install the Python and notification dependencies. Install

1. `python3`
2. `python3-xlib`
3. `python3-gobject`
4. `at-spi2-core`
5. `libnotif`

A running notification daemon such as SwayNC is also required. For screen sharing, install and configure PipeWire, WirePlumber, and xdg-desktop-portal-hyprland. Chat forwarding needs a working accessibility bus, Zoom's English message labels, and enabled native meeting-chat notifications.

- Install Zoom from flatpak: Run

```sh
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub us.zoom.Zoom
```

Launch Zoom once to create its configuration, then fully quit it, including
the tray process. Inside `~/.var/app/us.zoom.Zoom/config/zoomus.conf`, ensure
the existing `xwayland` setting is `xwayland=true`.

- Clone the repo:

```sh
git clone https://github.com/sohamch08/hyprZoom.git
cd hyprZoom
python3 install.py
```

Run the installer without sudo. It copies the Lua module and Python scripts
under `~/.config/hypr/`, the service to `~/.config/systemd/user/`, the executable
wrapper to `~/.local/bin/zoom-with-chat`, and the desktop entry to
`~/.local/share/applications/us.zoom.Zoom.desktop`.

Existing destination files are moved to `.bak`, `.bak.1`, and so on before
replacement, so rerunning the installer also updates older installations.

[`us.Zoom.desktop`](./us.Zoom.desktop) is a template: the installer replaces
`$HOME` with your absolute home path. Do not copy the template directly into
your applications directory.

- Hyprland config change: Add this once to `~/.config/hypr/hyprland.lua`, after
  your general window rules. Skip it if your configuration already loads the module.

```lua
require("modules.zoomrules")
```

- Reload Hyprland and systemd, and keep the listener disabled at login:

```sh
hyprctl reload
hyprctl configerrors
systemctl --user daemon-reload
systemctl --user disable --now zoom-hyprland-chat.service
```

If migrating from the older HyprLife setup, also stop and disable its old
service to prevent duplicate listeners:

```sh
systemctl --user disable --now hyprlife-zoom-chat.service
```

- Launch **Zoom from the application menu**. Its desktop entry uses the wrapper
  to start and stop the listener. Running `flatpak run us.zoom.Zoom` directly
  bypasses the wrapper. Do not run `systemctl enable --now` for this setup.

- Check `zoom-hyprland-chat.service` status:

```sh
systemctl --user status zoom-hyprland-chat.service
```

| Zoom state               | Expected service status |
| ------------------------ | ----------------------- |
| Closed                   | `inactive (dead)`       |
| Open through the wrapper | `active (running)`      |
| Shortly after closing    | `inactive (dead)`       |

To inspect errors or chat delivery confirmations:

```sh
journalctl --user -u zoom-hyprland-chat.service -b
```

Run the regression tests from the repository directory:

```sh
python3 -B -m unittest discover -s tests
```
