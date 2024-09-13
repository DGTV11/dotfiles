# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
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

from libqtile import bar, qtile, hook
import os, subprocess

from qtile_extras import widget, layout
from qtile_extras.layout.decorations import ScreenGradientBorder
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()


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


@lazy.function
def shell(qtile, command):
    os.system(command)


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
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn("qutebrowser"), desc="Launch Qutebrowser"),
    Key([mod, "shift"], "b", lazy.spawn("firefox"), desc="Launch Firefox"),
    Key([mod], "s", lazy.spawn("bash -c 'LD_PRELOAD=/usr/local/lib/spotify-adblock.so spotify'"), desc="Launch Spotify"),
    Key([mod], "o", lazy.spawn("obsidian"), desc="Launch Obsidian"),
    Key([mod], "d", lazy.spawn("discord"), desc="Launch Discord"),
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
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
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
        [mod], "f", lazy.spawn("rofi -show filebrowser"), desc="Browse files with rofi"
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
    Key([], "Print", lazy.spawn("/home/danielwee/.config/qtile/screenshotter.sh full")),
    Key(
        ["control"],
        "Print",
        lazy.spawn("/home/danielwee/.config/qtile/screenshotter.sh screen"),
    ),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
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

layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": "FFFFFF",
    "border_normal": "CCCCCC",
}

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(border_width=10, margin=5, border_focus=ScreenGradientBorder()),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

from Xlib import display as xdisplay
from libqtile.utils import send_notification


def get_num_monitors():
    try:
        # Run xrandr command with --listmonitors option
        result = subprocess.run(['xrandr', '--listmonitors'], stdout=subprocess.PIPE, text=True, check=True)
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

num_monitors = get_num_monitors()

