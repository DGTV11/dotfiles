# Obligatory warning
echo "WARNING: This script is EXPERIMENTAL and may not work for your system! Please double-check this script before running it!"
echo "This script assumes that you have followed the install instructions in the README!"

read -p "Do you wish to continue (y/n)?" CONT
if [ ! "$CONT" = "y" ]; then
  [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

# Prepare home directory
mkdir ~/Documents ~/Downloads ~/Music ~/Pictures

# Make temporary working directory and dotfiles folder
mkdir /tmp/workdir
cd /tmp/workdir

# Install packages
## AUR Helper
echo "Installing rustup and sccache"
yes | sudo pacman -S rustup sccache
rustup default stable

echo "Installing AUR helper..."
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
cd ../
rm -rf paru

## Basic packages
echo "Installing basic packages..."
yes | sudo pacman -S pacman-contrib python python-pip lua go neovim qtile python-xlib lightdm lightdm-slick-greeter plymouth picom udiskie pulseaudio xorg-server xorg-xrandr autorandr docker docker-compose xclip nftables reflector bluez bluez-utils tlp fcitx5-im fcitx5-chinese-addons xf86-input-evdev touchegg
paru -S qtile-extras dcron nvm rofi-greenclip

echo "Installing node (version 20) and pnpm..."
source /usr/share/nvm/init-nvm.sh
nvm install 20
npm install -g pnpm@latest-10

echo "Setting up basic packages..."
sudo systemctl enable lightdm.service

sudo systemctl enable docker.service
sudo usermod -aG docker $USER

sudo systemctl enable dcron.service

sudo systemctl enable bluetooth.service

sudo systemctl enable tlp.service

sudo systemctl enable touchegg.service

## Applications
echo "Installing CLI/TUI applications..."
yes | sudo pacman -S fastfetch starship less curl wget btop openssh rsync stow fzf playerctl bat lazygit yazi starship zoxide thefuck ffmpeg yt-dlp termdown ncdu unzip zip tar screen ueberzugpp silicon tree-sitter-cli axel trash-cli xdotool tealdeer texlive jellyfin-tui
paru -S pfetch-rs pulseaudio-ctl cava brillo unimatrix btail

echo "Installing GUI applications..."
yes | sudo pacman -S alacritty rofi firefox qutebrowser workrave obsidian thunar solanum discord libreoffice flameshot imagemagick xournalpp pdfarranger virt-manager blueman prismlauncher
paru -S wasistlos rofimoji llpp klogg anki mirage

## Themes & fonts
echo "Installing themes and fonts..."
yes | sudo pacman -S ttf-jetbrains-mono-nerd ttf-space-mono-nerd noto-fonts-cjk noto-fonts-emoji
paru -S phinger-cursors ttf-ubraille ttf-ms-win11-auto ttf-adobe-kaiti maplemono-ttf maplemononormal-ttf ttf-aptos

yes | sudo pacman -S sassc gtk-engine-murrine gnome-themes-extra
git clone https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme.git
cd Catppuccin-GTK-Theme
sudo themes/install.sh --dest /usr/share/themes --name Catppuccin
cd ../
rm -rf Catppuccin-GTK-Theme

axel https://github.com/PrismLauncher/Themes/releases/download/2025-05-25_1748167007/Catppuccin-Mocha-theme.zip -o /home/danielwee/.local/share/PrismLauncher/themes/Catppuccin-Mocha-theme.zip
unzip /home/danielwee/.local/share/PrismLauncher/themes/Catppuccin-Mocha-theme.zip -d /home/danielwee/.local/share/PrismLauncher/themes/
mv /home/danielwee/.local/share/PrismLauncher/themes/themes/** /home/danielwee/.local/share/PrismLauncher/themes/
rm /home/danielwee/.local/share/PrismLauncher/themes/Catppuccin-Mocha-theme.zip /home/danielwee/.local/share/PrismLauncher/themes/themes/


## Formatters
echo "Installing code formatters"
yes | sudo pacman -S python-black python-isort prettier
git clone https://github.com/moorereason/mdfmt.git
cd mdfmt
go install
cd ../
rm -rf mdfmt

## Python packages
echo "Installing Python packages..."
yes | sudo pacman -S sagemath python-pycryptodome python-pwntools python-psutil
paru -S python-pulsectl-asyncio

# Configure system
echo "Configuring system..."

## Move into dotfiles directory
cd $HOME/dotfiles

## Wallpapers
mkdir .config/qtile/wallpapers
axel https://i.redd.it/2ksegq0ad9zc1.png -o .config/qtile/wallpapers/distant-horizons-wallpaper-with-bee.png
axel https://i.redd.it/n105zgebijoc1.png -o .config/qtile/wallpapers/distant-horizons-wallpaper-vanillagen.png
axel https://i.redd.it/2h0nqre8no5d1.jpg -o .config/qtile/wallpapers/distant-horizons-cool-map-1.png
axel https://i.redd.it/qs2cs7e8no5d1.jpg -o .config/qtile/wallpapers/distant-horizons-cool-map-2.png
cp misc/images/wallpapers/* .config/qtile/wallpapers

## fcitx5 theme
git clone https://github.com/catppuccin/fcitx5.git
mkdir -p ~/.local/share/fcitx5/themes/
cp -r ./fcitx5/src/* ~/.local/share/fcitx5/themes

## /etc/pacman.conf
sudo cp misc/pacman.conf /etc/pacman.conf

## /usr/share/pixmaps/
sudo cp misc/images/jigglypuff.jpg /usr/share/pixmaps/jigglypuff.jpg
sudo cp misc/images/lockscreen-wallpaper.jpg /usr/share/pixmaps/lockscreen-wallpaper.jpg
sudo cp misc/images/sigmarch.png /usr/share/pixmaps/sigmarch.png
sudo chown root:root /usr/share/pixmaps/jigglypuff.jpg /usr/share/pixmaps/lockscreen-wallpaper.jpg /usr/share/pixmaps/sigmarch.png
sudo chmod 644 /usr/share/pixmaps/jigglypuff.jpg /usr/share/pixmaps/lockscreen-wallpaper.jpg /usr/share/pixmaps/sigmarch.png

# ## /etc/lightdm/lightdm-gtk-greeter.conf
# sudo cp misc/lightdm-gtk-greeter.conf /etc/lightdm/lightdm-gtk-greeter.conf
# sudo chown root:root /etc/lightdm/lightdm-gtk-greeter.conf
# sudo chmod 644 /etc/lightdm/lightdm-gtk-greeter.conf

## /etc/lightdm/slick-greeter.conf
sudo cp misc/slick-greeter.conf /etc/lightdm/slick-greeter.conf
sudo chown root:root /etc/lightdm/slick-greeter.conf
sudo chmod 644 /etc/lightdm/slick-greeter.conf

## /etc/lightdm/lightdm.conf
sudo cp misc/lightdm.conf /etc/lightdm/lightdm.conf
sudo chown root:root /etc/lightdm/lightdm.conf
sudo chmod 644 /etc/lightdm/lightdm.conf

## /root/.bashrc
sudo cp misc/root-bashrc /root/.bashrc
sudo chown root:root /root/.bashrc
sudo chmod 755 /root/.bashrc

## /usr/share/plymouth/themes/
sudo mkdir /usr/share/plymouth/themes/bgrt-alt
sudo cp -r misc/bgrt-alt.plymouth /usr/share/plymouth/themes/bgrt-alt/bgrt-alt.plymouth
sudo chown -R root:root /usr/share/plymouth/themes/bgrt-alt
sudo cp -r /usr/share/plymouth/themes/spinner /usr/share/plymouth/themes/spinner-alt
sudo cp misc/images/sigmarch.png /usr/share/plymouth/themes/spinner-alt/watermark.png
plymouth-set-default-theme -R bgrt-alt

## /etc/systemd/system/
sudo cp misc/systemd-services/paccache.timer /etc/systemd/system/paccache.timer
sudo cp misc/systemd-services/reflector.timer /etc/systemd/system/reflector.timer

sudo cp misc/systemd-services/paccache.service /usr/lib/systemd/system/paccache.service
sudo cp misc/systemd-services/reflector.service /usr/lib/systemd/system/reflector.service

sudo chown root:root /etc/systemd/system/paccache.timer /etc/systemd/system/paccache.timer /usr/lib/systemd/system/paccache.service /usr/lib/systemd/system/reflector.service

sudo systemctl enable paccache.timer reflector.timer

## /usr/local/bin/
axel https://gitweb.gentoo.org/repo/gentoo.git/plain/app-text/manpager/files/manpager.c -o /tmp/workdir/manpager.c
sudo gcc /tmp/workdir/manpager.c -o /usr/local/bin/manpager

## /etc/sudoers
cat misc/sudoers | sudo tee /etc/sudoers

## git
git config --global core.editor nvim
git config --global init.defaultBranch main

## ~/
rm -rf ~/.config ~/.bash_profile ~/.bashrc
stow .

# Give final messages
echo "Configuration almost ready!"
echo "Please add \"quiet loglevel=3 splash\" kernel paramaters and \"plymouth\" hook to initramfs (then run \"mkinitcpio -P\"), then reboot the system"
