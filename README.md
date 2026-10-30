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

- [`zoomrules.lua`](/home/soham/projects/hyprZoom/zoomrules.lua) controls tiling, floating, appearance, dialog sizing, and popup placement.
- [`zoom-chat-popup.py`](/home/soham/projects/hyprZoom/scripts/zoom-chat-popup.py) identifies chat bubbles so Lua can keep them with their meeting without stealing focus.
- [`zoom-chat-notifications.py`](/home/soham/projects/hyprZoom/scripts/zoom-chat-notifications.py) uses accessibility events to send desktop notifications containing the sender and message.
- [`zoom-sharing-input.py`](/home/soham/projects/hyprZoom/scripts/zoom-sharing-input.py) repairs the sharing controls’ X11 window type so clicks work.
- [`zoom-hyprland-chat.service`](/home/soham/projects/hyprZoom/zoom-hyprland-chat.service) starts the notification listener with your session and restarts it after failures.