widget_defaults = dict(
    font="Fira Code",
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


def primary_top_bar():
    return bar.Bar(
        [
            widget.GroupBox(
                font="Fira Code",
                fontsize=16,
                padding=8,
                borderwidth=3,
                active="#c3cdd9",
                inactive="#7c7c7c",
                highlight_method="block",
                this_current_screen_border="#7aa2f7",
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.TextBox(
                text=f"Monitor 1/{num_monitors}",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.WindowName(
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Clock(
                format="%Y-%m-%d %a %I:%M %p",
                font="Fira Code",
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
            separator(),
            widget.Battery(
                format="{percent:2.0%} {hour:d}:{min:02d}",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.CPU(
                format="CPU: {load_percent}%",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.Memory(
                format="RAM: {MemUsed:.0f}M/{MemTotal:.0f}M",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.Memory(
                format="Swap: {SwapUsed:.0f}M/{SwapTotal:.0f}M",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.WidgetBox(widgets=[
                widget.DF(
                    partition="/",
                    format="/: {uf}{m} ({r:.0f}%)",
                    visible_on_warn=False,
                    font="Fira Code",
                    fontsize=14,
                    padding=10,
                    decorations=[
                        rect_decor(),
                    ],
                ),
                widget.DF(
                    partition="/home",
                    format="/home: {uf}{m} ({r:.0f}%)",
                    visible_on_warn=False,
                    font="Fira Code",
                    fontsize=14,
                    padding=10,
                    decorations=[
                        rect_decor(),
                    ],
                ),
            ]),
            separator(),
            widget.Volume(
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.TextBox(
                text="Logout",
                fontsize=14,
                padding=10,
                mouse_callbacks={"Button1": lazy.shutdown()},
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.TextBox(
                text="Shutdown",
                fontsize=14,
                padding=10,
                mouse_callbacks={"Button1": lazy.spawn("poweroff")},
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.CheckUpdates(
                font="Fira Code",
                fontsize=14,
                padding=10,
                update_interval=60,
                distro="Arch_checkupdates",
                decorations=[
                    rect_decor(),
                ],
            ),
        ],
        30,  # height of the bar
        background="#1f2335",  # Dark blue-grey background
        foreground="#c3cdd9",  # Light grey text
        opacity=0.8,
        margin=[10, 10, 0, 10],  # Add margin
    )

def secondary_top_bar(monitor_num):
    return bar.Bar(
        [
            widget.GroupBox(
                font="Fira Code",
                fontsize=16,
                padding=8,
                borderwidth=3,
                active="#c3cdd9",
                inactive="#7c7c7c",
                highlight_method="block",
                this_current_screen_border="#7aa2f7",
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.TextBox(
                text=f"Monitor {monitor_num}/{num_monitors}",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.WindowName(
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Clock(
                format="%Y-%m-%d %a %I:%M %p",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.Battery(
                format="{percent:2.0%} {hour:d}:{min:02d}",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.CPU(
                format="CPU: {load_percent}%",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.Memory(
                format="RAM: {MemUsed:.0f}M/{MemTotal:.0f}M",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.Memory(
                format="Swap: {SwapUsed:.0f}M/{SwapTotal:.0f}M",
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.WidgetBox(widgets=[
                widget.DF(
                    partition="/",
                    format="/: {uf}{m} ({r:.0f}%)",
                    visible_on_warn=False,
                    font="Fira Code",
                    fontsize=14,
                    padding=10,
                    decorations=[
                        rect_decor(),
                    ],
                ),
                widget.DF(
                    partition="/home",
                    format="/home: {uf}{m} ({r:.0f}%)",
                    visible_on_warn=False,
                    font="Fira Code",
                    fontsize=14,
                    padding=10,
                    decorations=[
                        rect_decor(),
                    ],
                ),
            ]),
            separator(),
            widget.Volume(
                font="Fira Code",
                fontsize=14,
                padding=10,
                decorations=[
                    rect_decor(),
                ],
            ),
            separator(),
            widget.TextBox(
                text="Logout",
                fontsize=14,
                padding=10,
                mouse_callbacks={"Button1": lazy.shutdown()},
                decorations=[
                    rect_decor(),
                ],
            ),
            widget.TextBox(
                text="Shutdown",
                fontsize=14,
                padding=10,
                mouse_callbacks={"Button1": lazy.spawn("poweroff")},
                decorations=[
                    rect_decor(),
                ],
            ),
        ],
        30,  # height of the bar
        background="#1f2335",  # Dark blue-grey background
        foreground="#c3cdd9",  # Light grey text
        opacity=0.8,
        margin=[10, 10, 0, 10],  # Add margin
    )

screens = [
Screen(
    wallpaper="/home/danielwee/Pictures/Wallpapers/epic-jigglypuff-hd-wallpaper.jpg",
    wallpaper_mode="fill",
    top=primary_top_bar(),
),
]


if num_monitors > 1:
    for m in range(num_monitors - 1):
        screens.append(
            Screen(
                wallpaper="/home/danielwee/Pictures/Wallpapers/epic-jigglypuff-hd-wallpaper.jpg",
                wallpaper_mode="fill",
                top=secondary_top_bar(m+2),
            ),
        )

@hook.subscribe.screen_change
def restart_on_randr(_):
    qtile.reload_config()

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


@hook.subscribe.startup_once
def autostart():
    as_script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([as_script])


'''
# Persistence
import json
import psutil
import os

from libqtile import hook, qtile
from libqtile.backend.base import Window
from libqtile.log_utils import logger

CONFIG_PATH = os.path.expanduser("~/.config/qtile/")

excluded_apps = ["plank"]


class Session:
    def __init__(self):
        self.apps: list[dict[int, str]] = []
        self.save_path = os.path.join(CONFIG_PATH, "json", "session.json")
        if not os.path.exists(self.save_path):
            self.from_windows()
        else:
            self.restore()

    def add_app(self, wid: int, exe: str):
        if not (
            any(app["wid"] == wid for app in self.apps)
            or any(i in exe for i in excluded_apps)
            or qtile.windows_map[wid].group.name == "scratchpad"
        ):
            logger.info("Adding %s to session", exe)
            self.apps.append({"wid": wid, "exe": exe})
        else:
            logger.info("NOT adding excluded app %s to session", exe)
        self.log()

    def remove_app(self, wid: int):
        for i in range(len(self.apps)):
            if self.apps[i]["wid"] == wid:
                exe = next((app["exe"] for app in self.apps if app["wid"] == wid), None)
                logger.info("Removing %s from session", exe)
                del self.apps[i]
                break
        self.log()

    def save(self):
        with open(self.save_path, "w") as f:
            json.dump(self.apps, f)
        apps = [app["exe"] for app in self.apps]
        logger.info("Saving session with apps: %s", ",".join(apps))

    def restore(self):
        with open(self.save_path, "r") as f:
            self.apps = json.load(f)

    def clear(self):
        self.log()
        logger.info("Clearing session")
        self.apps = []
        self.log()

    def from_windows(self):
        self.log()
        logger.info("Setting sessio@hook.subscribe.screen_change
def restart_on_randr(_):n from current windows")
        windows = qtile.windows()
        if windows:
            for window in windows:
                wid = window["id"]
                exe = psutil.Process(int(qtile.windows_map[wid].get_pid())).exe()
                self.add_app(
                    wid=wid,
                    exe=exe,
                )
        self.log()

    def log(self):
        logger.info("Session: %s", @hook.subscribe.screen_change
def restart_on_randr(_):self.apps)


@hook.subscribe.startup_once
def setup_session():
    global session
    session = Session()


@hook.subscribe.startup_once
def restore_session():
    if "session" in globals():
        apps = [app["exe"] for app in session.apps]
        logger.info("Restoring session with apps: %s", ",".join(apps))
        for app in apps:
            qtile.spawn(app)


@hook.subscribe.client_managed
def add_app_to_session(client: Window):
    if "session" in globals():
        wid = client.info()["id"]
        exe = psutil.Process(client.window.get_net_wm_pid()).exe()
        session.add_app(wid, exe)


@hook.subscribe.client_killed
def remove_app_from_session(client: Window):
    if "session" in globals():
        wid = client.info()["id"]
        session.remove_app(wid)


@hook.subscribe.shutdown
@hook.subscribe.user("save_session")
def save_session():
    if "session" in globals():
        session.save()


@hook.subscribe.user("get_session"@hook.subscribe.screen_change
def restart_on_randr(_):)
def log_session():
    if "session" in globals():
        session.log()


@hook.subscribe.user("set_session")
def set_session():
    if "session" in globals():
        session.from_windows()


@hook.subscribe.user("clear_session")
def clear_session():
    if "session" in globals():
        session.clear()
        if os.path.exists(session.save_path):
            os.remove(session.save_path)
'''
