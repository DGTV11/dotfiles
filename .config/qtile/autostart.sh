#!/bin/sh
# thunar --daemon &
picom &
udiskie > /dev/null 2>&1 &
greenclip daemon &
autorandr --change --default laptop
# nitrogen --restore &
# xscreensaver -no-splash & #*I kinda screwed up my arch/xscreensaver install and gave up
workrave &
fcitx5 &
