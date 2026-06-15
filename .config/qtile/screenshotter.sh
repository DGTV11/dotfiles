#!/bin/sh

# Remove the previous screenshot if it exists
[ -f /tmp/screenshot.png ] && rm /tmp/screenshot.png

# Take a new screenshot
ksnip --$1 --saveto /tmp/screenshot.png

xclip -selection clipboard -target image/png /tmp/screenshot.png

# Notify user which mode was used
notify-send "Screenshotted in '$1' mode"
