#!/bin/sh

[ -f /tmp/screenshot.png ] && rm /tmp/screenshot.png

case "$1" in
  fullscreen)
    maim /tmp/screenshot.png
    ;;
  current)
    eval $(xdotool getmouselocation --shell)
    GEOM=$(xrandr --query | grep ' connected' | while read line; do
      RES=$(echo "$line" | grep -oP '\d+x\d+\+\d+\+\d+' | head -1)
      [ -z "$RES" ] && continue
      W=$(echo "$RES" | cut -dx -f1)
      H=$(echo "$RES" | cut -dx -f2 | cut -d+ -f1)
      OX=$(echo "$RES" | cut -d+ -f2)
      OY=$(echo "$RES" | cut -d+ -f3)
      if [ "$X" -ge "$OX" ] && [ "$X" -lt "$((OX+W))" ] && [ "$Y" -ge "$OY" ] && [ "$Y" -lt "$((OY+H))" ]; then
        echo "${W}x${H}+${OX}+${OY}"
      fi
    done | head -1)
    maim -g "$GEOM" /tmp/screenshot.png
    ;;
  *)
    echo "Usage: $0 {fullscreen|current}"
    exit 1
    ;;
esac

xclip -selection clipboard -target image/png /tmp/screenshot.png
notify-send "Screenshotted in '$1' mode"
