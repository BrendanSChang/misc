# dotfiles
Vim and tmux configuration files.

The setup here is based off of the instructions from this repository:
[vim-as-an-ide](https://github.com/jez/vim-as-an-ide).

The vim setup uses Vundle for plugin management. It is configured to use the
solarized colorscheme. For GNOME, the terminal was configured via the script/
instructions at
[gnome-terminal-colors-solarized](https://github.com/Anthony25/gnome-terminal-colors-solarized).
The patched font used for airline and tmuxline is Ubuntu Mono for Powerline,
found at
[ubuntu-mono-powerline-ttf](https://github.com/pdf/ubuntu-mono-powerline-ttf).

For simplicity, running `setup-ubuntu.sh` should take care of most things, but
it is a bit crude. A couple of things to note:

- The setup script is currently configured for Ubuntu (tested on 17.04) with
GNOME as the terminal emulator
- It is recommended to use a separate terminal profile (i.e. not the default)
- The setup script will probably require user input at some point
- The selected terminal profile has to be manually set to use the Ubuntu Mono
patched font
- The script does not clean up after itself (it only creates one arbitrary
directory for the GNOME terminal settings)
- The last thing the script does is install the plugins, which will probably
leave you in a Vim session, so just `:qall` to exit
- You may also have to install YCM if it's throwing errors, in which case
navigate to ~/.vim/plugged/YouCompleteMe and run ./install.py --clang-completer

To setup on Cygwin:

- Unless curl is installed, plug will have to be manually downloaded
- The patched font will also have to be manually installed and set via options
- Instead of configuring GNOME with solarized, a MinTTY configuration should be
used (such as
[mintty-colors-solarized](https://github.com/karlin/mintty-colors-solarized))
- ctags and tmux should be installed through the Cygwin package manager, which
is accessible through the Cygwin setup
- YouCompleteMe has not been tested yet

> TODO(brendan): Out of date, currently now using gruvbox and starship
