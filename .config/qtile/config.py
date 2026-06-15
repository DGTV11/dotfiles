# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# Copyright (c) 2025 Daniel Wee
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, hook, qtile
from libqtile.config import Click, Drag, DropDown, Group, Key, Match, ScratchPad, Screen
from libqtile.lazy import lazy
from libqtile.scripts.main import VERSION
from libqtile.utils import guess_terminal
from qtile_extras import layout, widget
from qtile_extras.layout.decorations import ScreenGradientBorder
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

import custom_widgets

mod = "mod4"
# terminal = guess_terminal()
terminal = "alacritty"


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


reloading_config = False


def adjust_bar_visibility(qtile):
    global reloading_config

    bar = qtile.current_screen.top
    current_window = qtile.current_window

    if reloading_config:
        bar.show(False)
        return

    if current_window and current_window.fullscreen:
        if bar and bar.is_show():
            bar.show(False)
        for window in qtile.current_group.windows:
            if window != current_window:
                window.set_opacity(0)
    else:
        if bar and not bar.is_show():
            bar.show(True)
        for window in qtile.current_group.windows:
            if window != current_window:
                window.set_opacity(100)


@hook.subscribe.client_focus
@hook.subscribe.client_managed
@hook.subscribe.client_new
@hook.subscribe.client_killed
@hook.subscribe.layout_change
def on_window_event(*args):
    adjust_bar_visibility(qtile)


def shuffle_wallpapers(qtile):
    for wallpaper in wallpaper_widgets:
        wallpaper.shuffle()


