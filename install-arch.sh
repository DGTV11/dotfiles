# Prepare home directory
mkdir ~/Documents ~/Downloads ~/Music ~/Pictures

# Make temporary working directory and dotfiles folder
mkdir /tmp/workdir
ORIG_DIR=$(pwd)
cd ../
cd /tmp/workdir

mv $ORIG_DIR $HOME/dotfiles

# Install packages
## AUR Helper
echo "Installing AUR helper..."
sudo pacman -S --needed base-devel
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
cd ../
rm -rf paru

## Basic packages
echo "Installing basic packages..."
sudo pacman -S python python-pip rustup sccache neovim qtile lightdm lightdm-gtk-greeter plymouth picom udiskie pulseaudio greenclip xorg-server xorg-xrandr autorandr checkupdates docker docker-compose xclip nvm nftbales reflector
paru -S qtile-extras dcron

echo "Installing node (version 20) and pnpm..."
nvm use 20
npm install -g pnpm@latest-10

echo "Setting up basic packages..."
sudo systemctl start lightdm.service
git config --global core.editor nvim

sudo systemctl enable docker
sudo usermod -aG docker $USER

sudo systemctl enable dcron.service

## Applications
echo "Installing CLI applications..."
sudo pacman -S curl wget cava btop ssh rsync stow fzf pulseaudio-ctl playerctl brillo unimatrix bat laztgit zoxide ffmpeg yt-dlp termdown du ncdu unzip zip tar screen
paru -S pfetch-rs

echo "Installing GUI applications..."
sudo pacman -S alacritty rofi firefox qutebrowser workrave obsidian anki thunar solanum discord libreoffice flameshot klogg imagemagick xournalpp
paru -S wasistlos rofimoji llpp

## Themes & fonts
echo "Installing themes and fonts..."
sudo pacman -S ttf-jetbrains-mono-nerd ttf-space-mono-nerd noto-fonts-cjk noto-fonts-emoji
paru -S phinger-cursors ttf-ubraille ttf-ms-win11-auto

git clone https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme.git
cd Catppuccin-GTK-Theme
python3 ./install.sh --dest /usr/share/themes --tweak mac
cd ../
rm -rf Catppuccin-GTK-Theme

## Python packages
echo "Installing Python packages..."
sudo pacman -S sagemath python-pycryptodome python-pwntools python-psutil python-black
paru -S python-pulsectl-asyncio

# Configure system
echo "Configuring system..."

## Move into dotfiles directory
cd $HOME/dotfiles

## /etc/sudoers
cat misc/sudoers | sed 's/sigmauser/danielwee/g' | sudo tee /etc/sudoers

## /etc/pacman.conf
sudo cp misc/pacman.conf /etc/pacman.conf

## /usr/share/pixmaps/
cp misc/images/jigglypuff.jpg /usr/share/pixmaps/jigglypuff.jpg
cp misc/images/lockscreen-wallpaper.jpg /usr/share/pixmaps/lockscreen-wallpaper.jpg
sudo chown root:root /usr/share/pixmaps/jigglypuff.jpg /usr/share/pixmaps/lockscreen-wallpaper.jpg
sudo chmod 644 /usr/share/pixmaps/jigglypuff.jpg /usr/share/pixmaps/lockscreen-wallpaper.jpg

## /etc/lightdm/lightdm-gtk-greeter.conf
cp misc/lightdm-gtk-greeter.conf /etc/lightdm/lightdm-gtk-greeter.conf
sudo chown root:root /etc/lightdm/lightdm-gtk-greeter.conf
sudo chmod 644 /etc/lightdm/lightdm-gtk-greeter.conf

## /usr/share/plymouth/themes/
sudo cp -r misc/bgrt-alt.plymouth /usr/share/plymouth/themes/bgrt-alt/bgrt-alt.plymouth
sudo chown -R root:root /usr/share/plymouth/themes/bgrt-alt
sudo cp -r /usr/share/plymouth/themes/spinner /usr/share/plymouth/themes/spinner-alt
sudo cp misc/images/spinner-watermark.png /usr/share/plymouth/themes/spinner-alt/watermark.png
plymouth-set-default-theme -R bgrt-alt

## /etc/systemd/system/
sudo cp misc/systemd-services/paccache.timer /etc/systemd/system/paccache.timer
sudo cp misc/systemd-services/reflector.timer /etc/systemd/system/reflector.timer

sudo cp misc/systemd-services/paccache.service /usr/lib/systemd/system/paccache.service
sudo cp misc/systemd-services/reflector.service /usr/lib/systemd/system/reflector.service

sudo chown root:root /etc/systemd/system/paccache.timer /etc/systemd/system/paccache.timer /usr/lib/systemd/system/paccache.service /usr/lib/systemd/system/reflector.service

sudo systemctl enable paccache.timer reflector.timer

## /usr/local/bin/
wget --output-document /tmp/workdir/manpager.c https://gitweb.gentoo.org/repo/gentoo.git/plain/app-text/manpager/files/manpager.c
sudo gcc /tmp/workdir/manpager.c -o /usr/local/bin/manpager

## ~/
stow .

# Give final messages
echo "Configuration almost ready!"
echo "Please add \"quiet loglevel=3 splash\" kernel paramaters and \"plymouth\" hook to initramfs (then run \"mkinitcpio -P\"), then reboot the system"
