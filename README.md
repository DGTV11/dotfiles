# dotfiles
## Installation from scratch
### Arch Linux
0) Get live environment and target x86_64 system (preferably EFI, ensure that `cat /sys/firmware/efi/fw_platform_size` returns `64`)

- VMs should have at least 20GB of total disk space

1) (Optional) Set font size to something saner
```bash
# setfont ter-132b
```

2) Connect to wifi using `iwctl`

3) Verify if internet connection works
```bash
# ping -w 1 -c 1 8.8.8.8 > /dev/null && echo "success" || echo "unsuccessful"
```
4) Partition disks using `lsblk` and `cfdisk`

| Mount point on the installed system | Partition | Partition type | Suggested size |
| --- | --- | --- | --- |
| /boot | /dev/efi_system_partition | EFI system partition | 512MiB-1 GiB |
| \[SWAP\] |/dev/swap_partition | Linux swap | At least 4 GiB (if needed) |
| / | /dev/root_partition | Linux x86-64 root (/) |Remainder of the device. At least 23–32 GiB. |

5) Format partitions
```bash
# mkfs.ext4 /dev/<root_partition>
# mkswap /dev/<swap_partition>
# mkfs.fat -F 32 /dev/<boot_partition>
```

6) Mount partitions
```bash
# mount /dev/<root_partition> /mnt
# mount --mkdir /dev/<boot_partition> /mnt/boot
# swapon /dev/<swap_partition>
```

7) Update mirrorlist
```bash
# pacman -Sy pacman-contrib
# cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup
# rankmirrors -n 6 /etc/pacman.d/mirrorlist.backup > /etc/pacman.d/mirrorlist
```

8) Bootstrap system
```bash
# pacstrap -K /mnt base base-devel linux-zen linux-firmware sof-firmware sof-tools grub efibootmgr net-tools networkmanager neovim git
```

9) Generate fstab and verify it
```bash
# genfstab -U /mnt >> /mnt/etc/fstab
# cat /mnt/etc/fstab
```

10) Chroot into system
```bash
# arch-chroot /mnt
```

11) Setup localtime
```bash
# ln -sf /usr/share/zoneinfo/<Region>/<City> /etc/localtime
# hwclock --systohc
```

12) Setup locales (locale format is `<language>_<COUNTRY>.<LOCALE TYPE>`)
```bash
# echo "<locale> <locale type>" > /etc/locale.gen
# echo "LANG=<locale>" > /etc/locale.conf
# locale-gen
```

13) Setup hostname
```bash
# echo "<hostname>" > /etc/hostname
```

14) Add a root password
```bash
# passwd
```

15) Add user
```bash
# useradd -m -G wheel -s /bin/bash <username>
# passwd <username>
```

16) Uncomment the line `%wheel ALL=(ALL) ALL` in /etc/sudoers
- Run the below command:
```bash
# EDITOR=nvim visudo
```

17) Enable NetworkManager
```bash
# systemctl enable NetworkManager
```

18) Install GRUB
```bash
# grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
# grub-mkconfig -o /boot/grub/grub.cfg
```

19) Reboot and log into regular user

20) Clone dotfiles repository
```bash
$ git clone https://github.com/DGTV11/dotfiles.git
```

21) Run `install-arch.sh`
```bash
$ cd dotfiles
$ ./install-arch.sh
```

22) Add `quiet loglevel=3 splash` kernel paramaters 

23) Add `plymouth` hook to initramfs (then run `mkinitcpio -P`)

24) Reboot the system again

25) Enjoy your new system

## Attribution
- Atom icon by nawicon (https://www.freepik.com/icon/atom_5310935)
- Arch installation guide modified from Sawntoe's guide and official Arch install guide (https://gist.github.com/sawntoe/de38953fb367e87417e399f13ad3353f, https://wiki.archlinux.org/title/Installation_guide)