# @lazy.function
# def shell(qtile, command):
#     os.system(command)


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    # * Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    # * Key(
    # *     [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    # * ),
    # * Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    # * Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    # Key(
    #     [mod, "shift"],
    #     "Return",
    #     lazy.layout.toggle_split(),
    #     desc="Toggle between split and unsplmakeit sides of stack",
    # ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn("qutebrowser"), desc="Launch Qutebrowser"),
    Key([mod, "shift"], "b", lazy.spawn("firefox"), desc="Launch Firefox"),
    Key(
        [mod],
        "s",
        lazy.spawn(
            "bash -c 'env LD_PRELOAD=/usr/lib/spotify-adblock.so spotify --uri=%U'"
        ),
        desc="Launch Spotify",
    ),
    # Key(
    #     [mod],
    #     "j",
    #     lazy.spawn("supersonic-desktop"),
    #     desc="Launch Supersonic",
    # ),
    Key([mod, "shift"], "s", lazy.spawn("solanum"), desc="Launch Solanum"),
    Key([mod], "o", lazy.spawn("obsidian"), desc="Launch Obsidian"),
    Key([mod], "z", lazy.spawn("zennotes"), desc="Launch ZenNotes"),
    Key([mod], "a", lazy.spawn("anki"), desc="Launch Anki"),
    Key([mod], "t", lazy.spawn("thunar"), desc="Launch Thunar"),
    Key([mod], "d", lazy.spawn("discord"), desc="Launch Discord"),
    Key([mod, "shift"], "v", lazy.spawn("virt-manager"), desc="Launch virt-manager"),
    # Key([mod], "m", lazy.spawn("modrinth-app"), desc="Launch Modrinth App"),
    Key([mod], "p", lazy.spawn("prismlauncher"), desc="Launch Prism Launcher"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod, "control"],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [mod],
        "r",
        lazy.spawn("rofi -show drun"),
        desc="Launch application menu with rofi",
    ),
    Key(
        [mod],
        "w",
        lazy.spawn("rofi -show window"),
        desc="Switch between open windows with rofi",
    ),
    Key(
        [mod],
        "e",
        lazy.spawn("rofimoji --action clipboard"),
        desc="Pick an emoji and copy it to the clipboard with rofimoji",
    ),
    Key(
        [mod],
        "v",
        lazy.spawn(
            "rofi -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}'"
        ),
        desc="Show clipboard history with rofi",
    ),
    Key(
        [mod, "control"],
        "s",
        lazy.function(shuffle_wallpapers),
        desc="Shuffle all wallpapers",
    ),
    Key(
        [mod, "shift"],
        "a",
        lazy.spawn("autorandr --change --default laptop"),
        desc="Shuffle all wallpapers",
    ),
    Key(
        [mod, "shift"],
        "comma",
        lazy.function(window_to_next_screen),
        desc="Move window to next screen",
    ),
    Key(
        [mod, "shift"],
        "period",
        lazy.function(window_to_previous_screen),
        desc="Move window to previous screen",
    ),
    Key(
        [mod, "control"],
        "comma",
        lazy.function(window_to_next_screen, switch_screen=True),
        desc="Move window to next screen and switch focus to it",
    ),
    Key(
        [mod, "control"],
        "period",
        lazy.function(window_to_previous_screen, switch_screen=True),
        desc="Move window to previous screen and switch focus to it",
    ),
    Key(
        [mod, "control"],
        "l",
        # lazy.function(toggle_golden_ratio),
        lazy.next_layout(),
        desc="Toggle layout",
    ),
    Key([mod], "comma", lazy.next_screen(), desc="Switch focus to the next screen"),
    Key(
        [mod], "period", lazy.prev_screen(), desc="Switch focus to the previous screen"
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pulseaudio-ctl down"),
        desc="Lower Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pulseaudio-ctl up"),
        desc="Raise Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pulseaudio-ctl mute"),
        desc="Mute/Unmute Volume",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
    Key(
        ["control"],
        "Page_Up",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player",
    ),
    Key(
        ["control"],
        "Page_Down",
        lazy.spawn(f"/home/{os.getlogin()}/.config/qtile/screenshotter.sh fullscreen"),
        desc="Screenshot",
    ),
    Key(
        ["control", "shift"],
        "Page_Down",
        lazy.spawn(f"/home/{os.getlogin()}/.config/qtile/screenshotter.sh current"),
    ),
    Key(["shift"], "Page_Up", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key(
        ["shift"],
        "Page_Down",
        lazy.spawn("playerctl previous"),
        desc="Skip to previous",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("sudo brillo -q -u 200000 -U 5%"),
        desc="Lower Brightness by 5%",
    ),
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("sudo brillo -q -u 200000 -A 5%"),
        desc="Raise Brightness by 5%",
    ),
    Key(
        [],
        "Print",
        lazy.spawn(f"/home/{os.getlogin()}/.config/qtile/screenshotter.sh fullscreen"),
    ),
    Key(
        ["control"],
        "Print",
        lazy.spawn(f"/home/{os.getlogin()}/.config/qtile/screenshotter.sh current"),
    ),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
# for vt in range(1, 8):
#     keys.append(
#         Key(
#             ["control", "mod1"],
#             f"f{vt}",
#             lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
#             desc=f"Switch to VT{vt}",
#         )
#     )


numerical_groups = [Group(i) for i in "123456789"]
groups = numerical_groups + [
    ScratchPad(
        name="scratchpad",
        dropdowns=[
            DropDown(
                "term1",
                terminal,
                x=0.1,
                y=0.1,
                width=0.8,
                height=0.8,
                opacity=1.0,
                on_focus_lost_hide=False,
            ),
            DropDown(
                "term2",
                terminal,
                x=0.1,
                y=0.1,
                width=0.8,
                height=0.8,
                opacity=1.0,
                on_focus_lost_hide=False,
            ),
            # DropDown(
            #     "music",
            #     "supersonic-desktop",
            #     x=0.1,
            #     y=0.1,
            #     width=0.8,
            #     height=0.8,
            #     opacity=1.0,
            #     on_focus_lost_hide=False,
            # ),
            DropDown(
                "music",
                f"alacritty --command jellyfin-tui",
                x=0.1,
                y=0.1,
                width=0.8,
                height=0.8,
                opacity=1.0,
                on_focus_lost_hide=False,
            ),
            # DropDown(
            #     "whatsapp",
            #     "wasistlos",
            #     x=0.1,
            #     y=0.1,
            #     width=0.8,
            #     height=0.8,
            #     opacity=1.0,
            #     on_focus_lost_hide=False,
            # ),
        ],
        single=True,
    )
]

