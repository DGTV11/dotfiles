# ~/.bashrc: executed by bash(1) for non-login shells.

# ==============================================================================
# Basic Setup
# ==============================================================================

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary, update the values of LINES and COLUMNS.
shopt -s checkwinsize

# enable programmable completion features (if not enabled)
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi

# ==============================================================================
# Shell Enhancements and Customizations
# ==============================================================================

# Pattern "**" matches all files and subdirectories
#shopt -s globstar

# make less more friendly for non-text input files
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot environment (if applicable)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# create thefuck aliases
eval "$(thefuck --alias)"
eval "$(thefuck --alias fk)"

# initalise zoxide
eval "$(zoxide init bash)"

# initalise fzf
eval "$(fzf --bash)"

# initalise starship shell
eval "$(starship init bash)"

# ==============================================================================
# Prompt Customization
# ==============================================================================

# Set a fancy prompt (non-color unless terminal supports color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# Uncomment to enable color prompt
# force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# Set title for xterm
case "$TERM" in
    xterm*|rxvt*)
        PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
        ;;
    *)
        ;;
esac

# ==============================================================================
# Aliases
# ==============================================================================

# enable color support for ls, grep, etc.
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Additional aliases
alias cat="bat"
alias neofetch="fastfetch"
alias cmatrix="/bin/unimatrix"
alias lg="lazygit"
alias cd="z"

# Utility aliases
alias pdf="llpp"
alias img="magick display"
alias ci='ping -w 1 -c 1 8.8.8.8 > /dev/null && echo "success" || echo "unsuccessful"'
alias log='klogg'
#alias remenissions='sudo docker run --rm -it -v $(pwd):/shared remenissions'
alias c="clear"
alias e="exit"
alias q="exit"
#alias n="nvim"
alias sn="shutdown now"
alias office="libreoffice"
alias ytdown="yt-dlp --embed-thumbnail -f bestaudio -x --audio-format mp3 --audio-quality 0"
# alias rpivpn="sudo openvpn --config /etc/openvpn/openvpn.conf"

# Alert for long running commands
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# ==============================================================================
# Path and Environment Variables
# ==============================================================================

# pipx path
export PATH="$PATH:$HOME/.local/bin"

# Spicetify
export PATH="$PATH:$HOME/.spicetify"

# Cargo environment
. "$HOME/.cargo/env"

# Cargo wrapper
export RUSTC_WRAPPER=sccache

# NVM (Node Version Manager)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

# Default editor
export EDITOR=nvim
export VISUAL=nvim

# Shorten directories in prompt
export PROMPT_DIRTRIM=1

# pfetch config
export PF_INFO="ascii title os kernel uptime pkgs shell memory palette"
export PF_CUSTOM_LOGOS=~/.config/pfetch_logos

# manpager
export MANPAGER='/usr/local/bin/manpager'

# ==============================================================================
# Custom Functions
# ==============================================================================

# Countdown timer
countdown() {
    start="$(( $(date '+%s') + $1))"
    while [ $start -ge $(date +%s) ]; do
        time="$(( $start - $(date +%s) ))"
        printf '%s\r' "$(date -u -d "@$time" +%H:%M:%S)"
        sleep 0.1
    done
}

# Stopwatch
stopwatch() {
    start=$(date +%s)
    while true; do
        time="$(( $(date +%s) - $start))"
        printf '%s\r' "$(date -u -d "@$time" +%H:%M:%S)"
        sleep 0.1
    done
}

# ==============================================================================
# Obligatory Startup Flex
# ==============================================================================
#if [ "$(tput cols)" -lt 80 ]; then
if [ "$(tput cols)" -lt 80 ]; then
    pfetch
else
    neofetch
fi
