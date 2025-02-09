#!/bin/sh

# Remove the previous screenshot if it exists
[ -f /tmp/screenshot.png ] && rm /tmp/screenshot.png

# Take a new screenshot
flameshot $1 --clipboard --path /tmp/screenshot.png

# Notify user which mode was used
notify-send "Screenshotted in '$1' mode"