for i in numerical_groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

keys.extend(
    [
        Key(
            [mod, "control"],
            "Return",
            lazy.group["scratchpad"].dropdown_toggle("term1"),
            desc="Toggle 1st terminal in scratchpad",
        ),
        Key(
            [mod, "shift"],
            "Return",
            lazy.group["scratchpad"].dropdown_toggle("term2"),
            desc="Toggle 2nd terminal in scratchpad",
        ),
        Key(
            [mod, "control"],
            "j",
            lazy.group["scratchpad"].dropdown_toggle("music"),
            desc="Toggle Supersonic in scratchpad",
        ),
    ]
)

layout_theme = {
    "border_width": 2,
    "margin": 10,
    # "border_focus": "FFFFFF",
    "border_focus": "B8C0E0",
    # "border_normal": "CCCCCC",
    "border_normal": "6C7086",
}

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(border_width=10, margin=5, border_focus=ScreenGradientBorder()),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    layout.Spiral(**layout_theme, new_client_position="after_current"),
    layout.Spiral(**layout_theme, ratio=0.5, new_client_position="after_current"),
]

from libqtile.utils import send_notification
from Xlib import display as xdisplay


def get_num_monitors():
    try:
        # Run xrandr command with --listmonitors option
        result = subprocess.run(
            ["xrandr", "--listmonitors"], stdout=subprocess.PIPE, text=True, check=True
        )
        output = result.stdout

        # Extract the number of monitors from the output
        lines = output.splitlines()
        if lines:
            # The first line contains the number of monitors
            num_monitors = int(lines[0].split()[1])
        else:
            # Default to 1 if the output is unexpected
            num_monitors = 1
    except Exception as e:
        # Handle any exceptions by setting a default number of monitors
        print(f"Error: {e}")
        return 1
    else:
        return num_monitors


WALLPAPER_PATH = (
    f"/home/{os.getlogin()}/.config/qtile/wallpapers/cloudy-quasar-catppuccin-mocha.png"
)

WALLPAPER_DIR = f"/home/{os.getlogin()}/.config/qtile/wallpapers/"


widget_defaults = dict(
    font="JetBrains Mono NL NF",
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()

# https://tailwindcss.com/docs/customizing-colors#default-color-palette
BLUE_50 = "eff6ff"
BLUE_100 = "dbeafe"
BLUE_200 = "bfdbfe"
BLUE_300 = "93c5fd"
BLUE_400 = "60a5fa"
BLUE_500 = "3b82f6"
BLUE_600 = "2563eb"
BLUE_700 = "1d4ed8"
BLUE_800 = "1e40af"
BLUE_900 = "1e3a8a"
BLUE_950 = "172554"


def separator():
    return widget.Sep(
        linewidth=1,
        padding=8,
        foreground="#3b4261",
    )


def rect_decor():
    return RectDecoration(colour="#1f2335", radius=8, filled=True, padding_y=2)


wallpaper_widgets = []


def wallpaper_widget():
    ww = custom_widgets.SortedWallpaper(
        font="JetBrains Mono NL NF",
        fontsize=14,
        padding=10,
        scroll_fixed_width=True,
        scroll=True,
        width=300,
        directory=WALLPAPER_DIR,
        random_selection=False,
        random_initial=True,
        shuffle_timeout=(60 * 15),
        wallpaper_command=None,
        # reverse_sorting=True,
        decorations=[
            rect_decor(),
        ],
    )

    wallpaper_widgets.append(ww)

    return ww


def primary_top_bar():
    return bar.Bar(
        [
            widget.GroupBox(
                font="JetBrains Mono NL NF",
                fontsize=16,
                padding=8,
                borderwidth=3,
                active="#c3cdd9",
                inactive="#7c7c7c",
                highlight_method="block",
                disable_drag=True,
                this_current_screen_border="#7aa2f7",
                decorations=[
                    rect_decor(),
                ],
            ),
            # separator(),
            # widget.TextBox(
            #     text=f"Monitor 1/{num_monitors}",
            #     font="JetBrains Mono NL NF",
            #     fontsize=14,
            #     padding=10,
            #     decorations=[
            #         rect_decor(),
            #     ],
            # ),
            separator(),
            wallpaper_widget(),
            separator(),
            widget.Spacer(),
            widget.WindowName(
                scroll=True,
                width=400,
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.Spacer(),
            separator(),
            widget.Volume(
                font="JetBrains Mono NL NF",
                fmt="Vol: {}",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Battery(
                format="{percent:2.0%} {hour:d}:{min:02d}",
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.TextBox(
                text=(
                    widget.DF(
                        partition="/",
                        visible_on_warn=False,
                    ).poll()
                    + "\n"
                    + widget.DF(
                        partition="/home",
                        visible_on_warn=False,
                    ).poll()
                ),
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.CheckUpdates(
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                update_interval=60,
                distro="Arch_checkupdates",
                no_update_string="No updates",
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Clock(
                format="%Y-%m-%d %a\n%I:%M %p",
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Systray(
                padding=5,
                decorations=[
                    rect_decor(),
                ],
            ),
        ],
        40,  # height of the bar
        background="#1f2335",  # Dark blue-grey background
        foreground="#c3cdd9",  # Light grey text
        opacity=0.8,
        margin=[10, 10, 0, 10],  # Add margin
    )


def secondary_top_bar(monitor_num):
    return bar.Bar(
        [
            widget.GroupBox(
                font="JetBrains Mono NL NF",
                fontsize=16,
                padding=8,
                borderwidth=3,
                active="#c3cdd9",
                inactive="#7c7c7c",
                highlight_method="block",
                disable_drag=True,
                this_current_screen_border="#7aa2f7",
                decorations=[
                    rect_decor(),
                ],
            ),
            # separator(),
            # widget.TextBox(
            #     text=f"Monitor {monitor_num}/{num_monitors}",
            #     font="JetBrains Mono NL NF",
            #     fontsize=14,
            #     padding=10,
            #     decorations=[
            #         rect_decor(),
            #     ],
            # ),
            separator(),
            wallpaper_widget(),
            separator(),
            widget.Spacer(),
            widget.WindowName(
                scroll=True,
                width=400,
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.Spacer(),
            separator(),
            widget.Volume(
                font="JetBrains Mono NL NF",
                fmt="Vol: {}",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Battery(
                format="{percent:2.0%} {hour:d}:{min:02d}",
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.TextBox(
                text=(
                    widget.DF(
                        partition="/",
                        visible_on_warn=False,
                    ).poll()
                    + "\n"
                    + widget.DF(
                        partition="/home",
                        visible_on_warn=False,
                    ).poll()
                ),
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Clock(
                format="%Y-%m-%d %a\n%I:%M %p",
                font="JetBrains Mono NL NF",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            # widget.Backlight(
            #     font="JetBrains Mono NL NF",
            #     fontsize=14,
            #     padding=10,
            #     decorations=[
            #         rect_decor(),
            #     ],
            # ),
        ],
        40,  # height of the bar
        background="#1f2335",  # Dark blue-grey background
        foreground="#c3cdd9",  # Light grey text
        opacity=0.8,
        margin=[10, 10, 0, 10],  # Add margin
    )


screens = [
    Screen(top=primary_top_bar()),
    Screen(top=secondary_top_bar(2)),
    Screen(top=secondary_top_bar(3)),
    Screen(top=secondary_top_bar(4)),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
# wmname = f"Qtile {VERSION}"


@hook.subscribe.startup_once
def autostart():
    as_script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([as_script])
